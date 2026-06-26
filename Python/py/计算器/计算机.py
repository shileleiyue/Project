# 导入tkinter库
import tkinter as t


# 定义点击函数
def dj0():
    jsck.insert(t.END, 0)


def dj1():
    jsck.insert(t.END, 1)


def dj2():
    jsck.insert(t.END, 2)


def dj3():
    jsck.insert(t.END, 3)


def dj4():
    jsck.insert(t.END, 4)


def dj5():
    jsck.insert(t.END, 5)


def dj6():
    jsck.insert(t.END, 6)


def dj7():
    jsck.insert(t.END, 7)


def dj8():
    jsck.insert(t.END, 8)


def dj9():
    jsck.insert(t.END, 9)


def k_jia():
    jsck.insert(t.END, '+')


def k_jian():
    jsck.insert(t.END, '-')


def k_cheng():
    jsck.insert(t.END, '*')


def k_chu():
    jsck.insert(t.END, '/')


def djd():
    jsck.insert(t.END, '.')


def k_dy():
    try:
        jg = jsck.get()
        if jg == '':
            jsck.delete(0, t.END)
            jsck.insert(t.END, '')
        else:
            jsck.delete(0, t.END)
            jsck.insert(t.END, eval(jg))
    except Exception:
        jsck.insert(t.END, '错误')


def k_gl():
    if jsck.get() == '错误':
        jsck.delete(0, t.END)
    else:
        jsck.delete(len(jsck.get()) - 1, t.END)


# 创建窗口
w = t.Tk()

# 定义窗口大小
w.geometry('600x350')

# 锁定窗口大小
w.resizable(False, False)

# 定义计算窗口
jsck = t.Entry(w)

# 添加计算窗口
jsck.pack()

# 定义计算键
a0 = t.Button(w, text='0', command=dj0)
a1 = t.Button(w, text='1', command=dj1)
a2 = t.Button(w, text='2', command=dj2)
a3 = t.Button(w, text='3', command=dj3)
a4 = t.Button(w, text='4', command=dj4)
a5 = t.Button(w, text='5', command=dj5)
a6 = t.Button(w, text='6', command=dj6)
a7 = t.Button(w, text='7', command=dj7)
a8 = t.Button(w, text='8', command=dj8)
a9 = t.Button(w, text='9', command=dj9)
jia = t.Button(w, text='+', command=k_jia)
jian = t.Button(w, text='-', command=k_jian)
cheng = t.Button(w, text='*', command=k_cheng)
chu = t.Button(w, text='/', command=k_chu)
d = t.Button(w, text='.', command=djd)
dy = t.Button(w, text='=', command=k_dy)
gl = t.Button(w, text='x', command=k_gl)

# 添加计算键
a1.place(x=120, y=50)
a2.place(x=210, y=50)
a3.place(x=300, y=50)
a4.place(x=120, y=120)
a5.place(x=210, y=120)
a6.place(x=300, y=120)
a7.place(x=120, y=190)
a8.place(x=210, y=190)
a9.place(x=300, y=190)
a0.place(x=210, y=260)
jia.place(x=390, y=50)
jian.place(x=390, y=120)
cheng.place(x=390, y=190)
chu.place(x=390, y=260)
d.place(x=120, y=260)
dy.place(x=300, y=260)
gl.place(x=480, y=0)

# 实现窗口循环
w.mainloop()