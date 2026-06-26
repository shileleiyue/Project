import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ------------------------------
# 1. 读取数据
# ------------------------------
file_path = "350881459_按序号_关于影视行业环境与观众沉浸体验研究的详细问卷_274_274.xlsx"
df = pd.read_excel(file_path, header=0)

# 处理公式列
col_short = [c for c in df.columns if '5.' in c and '短视频' in c][0]
formula_cols = []
for col in df.columns:
    if df[col].dtype == 'object':
        first = df[col].first_valid_index()
        if first and str(df.loc[first, col]).startswith('='):
            formula_cols.append(col)
for col in formula_cols:
    df[col] = 6 - df[col_short]

# 定义因变量原始列
y1_col = [c for c in df.columns if '6.' in c and '长视频平台' in c][0]

# ------------------------------
# 2. 核心自变量（与之前相同）
# ------------------------------
core_vars = [
    '1. 您的年龄段：',
    '2. 您目前从事的行业/身份：',
    '5. 您平均每天花费在短视频平台（如抖音、快手、视频号等）上的总时长约为：',
    '4. 您通常通过哪些设备观看影视内容？（可多选）(智能手机)',
    '4 (平板电脑)',
    '4 (笔记本电脑)',
    '4 (台式电脑)',
    '4 (智能电视/投影仪)',
    '4 (VR设备)',
    '11. 导致您无法沉浸观看长视频的主要外部干扰因素是？（）(手机应用的通知提醒)',
    '11(工作/学习事务的插入)',
    '11(家庭/社交环境的干扰)',
    '11(其他娱乐内容的诱惑)',
    '11(算法推荐的其他内容预览)',
    '12. 导致您无法沉浸观看长视频的主要内容内部因素是？（）(剧情拖沓、节奏缓慢)',
    '12(情节逻辑漏洞或槽点多)',
    '12(演技或制作粗糙)',
    '12(广告插入频繁)',
    '12(题材或风格不感兴趣)',
    '13. 在什么情况下，您最可能获得一次沉浸式的观看体验？（可多选）(深夜或独处时)',
    '13(影院观影)',
    '13(使用高质量视听设备时)',
    '13(内容本身极其吸引人)',
    '13(与志同道合者一起观看讨论)',
    '23. 以下哪些技术或形式，最能提升您的沉浸感？（）(4K)',
    '23(HDR、杜比视界/全景声等高规格视听)',
    '23(互动叙事（可选择分支影响剧情）)',
    '23(VR/AR/XR等虚拟现实体验)',
    '23(模拟影院效果的“云影院”或专属播放模式)',
    '23(伴随式的创作解说、细节彩蛋揭秘)',
    '24. 您是否愿意为获得更好的沉浸体验而付费（如购买更高码流、解锁导演剪辑版、体验互动剧情等）？',
]

X_vars = [v for v in core_vars if v in df.columns]
print(f"选取 {len(X_vars)} 个核心自变量")

