import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def multi_yax_plot(ax, 
                   leftax_df=pd.DataFrame(),  # left  axis data frame 
                   rightax_df=pd.DataFrame(), # right axis data frame
                   leftax_limits=None,        # options include:
                   rightax_limits=None,       # None | [low,high] | [[low,high], [low,high], [low,high]]
                   leftax_style="-",          # options include:
                   rightax_style="-",         # "-", ".", ".-" | ["-",".",":"]
                   colors="bright",           # "palette" | ["k", "r", "g"]
                   linewidth=None,
                   markersize=None,
                   ylabel_fontsize=15):
    
    def set_spines(ax,which="left",loc=0,color="k"):
        if which!= "host":
            left_right = ["right","left"]
            if which == "left": left_right = ["left","right"]
            ax.spines[left_right[0]].set_position(("axes", loc))
            ax.spines[left_right[0]].set_visible(True)
            ax.spines[left_right[0]].set_linewidth(3)
            ax.spines[left_right[1]].set_visible(False)
            ax.spines["bottom"].     set_visible(False)
            ax.spines["top"].        set_visible(False)
            plt.setp(ax.spines.values(), color=color)
            ax.yaxis.set_label_position(which)
            ax.yaxis.set_ticks_position(which)
            ax.yaxis.label.set_color(color)
            ax.tick_params(axis='y', colors=color,width=2,size=5)
        else:
            ax.axes.get_yaxis().set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(True)
    
    if leftax_limits  is None:leftax_limits =[[None,None] for _ in range(leftax_df. shape[1])]
    if rightax_limits is None:rightax_limits=[[None,None] for _ in range(rightax_df.shape[1])]
    if not any(isinstance(x, list) for x in leftax_limits): leftax_limits =[[leftax_limits[0], leftax_limits[1]] for _ in range(leftax_df. shape[1])]
    if not any(isinstance(x, list) for x in rightax_limits):rightax_limits=[[rightax_limits[0],rightax_limits[1]]for _ in range(rightax_df.shape[1])]
    if not isinstance(leftax_style, list): leftax_style =[leftax_style  for _ in range(leftax_df. shape[1])]
    if not isinstance(rightax_style,list): rightax_style=[rightax_style for _ in range(rightax_df.shape[1])]
    if not isinstance(colors,list): colors = sns.color_palette(colors, leftax_df.shape[1]+rightax_df.shape[1])
    
    set_spines(ax, which="host")
    ax_left  = [ax.twinx() for _ in range(leftax_df. shape[1])]
    ax_right = [ax.twinx() for _ in range(rightax_df.shape[1])]
    
    for i,col in enumerate(leftax_df.columns):
        set_spines(ax_left[i], which="left", loc=-(i*1.2)/plt.gcf().get_size_inches()[0], color=colors[i])
        ax_left[i].set_ylabel(col,fontweight='bold',fontsize=ylabel_fontsize,loc="bottom")
        ax_left[i].plot(leftax_df.index,leftax_df[col],
                        leftax_style[i],color=colors[i],
                        linewidth=linewidth,markersize=markersize,
                        drawstyle="steps-post")
        ax_left[i].set_ylim(leftax_limits[i][0],leftax_limits[i][1])

    if leftax_df.columns.shape[0] == 0: i=0
    for j,col in enumerate(rightax_df.columns):
        set_spines(ax_right[j], which="right", loc=1+j*1.2/plt.gcf().get_size_inches()[0], color=colors[i+j+1])
        ax_right[j].set_ylabel(col,fontweight='bold',fontsize=ylabel_fontsize,loc="bottom")
        ax_right[j].plot(rightax_df.index,rightax_df[col],
                         rightax_style[j],color=colors[i+j+1],
                         linewidth=linewidth,markersize=markersize,
                         drawstyle="steps-post")
        ax_right[j].set_ylim(rightax_limits[j][0],rightax_limits[j][1])
    return ax_left, ax_right