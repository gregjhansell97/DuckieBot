#from Controls import Control

class Driver:
    '''
    '''
    def __init__(self):
        self._keys_pressed = []
        self._keys_released = []
        self.speed_accel = 0.2
        self.omega_accel = 0.2
        self.speed = 0
        self.omega = 0

    def set_input(next_pressed=[], next_released=[]):
        print("#"*50)
        print(next_pressed)
        print(next_released)
        print("#"*50)
        return

        if "up" in next_released or "down" in next_released:
            self.speed = 0
        elif "right" in next_released or "left" in next_released:
            self.omega = 0
        
        if "up" in next_pressed:
            self.speed += 
      
        self._keys_pressed = 
       pass

    def frame(self, frame):
        return frame
        
