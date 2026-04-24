import turtle

# 设置游戏界面大小
window = turtle.Screen()
window.title("推箱子游戏")
window.bgcolor("black")
window.setup(500, 500)
window.tracer(0)  # 关闭动画效果，加快运行速度

# 定义箱子、玩家和墙壁的类
class Box:
    def __init__(self, x, y):
        self.x = x * 20 + 10  # 根据窗口大小调整坐标值，这里假设每个格子为 20px 大小，箱子的中心在格子内。
    box_size = [i for i in range(4)]
    for _ in range(4):
        self.y = y * 20 + 10 - box_size[x][y] / 2
        self.image = turtle.Turtle()
        self.image.speed(0)
        self.image.up()
        self.image.goto(self.x, self.y)
        self.image.down()
        self.image.color("red")   # 定义箱子的颜色为红色。
    if x == y == 3:     # 如果箱子在目标位置，颜色变为绿色。
        self.image._shapes["turtle"].fillcolor("green")
    def move(self, dx, dy):
        new_x = (self._get_pos()[0] + dx) // 20 * 20 + 10
        new_y = (self._get_pos()[1] + dy) // 20 * 20 + 10 - box_size[new_x][new_y] / 2
    if not wall_collision((new_x, new_y), (dx, dy)):
        old_x, old_y = (self._get_pos()[i] for i in range(2))
    if new_x < old_x:
        for obj in players + boxes:
            if obj is not self and obj._get_pos()[i] >= new_x and obj._get_pos()[i] <= old_x:
                False
    elif new_x > old_x:
       for obj in players + boxes:
           if obj[已停止]:
               print("结束了")


