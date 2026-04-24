import matplotlib.pyplot as plt
import numpy as np
import re

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# 总人数
total = 274

# 定义所有问题的数据
questions = [
    {
        'num': 1,
        'title': '您的年龄段',
        'options': ['18岁以下', '18-25岁', '26-35岁', '36-45岁', '46-55岁', '56岁及以上'],
        'counts': [57, 76, 56, 45, 22, 18],
        'multiple': False
    },
    {
        'num': 2,
        'title': '您目前从事的行业/身份',
        'options': ['学生', '互联网/科技行业', '文化传媒/影视行业', '金融/商业', '教育/科研', '自由职业', '其他'],
        'counts': [61, 68, 51, 46, 23, 25, 0],
        'multiple': False
    },
    {
        'num': 3,
        'title': '您平均每月在影视内容上的消费金额',
        'options': ['0元', '1-30元', '31-50元', '51-100元', '100元以上'],
        'counts': [28, 91, 72, 57, 26],
        'multiple': False
    },
    {
        'num': 4,
        'title': '您通常通过哪些设备观看影视内容? (可多选)',
        'options': ['智能手机', '平板电脑', '笔记本电脑', '台式电脑', '智能电视/投影仪', 'VR设备', '其他'],
        'counts': [70, 93, 90, 115, 109, 67, 0],
        'multiple': True
    },
    {
        'num': 5,
        'title': '您平均每天花费在短视频平台上的总时长',
        'options': ['少于30分钟', '30分钟-1小时', '1-2小时', '2-3小时', '3小时以上'],
        'counts': [30, 90, 71, 56, 27],
        'multiple': False
    },
    {
        'num': 6,
        'title': '您平均每天花费在长视频平台上的总时长',
        'options': ['少于30分钟', '30分钟-1小时', '1-2小时', '2-3小时', '3小时以上'],
        'counts': [30, 31, 91, 67, 55],
        'multiple': False
    },
    {
        'num': 7,
        'title': '在观看长视频时，您使用"倍速播放"功能的频率是',
        'options': ['几乎总是使用', '经常使用', '偶尔使用', '很少使用', '从不使用'],
        'counts': [34, 29, 65, 52, 94],
        'multiple': False
    },
    {
        'num': 8,
        'title': '在观看一集45分钟左右的剧集时，您通常如何处理?',
        'options': ['一次性专注看完', '分2-3次看完', '边看边做其他事', '后台播放', '其他'],
        'counts': [108, 75, 61, 30, 0],
        'multiple': False
    },
    {
        'num': 9,
        'title': '您是否经常在观看视频的同时进行"多任务处理"?',
        'options': ['总是如此', '经常如此', '有时如此', '很少如此', '从不如此'],
        'counts': [33, 93, 65, 55, 28],
        'multiple': False
    },
    {
        'num': 10,
        'title': '您认为自己的"注意力持续时间"在过去3年内有何变化?',
        'options': ['明显变短了', '略有变短', '基本没变', '变得更长了'],
        'counts': [103, 85, 57, 29],
        'multiple': False
    },
    {
        'num': 11,
        'title': '导致您无法沉浸观看长视频的主要外部干扰因素是? (多选)',
        'options': ['手机应用的通知提醒', '工作/学习事务的插入', '家庭/社交环境的干扰',
                    '其他娱乐内容的诱惑', '算法推荐的其他内容预览', '其他'],
        'counts': [81, 107, 109, 121, 134, 0],
        'multiple': True
    },
    {
        'num': 12,
        'title': '导致您无法沉浸观看长视频的主要内容内部因素是? (多选)',
        'options': ['剧情拖沓、节奏缓慢', '情节逻辑漏洞或槽点多', '演技或制作粗糙',
                    '广告插入频繁', '题材或风格不感兴趣', '其他'],
        'counts': [71, 98, 113, 115, 139, 0],
        'multiple': True
    },
    {
        'num': 13,
        'title': '在什么情况下，您最可能获得一次沉浸式的观看体验? (多选)',
        'options': ['深夜或独处时', '影院观影', '使用高质量视听设备时',
                    '内容本身极其吸引人', '与志同道合者一起观看讨论', '其他'],
        'counts': [87, 96, 116, 112, 129, 0],
        'multiple': True
    },
    {
        'num': 14,
        'title': '您是否听说过或关注"影视寒冬"这一说法?',
        'options': ['非常了解', '大致了解', '仅听说过', '完全没听说过'],
        'counts': [105, 85, 58, 26],
        'multiple': False
    },
    {
        'num': 15,
        'title': '您认为"影视寒冬"最直接的表现是什么? (多选)',
        'options': ['新开机的大制作项目减少', '平台和片方更谨慎，不敢冒险',
                    '演员、从业者工作机会变少', '同质化、保守的续集/IP剧增多',
                    '微短剧、小程序剧等"轻量"内容爆发', '观众可选择的优质新作变少', '其他'],
        'counts': [65, 83, 95, 107, 121, 54, 0],
        'multiple': True
    },
    {
        'num': 16,
        'title': '在您看来，"影视寒冬"与"注意力碎片化"之间是否存在关联?',
        'options': ['有强关联', '有一定关联', '关联不大', '不清楚'],
        'counts': [103, 88, 54, 29],
        'multiple': False
    },
    {
        'num': 17,
        'title': '"影视寒冬"下，您感觉影视内容的整体质量如何变化?',
        'options': ['明显下降', '略有下降', '基本持平', '有所提升', '两极分化更严重'],
        'counts': [29, 92, 69, 56, 28],
        'multiple': False
    },
    {
        'num': 18,
        'title': '最近一年，您完整看完的剧集平均有多少集?',
        'options': ['少于10集', '10-20集', '21-30集', '31-40集', '40集以上'],
        'counts': [29, 32, 90, 68, 55],
        'multiple': False
    },
    {
        'num': 19,
        'title': '最近一年，您弃剧的主要原因是什么? (多选)',
        'options': ['剧情注水，失去追看动力', '更新周期长，忘了或失去兴趣',
                    '时间不允许，无法持续跟进', '被其他新内容吸引',
                    '口碑崩塌或剧透影响', '其他'],
        'counts': [84, 98, 101, 120, 144, 0],
        'multiple': True
    },
    {
        'num': 20,
        'title': '您认为"影视寒冬"对您的个人观看习惯产生了什么影响? (多选)',
        'options': ['转向观看更多短视频', '更依赖口碑和评分选择长视频',
                    '降低了对新作的期待值', '更愿意重温经典老剧/电影',
                    '开始观看更多海外内容', '无明显影响', '其他'],
        'counts': [71, 101, 105, 114, 146, 0, 0],
        'multiple': True
    },
    {
        'num': 21,
        'title': '您认为"沉浸式体验"对于长视频的未来重要吗?',
        'options': ['至关重要', '比较重要', '一般', '不重要'],
        'counts': [104, 92, 48, 30],
        'multiple': False
    },
    {
        'num': 22,
        'title': '一个能让您沉浸的剧集/电影，最核心的吸引点是什么?',
        'options': ['极致抓人的故事与悬念', '深刻的情感共鸣与人物弧光',
                    '宏大/新颖的世界观与视觉奇观', '精妙的叙事结构与艺术表达',
                    '真实的社会洞察与议题探讨'],
        'counts': [31, 94, 64, 56, 29],
        'multiple': False
    },
    {
        'num': 23,
        'title': '以下哪些技术或形式，最能提升您的沉浸感? (多选)',
        'options': ['4K', 'HDR/杜比视界/全景声', '互动叙事', 'VR/AR/XR体验',
                    '模拟影院效果的云影院', '伴随式创作解说', '其他'],
        'counts': [72, 91, 102, 108, 116, 50, 0],
        'multiple': True
    },
    {
        'num': 24,
        'title': '您是否愿意为获得更好的沉浸体验而付费?',
        'options': ['愿意', '可能愿意', '不愿意', '坚决反对'],
        'counts': [32, 132, 85, 25],
        'multiple': False
    },
    {
        'num': 25,
        'title': '您认为"沉浸感"的营造，主要责任在于?',
        'options': ['内容创作者', '制作方', '播放平台', '观众自身', '多方协同'],
        'counts': [33, 88, 71, 55, 27],
        'multiple': False
    },
    {
        'num': 26,
        'title': '在内容形式上，您认为以下哪种探索对长视频的未来更有意义? (多选)',
        'options': ['更精炼的短剧集', '单片付费的网络电影', '系列化季播精品剧',
                    '融合游戏化元素的互动影集', '基于VR/元宇宙的叙事体验', '其他'],
        'counts': [56, 49, 87, 104, 108, 0],
        'multiple': True
    },
    {
        'num': 27,
        'title': '平台可以采取哪些措施来帮助用户更好地沉浸? (多选)',
        'options': ['提供专注模式', '优化算法减少干扰', '设立精品剧场',
                    '强化社交功能', '提供灵活观看计划', '其他'],
        'counts': [80, 85, 117, 123, 141, 0],
        'multiple': True
    },
    {
        'num': 28,
        'title': '长视频的"沉浸体验"与短视频的"碎片化消费"会是怎样的关系?',
        'options': ['对抗关系', '互补关系', '融合关系', '其他'],
        'counts': [140, 104, 30, 0],
        'multiple': False
    },
    {
        'num': 29,
        'title': '整体上，您对国产长视频内容的未来持何种态度?',
        'options': ['乐观', '谨慎乐观', '中性', '悲观', '不关心'],
        'counts': [27, 97, 64, 59, 27],
        'multiple': False
    }
]

