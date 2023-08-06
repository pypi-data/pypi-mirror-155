import datetime

def dataIsolate(data, aggPeriod, 
                highSTDdict,
                lowSTDdict):
    '''
        function to isolate data peiods for SISO System Identification
        
        Parameters
        ----------
        data : pandas - DataFrame
            Input DataFrame
        
        aggPeriod : int - minutes
            Period over which to aggregate data for std - minutes
            
        highSTDdict : dictionary
            keys:   tags that need to have a high STD
            values: min STD limit allowed for each tag
    
        lowSTDdict : dictionary
            keys:   tags that need to have a low STD 
            values: max STD limit allowed for each tag
    
        Returns
        -------
        s : pandas - DataFrame
        columns - start & end DateTimes sorted decending according to 
        highSTDtags calculated STD's
    '''
    
    tags = list(highSTDdict.keys()) + list(lowSTDdict.keys())
    s = data[tags].resample(str(aggPeriod)+"T", closed="left").std()
    
    s["mask"] = True
    for key in highSTDdict.keys():s["mask"] = s["mask"] & (s[key]>highSTDdict[key])
    for key in lowSTDdict.keys(): s["mask"] = s["mask"] & (s[key]<lowSTDdict [key])
           
    s = s.loc[s["mask"],:]
    s = s.sort_values(by = [list(highSTDdict.keys())[0]], ascending = 0).drop(["mask"],axis=1)
    
    s["startDateTime"] = s.index
    s["endDateTime"]   = s.index + datetime.timedelta(minutes=aggPeriod)
    s = s.reset_index().iloc[:,1:]

    return s

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from datagen.random_walk import gen_data

    rows = 17281
    data = pd.DataFrame(
        gen_data(rows=rows),
        index=pd.date_range(start="2022-06-01",end="2022-06-02", periods = rows).to_pydatetime().tolist())
    data[["x1","x4"]].plot()
    s = dataIsolate(
        data, 
        aggPeriod=120, 
        highSTDdict={"x4":30},
        lowSTDdict={"x1":12})
    ax = plt.gca()

    for index in s.index:
        mask = (data.index > s.loc[index,"startDateTime"]) & (data.index < s.loc[index,"endDateTime"])
        ax.fill_between(x = data.index, y1=data.min().min(), y2=data.max().max(), where = mask, color = "k", alpha=0.1)
    print (s)
    plt.show()