def gain_update(kc_small,kc_large,cv,cv_limits=[None,None,None,None]):
    '''

    ------------------------------------------------
     positive kc
    ------------------------------------------------
    ...lim[0]                 lim[3]...  -> kc_large
             .               .
              .             .
              lim[1]...lim[2]            -> kc_small


    ------------------------------------------------
      negative kc
    ------------------------------------------------
              lim[1]...lim[2]            -> kc_small
              .             .
             .               .
    ...lim[0]                 lim[3]...  -> kc_large

    '''
    if   cv< cv_limits[0] or  cv>cv_limits[3]:return kc_large
    elif cv> cv_limits[1] and cv<cv_limits[2]:return kc_small
    elif cv<=cv_limits[1]:return (kc_small-kc_large)*(cv-cv_limits[1])/(cv_limits[1]-cv_limits[0])+kc_small
    else:                 return (kc_large-kc_small)*(cv-cv_limits[3])/(cv_limits[3]-cv_limits[2])+kc_large

if __name__ == "__main__":

    import numpy as np
    import matplotlib.pyplot as plt

    levels     = np.arange(0,100,0.1)
    level_low  = 20
    level_high = 80
    kc_small   = -0.1
    kc_large   = -1
    gains      = []
    
    for level in levels:
        gains.append(gain_update(kc_small  = kc_small, 
                                 kc_large  = kc_large, 
                                 cv        = level, 
                                 cv_limits =[level_low  - (level_high-level_low)*0.1,
                                             level_low  + (level_high-level_low)*0.1,
                                             level_high - (level_high-level_low)*0.1,
                                             level_high + (level_high-level_low)*0.1]))
    fig, ax = plt.subplots(1,1,figsize=(7,7))
    ax.plot(levels,gains,"k")
    ax.plot([level_low, level_low ],[kc_small,kc_large],"r:")
    ax.plot([level_high,level_high],[kc_small,kc_large],"r:") 
    plt.show()       