class fuzzy:

    def __init__(self):
        self.input  = {}
        self.output = {}
        self.rules  = {}   

    def gen_xrange(self,io, N=100):
        '''
            generates a list of numbers between the min and max limits of all 
            the membership functions for an input|output (io)
            
            io: input[tag] | output[tag]
            N: number of increments
            return: list of number between min and max limits 
        '''
        def f_range(start, stop, inc):
            result = [start]
            while result[-1] < stop:
                result.append(result[-1]+inc)
            return result
        x = []
        for func in io["function"]:
            x.extend(io["function"][func]["limits"])
        x = f_range(min(x),max(x),(max(x)-min(x))/N)
        return x

    def memfunc(self,inpt=1,func="",limits=[0,1,2],memMax=1.):
        ''' inpt:   input
            func:   ltrap - left trapezium
                    rtrap - right trapezium
                    else  - triangle
            limits: func definition limits
            memMax: max allowed degree of membership
            
            return: degree of membership
        '''
        if   func == "ltrap" : return max(min((inpt-limits[2])/(limits[1]-limits[2]),memMax),0) # left trapesium
        elif func == "rtrap" : return max(min((limits[0]-inpt)/(limits[0]-limits[1]),memMax),0) # right trapesium
        elif inpt < limits[1]: return max(min((inpt-limits[0])/(limits[1]-limits[0]),memMax),0) # triangle left side
        else:                  return max(min((limits[2]-inpt)/(limits[2]-limits[1]),memMax),0) # triangle right side

    def gen_input_membership(self):
        '''
            generates input membership for each input on each memebership function
        '''
        for inpt in self.input.keys():
            for func in self.input[inpt]["function"].keys():
                self.input[inpt]["function"][func]["membership"] = self.memfunc(inpt  =self.input[inpt]["value"],
                                                                                func  =self.input[inpt]["function"][func]["type"],
                                                                                limits=self.input[inpt]["function"][func]["limits"],
                                                                                memMax=self.input[inpt]["function"][func]["membership_max"])

    def gen_output_membership(self):
        '''
            generates output membership for each rule on respective output memebership function
        '''
        for rule in self.rules.keys():
            membership = [self.input[inpt]["function"][self.rules[rule]["input"][inpt]]["membership"] for inpt in self.rules[rule]["input"]]
            membership = sum(membership)/float(len(membership))
            for otpt in self.rules[rule]["output"]:
                self.output[otpt]["function"][self.rules[rule]["output"][otpt]]["membership"] = min(membership,
                                                                                                    self.output[otpt]["function"][self.rules[rule]["output"][otpt]]["membership_max"]) 

    def calc_centroid(self):
        '''
            calculate the centroid for each output and assigns 
            it to the "value" key entry 
        '''
        for otpt in self.output.keys():
            x = self.gen_xrange(self.output[otpt])
            y = []
            for func in self.output[otpt]["function"].keys():
                y_ = [self.memfunc(inpt  =xi,
                                   func  =self.output[otpt]["function"][func]["type"],
                                   limits=self.output[otpt]["function"][func]["limits"],
                                   memMax=self.output[otpt]["function"][func]["membership"]) for xi in x]
                y.append(y_)
            y = [max(yi) for yi in zip(*y)]        
            try: self.output[otpt]["value"] = sum(xi*yi for xi,yi in zip(x,y))/sum(y)
            except: pass

    def gen_output(self):
        '''
            for a given set values in the inputs
            the following steps are followed:
            1. Update the input degree of membership for each membership function
            2. For each rule assign the degree of membership for each output
            3. Update the value for each output by calculating the centroid
               from the degree of membership from each membership function
        '''
        self.gen_input_membership()
        self.gen_output_membership()
        self.calc_centroid()

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from plotting.view_fuzzy_design import view_fuzzy_design

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
    import matplotlib.pyplot as plt
    plt.show()