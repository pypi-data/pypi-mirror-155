import time
import pandas                   as pd
import seaborn                  as sns
import matplotlib.pyplot        as plt

from typing                     import Tuple, TypeVar
from datetime                   import datetime
from dataclasses                import dataclass, field
from sklearn.metrics            import confusion_matrix
from matplotlib.collections     import QuadMesh


# Graphics and representation
## Console representation

@dataclass(init=True, repr=True)
class Logger():
    folder: str
    name: str
    date: datetime = datetime.now()
    
    keep_file_open: bool = True
    tracked_vars: list = field(default_factory=list)

    def log(self, string_to_log:str, moment:datetime) -> None:
        file = open('{}/{}_{}.log'.format(self.folder, self.name, self.date), 'w')
        file.write("'{}' - {}".format(string_to_log, moment))

        if self.tracked_vars != []:
            file.write('Tracked vars list:')
            for index, var in enumerated(self.tracked_vars):
                var_value = self.get_tracked_values(var)

                string_format = f'\nvar_index: {index}, var_value: {var_value}'
                file.write(string_format)
                print(string_format)

        if not self.keep_file_open:
            file.close()
    
    def track_variables(self, list_of_vars:list) -> None:
        self.tracked_vars = copy.copy(list_of_vars)

    def _annidated_level(var:TypeVar('T')) -> int:
        try:
            return len(var)

        except TypeError as te:
            return -1

    def get_tracked_values(self, tracked_vars:TypeVar('T'), tracked_vars_to_log:str='', 
                           sep_character:str='*', sep_elements:str='+', tab_level:int=0) -> str:
        
        tracked_vars_to_log += "{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}".format(sep_character)

        for index, element in enumerate(tracked_vars):
            
            tracked_vars_to_log += "{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}".format(sep_elements)

            if self._annidated_level(element) >= 0:
                tracked_vars_to_log += f'\nAnnidated element ({tab_level+1})'
                tracked_vars_to_log += self.get_tracked_values(element, tab_level=tab_level+1)
            else:
                tracked_vars_to_log += f'\nindex: {index}, value: {element}'
    
        tracked_vars_to_log += "{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}".format(sep_character)

        return tracked_vars_to_log

def printProgressBar (iteration:int, total:int, prefix:str='', suffix:str='', 
                      decimals:int=1, length:int=100, fill:str='█') -> None:
    # Code from: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def compute_time(method:callable) -> None:
    init_time = time.time()
    eval(method)
    final_time = time.time()

    print(f' --- Total time {final_time - init_time} --- init at: {init_time} | end at: {final_time}')

## Confusion matrix graphics 

def get_new_fig(fn:list, figsize:list=[9,9]) -> Tuple[plt.figure, plt.axes]:
    """ Init graphics """
    fig1 = plt.figure(fn, figsize)
    ax1 = fig1.gca()   #Get Current Axis
    ax1.cla() # clear existing plot
    return fig1, ax1

