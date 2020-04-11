import os
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
from pygame import mixer
import pygame

root = Tk()

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)


def browse_file():
    global filename
    filename = filedialog.askopenfilename()


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About AmpHead', 'Music Player Created by Charmil Mal, Manav Lohiya, Asad Khan')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  # initializing the mixer
root.title("AmpHead")
root.iconbitmap(r'images/amphead.ico')

filelabel = Label(root, text='Let\'s get the speakers running.')
filelabel.pack(pady=10)

lengthlabel = Label(root, text='Total Length : --:--')
lengthlabel.pack()


def show_details(filename):
    filelabel['text'] = "Playing" + ' - ' + os.path.basename(filename)

    file_data = os.path.splitext(filename)

    if file_data[1] == '.mp3':
        audio = MP3(filename)
        total_length = audio.info.length
    else:
        a = mixer.Sound(filename)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

def onKeyPress(event):
    if event.char== ' ':
        isplay()
root.bind('<KeyPress>', onKeyPress)

def play_music():
    global paused
    set_vol(80)
    if paused:
        playBtn.configure(image=pausePhoto)
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            global filename
            mixer.music.load(filename)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(filename)
            show_details(filename)
        except:
            tkinter.messagebox.showinfo('File not found', 'Playing default music.')
            filename='memories.mp3'
            mixer.music.load(filename)
            mixer.music.play()
            statusbar['text'] = "playing music" + ' - ' +os.path.basename(filename)
            show_details(filename)
            playBtn.configure(image=pausePhoto)


def stop_music():
    global paused
    playBtn.configure(image=playPhoto)
    global count
    mixer.music.stop()
    count=0
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    playBtn.configure(image=playPhoto)
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"
count=0
def isplay():
    global count
    if count==0:
        count=1
        play_music()
    else:
        if paused:
            play_music()
        else:
            pause_music()
        

def rewind_music():
    playBtn.configure(image=pausePhoto)
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    scale.set(val)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        set_vol(80)
        volumeBtn.configure(image=volumePhoto)
        muted = FALSE
    else:  # mute the music
        set_vol(0)
        volumeBtn.configure(image=mutePhoto)
        muted = TRUE


middleframe = Frame(root)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='images/play.png')
pausePhoto = PhotoImage(file='images/pause.png')
playBtn = Button(middleframe, image=playPhoto, command=isplay)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)


# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(root)
bottomframe.pack()

rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0,padx=20)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1,padx=20)

scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
set_vol(80)
scale.grid(row=0, column=2, pady=15, padx=30)

statusbar = Label(root, text="Welcome to AmpHead Music Player", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

def on_closing():
    stop_music()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
