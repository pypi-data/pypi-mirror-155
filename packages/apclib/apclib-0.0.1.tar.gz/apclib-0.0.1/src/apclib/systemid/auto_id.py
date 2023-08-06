import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from systemid.dataIsolate import dataIsolate
from systemid.TransferFunctionFit import TransferFunctionFit
from plotting.multi_yax_plot import multi_yax_plot
from plotting.update_legend import update_legend
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def auto_id(data, 
             aggPeriod=30, 
             optimize_iters = 1, 
             inpt="", 
             outp="", 
             highSTDdict={}, 
             lowSTDdict={},
             num=[1], 
             den=[20,0], 
             delay=0,
             minute_shift=datetime.timedelta(minutes=0),
             period_index=range(2),
             y0 = None):

    #--------------------------------------------------------------------------
    s = dataIsolate(data        = data,
                    aggPeriod   = aggPeriod,
                    highSTDdict = highSTDdict,
                    lowSTDdict  = lowSTDdict,
                    ).round(4)  
    
    print (s.shape)
    if period_index is None: period_index = range(5)
    s = s.iloc[period_index,:]
    print (s)
    fig, ax = plt.subplots(s.shape[0],2, sharey=False, figsize=(25,12))
    plt.subplots_adjust(wspace=0.55)
    
    for i,idx in enumerate(s.index):
        mask = (data.index > (s.loc[idx,"startDateTime"]) + minute_shift) &\
               (data.index < (s.loc[idx,"endDateTime"  ]) + minute_shift)
        di = data.loc[mask,list(highSTDdict.keys())+list(lowSTDdict.keys())].fillna(method="pad")
        di = di.loc[~di.isnull().any(axis=1),:]
        
        #----------------------------------------------------------------------
        tff = TransferFunctionFit(num,den,delay)
        tff.optimize(di[inpt],di[outp],optimize_iters)
        y0_ = y0
        if y0 is None: y0_ = di[outp][0]
        y = tff.gen_response(di[inpt], y0_)
    
        ax[i,0].plot(di.index, di[inpt],"k-", label = inpt,    drawstyle = "steps-post", linewidth  = 1.0)
        if i==0:update_legend(ax[i,0], ["k"],0,1.2,2,True)
        ax[i,0] = ax[i,0].twinx()
        ax[i,0].plot(di.index, di[outp],"r.", label = outp,    drawstyle = "steps-post", markersize = 4.0)
        ax[i,0].plot(di.index, y,       "r-", label = "model", drawstyle = "steps-post", linewidth  = 2.0)
        ax[i,0].set_ylim(min(min(y),di[outp].min()),max(max(y),di[outp].max()))
        if i==0:update_legend(ax[i,0],["r","r"],0.8,1.2,2,True)
        #----------------------------------------------------------------------
        text = F"num: { [round(x,6) for x in tff.num]}\n"  +\
               F"den:  {[int(round(x,0)) for x in tff.den]}\n"  +\
               F"del:   {tff.delay}\n"+\
               F"R2:    {round(tff.R2,2)}"
        ax[i,0].text(di.index[0]+(di.index[-1]-di.index[0])*1.15, 
                     di[outp].max(), 
                     text,ha='left',va='top', 
                     fontweight="bold",fontsize=12,color="white", 
                     bbox=dict(facecolor='firebrick',alpha=0.8,edgecolor='white'))
        #----------------------------------------------------------------------
        lims = []
        for lowSTD_tag in lowSTDdict.keys():
            min_   = data[lowSTD_tag].min()
            max_   = data[lowSTD_tag].max()
            range_ = max_ - min_
            lims.append([min_- 0.05*range_, max_ + 0.05*range_])
        leftax_df      = di[list(lowSTDdict.keys())].iloc[:,:3]
        rightax_df     = di[list(lowSTDdict.keys())].iloc[:,3:]
        leftax_limits  = lims[:3]
        rightax_limits = lims[3:]
        
        multi_yax_plot(ax[i,1],
                       leftax_df=leftax_df,
                       leftax_limits=leftax_limits,
                       rightax_df=rightax_df,
                       rightax_limits=rightax_limits,
                       colors=sns.color_palette("deep", len(lowSTDdict.keys())),linewidth=1)
    plt.show()

if __name__ == "__main__":
    import pandas as pd
    from datagen.random_walk import gen_data

    rows = 3601
    data = pd.DataFrame(
        gen_data(tag_info_dict={"y":{"start":0,"std":10},"u":{"start":0,"std":1},"d":{"start":0,"std":1}}, rows=rows),
        index=pd.date_range(start="2022-06-01",end="2022-06-02 01:00:00", periods = rows).to_pydatetime().tolist())

    data.loc[data.index > "2022-06-01 15:20:00", "u"] = data.loc[data.index > "2022-06-01 15:20:00", "u"] + 100
    data.plot()

    auto_id(data, 
             aggPeriod=120, 
             optimize_iters = 1, 
             inpt="u", 
             outp="y", 
             highSTDdict={"y":0,"u":0},
             lowSTDdict={"d":float("inf")},
             num=[1], 
             den=[20,1], 
             delay=0,
             minute_shift=datetime.timedelta(minutes=0),
             period_index=range(2),
             y0 = None)