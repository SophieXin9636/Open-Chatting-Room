from tkinter import Tk,Label,Button,Entry,StringVar
from tkinter.font import Font as tkfont
from tkinter.font import BOLD,ITALIC
from tkinter.filedialog import askdirectory,askopenfilename
from PIL import Image,ImageTk

#tk window basic setting: title and size###############################################
window=Tk()
window.title("Chat")
window.geometry("800x580")
#######################################################################################

#functions#############################################################################
##global var

#######################################################################################

#label / button########################################################################
##font
font_cr=tkfont(family="Times",size=8,slant=ITALIC)

##copyright
txt_copyright=Label(window,text="® 2021",font=font_cr)
#######################################################################################

#pack / place##########################################################################
##copyright
txt_copyright.place(x=300,y=550)
#######################################################################################

#window looping########################################################################
if __name__ == '__main__':
    window.mainloop()