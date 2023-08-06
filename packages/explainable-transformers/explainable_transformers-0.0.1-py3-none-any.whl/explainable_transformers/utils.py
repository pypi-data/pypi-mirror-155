import time
import gc
import numpy as np

import torch 

from torch.utils.data import DataLoader, sampler, TensorDataset, SequentialSampler


from numpy.linalg import norm 
from scipy.stats import pearsonr, spearmanr
from scipy.spatial import distance

import matplotlib.pyplot as plt 
import itertools 
from tqdm import tqdm 

def implemente_multiple_time(base_list, value, times):
    return base_list + [value] * times

def reshape_token_to_plot(text, heatmap, threshold= 10):
    num_token= len(text)
    token_adjusted= None
    heatmap_adjusted= None

    if num_token < threshold:
        diff_size= threshold - num_token
        text= text + ["" for i in range(diff_size)]
        heatmap= np.array(heatmap.tolist() + [0 for i in range(diff_size)])

    # easy case : 80 // 40 = 2 ==> 40*2==80 = true
    entire_part= num_token // threshold

    if entire_part * threshold == num_token:
        num_rows= entire_part
    else:
        num_rows= entire_part + 1

    # Now we need to define the number of "columns" needed (= the max of num character from rows)
    stock_num_character_per_row= []
    step_index= 0
    for i in range(num_rows): # TODO:  delete those awful double "for" bound
        max_token= threshold*(i+1)
        tokens_rows= text[step_index:max_token]

        token_per_row_len= 0
        for token in tokens_rows:
            try:
                assert type(token) in [str, np.str_]
            except:
                raise ValueError("Need a str object")
            token_per_row_len += len(token)


        # Get the num of character per row
        stock_num_character_per_row.append(token_per_row_len)

        # Update index of first token to take
        step_index= max_token

    # Get the num of col needed to create a matrix [num_rows x num_col]
    num_col= np.max(stock_num_character_per_row)

    # With num col and rows, adjust heatmap dimension and token
    heatmap_adjusted= []
    token_adjusted= []
    step_index = 0
    for i in range(num_rows):
        max_token = threshold * (i + 1)

        heatmap_rows= heatmap[step_index:max_token]
        tokens_rows = text[step_index:max_token]
        token_adjusted.append(tokens_rows)

        new_heatmap_row= []
        for j in range(len(heatmap_rows)):

            new_heatmap_row= implemente_multiple_time(new_heatmap_row
                                                      , value= heatmap_rows[j]
                                                      , times= len(tokens_rows[j]))

        # If the heatmap adjusted (by the number of token) is under the num of col, add some 0
        diff_len= num_col - len(new_heatmap_row)
        # heatmap_adjusted.append(np.pad(new_heatmap_row, (0, diff_len)))
        heatmap_adjusted.append(implemente_multiple_time(new_heatmap_row
                                                      , value= 0
                                                      , times= diff_len))

        # Update index of first heatmap value to take (associated to a token)
        step_index = max_token

    # Be sure, the last list of token get threshold num of value
    diff_len= threshold - len(token_adjusted[-1])
    token_adjusted[-1]= token_adjusted[-1] + [""]*diff_len


    return np.array(token_adjusted), np.array(heatmap_adjusted)


def cum_mean_token(arr):

    stock_loc_token= 0
    cum_mean_position= []
    for i in range(len(arr)):
        if i == 0:
            # add the middle position for the first token
            cum_mean_position.append(arr[i]/2)
            stock_loc_token += arr[i]
        else:
            cum_mean_position.append(stock_loc_token + arr[i]/2)
            # Update by adding the arr[i] (token length)
            stock_loc_token += arr[i]

    return cum_mean_position



def plot_text_and_heatmap(text, heatmap, figsize= (5, 5), cmap= 'Greens'
                          , alpha= 0.7, word_or_letter= "letter", threshold= None, fontsize_text= "xx-small"
                          , force_color= True):
    # if letter, then text is str
    # if word, text is a List[str] (tokens)
    if word_or_letter not in ["word", "letter"]:
        raise ValueError()

    color_map = plt.cm.get_cmap(cmap)

    # reshape to data to fit into a grid plot
    if word_or_letter == "letter":
        if threshold is None:
            threshold= 40
        sentence_adjusted, heatmap_adjusted = reshape_character_to_plot(text=text
                                                                        , heatmap=heatmap
                                                                        , threshold= threshold)
    else:
        if threshold is None:
            threshold= 10
        sentence_adjusted, heatmap_adjusted = reshape_token_to_plot(text=text
                                                                   , heatmap=heatmap
                                                                   , threshold= threshold)

    fig, ax = plt.subplots(figsize=figsize)

    # Plot heatmap grid
    vmax= 1
    vmin= -1 if np.min(heatmap_adjusted) < 0 else 0 # if there is neg value, put a -1
    # else 0


    im= ax.imshow(heatmap_adjusted, cmap=color_map, alpha= alpha, vmax= vmax, vmin= vmin)

    ax.set_yticks(range(heatmap_adjusted.shape[0]))  # data.shape[0]
    ax.set_xticks(range(heatmap_adjusted.shape[1]))  # data.shape[1]

    # Plot letters or words
    if word_or_letter == "letter":

        xticks = ax.get_xticks()
        yticks = ax.get_yticks()
        gridpoints = list(itertools.product(yticks, xticks))

        for i in gridpoints:
            plt.text(x=i[1], y=i[0], s=sentence_adjusted[i]
                     , fontsize='xx-small'
                     , weight="bold"
                     , verticalalignment= "center"
                     , horizontalalignment= "center" )


    else:
        x_localisation_per_row= []
        for row_token in sentence_adjusted:
            # We compute the x-postion for each token for each row
            cum_mean_token_per_row= cum_mean_token([len(x) for x in row_token])
            # Round like a boss
            x_localisation_per_row.append([(int(loc), cum_mean_token_per_row.index(loc))
                                           for loc in cum_mean_token_per_row])

        # Create the localisation combination
        gridpoints= []
        row= 0
        for x_loc_per_row in x_localisation_per_row:
            # row for y-axis, i for x-axis
            gridpoints += [[row, i, j] for i, j in x_loc_per_row]
            row += 1

        for i in gridpoints:
            plt.text(x=i[1], y=i[0], s=sentence_adjusted[i[0], i[2]]
                     , fontsize= fontsize_text#'xx-small'
                     , weight="bold"
                     , verticalalignment= "center"
                     , horizontalalignment= "center")

    cbar= fig.colorbar(im, aspect= 100, orientation="horizontal")
    cbar.ax.tick_params(labelsize=8)
    fig.tight_layout()
    plt.axis('off')
    plt.show()
    pass


def print_top_classes(predictions, CLS2IDX):
    prob = torch.softmax(predictions, dim=1)
    class_indices = predictions.data.topk(10, dim=1)[1][0].tolist()

    max_str_len = 0
    class_names = []
    for cls_idx in class_indices:
        class_names.append(CLS2IDX[cls_idx])
        if len(CLS2IDX[cls_idx]) > max_str_len:
            max_str_len = len(CLS2IDX[cls_idx])


    print("Top 5 classes")
    for cls_idx in class_indices:
        output_string = '\t{} : {}'.format(cls_idx, CLS2IDX[cls_idx])
        output_string += ' ' * (max_str_len - len(CLS2IDX[cls_idx])) + '\t\t'
        output_string += 'value = {:.3f}\t prob = {:.1f}%'.format(predictions[0, cls_idx], 100 * prob[0, cls_idx])
        print(output_string) 