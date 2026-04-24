import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def draw_red_envelope():
    # 定义红包的顶点
    vertices = [
        (0, 0),
        (10, 0),
        (10, 5),
        (5, 5),
        (5, 10),
        (0, 10)
    ]

    # 定义红包的路径
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    path = Path(vertices, codes)

    # 创建图形和坐标轴
    fig, ax = plt.subplots()

    # 绘制红包
    patch = patches.PathPatch(path, facecolor='red', edgecolor='gold', linewidth=3)
    ax.add_patch(patch)

    # 隐藏坐标轴
    ax.axis('off')

    # 显示图形
    plt.show()

draw_red_envelope()