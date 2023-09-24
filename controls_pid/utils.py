"""
MIT License, Kemal Ficici, 2018
github.com/kemfic
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

class process(object):
    process_response = 0

    def __init__(self, const_shift=0, noise=False):
        self.constant_shift = const_shift/512.0
        self.noise = noise

    def update(self, controller_response, current_state):
        self.process_response = self.process_response*0.96 - 0.01*controller_response + self.constant_shift +self.noise*((np.random.rand()-0.5)/100)
        self.process_response = min(1, self.process_response)
        self.process_response = max(-1, self.process_response)
        return current_state + self.process_response

def error(current_state, set_state):
    return current_state - set_state
    
class Plant(object):
    
    def __init__(self, control, d_t=0.1, t_max=60, set_steady=False, set_shift=False, set_sin=False, noise=False):
        self.delta_t = d_t
        self.t_max = t_max
        self.t = np.arange(0, self.t_max, self.delta_t)
        if set_sin:
            self.set_states = np.sin(self.t*4*np.pi/self.t_max)
        elif set_steady:
            self.set_states = np.zeros_like(self.t)
        else:
            self.set_states = np.zeros_like(self.t)
            self.set_states[200:400] = 1
        
        self.cur_process = process(set_shift, noise)        
        self.controller = control

    def simulate(self):
        states = np.zeros_like(self.t)
        states[0] = -1
        errors = np.zeros_like(self.t)
        errors[0] = error(states[0], self.set_states[0])


        for i in range(1,len(self.t)):
            controller_response = self.controller.update(errors[i-1], delta_t = self.delta_t)
            states[i] = self.cur_process.update(controller_response, states[i-1])
            errors[i] = error(states[i], self.set_states[i])
        
        errortotal = np.sum(abs(errors))

        plt.plot(states, color='blue', label='environment state')
        plt.plot(self.set_states, color='red', label = 'set (desired) state')
        plt.plot([], color='none', label = 'total error: ' + str(errortotal)[0:9])
        plt.xlabel('Time')
        plt.ylabel('Error')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
