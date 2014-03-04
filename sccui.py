import Leap, sys, pygame
import threading
import os
from Globals import NUM_CONTROLS, Controls, GLOBAL, NUM_TRACKS, INSTRUMENTS
from Leap import SwipeGesture
import time

class Controller(Leap.Listener):
    
    def setup(self, model, leap_controller, fileName):
        self.model = model
        self.leap_controller = leap_controller
        self.fileName = fileName
        
        self.thread = threading.Thread(target=self.keyboard_listener)
        self.thread.daemon = True
        self.thread.start()

        self.start_listen = False
        self.listening = False
        self.stop_listen = False
        self.conduct_tempo = False
        self.value = 0
        self.initial_value = 0

        self.controls = [Controls.VOLUME, Controls.PITCH, Controls.TEMPO, Controls.INSTRUMENT, Controls.TRACK]
        self.control_idx = 0
        
        self.exited = False

        self.swipeid = 0
        self.tap_list = []

    def keyboard_listener(self):
        pygame.init()

        self.windowWidth = 600
        self.windowHeight = 400
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
                    self.exited = True
                    self.leap_controller.remove_listener(self)
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print "quit"
                        # Remove the sample listener when done
                        self.exited = True
                        self.leap_controller.remove_listener(self) 
                        sys.exit()
                    elif event.key == pygame.K_e:
                        self.start_listen = True
                    elif event.key == pygame.K_t:
                        self.start_listen = True
                        self.conduct_tempo = True
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
                    elif event.key == pygame.K_SPACE:
                        self.restore_default()
                        print "Restoring Default for", model.current_control.name
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_e or event.key == pygame.K_t:
                        self.stop_listen = True
                        
            
            self.screen.blit(self.background, (0,0))
    
            # Update UI
            font = pygame.font.Font(None, 36)            
  
            intY = 0
            
            text = font.render("Now playing:  %s" % self.fileName, 1, self.defaultColor)
            self.screen.blit(text, (0,intY))
            intY += 20
            text = font.render("---------------------------------------------------------------------", 1, self.defaultColor)
            self.screen.blit(text, (0,intY))
            
            intY += 35
                           
            for n in self.controls:
                s = n.name + ":"
                # Display control labels
                if n == Controls.PLAY:
                    continue  
                if n == model.current_control:
                    text = font.render("%s" % s, 1, self.highlightColor, (255, 255, 255))
                else:
                    text = font.render("%s" % s, 1, self.defaultColor)
                              
                self.screen.blit(text, (0,intY))
                
                # Display global info on the side
                if n == Controls.TRACK:
                   text = font.render("    {0}          ".format("All"), 1, self.defaultColor)
                elif n == Controls.INSTRUMENT:
                    text = font.render("", 1, self.defaultColor)
                else:
                    text = font.render("    {0:.0f}       ".format(model.globals[n]), 1, self.defaultColor)
                self.screen.blit(text, (350,intY)) 
                
                # Display per track info
                if model.current_track == GLOBAL:
                    if n == Controls.TRACK:
                        text = font.render("    {0}          ".format("All"), 1, self.defaultColor)
                    elif n == Controls.INSTRUMENT:
                        text = font.render("", 1, self.defaultColor)
                    else:
                        text = font.render("    {0:.0f}       ".format(model.globals[n]), 1, self.defaultColor)
                        
                else:
                    if n == Controls.TRACK:
                        text = font.render("    {0}          ".format(model.current_track), 1, self.defaultColor)
                    elif n == Controls.INSTRUMENT:
                        text = font.render("    {0}          ".format(INSTRUMENTS[model.controls[n][model.current_track]]), 1, self.defaultColor)
                    elif n == Controls.TEMPO:
                        text = font.render("", 1, self.defaultColor)
                    else:
                        text = font.render("    {0}          ".format(model.controls[n][model.current_track]), 1, self.defaultColor)
                self.screen.blit(text, (150,intY))
                
                intY += 50
            
            # Display current progress in the song
            text = font.render("%s" % "PROGRESS:", 1, self.defaultColor)
            self.screen.blit(text, (0,intY))
            progress = float(model.current_time) / model.final_time
            text = font.render("    {0:.2%}          ".format(progress), 1, self.defaultColor)
            self.screen.blit(text, (350,intY))
            
            intY += 25
            pygame.draw.rect(self.screen, self.highlightColor, [180, intY, progress*350,20])
            pygame.draw.rect(self.screen, self.defaultColor, [180+(350*progress),intY, 350-(350*progress),20])
            
            
            pygame.display.flip()
    
    def on_init(self, controller):
        print "Initialized"
        #self.lastFrameID = 0
    
    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        print "Connected"
        
    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"
    
    def restore_default(self):
        model = self.model
    
        if model.current_control == Controls.TEMPO:
            model.set_global_value(model.default_tempo)
        elif model.current_control == Controls.INSTRUMENT:
            model.set_value(model.default_instruments[model.current_track])
        else:
            model.set_value(0)
    
    def on_frame(self, leapController):
        frame = leapController.frame()
        model = self.model

        if len(frame.hands) >= 1:
            hand = frame.hands[0]

            if self.start_listen:
                self.value = hand.palm_position.y
                if model.current_track == GLOBAL \
                    or model.current_control == Controls.TEMPO:
                    self.initial_value = model.globals[model.current_control]
                else:
                    self.initial_value = model.controls[model.current_control][model.current_track]
                print("Initial {0}".format(self.value))
                self.start_listen = False
                self.listening = True
                print("start listening")

            if self.stop_listen:
                self.listening = False
                self.stop_listen = False
                self.conduct_tempo = False
                print("stop listening")
            
            if self.listening:
                offset = int(hand.palm_position.y - self.value)
                sys.stdout.write('Offset: {0}          \r'.format(offset))
                
                if model.current_control == Controls.TRACK:
                    pass
                # do nothing for conducting tempo
                elif model.current_control == Controls.TEMPO \
                        and self.conduct_tempo:
                    pass
                elif model.current_control == Controls.TEMPO:
                    offset = int(offset * .5)
                    model.set_global_value(self.initial_value + offset)
                    print("Value {}".format(self.value))
                    print("Initial {}".format(self.initial_value))
                    print("Tempo {0}".format(model.globals[Controls.TEMPO]))
                elif model.current_control == Controls.INSTRUMENT:
                    offset = int(offset * .25)
                    model.set_value(min(max(self.initial_value + offset, 0), 127))
                elif model.current_control == Controls.PITCH:
                    offset = int(offset * .1)
                    model.set_value(self.initial_value + offset)
                else:
                    model.set_value(self.initial_value + offset)

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE \
                    and len(frame.gestures()) == 1 \
                    and not self.listening:
                # print(len(frame.gestures()))
                if gesture.id == self.swipeid:
                    continue
                self.swipeid = gesture.id
                swipe = SwipeGesture(gesture)
                # horizontal or vertical
                if abs(swipe.direction.y) > abs(swipe.direction.x):
                    if swipe.direction.y > 0:
                        # vertical up
                        self.control_idx = (self.control_idx - 1) % (len(self.controls) - 1)
                        model.set_control(self.controls[self.control_idx])
                        print("Control changed to {0}".format(model.current_control.name))
                    else:
                        # vertical down
                        self.control_idx = (self.control_idx + 1) % (len(self.controls) - 1)
                        model.set_control(self.controls[self.control_idx])
                        print("Control changed to {0}".format(model.current_control))
                else:
                    # horizontal left
                    offset = 0
                    if swipe.direction.x > 0:
                        offset = -1
                    else:
                    # horizontal right
                        offset = 1

                    if model.current_track == GLOBAL or model.current_control == Controls.TEMPO:
                        self.initial_value = model.globals[model.current_control]
                    else:
                        self.initial_value = model.controls[model.current_control][model.current_track]
                    if model.current_control == Controls.TRACK:
                        pass
                    elif model.current_control == Controls.TEMPO:
                        model.set_global_value(self.initial_value + offset)
                        print("Value {}".format(self.value))
                        print("Initial {}".format(self.initial_value))
                        print("Tempo {0}".format(model.globals[Controls.TEMPO]))
                    elif model.current_control == Controls.INSTRUMENT:
                        model.set_value(min(max(self.initial_value + offset, 0), 127))
                    else:
                        model.set_value(self.initial_value + offset)
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP \
                        and self.listening and self.conduct_tempo:
                
                t = time.time()
                if len(self.tap_list) < 10:
                    if len(self.tap_list) > 0:
                        dif = t - self.tap_list[-1]
                        if dif < .1:
                            continue
                    self.tap_list.append(time.time())
                    print("TAP")
                else:
                    dif = t - self.tap_list[-1]
                    if dif < .1:
                        continue
                    self.tap_list.pop(0)
                    self.tap_list.append(time.time())
                    print("TAP")

                    # calculate and set tempo bpm
                    bpm = []
                    for i in range(0, len(self.tap_list), 2):
                        dif = self.tap_list[i+1] - self.tap_list[i]
                        bpm.append(1.0/(dif * (1.0/60)))

                    print(bpm)
                    avgbpm = sum(bpm)/len(bpm)
                    print(avgbpm)
                    model.set_global_value(avgbpm)
