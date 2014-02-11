import Leap, sys


"""A simple listener for the
leap controller"""
class SimpleListener(Leap.Listener):
    
    def set_model(self, model):
        self._model = model
        
    def on_init(self, controller):
        print "Initialized"
        #self.lastFrameID = 0
    
    def on_connect(self, controller):
        print "Connected"
        
        
    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"
        
        """
        while True:
            if(self.leap_controller.is_connected):
                self.processFrame(self.leap_controller.frame())
        """
        
    def on_frame(self, leapController):
        frame = leapController.frame()

        if len(frame.hands) >= 2:
            hand_left = frame.hands.leftmost
            hand_right = frame.hands.rightmost

            if(len(hand_left.fingers) == 1):
                print "1 finger -----------------------"
                self._model.control.value = "volume"
                self._model.volume.value = int(hand_right.stabilized_palm_position.y)
                #self._dcb("volume", int(hand_right.stabilized_palm_position.y))
            elif(len(hand_left.fingers) == 2):
                print "2 finger -----------------------"
                self._model.control.value = "pitch"
                self._model.pitch.value = int(hand_right.stabilized_palm_position.x)
                #self._dcb("pitch", int(hand_right.stabilized_palm_position.x))
            elif(len(hand_left.fingers) == 3):
                print "3 finger -----------------------"
                self._model.control.value = "track"
                self._model.track.value = int(hand_right.stabilized_palm_position.z / 50)
                #self._dcb("track", int(hand_right.stabilized_palm_position.z / 50))
        
    def state_string(self, state):
       if state == Leap.Gesture.STATE_START:
           return "STATE_START"
    
       if state == Leap.Gesture.STATE_UPDATE:
           return "STATE_UPDATE"
    
       if state == Leap.Gesture.STATE_STOP:
           return "STATE_STOP"
    
       if state == Leap.Gesture.STATE_INVALID:
           return "STATE_INVALID"