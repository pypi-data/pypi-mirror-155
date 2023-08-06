import os 
 
import copy
import time

import cv2
import numpy as np

import torch 

from tqdm.notebook import tqdm

from torch.utils.tensorboard import SummaryWriter

class VisionTransformerWrapper: 


    def __init__(self, model, device, num_attn_layers=6, id='vit_model'):

        self.model = model 
        self.device = device
        self.dict_layers = dict(self.model.named_modules())
        self.num_attn_layers=num_attn_layers
        self.gradients = {}
        self.attn_maps = {}
        self.features = {}
        self.stack_names = []
        self.registered_hook = False
        self.extracting_features = False
        self.model_id = id
        self.attention_layers = np.arange(num_attn_layers).astype(int).tolist()

        self.model_backup = copy.deepcopy(self.model.state_dict())

    def save_gradients(self, grads):
        name = self.stack_names.pop()
        self.gradients[name] = grads


    def get_latentvariables(self, name):
        def hook(model, input, output):
            self.features[name] = input[0].detach()
        return hook

    def get_features(self, name):
        def hook(model, input, output):
            if not self.extracting_features:
                self.stack_names.append(name)            
                output[1].register_hook(self.save_gradients)
                self.attn_maps[name] = output[1]

        return hook

    def register_hook(self):
        self.registered_hook = True

        # for layer in range(self.num_attn_layers):
        for layer in self.attention_layers:
            id_layer = self.model_id+'.encoder.layer.'+str(layer)
            #print("registering for layer:", id_layer)
            self.dict_layers[id_layer].register_forward_hook(self.get_features(id_layer))

        self.dict_layers['classifier'].register_forward_hook(self.get_latentvariables('logits'))

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
        cam = cam.reshape(-1, cam.shape[-2], cam.shape[-1])   
        grad = grad.reshape(-1, grad.shape[-2], grad.shape[-1])
        cam = grad * cam
        cam = cam.clamp(min=0).mean(dim=0)
        return cam 

    def _apply_self_attention_rules(self, R_ss, cam_ss):
        R_ss_addition = torch.matmul(cam_ss, R_ss)
        return R_ss_addition

    # create heatmap from mask on image
    def _show_cam_on_image(self, img, mask):
        heatmap = cv2.applyColorMap(np.uint8(255 * mask), cv2.COLORMAP_JET)
        heatmap = np.float32(heatmap) / 255
        cam = heatmap + np.float32(img)
        cam = cam / np.max(cam)
        return cam

    def _generate_relevance(self, model, input, n_tokens, index=None, max_layers=-1):

        output = model(input)[0]

        if index == None:        
            index = np.argmax(output.cpu().data.numpy(), axis=-1)

        one_hot = np.zeros((1, output.size()[-1]), dtype=np.float32)
        one_hot[0, index] = 1
        one_hot_vector = one_hot 
        one_hot = torch.from_numpy(one_hot).requires_grad_(True)

        one_hot = torch.sum(one_hot.to(self.device) * output)
        # one_hot = torch.sum(one_hot.cuda()*torch.softmax(output, dim=1).unsqueeze(0))    

        model.zero_grad()

        one_hot.backward(retain_graph=True)

        num_tokens = n_tokens

        MLAYERS = self.num_attn_layers if max_layers == -1 else max_layers

        R = torch.eye(num_tokens, num_tokens).to(self.device) 
        for layer in range(MLAYERS):
            # print("Computing contribution for layer {}".format(self.attention_layers[MLAYERS-layer-1]))
            id = self.model_id+'.encoder.layer.'+str(self.attention_layers[MLAYERS-layer-1])
            grad = self.gradients[id]
            cam = self.attn_maps[id]
            cam = self._avg_heads(cam, grad)
            R += self._apply_self_attention_rules(R.to(self.device), cam.to(self.device))
        return R[0, 1:]

    def generate_visualization(self, original_image, patch_size=16, class_index=None, max_layers=-1):
        
        if not self.registered_hook:
            raise Exception("Sorry, you cannot generate explanations for unregistered models. Please, use ExplainableVisionTransformer.register_hook()")
        
        self.gradients = {}
        self.attn_maps = {}
        n_tokens = int((original_image.shape[1]*original_image.shape[2]) / patch_size**2 + 1) # +1 for the [CLS] token
        
        transformer_attribution = self._generate_relevance(self.model, original_image.unsqueeze(0).to(self.device), n_tokens, index=class_index, max_layers=max_layers).detach()
        
        side = int(np.sqrt(transformer_attribution.shape[0]))

        transformer_attribution = transformer_attribution.reshape(1, 1, side, side)
        scale_factor = int(original_image.shape[1]/side)

        transformer_attribution = torch.nn.functional.interpolate(transformer_attribution, scale_factor=scale_factor, mode='bilinear')
        transformer_attribution = transformer_attribution.reshape(original_image.shape[1], original_image.shape[1]).to(self.device).cpu().numpy()
        transformer_attribution = (transformer_attribution - transformer_attribution.min()) / (transformer_attribution.max() - transformer_attribution.min())

        image_transformer_attribution = original_image.permute(1, 2, 0).data.cpu().numpy()
        image_transformer_attribution = (image_transformer_attribution - image_transformer_attribution.min()) / (image_transformer_attribution.max() - image_transformer_attribution.min())

        vis = self._show_cam_on_image(image_transformer_attribution, transformer_attribution)
        vis = np.uint8(255*vis)
        vis = cv2.cvtColor(np.array(vis), cv2.COLOR_RGB2BGR)
        return vis, transformer_attribution

    def top_classes(self, predictions, cls2idx):
        prob = torch.softmax(predictions, dim=1)
        class_indices = predictions.data.topk(10, dim=1)[1][0].tolist()

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

        writer = SummaryWriter(f'runs/{model_name}')
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
                for inputs, labels in tqdm(dataloaders[phase]):
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
            
            writer.add_scalars(f'{model_name}/loss', {'train': running_loss['train'], 'val': running_loss['val']}, global_step)
            writer.add_scalars(f'{model_name}/acc', {'train': running_acc['train'], 'val': running_acc['val']}, global_step)
            writer.add_scalar(f'{model_name}/lr', scheduler.get_last_lr()[0], global_step)
            

            global_step += 1

            print()

        print('Best val Acc: {:.4f}'.format(best_acc))

        self.model.load_state_dict(best_model_wts)

        print('model saved')
        writer.close() 

        return history






