# -*- coding: utf-8 -*-
"""
影视行业调研数据分析程序（整合绘图）
"""
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from scipy.stats import chi2_contingency
import jieba
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

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
chinese_font = set_chinese_font()

# ==================== 配置 ====================
DATA_FILE = "350881459_按序号_关于影视行业环境与观众沉浸体验研究的详细问卷_274_274.xlsx"
OUTPUT_DIR = "分析结果"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 列名映射（已修正全角引号）====================
COLUMN_MAPPING = {
    1: {'type': 'single',
        'col': '1. 您的年龄段：',
        'options': ['18岁以下', '18-25岁', '26-35岁', '36-45岁', '46-55岁', '56岁及以上']},
    2: {'type': 'single',
        'col': '2. 您目前从事的行业/身份：',
        'options': ['学生', '互联网/科技行业', '文化传媒/影视行业', '金融/商业', '教育/科研', '自由职业', '其他']},
    3: {'type': 'single',
        'col': '3. 您平均每月在影视内容（包括会员、点播等）上的消费金额约为：',
        'options': ['0元', '1-30元', '31-50元', '51-100元', '100元以上']},
    4: {'type': 'multi',
        'cols': {
            '智能手机': '4. 您通常通过哪些设备观看影视内容？（可多选）(智能手机)',
            '平板电脑': '4 (平板电脑)',
            '笔记本电脑': '4 (笔记本电脑)',
            '台式电脑': '4 (台式电脑)',
            '智能电视/投影仪': '4 (智能电视/投影仪)',
            'VR设备': '4 (VR设备)',
            '其他': '4 (其他：)'
        },
        'options': ['智能手机', '平板电脑', '笔记本电脑', '台式电脑', '智能电视/投影仪', 'VR设备', '其他']},
    5: {'type': 'single',
        'col': '5. 您平均每天花费在短视频平台（如抖音、快手、视频号等）上的总时长约为：',
        'options': ['少于30分钟', '30分钟-1小时', '1-2小时', '2-3小时', '3小时以上']},
    6: {'type': 'single',
        'col': '6. 您平均每天花费在长视频平台（如爱优腾芒、B站长内容、Netflix等）上的总时长约为：',
        'options': ['少于30分钟', '30分钟-1小时', '1-2小时', '2-3小时', '3小时以上']},
    7: {'type': 'single',
        'col': '7. 在观看长视频时，您使用“倍速播放”功能的频率是：',
        'options': ['几乎总是使用', '经常使用', '偶尔使用', '很少使用', '从不使用']},
    8: {'type': 'single',
        'col': '8. 在观看一集45分钟左右的剧集时，您通常如何处理？',
        'options': ['一次性专注看完', '分2-3次看完', '边看边做其他事', '后台播放', '其他']},
    9: {'type': 'single',
        'col': '9. 您是否经常在观看视频的同时进行“多任务处理”（如回消息、刷社交软件、玩游戏等）？',
        'options': ['总是如此', '经常如此', '有时如此', '很少如此', '从不如此']},
    10: {'type': 'single',
         'col': '10. 您认为自己的“注意力持续时间”在过去3年内有何变化？',
         'options': ['明显变短了', '略有变短', '基本没变', '变得更长了']},
    11: {'type': 'multi',
         'cols': {
             '手机应用的通知提醒': '11. 导致您无法沉浸观看长视频的主要外部干扰因素是？（）(手机应用的通知提醒)',
             '工作/学习事务的插入': '11(工作/学习事务的插入)',
             '家庭/社交环境的干扰': '11(家庭/社交环境的干扰)',
             '其他娱乐内容的诱惑': '11(其他娱乐内容的诱惑)',
             '算法推荐的其他内容预览': '11(算法推荐的其他内容预览)',
             '其他': '11(其他：)'
         },
         'options': ['手机应用的通知提醒', '工作/学习事务的插入', '家庭/社交环境的干扰',
                     '其他娱乐内容的诱惑', '算法推荐的其他内容预览', '其他']},
    12: {'type': 'multi',
         'cols': {
             '剧情拖沓、节奏缓慢': '12. 导致您无法沉浸观看长视频的主要内容内部因素是？（）(剧情拖沓、节奏缓慢)',
             '情节逻辑漏洞或槽点多': '12(情节逻辑漏洞或槽点多)',
             '演技或制作粗糙': '12(演技或制作粗糙)',
             '广告插入频繁': '12(广告插入频繁)',
             '题材或风格不感兴趣': '12(题材或风格不感兴趣)',
             '其他': '12(其他：)'
         },
         'options': ['剧情拖沓、节奏缓慢', '情节逻辑漏洞或槽点多', '演技或制作粗糙',
                     '广告插入频繁', '题材或风格不感兴趣', '其他']},
    13: {'type': 'multi',
         'cols': {
             '深夜或独处时': '13. 在什么情况下，您最可能获得一次沉浸式的观看体验？（可多选）(深夜或独处时)',
             '影院观影': '13(影院观影)',
             '使用高质量视听设备时': '13(使用高质量视听设备时)',
             '内容本身极其吸引人': '13(内容本身极其吸引人)',
             '与志同道合者一起观看讨论': '13(与志同道合者一起观看讨论)',
             '其他': '13(其他：)'
         },
         'options': ['深夜或独处时', '影院观影', '使用高质量视听设备时',
                     '内容本身极其吸引人', '与志同道合者一起观看讨论', '其他']},
    14: {'type': 'single',
         'col': '14. 您是否听说过或关注“影视寒冬”这一说法？',
         'options': ['非常了解', '大致了解', '仅听说过', '完全没听说过']},
    15: {'type': 'multi',
         'cols': {
             '新开机的大制作项目减少': '15. 您认为“影视寒冬”最直接的表现是什么？（）(新开机的大制作项目减少)',
             '平台和片方更谨慎，不敢冒险': '15(平台和片方更谨慎，不敢冒险)',
             '演员、从业者工作机会变少': '15(演员、从业者工作机会变少)',
             '同质化、保守的续集/IP剧增多': '15(同质化、保守的续集/IP剧增多)',
             '微短剧、小程序剧等“轻量”内容爆发': '15(微短剧、小程序剧等“轻量”内容爆发)',
             '观众可选择的优质新作变少': '15(观众可选择的优质新作变少)',
             '其他': '15(其他：)'
         },
         'options': ['新开机的大制作项目减少', '平台和片方更谨慎，不敢冒险',
                     '演员、从业者工作机会变少', '同质化、保守的续集/IP剧增多',
                     '微短剧、小程序剧等“轻量”内容爆发', '观众可选择的优质新作变少', '其他']},
    16: {'type': 'single',
         'col': '16. 在您看来，“影视寒冬”与“注意力碎片化”之间是否存在关联？',
         'options': ['有强关联', '有一定关联', '关联不大', '不清楚']},
    17: {'type': 'single',
         'col': '17. “影视寒冬”下，您感觉影视内容的整体质量如何变化？',
         'options': ['明显下降', '略有下降', '基本持平', '有所提升', '两极分化更严重']},
    18: {'type': 'single',
         'col': '18. 最近一年，您完整看完（未弃剧）的剧集（单部）平均有多少集？',
         'options': ['少于10集', '10-20集', '21-30集', '31-40集', '40集以上']},
    19: {'type': 'multi',
         'cols': {
             '剧情注水，失去追看动力': '19. 最近一年，您弃剧的主要原因是什么？（）(剧情注水，失去追看动力)',
             '更新周期长，忘了或失去兴趣': '19(更新周期长，忘了或失去兴趣)',
             '时间不允许，无法持续跟进': '19(时间不允许，无法持续跟进)',
             '被其他新内容吸引': '19(被其他新内容吸引)',
             '口碑崩塌或剧透影响': '19(口碑崩塌或剧透影响)',
             '其他': '19(其他：)'
         },
         'options': ['剧情注水，失去追看动力', '更新周期长，忘了或失去兴趣',
                     '时间不允许，无法持续跟进', '被其他新内容吸引',
                     '口碑崩塌或剧透影响', '其他']},
    20: {'type': 'multi',
         'cols': {
             '转向观看更多短视频': '20. 您认为“影视寒冬”对您的个人观看习惯产生了什么影响？（可多选）(转向观看更多短视频)',
             '更依赖口碑和评分选择长视频': '20(更依赖口碑和评分选择长视频)',
             '降低了对新作的期待值': '20(降低了对新作的期待值)',
             '更愿意重温经典老剧/电影': '20(更愿意重温经典老剧/电影)',
             '开始观看更多海外内容': '20(开始观看更多海外内容)',
             '无明显影响': '20(无明显影响)',
             '其他': '20(其他：)'
         },
         'options': ['转向观看更多短视频', '更依赖口碑和评分选择长视频',
                     '降低了对新作的期待值', '更愿意重温经典老剧/电影',
                     '开始观看更多海外内容', '无明显影响', '其他']},
    21: {'type': 'single',
         'col': '21. 您认为“沉浸式体验”对于长视频的未来重要吗？',
         'options': ['至关重要', '比较重要', '一般', '不重要']},
    22: {'type': 'single',
         'col': '22. 一个能让您沉浸的剧集/电影，最核心的吸引点是什么？（单选）',
         'options': ['极致抓人的故事与悬念', '深刻的情感共鸣与人物弧光',
                     '宏大/新颖的世界观与视觉奇观', '精妙的叙事结构与艺术表达',
                     '真实的社会洞察与议题探讨']},
    23: {'type': 'multi',
         'cols': {
             '4K': '23. 以下哪些技术或形式，最能提升您的沉浸感？（）(4K)',
             'HDR、杜比视界/全景声等高规格视听': '23(HDR、杜比视界/全景声等高规格视听)',
             '互动叙事（可选择分支影响剧情）': '23(互动叙事（可选择分支影响剧情）)',
             'VR/AR/XR等虚拟现实体验': '23(VR/AR/XR等虚拟现实体验)',
             '模拟影院效果的“云影院”或专属播放模式': '23(模拟影院效果的“云影院”或专属播放模式)',
             '伴随式的创作解说、细节彩蛋揭秘': '23(伴随式的创作解说、细节彩蛋揭秘)',
             '其他': '23(其他：)'
         },
         'options': ['4K', 'HDR、杜比视界/全景声等高规格视听', '互动叙事（可选择分支影响剧情）',
                     'VR/AR/XR等虚拟现实体验', '模拟影院效果的“云影院”或专属播放模式',
                     '伴随式的创作解说、细节彩蛋揭秘', '其他']},
    24: {'type': 'single',
         'col': '24. 您是否愿意为获得更好的沉浸体验而付费（如购买更高码流、解锁导演剪辑版、体验互动剧情等）？',
         'options': ['愿意', '可能愿意', '不愿意', '坚决反对']},
    25: {'type': 'single',
         'col': '25. 您认为“沉浸感”的营造，主要责任在于？',
         'options': ['内容创作者', '制作方', '播放平台', '观众自身', '多方协同']},
    26: {'type': 'multi',
         'cols': {
             '更精炼的短剧集（如8-12集）': '26. 在内容形式上，您认为以下哪种探索对长视频的未来更有意义？（）(更精炼的短剧集（如8-12集）)',
             '单片付费的电影级网络电影': '26(单片付费的电影级网络电影)',
             '系列化、季播的精品剧': '26(系列化、季播的精品剧)',
             '融合游戏化元素的互动影集': '26(融合游戏化元素的互动影集)',
             '基于VR/元宇宙的叙事体验': '26(基于VR/元宇宙的叙事体验)',
             '其他': '26(其他：)'
         },
         'options': ['更精炼的短剧集（如8-12集）', '单片付费的电影级网络电影',
                     '系列化、季播的精品剧', '融合游戏化元素的互动影集',
                     '基于VR/元宇宙的叙事体验', '其他']},
    27: {'type': 'multi',
         'cols': {
             '提供“专注模式”（屏蔽通知、简化UI）': '27. 平台可以采取哪些措施来帮助用户更好地沉浸？（）(提供“专注模式”（屏蔽通知、简化UI）)',
             '优化算法，减少无关推荐干扰': '27(优化算法，减少无关推荐干扰)',
             '设立“精品剧场”或专题策划': '27(设立“精品剧场”或专题策划)',
             '强化社交功能，如高质量的弹幕、小组讨论': '27(强化社交功能，如高质量的弹幕、小组讨论)',
             '提供更灵活的观看计划与提醒': '27(提供更灵活的观看计划与提醒)',
             '其他': '27(其他：)'
         },
         'options': ['提供“专注模式”（屏蔽通知、简化UI）', '优化算法，减少无关推荐干扰',
                     '设立“精品剧场”或专题策划', '强化社交功能，如高质量的弹幕、小组讨论',
                     '提供更灵活的观看计划与提醒', '其他']},
    28: {'type': 'single',
         'col': '28. 您认为，在未来，长视频的“沉浸体验”与短视频的“碎片化消费”会是怎样的关系？',
         'options': ['对抗关系', '互补关系', '融合关系', '其他']},
    29: {'type': 'single',
         'col': '29. 整体上，您对国产长视频内容的未来持何种态度？',
         'options': ['乐观', '谨慎乐观', '中性', '悲观', '不关心']},
    30: {'type': 'text',
         'col': '30. 如果请您给影视内容创作者提一个最重要的建议，以应对当下的挑战，您会说什么？'}
}