def configcell_text_and_colors(array_df:pd.DataFrame, lin:int, col:int, oText:str, facecolors, posi, fz, fmt, show_null_values=0) -> Tuple[list, list]:
    """
      config cell text and colors
      and return text elements to add and to dell
      @TODO: use fmt
    """
    text_add = []; text_del = [];
    cell_val = array_df[lin][col]
    tot_all = array_df[-1][-1]
    per = (float(cell_val) / tot_all) * 100
    curr_column = array_df[:,col]
    ccl = len(curr_column)

    #last line  and/or last column
    if(col == (ccl - 1)) or (lin == (ccl - 1)):
        #tots and percents
        if(cell_val != 0):
            if(col == ccl - 1) and (lin == ccl - 1):
                tot_rig = 0
                for i in range(array_df.shape[0] - 1):
                    tot_rig += array_df[i][i]
                per_ok = (float(tot_rig) / cell_val) * 100
            elif(col == ccl - 1):
                tot_rig = array_df[lin][lin]
                per_ok = (float(tot_rig) / cell_val) * 100
            elif(lin == ccl - 1):
                tot_rig = array_df[col][col]
                per_ok = (float(tot_rig) / cell_val) * 100
            per_err = 100 - per_ok
        else:
            per_ok = per_err = 0

        per_ok_s = ['%.2f%%'%(per_ok), '100%'] [per_ok == 100]

        #text to DEL
        text_del.append(oText)

        #text to ADD
        font_prop = fm.FontProperties(weight='bold', size=fz)
        text_kwargs = dict(color='w', ha="center", va="center", gid='sum', fontproperties=font_prop)
        lis_txt = ['%d'%(cell_val), per_ok_s, '%.2f%%'%(per_err)]
        lis_kwa = [text_kwargs]
        dic = text_kwargs.copy(); dic['color'] = 'g'; lis_kwa.append(dic);
        dic = text_kwargs.copy(); dic['color'] = 'r'; lis_kwa.append(dic);
        lis_pos = [(oText._x, oText._y-0.3), (oText._x, oText._y), (oText._x, oText._y+0.3)]
        for i in range(len(lis_txt)):
            newText = dict(x=lis_pos[i][0], y=lis_pos[i][1], text=lis_txt[i], kw=lis_kwa[i])
            text_add.append(newText)

        #set background color for sum cells (last line and last column)
        carr = [0.27, 0.30, 0.27, 1.0]
        if(col == ccl - 1) and (lin == ccl - 1):
            carr = [0.17, 0.20, 0.17, 1.0]
        facecolors[posi] = carr

    else:
        if(per > 0):
            txt = '%s\n%.2f%%' %(cell_val, per)
        else:
            if(show_null_values == 0):
                txt = ''
            elif(show_null_values == 1):
                txt = '0'
            else:
                txt = '0\n0.0%'
        oText.set_text(txt)

        #main diagonal
        if(col == lin):
            #set color of the textin the diagonal to white
            oText.set_color('w')
            # set background color in the diagonal to blue
            facecolors[posi] = [0.35, 0.8, 0.55, 1.0]
        else:
            oText.set_color('r')

    return text_add, text_del

def insert_totals(df_cm:pd.DataFrame) -> None:
    """ insert total column and line (the last ones) """
    sum_col = []
    for c in df_cm.columns:
        sum_col.append( df_cm[c].sum() )
    sum_lin = []
    for item_line in df_cm.iterrows():
        sum_lin.append( item_line[1].sum() )
    df_cm['sum_lin'] = sum_lin
    sum_col.append(np.sum(sum_lin))
    df_cm.loc['sum_col'] = sum_col

def pretty_plot_confusion_matrix(df_cm:pd.DataFrame, annot:bool=True, cmap:str="Oranges", fmt:str='.2f', fz:int=11,
      lw:float=0.5, cbar:bool=False, figsize:list=[8,8], show_null_values:int=0, pred_val_axis:str='y', save_route:str='') -> None:
    """
      print conf matrix with default layout (like matlab)
      params:
        df_cm          dataframe (pandas) without totals
        annot          print text in each cell
        cmap           Oranges,Oranges_r,YlGnBu,Blues,RdBu, ... see:
        fz             fontsize
        lw             linewidth
        pred_val_axis  where to show the prediction values (x or y axis)
                        'col' or 'x': show predicted values in columns (x axis) instead lines
                        'lin' or 'y': show predicted values in lines   (y axis)
    """
    if(pred_val_axis in ('col', 'x')):
        xlbl = 'Predicted'
        ylbl = 'Actual'
    else:
        xlbl = 'Actual'
        ylbl = 'Predicted'
        df_cm = df_cm.T

    # create "Total" column
    insert_totals(df_cm)

    #this is for print allways in the same window
    fig, ax1 = get_new_fig('Conf matrix default', figsize)

    #thanks for seaborn
    ax = sns.heatmap(df_cm, annot=annot, annot_kws={"size": fz}, linewidths=lw, ax=ax1,
                    cbar=cbar, cmap=cmap, linecolor='w', fmt=fmt)

    #set ticklabels rotation
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, fontsize = 10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation = 25, fontsize = 10)

    # Turn off all the ticks
    for t in ax.xaxis.get_major_ticks():
        t.tick1line.set_visible(False)
        t.tick2line.set_visible(False)
    for t in ax.yaxis.get_major_ticks():
        t.tick1line.set_visible(False)
        t.tick2line.set_visible(False)

    #face colors list
    quadmesh = ax.findobj(QuadMesh)[0]
    facecolors = quadmesh.get_facecolors()

    #iter in text elements
    array_df = np.array( df_cm.to_records(index=False).tolist() )
    text_add = []; text_del = [];
    posi = -1 #from left to right, bottom to top.
    for t in ax.collections[0].axes.texts: #ax.texts:
        pos = np.array( t.get_position()) - [0.5,0.5]
        lin = int(pos[1]); col = int(pos[0]);
        posi += 1

        #set text
        txt_res = configcell_text_and_colors(array_df, lin, col, t, facecolors, posi, fz, fmt, show_null_values)

        text_add.extend(txt_res[0])
        text_del.extend(txt_res[1])

    #remove the old ones
    for item in text_del:
        item.remove()
    #append the new ones
    for item in text_add:
        ax.text(item['x'], item['y'], item['text'], **item['kw'])

    #titles and legends
    ax.set_title('Confusion matrix')
    ax.set_xlabel(xlbl)
    ax.set_ylabel(ylbl)
    
    plt.tight_layout()  #set layout slim
    
    if save_route != '':
        plt.savefig(save_route)
    else: 
        plt.show()

