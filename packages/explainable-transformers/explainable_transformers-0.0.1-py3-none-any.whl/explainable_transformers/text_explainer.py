import os 
import gc
import copy
import time

import numpy as np

import torch 



class NLPTransformerWrapper:


    def __init__(self, model, device, num_attn_layers, id, classifier_id, attention_path, cls_at_end=False):

        self.model = model 
        self.device = device
        self.dict_layers = dict(self.model.named_modules())
        self.num_attn_layers = num_attn_layers
        self.gradients = {}
        self.attn_maps = {}
        self.features = {}
        self.stack_names = []
        self.registered_hook = False
        self.extracting_features = False
        self.model_id = id
        self.attention_layers = np.arange(num_attn_layers).astype(int).tolist()
        self.classifier_id = classifier_id
        self.attention_path = attention_path
        self.cls_at_end = cls_at_end

        self.model_backup = copy.deepcopy(self.model.state_dict())


    def save_gradients(self, grads):
        name = self.stack_names.pop()
        self.gradients[name] = grads


    def get_latentvariables(self, name):
        def hook(model, input, output):
            self.features[name] = input[0].detach()
            # for i in range(len(input)):
            #     print("input["+str(i)+"]: ",i, input[i].shape)
            # for i in range(len(output)):
            #     print("output["+str(i)+"]: ", i, output[i].shape)
            # print()
        return hook

    def get_features(self, name):
        def hook(model, input, output):
            if not self.extracting_features:
                self.stack_names.append(name) 

                # for i in range(len(input)):
                #     print("input>> {}: {}".format(i, input[i].shape))
                
                # for i in range(len(output)):
                #     print("output>> {}: {}".format(i, output[i].shape))

                # bert modified
                # output.register_hook(self.save_gradients)
                # self.attn_maps[name] = output

                # BERT or RoBERTa or XLNet
                input[0].register_hook(self.save_gradients)
                if name not in self.attn_maps:
                    self.attn_maps[name] = input[0]


                

        return hook

    def register_hook(self):
        self.registered_hook = True

        # for layer in range(self.num_attn_layers):
        for layer in self.attention_layers:
            # bert modified
            # id_layer = self.model_id+'.encoder.layer.'+str(layer)+'.attention.self.softmax'
            
            # BERT or RoBERTa
            # id_layer = self.model_id+'.encoder.layer.'+str(layer)+'.attention.self.dropout'

            # XLNet 
            # id_layer = self.model_id+'.layer.'+str(layer)+'.rel_attn.dropout'

            id_layer = self.model_id+(self.attention_path.replace('#', str(layer)))
    

            #print("registering for layer:", id_layer)
            self.dict_layers[id_layer].register_forward_hook(self.get_features(id_layer))

        # self.dict_layers['classifier'].register_forward_hook(self.get_latentvariables('logits'))
        # self.dict_layers['logits_proj'].register_forward_hook(self.get_latentvariables('logits'))
        self.dict_layers[self.classifier_id].register_forward_hook(self.get_latentvariables('logits'))
        

    def extract_features(self, loader):
        self.model.eval()


        self.extracting_features = True
        FEATS = []
        LABELS = []
        self.features = {}

        with torch.no_grad():
            for iters, (batch_x, batch_t) in enumerate(loader):
                batch_x = batch_x.to(self.device)
                batch_t = batch_t.to(self.device)

                predict, _ = self.model(batch_x)

                FEATS.append(self.features['logits'].cpu().numpy())
                LABELS.append(batch_t.cpu().numpy())

        self.extracting_features = False

        return np.concatenate(FEATS), np.concatenate(LABELS)

    def _avg_heads(self, cam, grad):
        # print("before: cam {}, grad {}".format(cam.shape, grad.shape))
        cam = cam[0].reshape(-1, cam.shape[-1], cam.shape[-1])   
        grad = grad[0].reshape(-1, grad.shape[-1], grad.shape[-1])
        # print("after: cam {}, grad {}".format(cam.shape, grad.shape))
        cam = grad * cam
        cam = cam.clamp(min=0).mean(dim=0)

        return cam


    def _apply_self_attention_rules(self, R_ss, cam_ss):
        R_ss_addition = torch.matmul(cam_ss, R_ss)
        return R_ss_addition

    def _free_gpu_load(self):
        # keys = list(self.gradients.keys())
        # for key in keys:
        #     del self.gradients[key]

        # keys = list(self.attn_maps.keys())
        # for key in keys:
        #     del self.attn_maps[key]
        self.gradients.clear()
        self.attn_maps.clear()
        del self.gradients
        del self.attn_maps
        gc.collect()
        torch.cuda.empty_cache()


    def generate_relevance(self, model, input_ids, attention_mask, index=None, max_layers=-1):

        output = model(input_ids=input_ids, attention_mask=attention_mask)[0]
        output = output.to(self.device)
        kwargs = {"alpha": 1}

        if index == None:
            index = np.argmax(output.cpu().data.numpy(), axis=-1)
        # xlnet funcionou para np.zeros(num_tokens, outputsize()[-1])
        # one_hot = np.zeros((input_ids.shape[1], output.size()[-1]), dtype=np.float32)
        # one_hot[input_ids.shape[1]-1, index] = 1
        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0, index] = 1
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)
        one_hot = torch.sum(one_hot.to(self.device) * output)

        self.model.zero_grad()
        one_hot.backward(retain_graph=True)

        MLAYERS = self.num_attn_layers if max_layers == -1 else (max_layers+1)
        num_tokens = input_ids.shape[1]

        # bert, roberta
        if self.cls_at_end:
            R = torch.eye(num_tokens, num_tokens).to(self.device) 
        else:
            R = torch.eye(num_tokens, 1).to(self.device) 

        # print(">>>>> MLAYERS: {}".format(MLAYERS))
        for layer in range(MLAYERS):

            # print("Computing contribution for layer {}".format(self.attention_layers[MLAYERS-layer-1]))
            # bert modified
            # id = self.model_id+'.encoder.layer.'+str(self.attention_layers[MLAYERS-layer-1])+'.attention.self.softmax'

            # BERT or RoBERTa
            # id = self.model_id+'.encoder.layer.'+str(self.attention_layers[MLAYERS-layer-1])+'.attention.self.dropout'

            # XLNet 
            # id = self.model_id+'.layer.'+str(self.attention_layers[MLAYERS-layer-1])+'.rel_attn.dropout'

            id = self.model_id+(self.attention_path.replace('#', str(self.attention_layers[MLAYERS-layer-1])))


            grad = self.gradients[id]
            cam = self.attn_maps[id]
            cam = self._avg_heads(cam, grad)
            # print("cam shape: {}, R shape: {}".format(cam.shape, R.shape))
            # cams.append(cam.unsqueeze(0))

            R += self._apply_self_attention_rules(R, cam)

            # del grad 
            # del cam 
            # del self.gradients[id]
            # del self.attn_maps[id]
            # gc.collect() 
            # torch.cuda.empty_cache()

        # print("mine: original: cams: {}, cams[0]: {}".format(len(cams), cams[0].shape))
        # rollout = self.compute_rollout_attention(cams, start_layer=MLAYERS-1)
        # print("Start layer {}, rollout {}".format(MLAYERS-1, rollout.shape))
        # rollout[:, 0, 0] = 0
        # rollout[:, 0, -1] = 0
        # return rollout[:, 0]
        R = R.permute((1, 0))

        # print("R dimensionality: {}".format(R.shape))

        del output 
        del one_hot
        # self._free_gpu_load()
        gc.collect()
        torch.cuda.empty_cache()

        if self.cls_at_end: # e.g., for XLNet
            R[-1][-2] = 0
            R[-1][-1] = 0
            return R[num_tokens-1]
        else:
            R[0][0] = 0
            R[0][-1] = 0
            return R[0]

    def generate_relevance_list(self, model, input_ids, attention_mask, index=None, max_layers=-1):
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        output = outputs[0]
        kwargs = {"alpha": 1}

        if index == None:
            index = np.argmax(output.cpu().data.numpy(), axis=-1)
        # xlnet funcionou para np.zeros(num_tokens, outputsize()[-1])
        # one_hot = np.zeros((input_ids.shape[1], output.size()[-1]), dtype=np.float32)
        # one_hot[input_ids.shape[1]-1, index] = 1
        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0, index] = 1
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)
        one_hot = torch.sum(one_hot.to(self.device) * output)

        self.model.zero_grad()
        one_hot.backward(retain_graph=True)

        MLAYERS = self.num_attn_layers if max_layers == -1 else (max_layers+1)
        num_tokens = input_ids.shape[1]

        # bert, roberta
        if self.cls_at_end:
            Rs = [torch.eye(num_tokens, num_tokens).to(self.device) for i in range(MLAYERS)]
        else:
            Rs = [torch.eye(num_tokens, 1).to(self.device) for i in range(MLAYERS)] 

        # print(">>>>> MLAYERS: {}".format(MLAYERS))
        for layer in range(MLAYERS):

            # print("Computing contribution for layer {}".format(self.attention_layers[MLAYERS-layer-1]))
            # bert modified
            # id = self.model_id+'.encoder.layer.'+str(self.attention_layers[MLAYERS-layer-1])+'.attention.self.softmax'

            # BERT or RoBERTa
            # id = self.model_id+'.encoder.layer.'+str(self.attention_layers[MLAYERS-layer-1])+'.attention.self.dropout'

            # XLNet 
            # id = self.model_id+'.layer.'+str(self.attention_layers[MLAYERS-layer-1])+'.rel_attn.dropout'

            id = self.model_id+(self.attention_path.replace('#', str(self.attention_layers[MLAYERS-layer-1])))


            grad = self.gradients[id]
            cam = self.attn_maps[id]
            cam = self._avg_heads(cam, grad)
            # print("cam shape: {}, R shape: {}".format(cam.shape, R.shape))
            # cams.append(cam.unsqueeze(0))
            # for i in range(layer+1):
            Rs[MLAYERS-layer-1] = self._apply_self_attention_rules(Rs[MLAYERS-layer-1], cam)
            grad.to(torch.device('cpu'))
            cam.to(torch.device('cpu'))
            self.gradients[id].to(torch.device('cpu'))
            self.attn_maps[id].to(torch.device('cpu'))
            del grad 
            del cam 
            del self.gradients[id]
            del self.attn_maps[id]

        for i in range(1, len(Rs)):
            Rs[i] += Rs[i-1]

        # print("mine: original: cams: {}, cams[0]: {}".format(len(cams), cams[0].shape))
        # rollout = self.compute_rollout_attention(cams, start_layer=MLAYERS-1)
        # print("Start layer {}, rollout {}".format(MLAYERS-1, rollout.shape))
        # rollout[:, 0, 0] = 0
        # rollout[:, 0, -1] = 0
        # return rollout[:, 0]
        Rs = [R.permute((1, 0)) for R in Rs]

        # print("R dimensionality: {}".format(R.shape))
        one_hot.detach().to(torch.device('cpu'))
        # outputs.to(torch.device('cpu'))
        output.to(torch.device('cpu'))
        # for i in range(len(outputs)):
        #     outputs[i].to(torch.device('cpu'))
        del outputs
        del output 
        del one_hot
        self._free_gpu_load()
        gc.collect()
        torch.cuda.empty_cache()
        new_R = []
        if self.cls_at_end: # e.g., for XLNet
            for i in range(len(Rs)):

                Rs[i][-1][-2] = 0
                Rs[i][-1][-1] = 0
                new_R.append(Rs[i][num_tokens-1].detach().cpu().numpy())
        else:
            
            for i in range(len(Rs)):

                Rs[i][0][0] = 0
                Rs[i][0][-1] = 0
                new_R.append(Rs[i][0].detach().cpu().numpy())
        for i in range(len(Rs)):
            Rs[i].to(torch.device('cpu'))
        
        del Rs 
        gc.collect()
        torch.cuda.empty_cache() 
        return new_R
    
    def generate_explanation(self, input_ids, attention_mask, class_index=None, start_layer=-1):
        
        if not self.registered_hook:
            raise Exception("Sorry, you cannot generate explanations for unregistered models. Please, use ExplainableVisionTransformer.register_hook()")
        
        self.gradients = {}
        self.attn_maps = {}

        # R = self.generate_relevance(self.model, input_ids, attention_mask, class_index, start_layer)[0]
        R = self.generate_relevance(self.model, input_ids, attention_mask, class_index, start_layer)
        R = (R - R.min()) / (R.max() - R.min() + 0.0000000001)

        return R

    def generate_explanation_list(self, input_ids, attention_mask, class_index=None):
        
        if not self.registered_hook:
            raise Exception("Sorry, you cannot generate explanations for unregistered models. Please, use ExplainableVisionTransformer.register_hook()")
        
        self.gradients = {}
        self.attn_maps = {}

        # R = self.generate_relevance(self.model, input_ids, attention_mask, class_index, start_layer)[0]
        Rs = self.generate_relevance_list(self.model, input_ids, attention_mask, class_index, 11)
        Rs = [(R - R.min()) / (R.max() - R.min() + 0.0000000001) for R in Rs]

        return Rs

    def top_classes(self, predictions, cls2idx):
        prob = torch.softmax(predictions, dim=1)
        class_indices = predictions.data.topk(5, dim=1)[1][0].tolist()

        max_str_len = 0
        class_names = []
        for cls_idx in class_indices:
            class_names.append(cls2idx[cls_idx])
            if len(cls2idx[cls_idx]) > max_str_len:
                max_str_len = len(cls2idx[cls_idx])

        top5 = []
        for cls_idx in class_indices:
            top5.append({
                'label': cls_idx,
                'description': cls2idx[cls_idx],
                'logit': predictions[0, cls_idx],
                'probability': prob[0, cls_idx]
            })

        return top5


    
    def train(self, model_name, criterion, optimizer, scheduler, dataloaders,
              num_epochs=25, attention=False, save_epochs=0):
        
        
        self.model.to(self.device)

        if not os.path.exists(f'runs/{model_name}/epochs'):
            os.mkdir(f'runs/{model_name}/epochs')

        best_model_wts = copy.deepcopy(self.model.state_dict())
        global_step, best_acc = 0, 0.0
        running_loss, running_acc = {}, {}
        history = {'train': {'acc': [], 'loss': []}, 'val': {'acc': [], 'loss': []}}

        for epoch in range(num_epochs):
            print("epoch {}/{}".format(epoch+1, num_epochs))
           
            tic = time.time()

            for phase in ['train', 'val']:
                if phase == 'train':
                    self.model.train()
                else: 
                    self.model.eval()

                running_loss[phase], running_acc[phase] = 0.0, 0
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(self.device)
                    labels = labels.to(self.device)

                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase=='train'):
                        outputs = None 
                        if attention:
                            outputs, _ = self.model(inputs)
                        else:
                            outputs = self.model(inputs)

                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    running_loss[phase] += loss.item()*inputs.shape[0]
                    running_acc[phase] += torch.sum(preds == labels.data)

                if phase == 'train':
                    scheduler.step()

                running_loss[phase] = running_loss[phase] / (len(dataloaders[phase])*dataloaders[phase].batch_size)
                running_acc[phase] = running_acc[phase].double() / (len(dataloaders[phase])*dataloaders[phase].batch_size)

                print("{} loss: {:.3f}, acc: {:.3f}".format(phase, running_loss[phase], running_acc[phase]))
                history[phase]['acc'].append(running_acc[phase])
                history[phase]['loss'].append(running_loss[phase])

                if phase == 'val' and running_acc[phase] > best_acc:
                    best_acc = running_acc[phase]
                    best_model_wts = copy.deepcopy(self.model.state_dict())


            toc = time.time()

            print("epoch time: {:.2f}".format(toc-tic))
            print("-"*10, '\n')

            if save_epochs != 0 and (epoch+1) % save_epochs == 0:
                torch.save(self.model.state_dict(), f'runs/{model_name}/epochs/{model_name}_epoch-{epoch+1}.pt')
            
            # writer.add_scalars(f'{model_name}/loss', {'train': running_loss['train'], 'val': running_loss['val']}, global_step)
            # writer.add_scalars(f'{model_name}/acc', {'train': running_acc['train'], 'val': running_acc['val']}, global_step)
            # writer.add_scalar(f'{model_name}/lr', scheduler.get_last_lr()[0], global_step)
            

            global_step += 1

            print()

        print('Best val Acc: {:.4f}'.format(best_acc))

        self.model.load_state_dict(best_model_wts)

        print('model saved')
        # writer.close() 

        return history






