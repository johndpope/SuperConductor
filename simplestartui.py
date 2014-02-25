''' Just and easy way to start from the command line '''

from sccui import Controller
from scm import Model
from scpv import PPPlayerView
import Leap, pygame, sys
import Tkinter, tkFileDialog, tkMessageBox

m = Model()
root = Tkinter.Tk()
root.withdraw()

extention = ""
while extention != "mid":
    tkMessageBox.showinfo("sccui", "Please select a midi file")
    file = tkFileDialog.askopenfilename()
    file_path = file.split('/')
    fileName = file_path[len(file_path)-1]
    fileSplit = fileName.split('.')
    extention = fileSplit[len(fileSplit)-1]
    
m.load_file(file)
c = Controller()
lc = Leap.Controller()
c.setup(m, lc, fileName)
lc.add_listener(c)
p = PPPlayerView(m)
p.play()

while True:
    # To exit cleanly, if controller thread has ended we need to end
    # player thread and this thread.
    if c.exited:
        p.exited = True
        exit()
    pass