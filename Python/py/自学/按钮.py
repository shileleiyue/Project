import calendar
from tkinter import *
def xinlabel():
    giobalxin
    s = Label(xin, text='完成')
    s.pack()
xin = Tk()
b1 = Button(xin,text='下一步',command=xinlabel)
b1.pack()
b2 = Button(xin,text='下一步',command=xinlabel)
b2.pack()
if b1 :
    year = int(2024)
    moon = int(1)

    print(calendar.month(year, moon))

xin.mainloop()
