import Leap, sys, pygame
import threading
import os
from Globals import NUM_CONTROLS, Controls, State, GLOBAL, NUM_TRACKS, INSTRUMENTS, PERCUSSION
from Leap import SwipeGesture
import time
import Tkinter, tkFileDialog, tkMessageBox

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
        self.conduct_tempo = False
        self.value = 0
        self.initial_value = 0
        
        self.start_multi_listen = False
        self.multi_listening = False
        self.stop_multi_listen = False
        self.value_x = 0
        self.initial_value_x = 0
        self.value_z = 0
        self.initial_value_z = 0
        
        self.controls = [Controls.VOLUME, Controls.PITCH, Controls.TEMPO, Controls.INSTRUMENT, Controls.TRACK]
        self.control_idx = 0
        
        self.exited = False
        self.replay = False

        self.swipeid = 0
        self.tap_list = []
        
        self.bgcolor = (102,0,204)

    def keyboard_listener(self):
        pygame.init()

        self.windowWidth = 750
        self.windowHeight = 550
        self.defaultColor = (255, 255, 255)
        self.highlightColor = (125, 125, 125)
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption("SuperConductor")
        
        root = Tkinter.Tk()
        root.withdraw()
        
        extention = ""
        
        model = self.model
        
        # Surface
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        
        while True:
            self.background.fill (self.bgcolor)
            self.screen.blit(self.background, (0,0))
            
            if (model.state != State.INIT):
                self.updateBGcolor()
            
            selectButton = self.drawButton(" Select file ", 595, 5, 3, 3)
            playButton = self.drawButton(" Play ", 7, 500, 3, 3)
            pauseButton = self.drawButton(" Pause ", playButton[2]+20, 500, 3, 3)
            stopButton = self.drawButton(" Stop ", pauseButton[2]+20, 500, 3, 3)
            
            self.drawKeys(510,405)
            
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
#                    elif event.key == pygame.K_t:

                    elif event.key == pygame.K_q:
                        if model.current_control == Controls.TEMPO:
                            self.start_listen = True
                            self.conduct_tempo = True
                        elif model.current_control != Controls.PITCH or model.current_track != GLOBAL:
                            pass
                        else:
                            self.start_multi_listen = True
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
                        if model.final_time != 0:
                            if float(model.current_time) / model.final_time == 1.0:
                                #self.replay = True
                                model.set_state(State.PLAY)
                                continue
                        self.restore_default()
                        print "Restoring Default for", model.current_control.name
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_e: # or event.key == pygame.K_t:
                        self.stop_listen = True
                    if event.key == pygame.K_q:
                        if model.current_control == Controls.TEMPO:
                            self.stop_listen = True
                        elif model.current_control != Controls.PITCH or model.current_track != GLOBAL:
                            pass
                        else:
                            self.stop_multi_listen = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    #select file
                    if ( pos[0] > selectButton[0] and pos[0] < selectButton[2] and pos[1] > selectButton[1] and pos[1] < selectButton[3] ):
                        #stop currently playing song
                        if (model.state == State.PLAY or model.state == State.PAUSE):
                            model.set_state(State.STOP)
                            
                        result = False
                        
                        while extention != "mid":
                            #ask user to choose a MIDI file
                            result = tkMessageBox.askokcancel("SuperConductor", "Please select a midi file.")
                            if result:
                                file = tkFileDialog.askopenfilename()
                                file_path = file.split('/')
                                fileName = file_path[len(file_path)-1]
                                fileSplit = fileName.split('.')
                                extention = fileSplit[len(fileSplit)-1]
                            else:
                                break
                        
                        if extention == "mid":      
                            model.initVars()
                            model.load_file(file)
                            model.fileName = fileName
                        
                            model.set_state(State.READY)
                        
                        extention = ""
                        
                    if (pos[1] > playButton[1] and pos[1] < playButton[3]):
                        #start
                        if (pos[0] > playButton[0] and pos[0] < playButton[2]):
                            if not ( model.state == State.INIT or model.state == State.PLAY):
                                model.set_state(State.PLAY)
                            else:
                                if (model.state == State.INIT):
                                    tkMessageBox.showinfo("sccui", "Please select a midi file")
                        #pause
                        if (pos[0] > pauseButton[0] and pos[0] < pauseButton[2]):
                            if (model.state == State.PLAY):
                                model.set_state(State.PAUSE)
                        #stop
                        if (pos[0] > stopButton[0] and pos[0] < stopButton[2]):
                            if (model.state == State.PLAY or model.state == State.PAUSE):
                                model.set_state(State.STOP)
                                self.restore_default()
    
            # Update UI
            font = pygame.font.SysFont("Lucida Console", 28)            
  
            intY = 10
            if model.fileName == None:
                printFileName = None
            elif len(model.fileName) > 20:
                printFileName = model.fileName[:20 - len(model.fileName)]
            else:
                printFileName = model.fileName
            text = font.render("Now playing:  %s" % printFileName, 1, self.defaultColor)
            self.screen.blit(text, (10,intY))
            intY += 30
            pygame.draw.rect(self.screen, self.defaultColor, [0, intY, self.windowWidth,3])
            
            intY += 20
            if ( model.state != State.INIT ):          
                for n in self.controls:
                    if n == Controls.PITCH and model.current_track == PERCUSSION:
                        s = "TYPE:"
                    else:
                        s = n.name + ":"
                    # Display control labels
                    if n == Controls.PLAY:
                        continue  
                    if n == model.current_control:
                        text = font.render("%s" % s, 1, self.highlightColor, (255, 255, 255))
                    else:
                        text = font.render("%s" % s, 1, self.defaultColor)
                                  
                    self.screen.blit(text, (10,intY))
                    
                    # Display net info on the side
                    if n == Controls.TRACK:
                       text = font.render("{0}".format("All"), 1, self.defaultColor)
                    elif n == Controls.INSTRUMENT or (n == Controls.PITCH and model.current_track == PERCUSSION):
                        text = font.render("", 1, self.defaultColor)
                    elif n == Controls.TEMPO:
                        text = font.render("{0:.0f}".format(model.globals[n]), 1, self.defaultColor)
                    else:
                        text = font.render("{0:+}".format(model.globals[n]), 1, self.defaultColor)
                    self.screen.blit(text, (400,intY)) 
                    
                    # Display per track info
                    if model.current_track == GLOBAL:
                        if n == Controls.TRACK:
                            text = font.render("{0}".format("All"), 1, self.defaultColor)
                        elif n == Controls.INSTRUMENT:
                            text = font.render("", 1, self.defaultColor)
                        elif n == Controls.TEMPO:
                            text = font.render("{0:.0f}".format(model.globals[n]), 1, self.defaultColor)
                        else:
                            text = font.render("{0:+}".format(model.globals[n]), 1, self.defaultColor)
                            
                    elif model.current_track == PERCUSSION:
                        if n == Controls.TRACK:
                            text = font.render("{0}".format("Percussion"), 1, self.defaultColor)
                        elif n == Controls.INSTRUMENT:
                            text = font.render("{0}".format("Percussion"), 1, self.defaultColor)
                        elif n == Controls.TEMPO:
                            text = font.render("", 1, self.defaultColor)
                        else:
                            text = font.render("{0:+}".format(model.controls[n][model.current_track]), 1, self.defaultColor)
                            
                    else:
                        if n == Controls.TRACK:
                            text = font.render("{0}".format(model.current_track + 1), 1, self.defaultColor)
                        elif n == Controls.INSTRUMENT:
                            text = font.render("{0}".format(INSTRUMENTS[model.controls[n][model.current_track]]), 1, self.defaultColor)
                        elif n == Controls.TEMPO:
                            text = font.render("", 1, self.defaultColor)
                        else:
                            text = font.render("{0:+}".format(model.controls[n][model.current_track]), 1, self.defaultColor)
                    self.screen.blit(text, (210,intY))
                    
                    if n == Controls.INSTRUMENT:
                        intY += 100
                    else:
                        intY += 50
                
                # Display current progress in the song
                text = font.render("%s" % "PROGRESS:", 1, self.defaultColor)
                self.screen.blit(text, (10,intY))
                progress = float(model.current_time) / model.final_time
                text = font.render("{0:.2%}".format(progress), 1, self.defaultColor)
                self.screen.blit(text, (400,intY))
                if progress == 1.0:
                    if (model.state != State.STOP):
                        model.set_state(State.STOP)
                    text = font.render("Press Space to replay", 1, self.defaultColor)
                    self.screen.blit(text, (10,intY + 70))
                
                intY += 35
                pygame.draw.rect(self.screen, self.defaultColor, [190, intY, 300,20])
                pygame.draw.rect(self.screen, self.highlightColor, [190, intY, progress*300,20])
                
            
            pygame.display.flip()
            
    def updateBGcolor(self):
        #light -> dark    
        #rgb: (153,51,255)->(127,0,255)->(102,0,204)->(76,0,153)->(51,0,102)->(25,0,51)
        #tempo:   400           320          240         160          80          0
        #red: 25 + (tempo/80)*25
        #green: tempo-320 * 0.64
        #blue: 51 + (tempo/80)*51
        red = 25 + (self.model.globals[Controls.TEMPO]/80)*25
        green = (self.model.globals[Controls.TEMPO] - 320) * 0.64
        blue = 51 + (self.model.globals[Controls.TEMPO]/80)*51
        
        if red <= 153:
            red = int(red)
        else:
            red = 153
            
        if green <= 51:
            if green < 0:
                green = 0
            else:
                green = int(green)
        else:
            green = 51
            
        if blue <= 255:
            blue = int(blue)
        else:
            blue = 255
            
        self.bgcolor = (red,green,blue)
        
        """
        red = 102 + model.globals[Controls.TEMPO]/4
        green = model.globals[Controls.TEMPO] - 150
        blue = 204 + (model.globals[Controls.TEMPO]/50)*2
                    
        if red <= 153:
            red = int(red)
        else:
            red = 153
            
        if green <= 51:
            if green < 0:
                green = 0
            else:
                green = int(green)
        else:
            green = 51
            
        if blue <= 255:
            blue = int(blue)
        else:
            blue = 255
        """
    
    def drawKeys(self, initX, initY):
        font = pygame.font.Font(None, 36)
        text = font.render("Keys:", 1, self.defaultColor)
        self.screen.blit(text, (initX,initY))
        y = initY+25
        font = pygame.font.Font(None, 30)
        if (self.model.current_track == GLOBAL or self.model.current_track == PERCUSSION) \
                and self.model.current_control == Controls.INSTRUMENT:
            text = font.render("E - ", 1, self.defaultColor)
        else:
            text = font.render("E - Change value", 1, self.defaultColor)
        self.screen.blit(text, (initX,y))
        y += 20
        if self.model.current_control == Controls.TEMPO:
            text = font.render("Q - Conduct", 1, self.defaultColor)
        elif self.model.current_control == Controls.PITCH and self.model.current_track == GLOBAL:
            text = font.render("Q - 3 Axis", 1, self.defaultColor)
        else:
            text = font.render("Q - ", 1, self.defaultColor)
        self.screen.blit(text, (initX,y))
        y += 20
        text = font.render("A, D - Select track", 1, self.defaultColor)
        self.screen.blit(text, (initX,y))
        y += 20
        text = font.render("W, S - Select control", 1, self.defaultColor)
        self.screen.blit(text, (initX,y))
        y += 20
        text = font.render("Space - Restore default", 1, self.defaultColor)
        self.screen.blit(text, (initX,y))
        
    def drawButton(self, word, initX, initY, border, shade):
        font = pygame.font.Font(None, 36)
        text = font.render(word, 1, (255,255,255))
        pygame.draw.rect(self.screen, (60, 60, 60), (initX, initY, text.get_width()+border+shade, text.get_height()+border+shade), 0)
        pygame.draw.rect(self.screen, (125, 125, 125), (initX, initY, text.get_width()+shade, text.get_height()+shade), 0)
        pygame.draw.rect(self.screen, (20,20,20), [initX,initY,text.get_width()+border+shade,text.get_height()+border+shade], 2)
        self.screen.blit(text, (initX+border,initY+border))
        return [initX, initY, initX+text.get_width()+border+shade, initY+text.get_height()+border+shade]
    
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
            if model.current_track == GLOBAL:
                return
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
                sys.stdout.write('Y Offset: {0}          \r'.format(offset))
                
                if model.current_control == Controls.TRACK:
                    pass
                # do nothing for conducting tempo
                elif model.current_control == Controls.TEMPO \
                        and self.conduct_tempo:
                    pass
                elif model.current_control == Controls.TEMPO:
                    offset = int(offset * .5)
                    model.set_global_value(max(self.initial_value + offset, 1))
                    print("Value {}".format(self.value))
                    print("Initial {}".format(self.initial_value))
                    print("Tempo {0}".format(model.globals[Controls.TEMPO]))
                elif model.current_control == Controls.INSTRUMENT:
                    offset = int(offset * .25)
                    model.set_value(min(max(self.initial_value + offset, 0), 127))
                elif model.current_control == Controls.PITCH:
                    offset = int(offset * .2)
                    model.set_value(min(max(self.initial_value + offset, -127), 127))
                else:
                    model.set_value(min(max(self.initial_value + offset, -127), 127))
                    
            if self.start_multi_listen:
                self.value = hand.palm_position.y
                self.value_x = -1 * hand.palm_position.x
                self.value_z = hand.palm_position.z
                self.initial_value = model.globals[model.current_control]
                self.initial_value_x = model.globals[Controls.TEMPO]
                self.initial_value_z = model.globals[Controls.VOLUME]
                self.start_multi_listen = False
                self.multi_listening = True
            
            if self.stop_multi_listen:
                self.multi_listening = False
                self.stop_multi_listen = False
                
            if self.multi_listening:
                offsetY = int(hand.palm_position.y - self.value)
                offsetX = int(hand.palm_position.x - self.value_x)
                offsetZ = int(hand.palm_position.z - self.value_z)
                
                offsetX = int(offsetX * .6)
                # set tempo
                model.current_control = Controls.TEMPO
                model.set_global_value(max(self.initial_value_x + offsetX, 1))
                
                # set volume
                offsetZ = int(offsetZ * -0.3)
                model.current_control = Controls.VOLUME
                model.set_global_value(self.initial_value_z + offsetZ)
                
                # set pitch
                model.current_control = Controls.PITCH
                offsetY = int(offsetY * .1)
                model.set_value(min(max(self.initial_value + offsetY, -127), 127))

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
                    pass