# ------------------------------
# 3. 变量名简化映射
# ------------------------------
var_shortnames = {
    '1. 您的年龄段：': '年龄段',
    '2. 您目前从事的行业/身份：': '行业',
    '5. 您平均每天花费在短视频平台（如抖音、快手、视频号等）上的总时长约为：': '短视频时长',
    '4. 您通常通过哪些设备观看影视内容？（可多选）(智能手机)': '设备_手机',
    '4 (平板电脑)': '设备_平板',
    '4 (笔记本电脑)': '设备_笔记本',
    '4 (台式电脑)': '设备_台式',
    '4 (智能电视/投影仪)': '设备_电视/投影',
    '4 (VR设备)': '设备_VR',
    '11. 导致您无法沉浸观看长视频的主要外部干扰因素是？（）(手机应用的通知提醒)': '干扰_手机通知',
    '11(工作/学习事务的插入)': '干扰_工作学习',
    '11(家庭/社交环境的干扰)': '干扰_家庭社交',
    '11(其他娱乐内容的诱惑)': '干扰_其他娱乐',
    '11(算法推荐的其他内容预览)': '干扰_算法推荐',
    '12. 导致您无法沉浸观看长视频的主要内容内部因素是？（）(剧情拖沓、节奏缓慢)': '内部_剧情拖沓',
    '12(情节逻辑漏洞或槽点多)': '内部_逻辑漏洞',
    '12(演技或制作粗糙)': '内部_演技粗糙',
    '12(广告插入频繁)': '内部_广告',
    '12(题材或风格不感兴趣)': '内部_题材不感兴趣',
    '13. 在什么情况下，您最可能获得一次沉浸式的观看体验？（可多选）(深夜或独处时)': '沉浸情境_独处',
    '13(影院观影)': '沉浸情境_影院',
    '13(使用高质量视听设备时)': '沉浸情境_高质设备',
    '13(内容本身极其吸引人)': '沉浸情境_内容吸引',
    '13(与志同道合者一起观看讨论)': '沉浸情境_同好讨论',
    '23. 以下哪些技术或形式，最能提升您的沉浸感？（）(4K)': '技术_4K',
    '23(HDR、杜比视界/全景声等高规格视听)': '技术_HDR/全景声',
    '23(互动叙事（可选择分支影响剧情）)': '技术_互动叙事',
    '23(VR/AR/XR等虚拟现实体验)': '技术_VR/AR',
    '23(模拟影院效果的“云影院”或专属播放模式)': '技术_云影院',
    '23(伴随式的创作解说、细节彩蛋揭秘)': '技术_彩蛋解说',
    '24. 您是否愿意为获得更好的沉浸体验而付费（如购买更高码流、解锁导演剪辑版、体验互动剧情等）？': '付费意愿',
}

# ------------------------------
# 4. 创建二分类因变量：高时长 vs 低时长
# ------------------------------
# 原变量取值1-5，定义 >=4 为高时长 (1)，否则为低时长 (0)
y_binary = (df[y1_col] >= 4).astype(int)
print(f"高时长样本数: {y_binary.sum()}, 低时长样本数: {(y_binary == 0).sum()}")

# ------------------------------
# 5. 准备自变量数据，处理缺失值
# ------------------------------
X = df[X_vars].copy()
y = y_binary.copy()

# 删除缺失行
valid_idx = X.dropna().index
X_clean = X.loc[valid_idx]
y_clean = y.loc[valid_idx]

X_clean = sm.add_constant(X_clean)
print(f"有效样本量: {len(X_clean)}")

# ------------------------------
# 6. 拟合逻辑回归模型
# ------------------------------
logit_model = sm.Logit(y_clean, X_clean).fit(disp=0)  # disp=0 不显示迭代过程
print(logit_model.summary())

# 提取结果
params = logit_model.params
conf = logit_model.conf_int()
pvalues = logit_model.pvalues
or_values = np.exp(params)  # 优势比
or_ci_low = np.exp(conf[0])
or_ci_high = np.exp(conf[1])

# 合并为DataFrame
results_df = pd.DataFrame({
    'coef': params,
    'or': or_values,
    'pvalue': pvalues,
    'ci_low': or_ci_low,
    'ci_high': or_ci_high
})
results_df = results_df.drop('const')  # 去掉截距项

# 标记显著变量（p<0.1）
sig_vars = results_df[results_df['pvalue'] < 0.1].index.tolist()
print(f"\n显著变量 (p<0.1): {[var_shortnames.get(v, v) for v in sig_vars]}")


