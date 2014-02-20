import Leap, sys, pygame
import threading
import os
from Globals import NUM_CONTROLS, Controls, GLOBAL, NUM_TRACKS, INSTRUMENTS

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

        self.controls = [Controls.VOLUME, Controls.PITCH, Controls.TEMPO, Controls.INSTRUMENT, Controls.TRACK]
        self.control_idx = 0

    def keyboard_listener(self):
        pygame.init()

        self.windowWidth = 600
        self.windowHeight = 300
        self.defaultColor = (255, 255, 255)
        self.highlightColor = (125, 125, 125)
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption("sccui")
        
        # Surface
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill ((50,0,80))
        
        model = self.model
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "quit"
                    # Remove the sample listener when done
                    self.leap_controller.remove_listener(self)
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print "quit"
                        # Remove the sample listener when done
                        self.leap_controller.remove_listener(self)
                        # user pressed ESC
                        sys.exit()
                    elif event.key == pygame.K_e:
                        self.start_listen = True
                    elif event.key == pygame.K_w:
                        self.control_idx = (self.control_idx - 1) % (len(self.controls) - 1)
                        model.set_control(self.controls[self.control_idx])
                        print("Control changed to {0}".format(model.current_control.name))
                    elif event.key == pygame.K_s:
                        self.control_idx = (self.control_idx + 1) % (len(self.controls) - 1)
                        model.set_control(self.controls[self.control_idx])
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
            
            self.screen.blit(self.background, (0,0))
    
            # Update UI
            font = pygame.font.Font(None, 36)            
  
            intX = 0
            intY = 0
            
            for n in self.controls:
                s = n.name + ":"
                if n == Controls.PLAY:
                    continue  
                if n == model.current_control:
                    text = font.render("%s" % s, 1, self.highlightColor, (255, 255, 255))
                else:
                    text = font.render("%s" % s, 1, self.defaultColor)
                              
                self.screen.blit(text, (intX,intY))
                if model.current_track == GLOBAL:
                    if n == Controls.TRACK:
                        text = font.render("    {0}          ".format("All"), 1, self.defaultColor)
                    elif n == Controls.INSTRUMENT:
                        text = font.render("    {0}          ".format("n/a"), 1, self.defaultColor)
                    else:
                        text = font.render("    {0:.0f}       ".format(model.globals[n]), 1, self.defaultColor)
                        
                else:
                    if n == Controls.TRACK:
                        text = font.render("    {0}          ".format(model.current_track), 1, self.defaultColor)
                    elif n == Controls.INSTRUMENT:
                        text = font.render("    {0}          ".format(INSTRUMENTS[model.controls[n][model.current_track]]), 1, self.defaultColor)
                    elif n == Controls.TEMPO:
                        text = font.render("    {0}          ".format("n/a"), 1, self.defaultColor)
                    else:
                        text = font.render("    {0}          ".format(model.controls[n][model.current_track]), 1, self.defaultColor)
                self.screen.blit(text, (150,intY))
                
                intY += 50
                
            text = font.render("%s" % "Progress:", 1, self.defaultColor)
            self.screen.blit(text, (intX,intY))
            text = font.render("    {0:.2%}          ".format(float(model.current_time) / model.final_time), 1, self.defaultColor)
            self.screen.blit(text, (150,intY))
            
            pygame.display.flip()
            
        exit()
    
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
                if model.current_track == GLOBAL:
                    self.initial_value = model.globals[model.current_control]
                else:
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
                    print("Tempo {0}".format(model.globals[Controls.TEMPO]))
                elif model.current_control == Controls.INSTRUMENT:
                    model.set_value(min(max(self.initial_value + offset, 0), 127))
                else:
                    model.set_value(self.initial_value + offset)


