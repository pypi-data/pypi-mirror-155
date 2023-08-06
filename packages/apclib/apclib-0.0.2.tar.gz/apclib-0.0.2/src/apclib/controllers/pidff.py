class pidff:

    def __init__(self, cv, sp, mv, mv_min, mv_max, dt, kc, ti, td=0, db=0, dv={}, kf={}):

        '''
         cv      controlled variable
         sp      set point
         mv      manipulated variable
         mv_min  manipulated variable lower limit
         mv_max  manipulated variable upper limit
         dt      sampling rate
         kc      controller gain
         ti      controller integral time constant
         td      controller derivative constant
         db      dead band
         dv      disturbance variable
         kf      feed forward gain (proportional)
        '''
        self.e      = [sp-cv]*3
        self.mv     = mv 
        self.mv_min = mv_min
        self.mv_max = mv_max
        self.dt     = dt
        self.kc     = kc
        self.ti     = ti
        self.td     = td 
        self.db     = db 
        self.dv     = dict(dv)
        self.kf     = dict(kf)

    def update_tune(self, mv_min, mv_max, kc, ti, td=0, db=0, kf={}):
        self.mv_min = mv_min
        self.mv_max = mv_max
        self.kc     = kc
        self.ti     = ti
        self.td     = td 
        self.db     = db 
        self.kf     = kf
        
    def update_mv(self, cv, sp, dv={}):
        self.e=[sp-cv,self.e[0],self.e[1]]
        if (abs(self.e[0]) > self.db*0.5) or self.db==0:                           # take control action if error falls outside deadband
            self.mv += (self.kc*                (self.e[0]-  self.e[1]          )+ #      P
                        self.kc/self.ti*self.dt*(self.e[0]                      )+ #      I
                        self.kc*self.td/self.dt*(self.e[0]-2*self.e[1]+self.e[2])) #      D
        for key in dv.keys():
            self.mv += self.kf[key]*(dv[key]-self.dv[key])                         #      FF
            self.dv[key]=dv[key]

        self.mv = max(min(self.mv,self.mv_max),self.mv_min)                        # clamp mv
        
        return self.mv

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from models.ramp import integrator_model
    import numpy as np
    import matplotlib.pyplot as plt

    N  =  400
    dt =  2
    k  = -0.01
    kd =  0.3
    de =  5

    y0 = 10
    cv = y0
    sp = y0+5
    mv = 50
    dv = {"1":10,
          "2":10}

    mv_min = -10000
    mv_max = 100000
    kc     = -10
    ti     = 20
    td     = 0 
    db     = 0
    kf     = {"1":-kd/k*1,
              "2":-kd/k*1}

    m =      integrator_model(k, de,dt,0,mv)
    d = {"1":integrator_model(kd,de,dt,0,dv["1"]),
         "2":integrator_model(kd,de,dt,0,dv["2"])}

    c = pidff(cv, sp, mv, mv_min, mv_max, dt, kc, ti, td, db, dv, kf)

    T=np.arange(0,N*dt,dt)
    CV=[];SP=[];MV=[];DV={"1":[],"2":[]}
    np.random.seed(1)
    for t in T:
        dv["1"] += np.random.normal(0,0.1)
        dv["2"] += np.random.normal(0,0.2)
        sp      += np.random.normal(0,0.0)

        c.update_tune(mv_min, mv_max, kc, ti, td, db, kf)
        mv  = c.update_mv(cv, sp, dv)
        cv  = m     .gen_response(mv     )+\
              d["1"].gen_response(dv["1"])+\
              d["2"].gen_response(dv["2"])+\
              y0
        CV.append(cv);SP.append(sp);MV.append(mv);DV["1"].append(dv["1"]);DV["2"].append(dv["2"])

    fig,ax=plt.subplots(3,1,figsize=(9,6),sharex=True)
    ax[0].plot(T,CV,"k-",drawstyle="steps-post",label="cv")
    ax[0].plot(T,SP,"r-",drawstyle="steps-post",label="sp")
    ax[0].plot(T,[sp-db*.5 for sp in SP],"r-",drawstyle="steps-post",label=None)
    ax[0].plot(T,[sp+db*.5 for sp in SP],"r-",drawstyle="steps-post",label=None)
    ax[1].plot(T,MV,"k-",drawstyle="steps-post",label="mv")
    ax[2].plot(T,DV["1"],"k-",drawstyle="steps-post",label="dv1")
    ax[2].plot(T,DV["2"],"k:",drawstyle="steps-post",label="dv2")
    ax[0].legend(loc="upper right",bbox_to_anchor=(1.1,1))
    ax[1].legend(loc="upper right",bbox_to_anchor=(1.1,1))    
    ax[2].legend(loc="upper right",bbox_to_anchor=(1.1,1))
    plt.show()