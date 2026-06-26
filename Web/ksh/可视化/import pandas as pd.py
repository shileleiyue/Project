import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

# 设置中文字体，防止乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 用 SimHei
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 读取 Excel 文件
file_path = "学习生活心理健康大问卷.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')

# 查看数据基本情况
print("数据形状：", df.shape)
print("列名：", df.columns.tolist())
print("\n前几行数据：")
print(df.head())

# ================== 数据清洗 ==================
# 重命名列以便操作（原列名较长）
df.columns = [
    '答题时间', '姓名', '性别', '学号', '省市', '寝室', '寝室长',
    '无课_周一12', '无课_周一34', '无课_周三56', '无课_周三78',
    '无课_周四12', '无课_周五56', '无课_周五78',
    '挂科', '挂科_补充', '学习压力', '课外学习需求',
    '困难科目_高数', '困难科目_体育', '困难科目_英语',
    '困难科目_算法', '困难科目_离散', '困难科目_网页', '困难科目_python',
    '心理压力', '室友关系', '班委评价', '班委意见', '老师意见'
]

# 处理挂科字段：包含“是”、“求安慰”等视为“是”
def parse_hangkou(val):
    if pd.isna(val):
        return '否'
    val_str = str(val).strip()
    if val_str in ['是', '求安慰']:
        return '是'
    else:
        return '否'

df['挂科'] = df['挂科'].apply(parse_hangkou)

# 学习压力、心理压力等有序分类
pressure_order = ['小', '适中', '较大', '大', '非常大']
df['学习压力'] = pd.Categorical(df['学习压力'], categories=pressure_order, ordered=True)
df['心理压力'] = pd.Categorical(df['心理压力'], categories=pressure_order, ordered=True)

# 课外学习需求
demand_order = ['不需要', '比较需要', '需要', '非常需要']
df['课外学习需求'] = pd.Categorical(df['课外学习需求'], categories=demand_order, ordered=True)

# 室友关系
relation_order = ['陌生人/路人', '朋友/搭子', '家人/亲人']
df['室友关系'] = pd.Categorical(df['室友关系'], categories=relation_order, ordered=True)

# ================== 统计分析 ==================
# 1. 挂科情况
hangke_count = df['挂科'].value_counts()
print("\n挂科情况：\n", hangke_count)

# 2. 学习压力分布
study_pressure = df['学习压力'].value_counts().sort_index()
print("\n学习压力分布：\n", study_pressure)

# 3. 心理压力分布
mental_pressure = df['心理压力'].value_counts().sort_index()
print("\n心理压力分布：\n", mental_pressure)

# 4. 课外学习需求
demand_dist = df['课外学习需求'].value_counts().sort_index()
print("\n课外学习需求分布：\n", demand_dist)

# 5. 室友关系
relation_dist = df['室友关系'].value_counts().sort_index()
print("\n室友关系分布：\n", relation_dist)

# 6. 困难科目统计（每个科目单独一列，值为空或非空，非空表示困难）
difficult_cols = ['困难科目_高数', '困难科目_体育', '困难科目_英语',
                   '困难科目_算法', '困难科目_离散', '困难科目_网页', '困难科目_python']
# 将列名映射为更易读的名称
subject_map = {
    '困难科目_高数': '高数',
    '困难科目_体育': '体育',
    '困难科目_英语': '英语',
    '困难科目_算法': '算法与程序实践',
    '困难科目_离散': '离散数学',
    '困难科目_网页': '网页设计与开发',
    '困难科目_python': 'Python程序设计'
}
difficult_count = {}
for col in difficult_cols:
    # 非空且内容不是空字符串
    cnt = df[col].notna().sum() - (df[col] == '').sum()  # 注意：空字符串也会被notna检测为True
    # 更简单：检查非空且不是空字符串
    cnt = df[col].apply(lambda x: pd.notna(x) and x.strip() != '').sum()
    difficult_count[subject_map[col]] = cnt
