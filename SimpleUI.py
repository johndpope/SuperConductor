'''
A simple UI
'''

from SimpleListener import SimpleListener
from SuperConductorModel import SuperConductorModel
from AbstractView import AbstractView
import pygame, sys, Leap, Player

class SimpleUI():
    def __init__(self, model):
        model.register_track_listener(self.update_track)
        model.register_current_note_listener(self.update_note)
        model.register_volume_listener(self.update_volume)
        model.register_pitch_listener(self.update_pitch)
        model.register_speed_listener(self.update_speed)
        model.register_instrument_listener(self.update_instrument)
        model.register_control_listener(self.update_control)
        
        self.windowWidth = 600
        self.windowHeight = 300
        
        #self.gesture = "None"
        self.control = "None"
        self.defaultColor = (255, 255, 255)
        self.highlightColor = (125, 125, 125)
        #self.gestureList = ("swipe", "key tap", "screen_tap", "Up", "Down", "circle clockwise", "circle counterclockwise")
        self.controlVal = {'volume':0, 'pitch':0, 'track':0, 'speed':0, 'insutrment':0, 'note':0}
        
        pygame.init()
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption("Simple UI")
        
        #Surface
        self.background = pygame.Surface(self.window.get_size())
        self.background = self.background.convert()
        self.background.fill ((50,0,80))
        
        # Create a sample listener and controller
        self.listener = SimpleListener()
        self.listener.set_model(model)
        self.controller = Leap.Controller()
        
        # Have the sample listener receive events from the controller
        self.controller.add_listener(self.listener)
    
    def callbackfunc(self, control, val):
        self.control = control 
        self.controlVal[control] = val
        
    def update_volume(self, volume_level):
        Player.velocity_offset(volume_level)
        self.controlVal['volume'] = volume_level
        
    def update_pitch(self, pitch_level):
        Player.pitch_offset(pitch_level)
        self.controlVal['pitch'] = pitch_level
        
    def update_track(self, track_name):
        self.controlVal['track'] = track_name
        
    def update_speed(self, speed_level):
        self.controlVal['speed'] = speed_level

    def update_instrument(self, instrument_number):
        self.controlVal['instrument'] = instrument_number

    def update_note(self, note_number):
        self.controlVal['note'] = note_number
    
    def update_control(self, control_name):
        self.control = control_name
   
    #Application Loop
    def main(self):  
        #clock = pygame.time.Clock()
        
        self.window.blit(self.background, (0,0))
        
        while True:  
            #clock.tick(60)
            #Handle Input Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "quit"
                    sys.exit()
                    # Remove the sample listener when done
                    self.controller.remove_listener(self.listener)
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # user pressed ESC
                        sys.exit()
                        # Remove the sample listener when done
                        self.controller.remove_listener(self.listener)
                        break
            
            self.window.blit(self.background, (0,0))
    
            font = pygame.font.Font(None, 36)            
  
            intX = 0
            intY = 0
            
            for n in self.controlVal.keys():
                if n == self.control:
                    text = font.render("%s" % n, 1, self.highlightColor, (255, 255, 255))
                else:
                    text = font.render("%s" % n, 1, self.defaultColor)
                    
                self.window.blit(text, (intX,intY))
                text = font.render("{0}          ".format(self.controlVal[n]), 1, self.defaultColor)
                self.window.blit(text, (150,intY))
                
                intY += 50
            
            
            pygame.display.flip()
        
        pygame.quit()
    
if __name__ == "__main__":
    m = SuperConductorModel()
    ui = SimpleUI(m)
    Player.midistart("songs\miley_cyrus-wrecking_ball.mid")
    ui.main()