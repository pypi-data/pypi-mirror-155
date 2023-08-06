class integrator_model:
    '''
        First order integrator model with dead-time
        K:          process gain
        delay:      dead-time
        dt:         sampling rate
        y0:         process output bias
        u:          process input (outflow-inflow)
    '''

    def __init__(self, K, delay, dt, y0, u0):
        self.K      = K
        self.delay  = delay
        self.dt     = dt
        self.y      = 0
        self.dy_dt  = 0
        self.y0     = y0
        self.dy_dt  = 0
        self.u_hist = [u0 for _ in range(int(round(delay/dt))+1)]
        self.u0     = u0

    def rk4(self, u):
        def dy_dt(y):
            return (u-self.u0)*self.K

        fa = dy_dt(self.y,              )
        fb = dy_dt(self.y + fa*self.dt/2)
        fc = dy_dt(self.y + fb*self.dt/2)
        fd = dy_dt(self.y + fc*self.dt  )
        
        self.y = self.y + self.dt/6*(fa + 2*fb + 2*fc + fd)

    def gen_response(self, u):
        # update model for delay updates
        new_shape = int(round(self.delay/self.dt))+1
        old_shape = len(self.u_hist)

        if new_shape > old_shape: 
            self.u_hist.extend([self.u_hist[-1] for _ in range(new_shape - old_shape)])
        else:
            self.u_hist = self.u_hist[:new_shape]
        
        # update history with new u
        for i in range(len(self.u_hist)-1):
            self.u_hist[i] = self.u_hist[i+1]
        self.u_hist[-1] = u
        
        # generate new response
        self.rk4(self.u_hist[0])
        
        return self.y + self.y0