# -*- coding: utf-8 -*-
"""
KMO和Bartlett检验 - 逐题删除分析
功能：
1. 对指定的一组单选题计算KMO和Bartlett球形度检验。
2. 分别删除每个题目，对剩余题目重复上述检验。
3. 汇总每次分析的关键指标，并保存为Excel文件。
"""

import os
import pandas as pd
import numpy as np
from factor_analyzer import calculate_kmo, calculate_bartlett_sphericity

# ==================== 配置 ====================
DATA_FILE = "350881459_按序号_关于影视行业环境与观众沉浸体验研究的详细问卷_274_274.xlsx"
OUTPUT_DIR = "分析结果"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 指定要分析的题目 ====================
QUESTIONS = [5, 8, 10, 14, 16, 21, 29]

# ==================== 列名映射 ====================
COLUMN_MAPPING = {
    1: '1. 您的年龄段：',
    2: '2. 您目前从事的行业/身份：',
    3: '3. 您平均每月在影视内容（包括会员、点播等）上的消费金额约为：',
    4: '4. 您通常通过哪些设备观看影视内容？（可多选）(智能手机)',
    5: '5. 您平均每天花费在短视频平台（如抖音、快手、视频号等）上的总时长约为：',
    6: '6. 您平均每天花费在长视频平台（如爱优腾芒、B站长内容、Netflix等）上的总时长约为：',
    7: '7. 在观看长视频时，您使用“倍速播放”功能的频率是：',
    8: '8. 在观看一集45分钟左右的剧集时，您通常如何处理？',
    9: '9. 您是否经常在观看视频的同时进行“多任务处理”（如回消息、刷社交软件、玩游戏等）？',
    10: '10. 您认为自己的“注意力持续时间”在过去3年内有何变化？',
    14: '14. 您是否听说过或关注“影视寒冬”这一说法？',
    16: '16. 在您看来，“影视寒冬”与“注意力碎片化”之间是否存在关联？',
    17: '17. “影视寒冬”下，您感觉影视内容的整体质量如何变化？',
    18: '18. 最近一年，您完整看完（未弃剧）的剧集（单部）平均有多少集？',
    21: '21. 您认为“沉浸式体验”对于长视频的未来重要吗？',
    24: '24. 您是否愿意为获得更好的沉浸体验而付费（如购买更高码流、解锁导演剪辑版、体验互动剧情等）？',
    29: '29. 整体上，您对国产长视频内容的未来持何种态度？',
}

# ==================== 加载数据 ====================
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")
    df = pd.read_excel(file_path)
    print(f"数据加载成功，共 {len(df)} 行，{len(df.columns)} 列")
    return df

# ==================== 单次KMO和Bartlett检验 ====================
def kmo_bartlett(data, analysis_name="当前分析"):
    """
    对输入数据data（DataFrame）进行KMO和Bartlett检验，返回指标字典。
    若失败则返回None。
    """
    data_clean = data.dropna()
    n = len(data_clean)
    p = data_clean.shape[1]

    print(f"\n【{analysis_name}】")
    print(f"  有效样本量: {n}, 变量数: {p}")

    if n < 5 or p < 2:
        print("  样本量或变量数不足，跳过")
        return None

    # 检查常数列
    stds = data_clean.std()
    if (stds == 0).any():
        zero_vars = stds[stds == 0].index.tolist()
        print(f"  警告：以下变量为常数：{zero_vars}，跳过")
        return None

    try:
        kmo_all, kmo = calculate_kmo(data_clean)
        chi2, p_value = calculate_bartlett_sphericity(data_clean)
        dof = p * (p - 1) // 2
    except Exception as e:
        print(f"  检验出错：{e}")
        return None

    result = {
        '分析名称': analysis_name,
        '状态': '成功',
        '变量数': p,
        '有效样本量': n,
        'KMO': round(kmo, 4),
        'Bartlett卡方': round(chi2, 4),
        'Bartlett自由度': dof,
        'Bartlett p值': p_value,
    }
    return result

# ==================== 逐题删除分析 ====================
def delete_one_analysis(df, questions):
    # 获取实际列名
    col_names = {}
    available_questions = []
    for q in questions:
        col = COLUMN_MAPPING.get(q)
        if col is None:
            print(f"警告：题号 {q} 未在COLUMN_MAPPING中定义，跳过")
            continue
        if col not in df.columns:
            print(f"警告：列 '{col}' 不存在，跳过")
            continue
        col_names[q] = col
        available_questions.append(q)

    if not available_questions:
        print("错误：没有可用的题目")
        return None

    print(f"\n将分析的题目：{available_questions}")

    # 全量分析
    results = []
    full_data = df[[col_names[q] for q in available_questions]].copy()
    full_res = kmo_bartlett(full_data, "全量分析")
    if full_res:
        results.append(full_res)
    else:
        results.append({'分析名称': '全量分析', '状态': '失败', '变量数': len(available_questions)})

    # 逐个删除
    for del_q in available_questions:
        remaining_q = [q for q in available_questions if q != del_q]
        remaining_data = df[[col_names[q] for q in remaining_q]].copy()
        res = kmo_bartlett(remaining_data, f"删除Q{del_q}")
        if res:
            results.append(res)
        else:
            results.append({'分析名称': f"删除Q{del_q}", '状态': '失败', '变量数': len(remaining_q)})

    return pd.DataFrame(results).fillna('')

# ==================== 主程序 ====================
def main():
    print("="*60)
    print("KMO和Bartlett检验 - 逐题删除分析")
    print("="*60)

    try:
        df = load_data(DATA_FILE)
    except Exception as e:
        print(f"加载数据失败：{e}")
        return

    results_df = delete_one_analysis(df, QUESTIONS)
    if results_df is None:
        return

    # 打印汇总结果
    print("\n" + "="*60)
    print("分析结果汇总")
    print("="*60)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)
    print(results_df.to_string(index=False))

    # 保存Excel
    out_file = os.path.join(OUTPUT_DIR, "KMO_Bartlett_逐题删除结果.xlsx")
    results_df.to_excel(out_file, index=False)
    print(f"\n结果已保存至：{out_file}")

if __name__ == "__main__":
    main()