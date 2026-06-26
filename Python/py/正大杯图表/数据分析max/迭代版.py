# -*- coding: utf-8 -*-
"""
影视行业调研分析脚本（最终版）
功能：
1. 信效度分析：针对指定组合 (6,7,9)、(6,7,9,10)、(6,7,9,8)、(6,7,9,18) 计算总α及删除项后的α。
2. 单变量图表：从汇总表 "350881459_1772196647a7Xnny (1).xlsx" 读取数据并绘制（已去除多选题的“其他”项）。
3. 双变量交叉分析、相关性分析、建议词云（仍使用原始数据，并已去除多选题的“其他”项）。
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
import pingouin as pg
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity
import warnings

warnings.filterwarnings('ignore')

# ==================== 配置 ====================
RAW_DATA_FILE = "350881459_按序号_关于影视行业环境与观众沉浸体验研究的详细问卷_274_274.xlsx"
SUMMARY_TABLE_FILE = "350881459_1772196647a7Xnny.xlsx"
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


chinese_font = set_chinese_font()

# ==================== 列名映射（已移除多选题的“其他”项）====================
COLUMN_MAPPING = {
    1: {'type': 'single',
        'col': '1. 您的年龄段：',
        'options': ['18岁以下', '18-25岁', '26-35岁', '36-45岁', '46-55岁', '56岁及以上']},
    2: {'type': 'single',
        'col': '2. 您目前从事的行业/身份：',
        'options': ['学生', '互联网/科技行业', '文化传媒/影视行业', '金融/商业', '教育/科研', '自由职业']},  # 移除“其他”
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
            # '其他': '4 (其他：)'   # 已移除
        },
        'options': ['智能手机', '平板电脑', '笔记本电脑', '台式电脑', '智能电视/投影仪', 'VR设备']},
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
        'options': ['一次性专注看完', '分2-3次看完', '边看边做其他事', '后台播放']},  # 移除“其他”
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
             # '其他': '11(其他：)'
         },
         'options': ['手机应用的通知提醒', '工作/学习事务的插入', '家庭/社交环境的干扰',
                     '其他娱乐内容的诱惑', '算法推荐的其他内容预览']},
    12: {'type': 'multi',
         'cols': {
             '剧情拖沓、节奏缓慢': '12. 导致您无法沉浸观看长视频的主要内容内部因素是？（）(剧情拖沓、节奏缓慢)',
             '情节逻辑漏洞或槽点多': '12(情节逻辑漏洞或槽点多)',
             '演技或制作粗糙': '12(演技或制作粗糙)',
             '广告插入频繁': '12(广告插入频繁)',
             '题材或风格不感兴趣': '12(题材或风格不感兴趣)',
             # '其他': '12(其他：)'
         },
         'options': ['剧情拖沓、节奏缓慢', '情节逻辑漏洞或槽点多', '演技或制作粗糙',
                     '广告插入频繁', '题材或风格不感兴趣']},
    13: {'type': 'multi',
         'cols': {
             '深夜或独处时': '13. 在什么情况下，您最可能获得一次沉浸式的观看体验？（可多选）(深夜或独处时)',
             '影院观影': '13(影院观影)',
             '使用高质量视听设备时': '13(使用高质量视听设备时)',
             '内容本身极其吸引人': '13(内容本身极其吸引人)',
             '与志同道合者一起观看讨论': '13(与志同道合者一起观看讨论)',
             # '其他': '13(其他：)'
         },
         'options': ['深夜或独处时', '影院观影', '使用高质量视听设备时',
                     '内容本身极其吸引人', '与志同道合者一起观看讨论']},
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
             # '其他': '15(其他：)'
         },
         'options': ['新开机的大制作项目减少', '平台和片方更谨慎，不敢冒险',
                     '演员、从业者工作机会变少', '同质化、保守的续集/IP剧增多',
                     '微短剧、小程序剧等“轻量”内容爆发', '观众可选择的优质新作变少']},
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
             # '其他': '19(其他：)'
         },
         'options': ['剧情注水，失去追看动力', '更新周期长，忘了或失去兴趣',
                     '时间不允许，无法持续跟进', '被其他新内容吸引',
                     '口碑崩塌或剧透影响']},
    20: {'type': 'multi',
         'cols': {
             '转向观看更多短视频': '20. 您认为“影视寒冬”对您的个人观看习惯产生了什么影响？（可多选）(转向观看更多短视频)',
             '更依赖口碑和评分选择长视频': '20(更依赖口碑和评分选择长视频)',
             '降低了对新作的期待值': '20(降低了对新作的期待值)',
             '更愿意重温经典老剧/电影': '20(更愿意重温经典老剧/电影)',
             '开始观看更多海外内容': '20(开始观看更多海外内容)',
             # '无明显影响': '20(无明显影响)',   # 如果“无明显影响”也算选项，我们保留它
             # '其他': '20(其他：)'
         },
         'options': ['转向观看更多短视频', '更依赖口碑和评分选择长视频',
                     '降低了对新作的期待值', '更愿意重温经典老剧/电影',
                     '开始观看更多海外内容']},  # 注意“无明显影响”可能也需要保留，但根据需求只移除“其他”
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
             # '其他': '23(其他：)'
         },
         'options': ['4K', 'HDR、杜比视界/全景声等高规格视听',
                     '互动叙事（可选择分支影响剧情）', 'VR/AR/XR等虚拟现实体验',
                     '模拟影院效果的“云影院”或专属播放模式',
                     '伴随式的创作解说、细节彩蛋揭秘']},
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
             # '其他': '26(其他：)'
         },
         'options': ['更精炼的短剧集（如8-12集）', '单片付费的电影级网络电影',
                     '系列化、季播的精品剧', '融合游戏化元素的互动影集',
                     '基于VR/元宇宙的叙事体验']},
    27: {'type': 'multi',
         'cols': {
             '提供“专注模式”（屏蔽通知、简化UI）': '27. 平台可以采取哪些措施来帮助用户更好地沉浸？（）(提供“专注模式”（屏蔽通知、简化UI）)',
             '优化算法，减少无关推荐干扰': '27(优化算法，减少无关推荐干扰)',
             '设立“精品剧场”或专题策划': '27(设立“精品剧场”或专题策划)',
             '强化社交功能，如高质量的弹幕、小组讨论': '27(强化社交功能，如高质量的弹幕、小组讨论)',
             '提供更灵活的观看计划与提醒': '27(提供更灵活的观看计划与提醒)',
             # '其他': '27(其他：)'
         },
         'options': ['提供“专注模式”（屏蔽通知、简化UI）', '优化算法，减少无关推荐干扰',
                     '设立“精品剧场”或专题策划', '强化社交功能，如高质量的弹幕、小组讨论',
                     '提供更灵活的观看计划与提醒']},
    28: {'type': 'single',
         'col': '28. 您认为，在未来，长视频的“沉浸体验”与短视频的“碎片化消费”会是怎样的关系？',
         'options': ['对抗关系', '互补关系', '融合关系', '其他']},  # 这里的“其他”是单选题选项，不属于多选题的“其他”，保留
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


def plot_single_bar(data, title, options, filename, total=None):
    """绘制单选题/多选题的水平条形图"""
    if total is None:
        total = len(data) if isinstance(data, pd.Series) else data.sum()
    if isinstance(data, pd.Series):
        counts = data.value_counts().reindex(options, fill_value=0)
    else:
        counts = pd.Series(data, index=options)
    percentages = (counts / total * 100).round(1)

    fig, ax = plt.subplots(figsize=(10, max(5, len(options) * 0.4)))
    y_pos = np.arange(len(options))
    bars = ax.barh(y_pos, counts.values, color='skyblue', edgecolor='grey')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(options, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('选择人数')
    ax.set_title(f'{title} (总人数={total})', fontsize=14, fontweight='bold')

    max_count = max(counts) if max(counts) > 0 else 1
    for i, (count, bar) in enumerate(zip(counts.values, bars)):
        if count > 0:
            ax.text(count + max_count * 0.01, bar.get_y() + bar.get_height() / 2,
                    f'{int(count)} ({percentages.iloc[i]}%)',
                    va='center', ha='left', fontsize=9)
    ax.set_xlim(0, max_count * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close()


def load_raw_data():
    """加载原始数据（数字编码）"""
    if not os.path.exists(RAW_DATA_FILE):
        raise FileNotFoundError(f"原始数据文件不存在：{RAW_DATA_FILE}")
    df = pd.read_excel(RAW_DATA_FILE)
    print(f"原始数据加载成功，共 {len(df)} 行，{len(df.columns)} 列")
    return df


def preprocess_for_descriptive(df_raw):
    df = df_raw.copy()
    for q, info in COLUMN_MAPPING.items():
        if info['type'] == 'single':
            col = info['col']
            if col not in df.columns:
                continue
            num_to_option = {i + 1: opt for i, opt in enumerate(info['options'])}
            df[col + '_label'] = df[col].map(num_to_option)
    return df


# ==================== 信度分析（指定组合）====================
def reliability_analysis_combinations(df):
    print("\n" + "=" * 50)
    print("开始信度分析（指定组合）")
    print("=" * 50)

    # 定义要分析的组合
    combinations = {
        '组合A (6,7,9)': [6, 7, 9],
        '组合B (6,7,9,10)': [6, 7, 9, 10],
        '组合C (6,7,9,8)': [6, 7, 9, 8],
        '组合D (6,7,9,18)': [6, 7, 9, 18]
    }

    # 获取列名
    q_cols = {q: COLUMN_MAPPING[q]['col'] for q in [6, 7, 8, 9, 10, 18]}

    # 检查所有所需列是否存在
    missing = [col for col in q_cols.values() if col not in df.columns]
    if missing:
        print("错误：以下列不存在，请检查列名：", missing)
        return

    # 准备原始数据（按方向编码）
    base_data = pd.DataFrame()
    base_data['Q6'] = df[q_cols[6]].map({1: 5, 2: 4, 3: 3, 4: 2, 5: 1})  # 反向
    base_data['Q7'] = df[q_cols[7]].copy()  # 正向
    base_data['Q8'] = df[q_cols[8]].copy()  # 正向
    base_data['Q9'] = df[q_cols[9]].copy()  # 正向
    base_data['Q10'] = df[q_cols[10]].map({1: 4, 2: 3, 3: 2, 4: 1})  # 反向
    base_data['Q18'] = df[q_cols[18]].map({1: 5, 2: 4, 3: 3, 4: 2, 5: 1})  # 反向

    # 删除缺失值
    base_data = base_data.dropna()
    print(f"有效样本量: {len(base_data)}")
    if len(base_data) < 3:
        print("样本量不足，无法进行信度分析。")
        return

    # 为每个组合计算信度
    results = []
    for combo_name, q_list in combinations.items():
        # 提取对应题目
        col_names = [f'Q{q}' for q in q_list]
        data_combo = base_data[col_names].copy()

        # 总信度
        alpha_total = pg.cronbach_alpha(data_combo)[0]

        # 删除每个题目后的信度
        item_stats = []
        for col in col_names:
            data_without = data_combo.drop(columns=[col])
            alpha_without = pg.cronbach_alpha(data_without)[0]
            item_stats.append({'删除题目': col, 'α值': round(alpha_without, 3)})

        results.append({
            '组合': combo_name,
            '总α': round(alpha_total, 3),
            '删除项统计': item_stats
        })

        # 打印结果
        print(f"\n{combo_name}:")
        print(f"  总 Cronbach's α = {alpha_total:.3f}")
        for stat in item_stats:
            print(f"  删除 {stat['删除题目']} 后 α = {stat['α值']}")

    # 保存结果到Excel
    with pd.ExcelWriter(os.path.join(OUTPUT_DIR, "信度分析结果（指定组合）.xlsx")) as writer:
        for combo_name, q_list in combinations.items():
            col_names = [f'Q{q}' for q in q_list]
            data_combo = base_data[col_names].copy()
            alpha_total = pg.cronbach_alpha(data_combo)[0]
            # 构建表格：总信度一行，删除项每行
            rows = []
            rows.append(['总信度', alpha_total, ''])
            for col in col_names:
                data_without = data_combo.drop(columns=[col])
                alpha_without = pg.cronbach_alpha(data_without)[0]
                rows.append([f'删除{col}', alpha_without, ''])
            df_res = pd.DataFrame(rows, columns=['项目', 'α值', '备注'])
            safe_sheet = combo_name[:31]
            df_res.to_excel(writer, sheet_name=safe_sheet, index=False)
    print(f"\n结果已保存至: {os.path.join(OUTPUT_DIR, '信度分析结果（指定组合）.xlsx')}")


# ==================== 效度分析（保持原样，但只对指定组合可能无意义，可保留或注释）====================
def validity_analysis_immersion(df):
    print("\n" + "="*50)
    print("开始效度分析（探索性因子分析）")
    print("="*50)

    q_cols = {q: COLUMN_MAPPING[q]['col'] for q in [6,7,8,9,10,18]}
    missing = [col for col in q_cols.values() if col not in df.columns]
    if missing:
        print("错误：以下列不存在，请检查列名：", missing)
        return

    data = pd.DataFrame()
    data['Q6'] = df[q_cols[6]].map({1:5, 2:4, 3:3, 4:2, 5:1})
    data['Q7'] = df[q_cols[7]].copy()
    data['Q8'] = df[q_cols[8]].copy()
    data['Q9'] = df[q_cols[9]].copy()
    data['Q10'] = df[q_cols[10]].map({1:4, 2:3, 3:2, 4:1})
    data['Q18'] = df[q_cols[18]].map({1:5, 2:4, 3:3, 4:2, 5:1})
    data = data.dropna()
    print(f"用于效度分析的有效样本量: {len(data)}")
    if len(data) < 5:
        print("样本量不足，无法进行因子分析。")
        return

    # KMO和Bartlett检验
    try:
        kmo_all, kmo = calculate_kmo(data)
        chi2, p = calculate_bartlett_sphericity(data)
        dof = data.shape[1] * (data.shape[1] - 1) // 2  # Bartlett检验自由度
    except Exception as e:
        print(f"KMO/Bartlett检验出错: {e}")
        return

    # 打印结果
    print(f"KMO = {kmo:.3f}")
    if kmo < 0.6:
        print("KMO值偏低，数据可能不适合因子分析")
    print(f"Bartlett's test: chi2={chi2:.2f}, p={p:.4f}, dof={dof}")
    if p < 0.05:
        print("Bartlett检验显著，适合因子分析")
    else:
        print("Bartlett检验不显著，数据可能不适合因子分析")

    # --- 单独保存KMO和Bartlett结果到文本文件 ---
    result_txt = os.path.join(OUTPUT_DIR, "效度检验摘要.txt")
    with open(result_txt, 'w', encoding='utf-8') as f:
        f.write("效度分析检验结果\n")
        f.write("="*30 + "\n")
        f.write(f"KMO检验值: {kmo:.3f}\n")
        f.write("Bartlett球形度检验:\n")
        f.write(f"  卡方值: {chi2:.2f}\n")
        f.write(f"  自由度: {dof}\n")
        f.write(f"  p值: {p:.4f}\n")
        f.write("="*30 + "\n")
        if p < 0.05:
            f.write("结论: Bartlett检验显著，适合因子分析。\n")
        else:
            f.write("结论: Bartlett检验不显著，可能不适合因子分析。\n")
        if kmo >= 0.6:
            f.write("KMO值尚可，可尝试因子分析。\n")
        else:
            f.write("KMO值偏低，因子分析效果可能不佳。\n")
    print(f"检验结果已单独保存至: {result_txt}")

    # 后续因子分析代码（如果不需要因子分析，可注释掉）
    # ...（此处省略因子分析代码）...


# ==================== 单变量绘图（从新汇总表读取，过滤“其他”项，并打印调试信息）====================
def plot_univariate_from_summary():
    print("\n开始绘制单变量图表（使用新汇总表，已过滤“其他”项）...")
    if not os.path.exists(SUMMARY_TABLE_FILE):
        print(f"错误：汇总表文件 {SUMMARY_TABLE_FILE} 不存在！")
        return

    # 读取整个Sheet
    df_summary = pd.read_excel(SUMMARY_TABLE_FILE, header=None)
    rows = df_summary.values.tolist()

    # 初始化
    q_data = {}  # 存储每个题目的选项和计数
    current_q = None
    current_options = []
    current_counts = []
    collecting = False
    skip_header = False

    for i, row in enumerate(rows):
        if not row or all(pd.isna(cell) for cell in row):
            continue

        first_cell = str(row[0]) if pd.notna(row[0]) else ''
        if first_cell and re.match(r'^\d+\.', first_cell) and ('单选题' in first_cell or '多选题' in first_cell):
            # 上一题结束，保存数据（过滤“其他”项）
            if current_q is not None and current_options and current_counts:
                # 过滤掉“其他”项
                filtered_opts = []
                filtered_cnts = []
                for opt, cnt in zip(current_options, current_counts):
                    # 如果选项文本包含“其他”（排除“其他娱乐内容的诱惑”这类包含“其他”但不是纯“其他”的项）
                    # 我们只过滤掉选项就是“其他”或“其他( )”之类的项
                    if opt.strip() == '其他' or opt.strip().startswith('其他') and len(opt) < 5:  # 简单判断
                        continue
                    filtered_opts.append(opt)
                    filtered_cnts.append(cnt)
                q_data[current_q] = (filtered_opts, filtered_cnts)
            # 提取题号
            match = re.match(r'^(\d+)\.', first_cell)
            q_num = int(match.group(1)) if match else None
            current_q = q_num
            current_options = []
            current_counts = []
            collecting = True
            skip_header = True
            continue

        if collecting:
            if skip_header:
                skip_header = False
                continue

            if '本题有效填写人次' in first_cell:
                collecting = False
                continue

            if len(row) >= 2 and pd.notna(row[0]) and pd.notna(row[1]):
                opt = str(row[0]).strip().replace('<br>', '').strip()
                count_val = row[1]
                if isinstance(count_val, str):
                    count_val = re.sub(r'<[^>]+>', '', count_val).strip()
                try:
                    count = int(float(count_val))
                except:
                    count = 0
                current_options.append(opt)
                current_counts.append(count)

    # 保存最后一题
    if current_q is not None and current_options and current_counts:
        filtered_opts = []
        filtered_cnts = []
        for opt, cnt in zip(current_options, current_counts):
            if opt.strip() == '其他' or opt.strip().startswith('其他') and len(opt) < 5:
                continue
            filtered_opts.append(opt)
            filtered_cnts.append(cnt)
        q_data[current_q] = (filtered_opts, filtered_cnts)

    # 打印调试信息
    print("从汇总表提取的题目数据：")
    for q, (opts, cnts) in q_data.items():
        print(f"Q{q}: 选项={opts}, 计数={cnts}")

    # 遍历所有题目，绘图
    for q, info in COLUMN_MAPPING.items():
        if info['type'] == 'text':
            continue
        if q not in q_data:
            print(f"警告：未找到Q{q}对应的数据，跳过")
            continue

        options_from_file, counts_from_file = q_data[q]
        if not options_from_file:
            print(f"警告：Q{q} 无有效选项，跳过")
            continue

        counts_series = pd.Series(counts_from_file, index=options_from_file)

        if info['type'] == 'single':
            title = f"Q{q}. {info['col']}"
        else:
            title = f"Q{q}. 多选题"

        filename = safe_filename(f"Q{q}_{title[:20]}_单变量.png")
        plot_single_bar(counts_series, title, options_from_file, filename, total=counts_series.sum())

    print("单变量图表绘制完成。")


# ==================== 其他分析函数（交叉、相关、词云）====================
def bivariate_analysis(df_label):
    print("\n开始双变量交叉分析...")
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
        g_col = COLUMN_MAPPING[g_q]['col'] + '_label'
        if g_col not in df_label.columns:
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
                t_col = COLUMN_MAPPING[t_q]['col'] + '_label'
                if t_col not in df_label.columns:
                    continue
                t_options = COLUMN_MAPPING[t_q]['options']
                crosstab = pd.crosstab(df_label[g_col], df_label[t_col])
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
                t_info = COLUMN_MAPPING[t_q]
                t_options = t_info['options']  # 已不含“其他”
                t_cols = t_info['cols']
                result_df = pd.DataFrame(index=g_options)
                for opt in t_options:
                    col_name = t_cols.get(opt)
                    if col_name is None or col_name not in df_label.columns:
                        continue
                    grouped = df_label.groupby(g_col)[col_name].mean() * 100
                    result_df[opt] = grouped.reindex(g_options, fill_value=0).round(1)
                if result_df.empty or result_df.isnull().all().all() or result_df.sum().sum() == 0:
                    print(f"警告：{g_name} 与 {t_name} 的多选交叉分析无有效数据，跳过")
                    continue
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
            df_res.to_excel(writer, sheet_name=safe_sheet)
    print("交叉分析完成，图表和表格已保存。")


def correlation_analysis(df_label):
    print("\n开始相关性分析...")
    var_pairs = [(10, 5), (10, 6), (9, 7), (14, 17), (16, 28), (24, 23)]
    results = []
    for q1, q2 in var_pairs:
        info1 = COLUMN_MAPPING.get(q1)
        info2 = COLUMN_MAPPING.get(q2)
        if not info1 or not info2 or info1['type'] != 'single' or info2['type'] != 'single':
            continue
        col1 = info1['col'] + '_label'
        col2 = info2['col'] + '_label'
        if col1 not in df_label.columns or col2 not in df_label.columns:
            continue
        crosstab = pd.crosstab(df_label[col1], df_label[col2])
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


def text_analysis(df_label):
    print("\n开始文本分析...")
    col = COLUMN_MAPPING[30]['col']
    if col not in df_label.columns:
        print("未找到建议列，跳过文本分析")
        return
    texts = df_label[col].dropna().astype(str)
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
    plt.figure(figsize=(10, 5))
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


# ==================== 主程序 ====================
def main():
    print("=" * 50)
    print("影视行业调研分析脚本（最终版）")
    print("=" * 50)

    try:
        df_raw = load_raw_data()
    except Exception as e:
        print(f"加载数据时出错：{e}")
        return

    # 信度分析（指定组合）
    print("\n" + "=" * 50)
    print("第一部分：信度分析（指定组合）")
    print("=" * 50)
    reliability_analysis_combinations(df_raw)

    # 效度分析（可选，如需保留可取消注释）
    validity_analysis_immersion(df_raw)

    # 数据预处理
    df_label = preprocess_for_descriptive(df_raw)

    # 单变量图表（从新汇总表绘制）
    plot_univariate_from_summary()

    # 其他分析
    print("\n" + "=" * 50)
    print("第二部分：其他描述性统计分析")
    print("=" * 50)
    bivariate_analysis(df_label)
    correlation_analysis(df_label)
    text_analysis(df_label)

    print("\n" + "=" * 50)
    print("所有分析完成！结果保存在文件夹：", OUTPUT_DIR)
    print("=" * 50)


if __name__ == "__main__":
    main()