difficult_df = pd.DataFrame(list(difficult_count.items()), columns=['科目', '困难人数'])
difficult_df = difficult_df.sort_values('困难人数', ascending=False)
print("\n困难科目统计：\n", difficult_df)

# 7. 性别与挂科关系
gender_hangkou = pd.crosstab(df['性别'], df['挂科'])
print("\n性别与挂科关系：\n", gender_hangkou)

# 8. 性别与学习压力关系
gender_study_pressure = pd.crosstab(df['性别'], df['学习压力'])
print("\n性别与学习压力关系：\n", gender_study_pressure)

# ================== 可视化 ==================
# 设置画布风格
sns.set_style("whitegrid")
fig = plt.figure(figsize=(18, 12))

# 1. 挂科情况饼图
plt.subplot(3, 3, 1)
plt.pie(hangke_count, labels=hangke_count.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('挂科情况')

# 2. 学习压力条形图
plt.subplot(3, 3, 2)
sns.barplot(x=study_pressure.index, y=study_pressure.values, palette='Blues_d')
plt.title('学习压力分布')
plt.xlabel('压力程度')
plt.ylabel('人数')

# 3. 心理压力条形图
plt.subplot(3, 3, 3)
sns.barplot(x=mental_pressure.index, y=mental_pressure.values, palette='Reds_d')
plt.title('心理压力分布')
plt.xlabel('压力程度')
plt.ylabel('人数')

# 4. 课外学习需求条形图
plt.subplot(3, 3, 4)
sns.barplot(x=demand_dist.index, y=demand_dist.values, palette='Greens_d')
plt.title('课外学习需求')
plt.xlabel('需求程度')
plt.ylabel('人数')

# 5. 室友关系饼图
plt.subplot(3, 3, 5)
plt.pie(relation_dist, labels=relation_dist.index, autopct='%1.1f%%', startangle=90, colors=['#ffcc99','#99ff99','#66b3ff'])
plt.title('室友关系')

# 6. 困难科目横向条形图
plt.subplot(3, 3, 6)
plt.barh(difficult_df['科目'], difficult_df['困难人数'], color='salmon')
plt.title('困难科目人数')
plt.xlabel('人数')
plt.ylabel('科目')
plt.gca().invert_yaxis()  # 使最多的在上方

# 7. 性别与挂科堆叠条形图
plt.subplot(3, 3, 7)
gender_hangkou.plot(kind='bar', stacked=True, ax=plt.gca(), color=['#66b3ff','#ff9999'])
plt.title('性别与挂科')
plt.xlabel('性别')
plt.ylabel('人数')
plt.legend(title='挂科', labels=['否', '是'])
plt.xticks(rotation=0)

# 8. 性别与学习压力分组条形图
plt.subplot(3, 3, 8)
gender_study_pressure.plot(kind='bar', ax=plt.gca(), colormap='viridis')
plt.title('性别与学习压力')
plt.xlabel('性别')
plt.ylabel('人数')
plt.legend(title='学习压力')
plt.xticks(rotation=0)

# 隐藏第9个子图（如果有）
plt.tight_layout()
plt.savefig('questionnaire_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 可选：额外生成无课时间分布热力图
# 统计每个时间段无课的人数
time_slots = ['无课_周一12', '无课_周一34', '无课_周三56', '无课_周三78',
              '无课_周四12', '无课_周五56', '无课_周五78']
time_names = ['周一1-2', '周一3-4', '周三5-6', '周三7-8', '周四1-2', '周五5-6', '周五7-8']
free_counts = []
for col in time_slots:
    cnt = df[col].notna().sum() - (df[col] == '').sum()
    free_counts.append(cnt)
free_df = pd.DataFrame({'时段': time_names, '无课人数': free_counts})
free_df = free_df.sort_values('无课人数', ascending=False)
print("\n无课时间段统计：\n", free_df)

plt.figure(figsize=(10, 5))
sns.barplot(x='时段', y='无课人数', data=free_df, palette='coolwarm')
plt.title('各时间段无课人数统计')
plt.xlabel('时段')
plt.ylabel('无课人数')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('free_time_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

print("分析完成，图表已保存。")