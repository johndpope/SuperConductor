
import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SimpleController():
    """This class is a simple controller for the
    super conductor project"""
    def __init__(self,  model):

        self.model = model

        self.leap_controller = Leap.Controller()

        self.lastFrameID = 0

        while True:
            if(self.leap_controller.is_connected):
                self.processFrame(self.leap_controller.frame())

    def processFrame(self, frame):
        if(frame.id == self.lastFrameID):
            return

        if len(frame.hands) >= 2:
            hand_left = frame.hands.leftmost
            hand_right = frame.hands.rightmost

            if(len(hand_left.fingers) == 1):
                self.model.volume.value = int(hand_right.stabilized_palm_position.y)
            elif(len(hand_left.fingers) == 2):
                self.model.pitch.value = int(hand_right.stabilized_palm_position.x)
            elif(len(hand_left.fingers) == 3):
                self.model.track.value = int(hand_right.stabilized_palm_position.z / 50)

        self.lastFrameID = frame.id

