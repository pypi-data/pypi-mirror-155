import numpy as np
from scipy import signal as si
from scipy.optimize import curve_fit

class TransferFunctionFit:
    def __init__(self, num, den, delay):
        self.num   = num   # transfer function numerator:   list
        self.den   = den   # transfer function denominator: list
        self.delay = delay # input-output delay:            int (seconds)
        self.R2    = None
        
    def gen_response(self, u, y0):
        # sampling interval in seconds
        dt = np.median((u.index[1:]-u.index[:-1]).seconds)
        
        # Delay input
        u_shift = np.repeat(u[0], int(round(self.delay/dt))+1)
        u       = np.array((u_shift.tolist() + u.values.tolist())\
                           [:u.shape[0]])-u[0]
            
        # Discrete time intervals            
        t  = np.arange(0,u.shape[0]*dt, dt)
        
        # Generate output   
        return si.TransferFunction(self.num,self.den).output(u,t)[1]+y0
    
    def optimize(self, u, y, iterations=1):
        for _ in range(iterations):
            
            # Set intial parameters and optimization bounds
            #------------------------------------------------------------------
            params_0 = self.num + self.den
            l_bounds = []
            u_bounds = []
            for el in params_0:
                if   el==0:l_bounds.append(-1e-100); u_bounds.append(1e-100 )  
                elif el>0 :l_bounds.append(el*0.01); u_bounds.append(el*1000)
                else      :l_bounds.append(el*1000.);u_bounds.append(el*.01 )
            if round(params_0[-1],1)==1: 
                l_bounds[-1]=1
                u_bounds[-1]=1+1e-15 
            if round(params_0[-2],2)==1 and round(params_0[-1],1)==0:
                l_bounds[-2]=1
                u_bounds[-2]=1+1e-15 
            
            # Fit numerator and denominator
            #------------------------------------------------------------------
            def model(u, *params):
                self.num   = params[:len(self.num)]
                self.den   = params[len(self.num):]
                return self.gen_response(u, y[0])
            params = curve_fit(model, u, y, 
                               p0 = params_0, 
                               bounds=(l_bounds,u_bounds))[0]
            self.num = params[:len(self.num)].tolist()
            self.den = params[len(self.num):].tolist()

            # Calc Delay
            #------------------------------------------------------------------
            if self.delay != 0:
                dt = np.median((u.index[1:]-u.index[:-1]).seconds)
                c_m = {}
                for de in range(0,int(u.shape[0]*0.2*dt),int(dt)):
                    self.delay = de
                    y_m        = self.gen_response(u, y[0])
                    c_m[de]    = np.corrcoef(y_m,y)[0,1]
                self.delay = max(c_m, key=c_m.get)
            
        #----------------------------------------------------------------------
        SSres   =  np.sum((y - self.gen_response(u, y[0]))**2)
        SStot   =  np.sum((y - np.mean(y))**2)
        self.R2 = (1 - SSres/SStot)

if __name__ == "__main__":
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from models.fopdt import first_order_model
    from models.ramp import integrator_model

    '''------------------------------------------------------------------------
       Compare Transfer function with base dy/dt models
    ----------------------------------------------------------------------- '''
    delay  = 0
    Kp     = 1
    Tc     = 10
    K      = 1    
    y0     = 0
    dt     = 5  # seconds
    period = 60 # seconds
    u0     = 0
    step   = 1
    
    start  = datetime.datetime(2021,1,1,0)
    end    = start + datetime.timedelta(seconds=period)
    t = np.arange(start,end,datetime.timedelta(seconds=dt)).astype(datetime.datetime)
    u = pd.Series(np.repeat(u0, t.shape[0]), index = t)
    u[1:] = u0+step
    
    fig, ax = plt.subplots(2,1, figsize=(12,15))
    # =========================================================================
    tff_  = TransferFunctionFit([Kp],[Tc,1],delay)
    fopd_ = first_order_model(Kp, Tc, delay, dt, y0, u0)
    fopd_ = [fopd_.gen_response(ui) for ui in u]
    fopd_.insert(0, y0)
    result = pd.DataFrame(np.c_[[u.index,u,tff_.gen_response(u,y0),fopd_[:-1]]].T)
    result.columns = ["Date", "u", "transferFunction", "dy/dt"]
    result.index = result.Date; result = result.drop(["Date"],axis=1) 
    result.index = np.arange(-dt,dt*(result.shape[0]-1),dt)
    result.plot(drawstyle="steps-post",ax=ax[0])
    for i,j in zip(result.index,result["transferFunction"]):
        ax[0].annotate(str(round(j,2)),xy=(i,j),ha="right",va="center")
    for i,j in zip(result.index,result["dy/dt"]):
        ax[0].annotate(str(round(j,2)),xy=(i,j),ha="right",va="center")
    ax[0].grid(True)
    # =========================================================================
    tff_  = TransferFunctionFit([K],[1,0],delay)
    foim_ = integrator_model(K, delay, dt, y0, 0)
    foim_ = [foim_.gen_response(ui) for ui in u]
    foim_.insert(0, y0)
    result = pd.DataFrame(np.c_[[u.index,u,tff_.gen_response(u,y0),foim_[:-1]]].T)
    result.columns = ["Date", "u", "transferFunction", "dy/dt"]
    result.index = result.Date; result = result.drop(["Date"],axis=1)
    result.index = np.arange(-dt,dt*(result.shape[0]-1),dt)
    result.plot(drawstyle="steps-post",ax=ax[1])
    for i,j in zip(result.index,result["transferFunction"]):
        ax[1].annotate(str(round(j,2)),xy=(i,j),ha="right",va="center")
    for i,j in zip(result.index,result["dy/dt"]):
        ax[1].annotate(str(round(j,2)),xy=(i,j),ha="right",va="center")
    ax[1].grid(True)
    plt.show()