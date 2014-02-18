import Leap, sys, pygame
import threading
from Globals import NUM_CONTROLS, Controls, GLOBAL, NUM_TRACKS

class Controller(Leap.Listener):
    
    def setup(self, model, leap_controller):
        self.model = model
        self.leap_controller = leap_controller

        self.thread = threading.Thread(target=self.keyboard_listener)
        self.thread.daemon = True
        self.thread.start()

        self.start_listen = False
        self.listening = False
        self.stop_listen = False
        self.value = 0
        self.initial_value = 0

    def keyboard_listener(self):
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        model = self.model

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "quit"
                    sys.exit()
                    # Remove the sample listener when done
                    self.leap_controller.remove_listener(self)
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print "quit"
                        # user pressed ESC
                        sys.exit()
                        # Remove the sample listener when done
                        self.leap_controller.remove_listener(self)
                        break
                    elif event.key == pygame.K_e:
                        self.start_listen = True
                    elif event.key == pygame.K_w:
                        model.set_control((model.current_control + 1) % NUM_CONTROLS)
                        print("Control changed to {0}".format(model.current_control))
                    elif event.key == pygame.K_s:
                        model.set_control((model.current_control - 1) % NUM_CONTROLS)
                        print("Control changed to {0}".format(model.current_control))
                    elif event.key == pygame.K_a:
                        model.set_track((model.current_track - 1) % NUM_TRACKS)
                        print("Track changed to {0}".format(model.current_track))
                    elif event.key == pygame.K_d:
                        model.set_track((model.current_track + 1) % NUM_TRACKS)
                        print("Track changed to {0}".format(model.current_track))
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_e:
                        self.stop_listen = True
        
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
        
    def on_frame(self, leapController):
        frame = leapController.frame()
        model = self.model

        if len(frame.hands) >= 1:
            hand = frame.hands[0]

            if self.start_listen:
                self.value = hand.palm_position.y
                self.initial_value = model.controls[model.current_control][model.current_track]
                print("Initial {0}".format(self.value))
                self.start_listen = False
                self.listening = True

            if self.stop_listen:
                self.listening = False
                self.stop_listen = False
            
            if self.listening:
                offset = int(hand.palm_position.y - self.value)
                sys.stdout.write('Offset: {0}          \r'.format(offset))
                
                if model.current_control == Controls.TRACK:
                    pass
                elif model.current_control == Controls.TEMPO:
                    model.set_global_value(self.initial_value + offset)
                    print("Tempo {0}".format(model.controls[Controls.TEMPO][GLOBAL]))
                elif model.current_control == Controls.INSTRUMENT:
                    model.set_value(min(max(self.initial_value + offset, 0), 127))
                else:
                    model.set_value(offset)