def safe_filename(s):
    return re.sub(r'[\\/*?:"<>|]','_',s)

# 为每个问题生成水平条形图
for q in questions:
    fig, ax = plt.subplots(figsize=(10, max(6, len(q['options']) * 0.5)))
    y_pos = np.arange(len(q['options']))

    bars = ax.barh(y_pos, q['counts'], color='skyblue', edgecolor='grey')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(q['options'], fontsize=10)
    ax.invert_yaxis()  # 让第一个选项在顶部
    ax.set_xlabel('选择人数', fontsize=12)
    ax.set_title(f'Q{q["num"]}. {q["title"]} (总人数={total})', fontsize=14, fontweight='bold')

    # 在条形上添加数值和百分比
    for i, (count, bar) in enumerate(zip(q['counts'], bars)):
        if count > 0:
            percentage = count / total * 100
            if q['multiple']:
                # 多选题百分比基于总人数
                text = f'{count} ({percentage:.1f}%)'
            else:
                text = f'{count} ({percentage:.1f}%)'
            ax.text(count + 1, bar.get_y() + bar.get_height() / 2, text,
                    va='center', ha='left', fontsize=9)

    # 调整x轴范围留出空间给文字
    max_count = max(q['counts'])
    ax.set_xlim(0, max_count * 1.15 if max_count > 0 else 10)


    safe_title = safe_filename(q["title"][:20])
    plt.savefig(f'Q{q["num"]:02d}_{safe_title}.png', dpi=150)
    plt.close()

print("所有图表已生成！")