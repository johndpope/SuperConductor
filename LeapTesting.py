import Leap, sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class TestListener(Leap.Listener):
    def on_init(self, controller):
        print "Initalized"

    def on_connect(self, controller):
        print "Connected"

        # Enable Gestures
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame
        frame = controller.frame()

        if not frame.hands.is_empty:
            hand = frame.hands[0]
            '''
            sys.stdout.write("Hands: {0}, fingers: {1}, tools: {2}, gestures: {3}         \r".format(
                len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures())))
            '''
            sys.stdout.write("Selector: {0},Palm Pos: {1}       \r".format(len(hand.fingers), hand.stabilized_palm_position.y))
            sys.stdout.flush()

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a test listener and controller
    listener = TestListener()
    controller = Leap.Controller()

    # have listener receive events
    controller.add_listener(listener)

    # keep going until enter
    print "Press Enter to quit..."
    sys.stdin.readline()

    # remove listener when done
    controller.remove_listener(listener)
    print " "

if __name__ == "__main__":
    main()
