def update_legend(ax, colors=None, x_loc=1.05, y_loc=1, linewidth=2,frameon=False):
    leg = ax.legend(loc = "upper left", bbox_to_anchor=(x_loc, y_loc), 
                    fontsize=10, frameon = frameon, edgecolor = "k", facecolor = "white")

    if colors is not None:
        for i,(c,l,text) in enumerate(zip(colors,leg.legendHandles,leg.get_texts())):
            text.set_color(c)
            l.set_linewidth(linewidth)
    else:
        for l,text in zip(leg.legendHandles,leg.get_texts()):
            try: text.set_color(l.get_color())
            except: continue
            text.set_fontweight('bold')