# ------------------------------
# 7. 绘制森林图（OR值及置信区间）
# ------------------------------
def plot_or_forest(results_df, top_n=20, filename='logistic_forest.png'):
    """绘制OR值的森林图，只显示显著变量或top N"""
    # 取p<0.1的变量，若不足top_n则取top_n个（按p值排序）
    sig_df = results_df[results_df['pvalue'] < 0.1].copy()
    if len(sig_df) == 0:
        # 如果没有显著变量，取p值最小的top_n
        sig_df = results_df.nsmallest(top_n, 'pvalue').copy()
    else:
        # 如果有显著变量，但少于top_n，可补充一些接近显著的
        if len(sig_df) < top_n:
            nonsig = results_df[results_df['pvalue'] >= 0.1].nsmallest(top_n - len(sig_df), 'pvalue')
            sig_df = pd.concat([sig_df, nonsig])
    # 按OR值排序便于绘图
    sig_df = sig_df.sort_values('or', ascending=True)

    # 使用简化名作为标签
    labels = [var_shortnames.get(v, v) for v in sig_df.index]
    or_vals = sig_df['or']
    ci_low = sig_df['ci_low']
    ci_high = sig_df['ci_high']
    pvals = sig_df['pvalue']

    y_pos = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10, max(6, len(labels) * 0.3)))
    ax.errorbar(or_vals, y_pos, xerr=[or_vals - ci_low, ci_high - or_vals],
                fmt='o', capsize=4, color='steelblue', ecolor='gray')
    ax.axvline(1, color='red', linestyle='--', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('优势比 (OR) with 95% CI')
    ax.set_title('影响高时长观看的因素 (逻辑回归)')
    # 在点旁边标注p值
    for i, (or_val, p) in enumerate(zip(or_vals, pvals)):
        ax.text(or_val + 0.1, i, f'p={p:.3f}', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()


plot_or_forest(results_df, top_n=15, filename='logistic_forest.png')

# ------------------------------
# 8. ROC曲线和AUC
# ------------------------------
y_pred_prob = logit_model.predict()
fpr, tpr, thresholds = roc_curve(y_clean, y_pred_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC曲线 (AUC = {roc_auc:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('假阳性率 (1-特异性)')
plt.ylabel('真阳性率 (灵敏度)')
plt.title('逻辑回归模型的ROC曲线')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.savefig('logistic_roc.png', dpi=150)
plt.show()

# ------------------------------
# 9. 混淆矩阵及分类报告
# ------------------------------
y_pred_class = (y_pred_prob >= 0.5).astype(int)
cm = confusion_matrix(y_clean, y_pred_class)
print("\n混淆矩阵:")
print(cm)

# 绘制混淆矩阵热力图
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['预测低时长', '预测高时长'],
            yticklabels=['实际低时长', '实际高时长'])
plt.title('混淆矩阵')
plt.ylabel('真实值')
plt.xlabel('预测值')
plt.savefig('logistic_confusion.png', dpi=150)
plt.show()

print("\n分类报告:")
print(classification_report(y_clean, y_pred_class, target_names=['低时长', '高时长']))

# ------------------------------
# 10. 保存结果摘要
# ------------------------------
with open('logistic_results.txt', 'w', encoding='utf-8') as f:
    f.write("逻辑回归分析结果\n")
    f.write("=" * 50 + "\n")
    f.write(f"有效样本量: {len(X_clean)}\n")
    f.write(f"高时长样本: {y_clean.sum()}, 低时长样本: {(y_clean == 0).sum()}\n\n")
    f.write("模型摘要:\n")
    f.write(str(logit_model.summary()))
    f.write("\n\n显著变量 (p<0.1):\n")
    for v in sig_vars:
        f.write(f"  {var_shortnames.get(v, v)}: OR={results_df.loc[v, 'or']:.3f}, "
                f"95%CI=[{results_df.loc[v, 'ci_low']:.3f}, {results_df.loc[v, 'ci_high']:.3f}], "
                f"p={results_df.loc[v, 'pvalue']:.4f}\n")
    f.write(f"\nROC AUC: {roc_auc:.3f}\n")
    f.write("\n混淆矩阵:\n")
    f.write(str(cm))
    f.write("\n\n分类报告:\n")
    f.write(classification_report(y_clean, y_pred_class, target_names=['低时长', '高时长']))

print("\n分析完成，结果已保存至 logistic_results.txt，图表已生成。")