def plot_confusion_matrix_from_data(y_test:pd.Series, predictions:pd.Series, columns:list=None, annot:bool=True, cmap:str="Oranges",
      fmt:str='.2f', fz:int=11, lw:float=0.5, cbar:bool=False, figsize:list=[8,8], show_null_values:int=0, pred_val_axis:str='lin') -> None:
    """
        plot confusion matrix function with y_test (actual values) and predictions (predic),
        whitout a confusion matrix yet
    """

    #data
    if(not columns):
        #labels axis integer:
        ##columns = range(1, len(np.unique(y_test))+1)
        #labels axis string:
        from string import ascii_uppercase
        columns = ['class %s' %(i) for i in list(ascii_uppercase)[0:len(np.unique(y_test))]]

    confm = confusion_matrix(y_test, predictions)
    cmap = 'Oranges';
    fz = 11;
    figsize=[9,9];
    show_null_values = 2
    df_cm = DataFrame(confm, index=columns, columns=columns)
    pretty_plot_confusion_matrix(df_cm, fz=fz, cmap=cmap, figsize=figsize, show_null_values=show_null_values, pred_val_axis=pred_val_axis)

## Graphics representation

def make_line_plot(characteristic:str, char_name:str, over_var:str, dataset_list:list, 
                   time_increment:int, time_init:int, time_final:int, filename:str='', 
                   file_format:str='svg') -> None:
    t = np.arange(0, len(dataset_list[0]), time_increment)
    fig, axs = plt.subplots()

    args_list = [dataset[characteristic] for dataset in dataset_list]

    for element in range(len(args_list)*2):
        if element % 2 == 0:
            args_list.insert(element, t)

    axs.plot(*args_list)

    axs.set_xlim(time_init, time_final)
    axs.set_xlabel(over_var)

    axs.set_ylabel(char_name)
    axs.set_ylim(40, 180)
    axs.grid(True)

    
    if filename != '':
        plt.savefig("{}.{}".format(filename, file_format))
    else:
        plt.show()

def make_hist_plot(char:str, char_date:list, dataset:pd.DataFrame, label_dict:dict, 
                   label_groups_list:list, width:int, n_groups:int, y_label:str, \
                   title:str, legend:bool=False,  filename:str='', file_format:str='svg') -> list:
    fig, ax = plt.subplots()
    ind = np.arange(n_groups)

    parameters_bars = []
    last_means = []

    means_week_day = []
    std_week_day = []

    for label_name in label_dict:

        days_to_check = label_dict[label_name]
        print(days_to_check)
        means_week_day.append(
            [dataset[(dataset[char_date] == day)][char].sum() for day in days_to_check])
        std_week_day.append(
            [dataset[(dataset[char_date] == day)][char].std() for day in days_to_check])

        if len(parameters_bars) == 0:
            parameters_bars.append(ax.bar(ind, means_week_day[0], width,
                                          yerr=std_week_day[0],
                                          label=label_name))

        else:
            print(means_week_day[-1])
            print(means_week_day[-2])

            parameters_bars.append(ax.bar(ind, means_week_day[-1], width,
                                          bottom=suma_listas(
                                              means_week_day[:-1]),
                                          yerr=std_week_day[-1],
                                          label=label_name))


    ax.axhline(0, color='grey', linewidth=0.8)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(ind)
    ax.set_xticklabels(tuple(label_groups_list))

    if legend:
        ax.legend()

    # Label with label_type 'center' instead of the default 'edge'

    for parameter_bar in parameters_bars:
        ax.bar_label(parameter_bar, label_type='center')
        
    ax.bar_label(parameters_bars[-1])

    if filename != '':
        plt.savefig("{}.{}".format(filename, file_format))
    else:
        plt.show()
        
    return means_week_day