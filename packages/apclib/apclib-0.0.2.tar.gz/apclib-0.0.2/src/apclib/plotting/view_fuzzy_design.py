import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def view_fuzzy_design(fuzzy):
    plt.rcParams.update({"lines.color":       "white",
                         "patch.edgecolor":   "white",
                         "text.color":        "white",
                         "axes.edgecolor":    "white",
                         "axes.labelcolor":   "white",
                         "xtick.color":       "white",
                         "ytick.color":       "white",
                         "axes.grid" :         False, 
                         "grid.color":        "lightgray",
                         "axes.facecolor":    "darkslategray",
                         "figure.facecolor":  "k",
                         "figure.edgecolor":  "k",
                         "savefig.facecolor": "k",
                         "savefig.edgecolor": "k",
                         'legend.handlelength':0})
    
    '''
        fuzzy: instance of fuzzy class
    '''
    num_rows = max(len(fuzzy.input.keys()), len(fuzzy.output.keys()))
    if num_rows == 1:num_rows = 2
    
    fig, ax = plt.subplots(num_rows, 3, figsize = (20, num_rows*3))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    colors = ["b","g","r","c","m","y","k","w"]*100
    colors = ["c","y","tomato"]*100
    
    # Plot input & output memebership functions
    fuzzy.gen_output()    
    for j,io in enumerate([fuzzy.input, fuzzy.output]):
        
        for i,key in enumerate(io.keys()):
            x = fuzzy.gen_xrange(io[key])
            for k,func in enumerate(io[key]["function"]):
                y = [fuzzy.memfunc(inpt  =xi,
                                   func  =io[key]["function"][func]["type"],
                                   limits=io[key]["function"][func]["limits"],
                                   memMax=io[key]["function"][func]["membership_max"]) for xi in x]
                ax[i,j].plot(x,y,color=colors[k],label=func)
                ax[i,j].text(io[key]["value"],
                             io[key]["function"][func]["membership"], 
                             str(round(io[key]["function"][func]["membership"],2)),
                             color="w",fontweight="bold",
                             ha="center", va="center", bbox=dict(facecolor=colors[k],edgecolor='none',pad=1.0))
                if j > 0:
                    y = [fuzzy.memfunc(inpt  =xi,
                                       func  =io[key]["function"][func]["type"],
                                       limits=io[key]["function"][func]["limits"],
                                       memMax=io[key]["function"][func]["membership"]) for xi in x]
                    ax[i,j].fill_between(x,y,color=colors[k],alpha=0.4)
            leg = ax[i,j].legend(loc="upper center", ncol=len(io[key]["function"].keys()),handletextpad=0.,frameon=True)
            for c,l,t in zip(colors,leg.legendHandles,leg.get_texts()):t.set_color(c);t.set_ha('left');t.set_fontweight('bold');l.set_linewidth(0)
            ax[i,j].set_ylim(-0.1,1.55)
            ax[i,j].set_yticks([0,.2,.4,.6,.8,1])
            ax[i,j].plot([io[key]["value"],io[key]["value"]],[0,1],"w--",linewidth=1)
            ax[i,j].text(io[key]["value"], 1.08, str(round(io[key]["value"],2)),fontsize=11,ha="center") 
            title = "INPUT"
            if j > 0: title = "OUTPUT" 
            ax[i,j].set_title(title+": "+key)
            
    # Simulate multiple scenarios
    io_links = {}
    for rule in fuzzy.rules.keys():
        for otpt in fuzzy.rules[rule]["output"].keys():
            if otpt not in io_links.keys():io_links[otpt] = []
            for inpt in fuzzy.rules[rule]["input"].keys():
                if inpt not in io_links[otpt]: io_links[otpt].append(inpt)
    for i,otpt in enumerate(io_links.keys()):
        x = {}
        for inpt,N in zip(io_links[otpt][:2],[50,10]): x[inpt] = fuzzy.gen_xrange(fuzzy.input[inpt],N)
  
        if len(x.keys()) == 1:
            inpt = list(x.keys())[0]
            y = []
            for xi in x[inpt]:
                fuzzy.input[inpt]["value"] = xi
                fuzzy.gen_output()
                y.append(fuzzy.output[otpt]["value"])
            ax[i,2].plot(x[inpt],y,"w",drawstyle="steps-post")
            ax[i,2].set_ylabel("OUTPUT: "+otpt)
            ax[i,2].set_xlabel("INPUT: " +inpt)
        else:
            low_len_key = [(key, len(x[key])) for key in x.keys()]
            low_len_key.sort(key=lambda x: x[1])
            low_len_key, high_len_key  = low_len_key[0][0],low_len_key[1][0]
            
            colors = sns.color_palette("Spectral",len(x[low_len_key]))[::-1]
            y_prev = []
            for k,xi in enumerate(x[low_len_key]):
                fuzzy.input[low_len_key]["value"] = xi
                y = []
                for xii in x[high_len_key]:
                    fuzzy.input[high_len_key]["value"] = xii
                    fuzzy.gen_output()
                    y.append(fuzzy.output[otpt]["value"])
                if k==0 or sum([(abs(yi/np.std(y)-y_previ/np.std(y_prev))) for yi,y_previ in zip(y,y_prev)]) > 1e-10:
                    ax[i,2].plot(x[high_len_key],y,color=colors[k],label=str(round(xi,2)),drawstyle="steps-post")
                    ax[i,2].text(x[high_len_key][int(len(y)*.5)],y[int(len(y)*.5)],str(round(xi,2)),
                                 color=colors[k],fontweight="bold",
                                 ha="center", va="center", bbox=dict(facecolor="k",edgecolor='none',pad=1.0,alpha=1))
                y_prev = y
            ax[i,2].set_ylabel("OUTPUT: "+otpt)
            ax[i,2].set_xlabel("INPUT: " +high_len_key)
            leg = ax[i,2].legend(loc="upper right", 
                                 frameon = False, 
                                 title = "INPUT: " + low_len_key, 
                                 bbox_to_anchor=(1.4, 1.),
                                 ncol=int(len(ax[i,2].lines)>5)+1,
                                 handletextpad=0.)
            for l,t in zip(leg.legendHandles,leg.get_texts()):
                t.set_color(l.get_color())
                t.set_ha('center')
                t.set_fontweight('bold')
                l.set_linewidth(0)
            leg.get_title().set_position((-15, 0))
            leg._legend_box.align = "left"
    
    # Clean empty plots
    for i in range(ax.shape[0]):
        for j in range(ax.shape[1]):
            if len(ax[i,j].lines) == 0:
                fig.delaxes(ax[i,j])

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from controllers.fuzzy import fuzzy

    if 1:
        # inputs
        l_c_rc = 20.
        y_c_rc = 26.
        h_c_rc = 27.
        
        l_c_rt = 0.4
        y_c_rt = 0.75
        h_c_rt = 0.8
        
        l_c_cc = 52.
        y_c_cc = 53.
        h_c_cc = 58.
        
        # outputs
        l_f_rc = 50
        h_f_rc = 120
        dr_f_rc_m = (h_f_rc-l_f_rc)/10
        
        l_v_s1 = 5
        h_v_s1 = 15
        dr_v_s1_m = (h_v_s1-l_v_s1)/10
        
        l_f_cc = 3
        h_f_cc = 10
        dr_f_cc_m = (h_f_cc-l_f_cc)/10

    fuzzy_c = fuzzy()

    # inputs
    p = [0.,.1,.3,.5,.7,.9,1.]
    fuzzy_c.input["y_c_rt"]   = {"value"   : y_c_rt, 
                                 "function":{"low"     :{"membership":0, "membership_max":1, "type":"ltrap", "limits":[l_c_rt+(h_c_rt-l_c_rt)*p[0], l_c_rt+(h_c_rt-l_c_rt)*p[0], l_c_rt+(h_c_rt-l_c_rt)*p[2]]},
                                             "good"    :{"membership":0, "membership_max":1, "type":"tria" , "limits":[l_c_rt+(h_c_rt-l_c_rt)*p[1], l_c_rt+(h_c_rt-l_c_rt)*p[3], l_c_rt+(h_c_rt-l_c_rt)*p[5]]},
                                             "high"    :{"membership":0, "membership_max":1, "type":"rtrap", "limits":[l_c_rt+(h_c_rt-l_c_rt)*p[4], l_c_rt+(h_c_rt-l_c_rt)*p[6], l_c_rt+(h_c_rt-l_c_rt)*p[6]]}}}

    fuzzy_c.input["y_c_rc"]   = {"value"    : y_c_rc, 
                                 "function":{"low"     :{"membership":0, "membership_max":1, "type":"ltrap", "limits":[l_c_rc+(h_c_rc-l_c_rc)*p[0], l_c_rc+(h_c_rc-l_c_rc)*p[0], l_c_rc+(h_c_rc-l_c_rc)*p[2]]},
                                             "good"    :{"membership":0, "membership_max":1, "type":"tria" , "limits":[l_c_rc+(h_c_rc-l_c_rc)*p[1], l_c_rc+(h_c_rc-l_c_rc)*p[3], l_c_rc+(h_c_rc-l_c_rc)*p[5]]},
                                             "high"    :{"membership":0, "membership_max":1, "type":"rtrap", "limits":[l_c_rc+(h_c_rc-l_c_rc)*p[4], l_c_rc+(h_c_rc-l_c_rc)*p[6], l_c_rc+(h_c_rc-l_c_rc)*p[6]]}}}

    fuzzy_c.input["y_c_cc"]   = {"value"    : y_c_cc, 
                                 "function":{"low"     :{"membership":0, "membership_max":1, "type":"ltrap", "limits":[l_c_cc+(h_c_cc-l_c_cc)*p[0], l_c_cc+(h_c_cc-l_c_cc)*p[0], l_c_cc+(h_c_cc-l_c_cc)*p[2]]},
                                             "good"    :{"membership":0, "membership_max":1, "type":"tria" , "limits":[l_c_cc+(h_c_cc-l_c_cc)*p[1], l_c_cc+(h_c_cc-l_c_cc)*p[3], l_c_cc+(h_c_cc-l_c_cc)*p[5]]},
                                             "high"    :{"membership":0, "membership_max":1, "type":"rtrap", "limits":[l_c_cc+(h_c_cc-l_c_cc)*p[4], l_c_cc+(h_c_cc-l_c_cc)*p[6], l_c_cc+(h_c_cc-l_c_cc)*p[6]]}}}

    # outputs    
    fuzzy_c.output["dr_f_rc"] = {"value"   : 0, 
                                 "function":{"reduce"  :{"membership":0, "membership_max":1, "type":"ltrap", "limits":[-dr_f_rc_m*2.09, -dr_f_rc_m, dr_f_rc_m     ]},
                                             "none"    :{"membership":0, "membership_max":1, "type":"tria" , "limits":[-dr_f_rc_m,       0,         dr_f_rc_m     ]},
                                             "increase":{"membership":0, "membership_max":1, "type":"rtrap", "limits":[-dr_f_rc_m,       dr_f_rc_m, dr_f_rc_m*2.09]}}}                                       

    fuzzy_c.output["dr_v_s1"] = {"value"   : 0, 
                                 "function":{"reduce"  :{"membership":0, "membership_max":1, "type":"ltrap", "limits":[-dr_v_s1_m*2.09, -dr_v_s1_m, dr_v_s1_m     ]},
                                             "none"    :{"membership":0, "membership_max":1, "type":"tria" , "limits":[-dr_v_s1_m,       0,         dr_v_s1_m     ]},
                                             "increase":{"membership":0, "membership_max":1, "type":"rtrap", "limits":[-dr_v_s1_m,       dr_v_s1_m, dr_v_s1_m*2.09]}}}                                          
                           
    fuzzy_c.output["dr_f_cc"] = {"value"   : 0, 
                                 "function":{"reduce"  :{"membership":0, "membership_max":1, "type":"ltrap", "limits":[-dr_f_cc_m*2.09, -dr_f_cc_m, dr_f_cc_m     ]},
                                             "none"    :{"membership":0, "membership_max":1, "type":"tria" , "limits":[-dr_f_cc_m,       0,         dr_f_cc_m     ]},
                                             "increase":{"membership":0, "membership_max":1, "type":"rtrap", "limits":[-dr_f_cc_m,       dr_f_cc_m, dr_f_cc_m*2.09]}}}                               

    # rules
    #-----------------------------------------------------------
    fuzzy_c.rules["f_rc1"] = {"input" :{"y_c_rt" :"high", 
                                        "y_c_rc" :"high"},
                              "output":{"dr_f_rc":"increase"}}

    fuzzy_c.rules["f_rc2"] = {"input" :{"y_c_rt" :"low", 
                                        "y_c_rc" :"low"},
                              "output":{"dr_f_rc":"reduce"}}

    fuzzy_c.rules["f_rc3"] = {"input" :{"y_c_rt" :"good",
                                        "y_c_rc" :"good"},
                              "output":{"dr_f_rc":"none"}}
    #-----------------------------------------------------------
    fuzzy_c.rules["v_rt1"] = {"input" :{"y_c_rt" :"high"},
                              "output":{"dr_v_s1":"increase"}}
    
    fuzzy_c.rules["v_rt2"] = {"input" :{"y_c_rt" :"low"},
                              "output":{"dr_v_s1":"reduce"}}

    fuzzy_c.rules["v_rt3"] = {"input" :{"y_c_rt" :"good"},
                              "output":{"dr_v_s1":"none"}}
    #-----------------------------------------------------------
    fuzzy_c.rules["f_cc1"] = {"input" :{"y_c_cc" :"high"},
                              "output":{"dr_f_cc":"increase"}}
    
    fuzzy_c.rules["f_cc2"] = {"input" :{"y_c_cc" :"low"},
                              "output":{"dr_f_cc":"reduce"}}

    fuzzy_c.rules["f_cc3"] = {"input" :{"y_c_cc" :"good"},
                              "output":{"dr_f_cc":"none"}}
    #-----------------------------------------------------------
    view_fuzzy_design(fuzzy_c)
    plt.show()