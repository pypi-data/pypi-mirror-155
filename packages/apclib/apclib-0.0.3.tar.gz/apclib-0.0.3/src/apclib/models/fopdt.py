class first_order_model:
    '''
        First order self-regualting model with dead-time
        Kp:         process gain
        Tc:         time constant
        delay:      dead-time
        dt:         sampling rate
        y0:         process output bias
        u0:         process input bias
    '''

    def __init__(self, Kp, Tc, delay, dt, y0, u0):
        self.Kp     = Kp
        self.Tc     = Tc
        self.delay  = delay
        self.dt     = dt
        self.y      = 0
        self.dy_dt  = 0
        self.y0     = y0
        self.dy_dt  = 0
        self.u0     = u0
        self.u_hist = [u0 for _ in range(int(round(delay/dt))+1)]

    def rk4(self, u):
        def dy_dt(y):
            return u*self.Kp/self.Tc - y/self.Tc

        fa = dy_dt(self.y,              )
        fb = dy_dt(self.y + fa*self.dt/2)
        fc = dy_dt(self.y + fb*self.dt/2)
        fd = dy_dt(self.y + fc*self.dt  )

        self.y = self.y + self.dt/6*(fa + 2*fb + 2*fc + fd)

    def gen_response(self, u):

        # update model for Kp and Tc updates
        self.u0 = self.u_hist[0] - (self.dy_dt + self.y/self.Tc)/(self.Kp/self.Tc)

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
        self.rk4(self.u_hist[0] - self.u0)

        # reset dy_dt to update u0 accordingly on next execute
        self.dy_dt = (self.u_hist[0] - self.u0)*self.Kp/self.Tc - self.y/self.Tc

        return self.y + self.y0