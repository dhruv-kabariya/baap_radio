from logging import root
from tkinter import *

player = Tk()

player.title("Welcome to Bap Radio")
player.geometry('1200*800')

frame = Frame(player)

frame.pack()


ip_aadr_box = Entry(frame, width=15)
ip_aadr_box.grid(column =1, row =0)


port_box = Entry(frame, width=5)
port_box.grid(column =3, row =0)

button = Button(frame, text ='Connect to Radio')  
button.grid(column=2,row=1)                         

player.mainloop() 