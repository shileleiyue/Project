import turtle as t
import time

W = 1000
H = 400

on_color_date = [(255, 77, 77), (255, 184, 77), (77, 255, 184)]
on_color_time = [(77, 121, 255), (184, 77, 255), (255, 77, 121)]
off_color = (30, 42, 56)
bg_color = (13, 17, 23)
sym_color = (170, 170, 170)

SEG_LENGTH = 36
SEG_WIDTH = 12
GAP_EXTRA = 4
DIGIT_GAP = 20
BLOCK_GAP = 40

def zhuanma(x):
    if x == 0:   return [1,1,1,1,1,1,0]
    elif x == 1: return [0,0,1,0,0,1,0]
    elif x == 2: return [1,0,1,1,1,0,1]
    elif x == 3: return [1,0,1,1,0,1,1]
    elif x == 4: return [0,1,1,1,0,1,0]
    elif x == 5: return [1,1,0,1,0,1,1]
    elif x == 6: return [1,1,0,1,1,1,1]
    elif x == 7: return [1,0,1,0,0,1,0]
    elif x == 8: return [1,1,1,1,1,1,1]
    elif x == 9: return [1,1,1,1,0,1,1]
    else:        return [0,0,0,0,0,0,0]

def draw_liubanxing(x, y, angle, length, width, color):
    radius = width // 2
    t.penup(); t.goto(x, y); t.setheading(angle); t.pendown()
    t.fillcolor(color); t.begin_fill()
    t.circle(radius, 90, steps=1)
    t.forward(length)
    t.circle(radius, 180, steps=2)
    t.forward(length)
    t.circle(radius, 90, steps=1)
    t.end_fill(); t.penup()

def draw_seg(x, y, angle, on, color_on):
    if on:
        draw_liubanxing(x, y, angle, SEG_LENGTH, SEG_WIDTH, color_on)
    else:
        draw_liubanxing(x, y, angle, SEG_LENGTH, SEG_WIDTH, off_color)

def draw_digit_fixed(x0, y0, code, color_on):
    gap = GAP_EXTRA
    half = SEG_LENGTH / 2.0
    cx_mid = x0 + SEG_LENGTH/2.0 + gap + SEG_WIDTH/2.0
    cx_left = x0 + gap + SEG_WIDTH/2.0
    cx_right = x0 + SEG_LENGTH + gap + SEG_WIDTH/2.0 + gap

    draw_seg(cx_mid, y0, 0, code[0], color_on)                     # a
    draw_seg(cx_right, y0 - half, 90, code[1], color_on)           # b
    draw_seg(cx_right, y0 - half - SEG_LENGTH, 90, code[2], color_on) # c
    draw_seg(cx_mid, y0 - 2*SEG_LENGTH, 0, code[3], color_on)     # d
    draw_seg(cx_left, y0 - half - SEG_LENGTH, 90, code[4], color_on) # e
    draw_seg(cx_left, y0 - half, 90, code[5], color_on)            # f
    draw_seg(cx_mid, y0 - SEG_LENGTH, 0, code[6], color_on)        # g

def draw_symbol(cx, cy, sym_type):
    if sym_type == '-':
        draw_liubanxing(cx, cy, 0, SEG_LENGTH*0.5, SEG_WIDTH*0.8, sym_color)
    elif sym_type == ':':
        dot_size = SEG_WIDTH * 1.2
        offset = SEG_LENGTH * 0.8
        t.penup()
        t.goto(cx, cy); t.dot(dot_size, sym_color)
        t.goto(cx, cy - offset*2); t.dot(dot_size, sym_color)
    elif sym_type == '.':
        t.penup(); t.goto(cx, cy); t.dot(SEG_WIDTH*0.9, sym_color)

def draw_time_string(time_str, start_x, start_y):
    x = start_x
    digit_width = SEG_LENGTH + GAP_EXTRA*2 + SEG_WIDTH
    sym_width = SEG_LENGTH*0.5 + 8

    space_pos = time_str.find(' ')
    date_part = time_str[:space_pos] if space_pos != -1 else time_str
    time_part = time_str[space_pos+1:] if space_pos != -1 else ""

    color_idx = 0
    for ch in date_part:
        if '0' <= ch <= '9':
            code = zhuanma(int(ch))
            clr = on_color_date[color_idx % 3]
            draw_digit_fixed(x, start_y, code, clr)
            x += digit_width
            color_idx += 1
        elif ch == '-':
            draw_symbol(x + sym_width/2, start_y - SEG_LENGTH, '-')
            x += sym_width

    x += BLOCK_GAP

    color_idx = 0
    for ch in time_part:
        if '0' <= ch <= '9':
            code = zhuanma(int(ch))
            clr = on_color_time[color_idx % 3]
            draw_digit_fixed(x, start_y, code, clr)
            x += digit_width
            color_idx += 1
        elif ch == ':':
            draw_symbol(x + sym_width/2, start_y - SEG_LENGTH, ':')
            x += sym_width

def refresh():
    t.clear(); t.bgcolor(bg_color)
    now = time.localtime()
    full_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
    draw_time_string(full_str, -400, 150)
    t.penup(); t.goto(0, H/2-30); t.color("#888888")
    t.write("六边形数码管时钟", align="center", font=("Arial", 14, "normal"))
    t.hideturtle(); t.update()
    t.ontimer(refresh, 1000)

def main():
    t.setup(W, H); t.colormode(255); t.bgcolor(bg_color)
    t.pensize(0); t.hideturtle(); t.speed(0); t.tracer(0)
    refresh(); t.mainloop()

if __name__ == "__main__":
    main()