# ==================== 工具函数 ====================
def safe_filename(s):
    s = str(s)
    s = re.sub(r'[\\/*?:"<>|]', '_', s)
    s = s.replace('\n', '').replace('\r', '')
    return s[:50]

def plot_single_bar(data, title, options, filename, total=None, multiple=False):
    if total is None:
        total = len(data) if isinstance(data, pd.Series) else data.sum()
    if isinstance(data, pd.Series):
        counts = data.value_counts().reindex(options, fill_value=0)
    else:
        counts = pd.Series(data, index=options)
    percentages = (counts / total * 100).round(1)

    fig, ax = plt.subplots(figsize=(10, max(5, len(options)*0.4)))
    y_pos = np.arange(len(options))
    bars = ax.barh(y_pos, counts.values, color='skyblue', edgecolor='grey')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(options, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('选择人数')
    ax.set_title(f'{title} (总人数={total})', fontsize=14, fontweight='bold')

    for i, (count, bar) in enumerate(zip(counts.values, bars)):
        if count > 0:
            ax.text(count + max(counts)*0.01, bar.get_y() + bar.get_height()/2,
                    f'{int(count)} ({percentages.iloc[i]}%)',
                    va='center', ha='left', fontsize=9)

    ax.set_xlim(0, max(counts) * 1.15 if max(counts) > 0 else 10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close()

def load_and_preprocess(filepath):
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    print(f"数据加载成功，共 {len(df)} 行，{len(df.columns)} 列")

    # 单选题：数字 -> 选项
    for q, info in COLUMN_MAPPING.items():
        if info['type'] == 'single':
            col = info['col']
            if col not in df.columns:
                print(f"警告：单选题列 {col} 不存在，跳过 Q{q}")
                continue
            # 构建映射（数字从1开始）
            num_to_option = {i+1: opt for i, opt in enumerate(info['options'])}
            # 检查原始数据中的唯一值
            unique_vals = df[col].dropna().unique()
            print(f"Q{q} {col} 原始唯一值: {unique_vals}")
            # 应用映射
            df[col] = df[col].map(num_to_option)
            # 检查是否有未映射的值
            if df[col].isna().any():
                print(f"警告：Q{q} {col} 中存在无法映射的值，将被设为NaN")

    # 多选题：生成选项列
    for q, info in COLUMN_MAPPING.items():
        if info['type'] == 'multi':
            cols_dict = info.get('cols', {})
            existing_opts = []
            for opt, col_name in cols_dict.items():
                if col_name in df.columns:
                    existing_opts.append(opt)
                    df[f'q{q}_{opt}'] = df[col_name].apply(lambda x: 1 if x in [1, '1', True, '是', 'Yes'] else 0)
                else:
                    print(f"警告：多选题 Q{q} 缺少选项列 {col_name}，该选项将被忽略")
            if not existing_opts:
                print(f"警告：多选题 Q{q} 没有可用的选项列，跳过")
                continue
            def get_selected(row):
                selected = []
                for opt in existing_opts:
                    if row[f'q{q}_{opt}'] == 1:
                        selected.append(opt)
                return selected
            df[f'q{q}_multi'] = df.apply(get_selected, axis=1)

    # 打印转换后的一列示例，验证
    print("\n转换后 Q1 前5行：")
    print(df[COLUMN_MAPPING[1]['col']].head())
    return df

def univariate_analysis(df):
    print("开始单变量分析...")
    # 调试：查看Q1转换后的情况
    col1 = COLUMN_MAPPING[1]['col']  # '1. 您的年龄段：'
    print(f"Q1 列名: {col1}")
    print("前5行数据：")
    print(df[col1].head())
    print("值分布：")
    print(df[col1].value_counts())

    results = []
    for q, info in COLUMN_MAPPING.items():
        if info['type'] == 'text':
            continue
        if info['type'] == 'single':
            col = info['col']
            if col not in df.columns:
                print(f"警告：列 {col} 不存在，跳过 Q{q}")
                continue
            title = f"Q{q}. {col}"
            counts = df[col].value_counts()
            ordered_counts = counts.reindex(info['options'], fill_value=0)
            res = pd.DataFrame({
                '选项': ordered_counts.index,
                '计数': ordered_counts.values,
                '百分比': (ordered_counts.values / len(df) * 100).round(1)
            })
            results.append((f"Q{q}_{col[:20]}", res))
            filename = safe_filename(f"Q{q}_{col[:20]}_单变量.png")
            plot_single_bar(ordered_counts, title, info['options'], filename, total=len(df))
        elif info['type'] == 'multi':
            opt_cols = {opt: f'q{q}_{opt}' for opt in info['options']}
            existing_opts = []
            for opt, col_name in opt_cols.items():
                if col_name in df.columns:
                    existing_opts.append(opt)
                else:
                    print(f"警告：多选题 Q{q} 的选项列 {col_name} 不存在，跳过该选项")
            if not existing_opts:
                print(f"警告：多选题 Q{q} 没有可用的选项列，跳过")
                continue
            counts = {}
            for opt in existing_opts:
                col_name = opt_cols[opt]
                counts[opt] = df[col_name].sum()
            ordered_counts = pd.Series({opt: counts.get(opt, 0) for opt in info['options']})
            title = f"Q{q}. 多选题"
            res = pd.DataFrame({
                '选项': ordered_counts.index,
                '计数': ordered_counts.values,
                '百分比（基于人数）': (ordered_counts.values / len(df) * 100).round(1),
                '百分比（基于选项数）': (ordered_counts.values / ordered_counts.sum() * 100).round(1) if ordered_counts.sum() > 0 else 0
            })
            results.append((f"Q{q}_多选题", res))
            filename = safe_filename(f"Q{q}_多选题.png")
            plot_single_bar(ordered_counts, title + " (多选)", info['options'], filename, total=len(df), multiple=True)

    excel_path = os.path.join(OUTPUT_DIR, "单变量统计表.xlsx")
    if os.path.exists(excel_path):
        try:
            os.remove(excel_path)
        except PermissionError:
            print(f"错误：无法写入 {excel_path}，请关闭该文件后重试。")
            return
    with pd.ExcelWriter(excel_path) as writer:
        for name, df_res in results:
            safe_sheet = safe_filename(name)[:31]
            df_res.to_excel(writer, sheet_name=safe_sheet, index=False)
    print("单变量分析完成，图表和表格已保存。")

def bivariate_analysis(df):
    print("开始双变量交叉分析...")
    group_vars = [(1, '年龄'), (2, '行业'), (3, '月消费'), (10, '注意力变化')]
    target_vars = [
        (5, '短视频时长'),
        (6, '长视频时长'),
        (7, '倍速频率'),
        (9, '多任务处理'),
        (11, '外部干扰', 'multi'),
        (12, '内部因素', 'multi'),
        (17, '质量变化'),
        (21, '沉浸重要性'),
        (24, '付费意愿'),
        (29, '未来态度'),
    ]
    cross_results = []
    for g_q, g_name in group_vars:
        g_col = COLUMN_MAPPING[g_q]['col']
        if g_col not in df.columns:
            print(f"分组变量 {g_col} 不存在，跳过")
            continue
        g_options = COLUMN_MAPPING[g_q]['options']
        for t_item in target_vars:
            if len(t_item) == 3:
                t_q, t_name, t_type = t_item
            else:
                t_q, t_name = t_item
                t_type = COLUMN_MAPPING[t_q]['type']
            if t_type == 'single':
                t_col = COLUMN_MAPPING[t_q]['col']
                if t_col not in df.columns:
                    continue
                t_options = COLUMN_MAPPING[t_q]['options']
                crosstab = pd.crosstab(df[g_col], df[t_col])
                crosstab = crosstab.reindex(index=g_options, columns=t_options, fill_value=0)
                cross_results.append((f"{g_name}_vs_{t_name}", crosstab))
                title = f"{g_name} 与 {t_name} 的交叉分析"
                filename = safe_filename(f"交叉_{g_name}_vs_{t_name}.png")
                crosstab_pct = crosstab.div(crosstab.sum(axis=1), axis=0) * 100
                fig, ax = plt.subplots(figsize=(12, 6))
                crosstab_pct.plot(kind='bar', ax=ax, colormap='viridis', edgecolor='black')
                ax.set_ylabel('百分比 (%)')
                ax.set_title(title)
                ax.legend(title=t_name, bbox_to_anchor=(1.05, 1), loc='upper left')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
                plt.close()
            elif t_type == 'multi':
                t_options = COLUMN_MAPPING[t_q]['options']
                result_df = pd.DataFrame(index=g_options)
                for opt in t_options:
                    opt_col = f'q{t_q}_{opt}'
                    if opt_col not in df.columns:
                        continue
                    grouped = df.groupby(g_col)[opt_col].mean() * 100
                    result_df[opt] = grouped.reindex(g_options, fill_value=0).round(1)
                cross_results.append((f"{g_name}_vs_{t_name}_多选", result_df))
                fig, ax = plt.subplots(figsize=(12, 6))
                result_df.plot(kind='bar', ax=ax, colormap='tab20', edgecolor='black')
                ax.set_ylabel('选择百分比 (%)')
                ax.set_title(f"{g_name} 与 {t_name} 的交叉分析（多选）")
                ax.legend(title='选项', bbox_to_anchor=(1.05, 1), loc='upper left')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(os.path.join(OUTPUT_DIR, safe_filename(f"交叉_{g_name}_vs_{t_name}_多选.png")), dpi=150)
                plt.close()

    excel_path = os.path.join(OUTPUT_DIR, "交叉分析表.xlsx")
    if os.path.exists(excel_path):
        try:
            os.remove(excel_path)
        except PermissionError:
            print(f"错误：无法写入 {excel_path}，请关闭该文件后重试。")
            return
    with pd.ExcelWriter(excel_path) as writer:
        for name, df_res in cross_results:
            safe_sheet = safe_filename(name)[:31]
            df_res.to_excel(writer, sheet_name=safe_sheet, index=False)
    print("交叉分析完成，图表和表格已保存。")

def correlation_analysis(df):
    print("开始相关性分析...")
    var_pairs = [(10,5), (10,6), (9,7), (14,17), (16,28), (24,23)]
    results = []
    for q1, q2 in var_pairs:
        info1 = COLUMN_MAPPING.get(q1)
        info2 = COLUMN_MAPPING.get(q2)
        if not info1 or not info2 or info1['type'] != 'single' or info2['type'] != 'single':
            continue
        col1, col2 = info1['col'], info2['col']
        if col1 not in df.columns or col2 not in df.columns:
            continue
        crosstab = pd.crosstab(df[col1], df[col2])
        chi2, p, dof, expected = chi2_contingency(crosstab)
        n = crosstab.sum().sum()
        min_dim = min(crosstab.shape) - 1
        cramer_v = np.sqrt(chi2 / (n * min_dim)) if min_dim != 0 else np.nan
        results.append({
            '变量1': info1['col'],
            '变量2': info2['col'],
            '卡方值': chi2,
            'p值': p,
            '自由度': dof,
            'Cramer V': cramer_v
        })
    if results:
        df_corr = pd.DataFrame(results)
        excel_path = os.path.join(OUTPUT_DIR, "相关性分析.xlsx")
        if os.path.exists(excel_path):
            try:
                os.remove(excel_path)
            except PermissionError:
                print(f"错误：无法写入 {excel_path}，请关闭该文件后重试。")
                return
        df_corr.to_excel(excel_path, index=False)
        print("相关性分析完成，结果已保存。")

def text_analysis(df):
    print("开始文本分析...")
    col = COLUMN_MAPPING[30]['col']
    if col not in df.columns:
        print("未找到建议列，跳过文本分析")
        return
    texts = df[col].dropna().astype(str)
    texts = texts[texts.str.strip() != '']
    if len(texts) == 0:
        print("没有有效建议文本，跳过")
        return
    word_list = []
    for t in texts:
        words = jieba.lcut(t)
        words = [w for w in words if len(w) > 1 and not w.isspace()]
        word_list.extend(words)
    word_freq = pd.Series(word_list).value_counts().head(50)

    font_path = None
    if chinese_font:
        for f in fm.fontManager.ttflist:
            if chinese_font in f.name:
                font_path = f.fname
                break
    wordcloud = WordCloud(font_path=font_path, width=800, height=400,
                          background_color='white').generate_from_frequencies(word_freq.to_dict())
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('观众建议词云')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '建议词云.png'), dpi=150)
    plt.close()

    excel_path = os.path.join(OUTPUT_DIR, '建议高频词.xlsx')
    if os.path.exists(excel_path):
        try:
            os.remove(excel_path)
        except PermissionError:
            print(f"错误：无法写入 {excel_path}，请关闭该文件后重试。")
            return
    word_freq.to_excel(excel_path, header=['频次'])
    print("文本分析完成，词云和高频词已保存。")

def main():
    print("="*50)
    print("影视行业调研数据分析程序启动")
    print("="*50)

    if not os.path.exists(DATA_FILE):
        print(f"错误：数据文件 {DATA_FILE} 不存在！请修改 DATA_FILE 变量。")
        return

    df = load_and_preprocess(DATA_FILE)
    univariate_analysis(df)
    bivariate_analysis(df)
    correlation_analysis(df)
    text_analysis(df)
    print("\n所有分析完成！结果保存在文件夹：", OUTPUT_DIR)

if __name__ == "__main__":
    main()