#                   if swipe.direction.y > 0:
#                       # vertical up
#                       self.control_idx = (self.control_idx - 1) % (len(self.controls) - 1)
#                       model.set_control(self.controls[self.control_idx])
#                       print("Control changed to {0}".format(model.current_control.name))
#                   else:
#                       # vertical down
#                       self.control_idx = (self.control_idx + 1) % (len(self.controls) - 1)
#                       model.set_control(self.controls[self.control_idx])
#                       print("Control changed to {0}".format(model.current_control))
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
                        model.set_global_value(max(self.initial_value + offset, 1))
                        print("Value {}".format(self.value))
                        print("Initial {}".format(self.initial_value))
                        print("Tempo {0}".format(model.globals[Controls.TEMPO]))
                    elif model.current_control == Controls.INSTRUMENT:
                        model.set_value(min(max(self.initial_value + offset, 0), 127))
                    else:
                        model.set_value(min(max(self.initial_value + offset, -127), 127))

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP \
                        and self.listening and self.conduct_tempo:
                
                self.bgcolor = (0, 150, 100)
                
                t = time.time()
                if len(self.tap_list) < 6:
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
                    for i in range(0, len(self.tap_list) - 1):
                        dif = self.tap_list[i+1] - self.tap_list[i]
                        bpm.append(1.0/(dif * (1.0/60)))

                    print(bpm)
                    avgbpm = sum(bpm)/len(bpm)
                    print(avgbpm)
                    model.set_global_value(avgbpm)
