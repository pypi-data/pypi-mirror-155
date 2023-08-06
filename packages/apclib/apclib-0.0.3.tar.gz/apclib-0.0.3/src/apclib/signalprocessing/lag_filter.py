class lag_filter:

    def __init__(self, signal, tc, dt):
        '''
        Calculates the 1st order lag of an input signal
            signal:  current signal
            fsignal: previous filtered signal
            tc:      lag/time constant
            dt:      sampling rate
        '''
        self.fsignal = signal
        self.tc = tc
        self.dt = dt
        
    def update(self, signal, tc=None, dt=None):
        if tc is not None: self.tc = tc
        if dt is not None: self.dt = dt
        if self.dt == 0: return signal
        lamb = 1./(self.tc/self.dt+1)
        self.fsignal = (1.-lamb)*self.fsignal + lamb*signal
        return self.fsignal

if __name__ == "__main__":

    import numpy as np
    import matplotlib.pyplot as plt
    
    N = 1000
    dt= 1    
    tc= 10
    t = np.arange(0,N*dt,dt)

    signal = 2
    lf = lag_filter(signal, tc, dt)
    T=[];M=[];F=[]
    np.random.seed(1)
    for ti in t:
        if ti == N*dt*0.25: tc*=2; print (ti, tc)
        if ti == N*dt*0.50: tc*=2; print (ti, tc)
        if ti == N*dt*0.75: tc*=2; print (ti, tc)
        
        signal += np.random.normal(0,10)        # true
        msignal = signal+np.random.normal(0,80) # measured
        fsignal = lf.update(msignal,tc,dt)      # filtered
        M.append(msignal)
        T.append( signal)
        F.append(fsignal)
        
    plt.figure(figsize=(20,7))
    plt.plot(t,M,"k-",linewidth=0.5,drawstyle="steps-post",label="measured")
    plt.plot(t,T,"b-",linewidth=1.0,drawstyle="steps-post",label="true")
    plt.plot(t,F,"r-",linewidth=2.0,drawstyle="steps-post",label="filtered")
    plt.legend(loc="upper right")
    plt.show()