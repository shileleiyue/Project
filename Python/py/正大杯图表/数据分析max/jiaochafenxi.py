# -*- coding: utf-8 -*-
"""
交叉分析：Q20 vs Q8  &  Q4 vs Q23
生成图表（PNG）和 Excel 表格，保存在“分析结果”文件夹。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# ==================== 配置 ====================
RAW_DATA_FILE = "350881459_按序号_关于影视行业环境与观众沉浸体验研究的详细问卷_274_274.xlsx"
OUTPUT_DIR = "分析结果"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 字体设置 ====================
def set_chinese_font():
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei',
                     'PingFang SC', 'Hiragino Sans GB', 'Noto Sans CJK SC']
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    for font in chinese_fonts:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['axes.unicode_minus'] = False
            print(f"使用中文字体：{font}")
            return font
    print("警告：未找到合适的中文字体，图表中文可能显示为方框。")
    return None

set_chinese_font()

# ==================== 加载原始数据 ====================
def load_data():
    if not os.path.exists(RAW_DATA_FILE):
        raise FileNotFoundError(f"文件不存在：{RAW_DATA_FILE}")
    df = pd.read_excel(RAW_DATA_FILE)
    print(f"数据加载成功，共 {len(df)} 行，{len(df.columns)} 列")
    return df

df = load_data()

# ==================== 定义列名（基于实际文件）====================
# 单选题 Q8 原始列名
Q8_RAW_COL = '8. 在观看一集45分钟左右的剧集时，您通常如何处理？'

# 多选题 Q4 各选项列名（已确认）
Q4_COLS = {
    '智能手机': '4. 您通常通过哪些设备观看影视内容？（可多选）(智能手机)',
    '平板电脑': '4 (平板电脑)',
    '笔记本电脑': '4 (笔记本电脑)',
    '台式电脑': '4 (台式电脑)',
    '智能电视/投影仪': '4 (智能电视/投影仪)',
    'VR设备': '4 (VR设备)',
}

# 多选题 Q20 各选项列名
Q20_COLS = {
    '转向观看更多短视频': '20. 您认为“影视寒冬”对您的个人观看习惯产生了什么影响？（可多选）(转向观看更多短视频)',
    '更依赖口碑和评分选择长视频': '20(更依赖口碑和评分选择长视频)',
    '降低了对新作的期待值': '20(降低了对新作的期待值)',
    '更愿意重温经典老剧/电影': '20(更愿意重温经典老剧/电影)',
    '开始观看更多海外内容': '20(开始观看更多海外内容)',
}

# 多选题 Q23 各选项列名
Q23_COLS = {
    '4K': '23. 以下哪些技术或形式，最能提升您的沉浸感？（）(4K)',
    'HDR、杜比视界/全景声等高规格视听': '23(HDR、杜比视界/全景声等高规格视听)',
    '互动叙事（可选择分支影响剧情）': '23(互动叙事（可选择分支影响剧情）)',
    'VR/AR/XR等虚拟现实体验': '23(VR/AR/XR等虚拟现实体验)',
    '模拟影院效果的“云影院”或专属播放模式': '23(模拟影院效果的“云影院”或专属播放模式)',
    '伴随式的创作解说、细节彩蛋揭秘': '23(伴随式的创作解说、细节彩蛋揭秘)',
}

# ==================== 数据预处理 ====================
# 生成 Q8 的标签列（用于分组）
q8_option_map = {1: '一次性专注看完', 2: '分2-3次看完', 3: '边看边做其他事', 4: '后台播放'}
Q8_LABEL_COL = 'Q8_处理方式'
df[Q8_LABEL_COL] = df[Q8_RAW_COL].map(q8_option_map)

# 检查必要列是否存在
required_q8 = Q8_RAW_COL
required_q4 = list(Q4_COLS.values())
required_q20 = list(Q20_COLS.values())
required_q23 = list(Q23_COLS.values())

missing = []
for col in [required_q8] + required_q4 + required_q20 + required_q23:
    if col not in df.columns:
        missing.append(col)
if missing:
    print("错误：以下列不存在，请检查列名：")
    for col in missing:
        print(f"  {col}")
    exit()

# ==================== 1. Q20 vs Q8 交叉分析 ====================
print("\n开始分析 Q20 vs Q8 ...")

# 筛选有效数据（Q8 非缺失）
df_valid = df[df[Q8_LABEL_COL].notna()].copy()

# 按 Q8 标签分组
grouped = df_valid.groupby(Q8_LABEL_COL)

# 计算每个 Q20 选项在每组中的选择比例（百分比）
result_q20_vs_q8 = pd.DataFrame()
for opt, col_name in Q20_COLS.items():
    result_q20_vs_q8[opt] = (grouped[col_name].mean() * 100).round(1)

# 按预期顺序排列行
q8_order = ['一次性专注看完', '分2-3次看完', '边看边做其他事', '后台播放']
result_q20_vs_q8 = result_q20_vs_q8.reindex(q8_order)
result_q20_vs_q8.index.name = 'Q8选项'

# 绘制分组柱状图
fig, ax = plt.subplots(figsize=(12, 6))
result_q20_vs_q8.plot(kind='bar', ax=ax, colormap='tab20', edgecolor='black')
ax.set_ylabel('选择百分比 (%)')
ax.set_title('Q8观看剧集方式 与 Q20观影习惯影响 的交叉分析')
ax.legend(title='Q20选项', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '交叉_Q20_vs_Q8.png'), dpi=150)
plt.close()

# 保存表格
excel_path = os.path.join(OUTPUT_DIR, '交叉分析表_Q20_vs_Q8.xlsx')
result_q20_vs_q8.to_excel(excel_path)
print(f"Q20 vs Q8 结果已保存至 {excel_path} 和 交叉_Q20_vs_Q8.png")

# ==================== 2. Q4 vs Q23 交叉分析 ====================
print("\n开始分析 Q4 vs Q23 ...")

# 构建共选次数矩阵
q4_options = list(Q4_COLS.keys())
q23_options = list(Q23_COLS.keys())
matrix = pd.DataFrame(index=q4_options, columns=q23_options, dtype=int)

for q4_opt in q4_options:
    col4 = Q4_COLS[q4_opt]
    for q23_opt in q23_options:
        col23 = Q23_COLS[q23_opt]
        # 同时选择两个选项的人数
        count = ((df[col4] == 1) & (df[col23] == 1)).sum()
        matrix.loc[q4_opt, q23_opt] = count

# 确保矩阵数据为整数类型（避免绘图时fmt='d'报错）
matrix = matrix.astype(int)

# 绘制热力图
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(matrix, annot=True, fmt='d', cmap='YlGnBu', ax=ax, cbar_kws={'label': '共选人数'})
ax.set_title('Q4观看设备 与 Q23沉浸技术 的共选人数热力图')
ax.set_xlabel('Q23 技术/形式')
ax.set_ylabel('Q4 设备')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '交叉_Q4_vs_Q23_热力图.png'), dpi=150)
plt.close()

# 保存表格
excel_path = os.path.join(OUTPUT_DIR, '交叉分析表_Q4_vs_Q23.xlsx')
matrix.to_excel(excel_path)
print(f"Q4 vs Q23 结果已保存至 {excel_path} 和 交叉_Q4_vs_Q23_热力图.png")

print("\n所有分析完成！")