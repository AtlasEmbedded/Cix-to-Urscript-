import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import configparser
import main
import subprocess


config = configparser.ConfigParser()
config.read('config.ini')

window = ctk.CTk()
window.title("UR20")
geometry = window.geometry("400x100")

label = ctk.CTkLabel(window, 
                     text="Enter file name:"
                     )
label.pack()

def find_file(cixfile):
    if main.find_file(cixfile) == 'file not found':
        label = ctk.CTkLabel(window, 
                             text="File not found"
                             )
        label.pack()
    else:
        config['CIX']['file'] = entry.get()
        with open ('config.ini', 'w') as configfile:
            config.write(configfile)

        cixfile = config.get('CIX', 'file')

        main.find_file(cixfile)
        main.parseSection(cixfile)
        main.parseMaindata(main.parseSection(cixfile))
        main.parseDrill(main.parseSection(cixfile))
        main.WriteConfig()
        window.destroy()

entry = ctk.CTkEntry(window,
                     placeholder_text="Enter file name:")
entry.pack()
entry.bind("<Return>", lambda event: find_file(entry.get()))

window.mainloop()


mainwindow = ctk.CTk()
mainwindow.title("UR20")
                     
def change_speedms():
    config['GlobalSettings']['speed_ms'] = speedms.get()
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)

def change_speedrads():
    config['GlobalSettings']['speed_rads'] = speedrads.get()
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)

def change_accelmss():
    config['GlobalSettings']['accel_mss'] = accelmss.get()
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)

def change_accelradss():
    config['GlobalSettings']['accel_radss'] = accelradss.get()
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)

def change_blendradius():
    config['GlobalSettings']['blend_radius'] = blendradius.get()
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)

def save():
    if speedms.get() == '':
        config['GlobalSettings']['speed_ms'] = '0.3'
    else:
        change_speedms()

    if speedrads.get() == '':
        config['GlobalSettings']['speed_rads'] = '0.75'
    else:
        change_speedrads()

    if accelmss.get() == '':
        config['GlobalSettings']['accel_mss'] = '3'
    else:
        change_accelmss()

    if accelradss.get() == '':   
        config['GlobalSettings']['accel_radss'] = '1.2'
    else:
        change_accelradss()

    if blendradius.get() =='':
        config['GlobalSettings']['blend_radius'] = '0.001'
    else:
        change_blendradius()

    with open ('config.ini', 'w') as configfile:
        config.write(configfile)
    
def default_settings():
    config['GlobalSettings']['speed_ms'] = '0.3'
    config['GlobalSettings']['speed_rads'] = '0.75'
    config['GlobalSettings']['accel_mss'] = '3'
    config['GlobalSettings']['accel_radss'] = '1.2'
    config['GlobalSettings']['blend_radius'] = '0.001'
    with open ('config.ini', 'w') as configfile:
        config.write(configfile)

def createscript():
    subprocess.call(['python', 'create.py'])

def change_tooloffset():
    offset = float(tooloffset.get()) / 1000 + float(config['ToolOffset']['URZdown'])
    config['ToolOffset']['URZdown'] = str(offset)
    with open ('config.ini', 'w') as configfile:
        config.write(configfile) 


label = ctk.CTkLabel(mainwindow,
                        text="Global Settings:"
                        )
label.pack()

speedms = ctk.CTkLabel(mainwindow,
                        text="Speed (ms):"
                        )
speedms.pack()
speedms = ctk.CTkEntry(mainwindow,
                        placeholder_text= str(config.get('GlobalSettings','speed_ms'))
                        )
speedms.pack()
speedms.bind("<Return>", lambda event: change_speedms())

speedrads = ctk.CTkLabel(mainwindow,
                        text="Speed (rads):"
                        )
speedrads.pack()
speedrads = ctk.CTkEntry(mainwindow,
                        placeholder_text= str(config.get('GlobalSettings','speed_rads'))
                        )
speedrads.pack()
speedrads.bind("<Return>", lambda event: change_speedrads())

accelmss = ctk.CTkLabel(mainwindow,
                        text="accel (mss):"
                        )
accelmss.pack()
accelmss = ctk.CTkEntry(mainwindow,
                        placeholder_text= str(config.get('GlobalSettings','accel_mss'))
                        )
accelmss.pack()
accelmss.bind("<Return>", lambda event: change_accelmss())

accelradss = ctk.CTkLabel(mainwindow,
                        text="accel (radss):"
                        )
accelradss.pack()
accelradss = ctk.CTkEntry(mainwindow,
                        placeholder_text= str(config.get('GlobalSettings','accel_radss'))
                        )
accelradss.pack()
accelradss.bind("<Return>", lambda event: change_accelradss())

blendradius = ctk.CTkLabel(mainwindow,
                        text="blend radius:"
                        )
blendradius.pack()
blendradius = ctk.CTkEntry(mainwindow,
                        placeholder_text= str(config.get('GlobalSettings','blend_radius'))
                        )
blendradius.pack()
blendradius.bind("<Return>", lambda event: change_blendradius())

tooloffset = ctk.CTkLabel(mainwindow,
                        text="Tool Offset (mm):"
                        )
tooloffset.pack()
tooloffset = ctk.CTkEntry(mainwindow,
                        placeholder_text= 0
                        )
tooloffset.pack()
tooloffset.bind("<Return>", lambda event: change_tooloffset())

save = ctk.CTkButton(mainwindow,
                        text="Save",
                        command = save
                        )
save.pack(padx=10, pady=10)

create = ctk.CTkButton(mainwindow,
                        text="Create UR Script",
                        command = createscript
                        )
create.pack(padx=10, pady=10)

default = ctk.CTkButton(mainwindow,
                        text="Default Settings",
                        command = default_settings
                        )
default.pack(padx=10, pady=10)

mainwindow.mainloop()