# 代码1：生成“各班各科均分与校级均分差值热力图（PPT版）”
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 构造数据（与原Excel一致）
data = {
    '班级': [1,2,3,4,5,6,7,8,9],
    '数学': [62.79,65.37,49.61,49.71,47.94,54.75,49.6,54.91,53.0],
    '英语': [55.17,63.71,59.43,56.79,58.76,57.56,54.46,56.43,60.7],
    '物理': [43.33,46.53,42.25,43.94,42.83,37.64,41.31,40.89,42.47],
    '化学': [38.54,37.0,35.18,35.15,36.17,37.56,37.69,40.15,40.7],
    '生物': [66.37,51.43,56.78,55.15,54.13,51.0,53.56,52.51,60.92]
}
df = pd.DataFrame(data)
school_avg = {'数学':54.19, '英语':58.11, '物理':42.35, '化学':37.57, '生物':55.76}  # 校均数据

# 2. 计算差值+设置索引
df_diff = df.set_index('班级') - pd.Series(school_avg)

# 3. PPT适配绘图
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.sans-serif'] = ['SimHei']  # 适配Windows系统中文
plt.figure(figsize=(12,6.75))  # 16:9比例

sns.heatmap(df_diff, annot=True, cmap='coolwarm', fmt='.2f',
            cbar_kws={'label':'与校级均分差值（分）'}, linewidths=0.5)
plt.title('各班各科均分与校级均分差值对比', fontsize=14, fontweight='bold')
plt.xlabel('科目', fontsize=12)
plt.ylabel('班级', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()

# 保存到本地（修改路径为你的电脑文件夹，如"C:/Users/XXX/Desktop/图1.png"）
plt.savefig("E:/班级科目均分差值图_PPT版.png", dpi=300)
plt.close()
print("图1已保存到本地")