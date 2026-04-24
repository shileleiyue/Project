# -*- coding: utf-8 -*-
"""
信效度分析独立脚本
对推荐的5个题目进行信度分析（Cronbach's α）和效度分析（探索性因子分析）
依赖库: pandas, numpy, openpyxl, pingouin, factor-analyzer
安装命令: pip install pandas numpy openpyxl pingouin factor-analyzer
"""
import os
import pandas as pd
import numpy as np
import pingouin as pg
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity

# ==================== 配置区（请根据实际文件修改）====================
DATA_FILE = "350881459_按序号_关于影视行业环境与观众沉浸体验研究的详细问卷_274_274.xlsx"
OUTPUT_DIR = "信效度分析结果"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 题目列名（请根据实际列名调整，特别注意全角/半角引号）
COL_Q7 = '7. 在观看长视频时，您使用“倍速播放”功能的频率是：'
COL_Q9 = '9. 您是否经常在观看视频的同时进行“多任务处理”（如回消息、刷社交软件、玩游戏等）？'
COL_Q10 = '10. 您认为自己的“注意力持续时间”在过去3年内有何变化？'
COL_Q21 = '21. 您认为“沉浸式体验”对于长视频的未来重要吗？'
COL_Q24 = '24. 您是否愿意为获得更好的沉浸体验而付费（如购买更高码流、解锁导演剪辑版、体验互动剧情等）？'

# ==================== 数据加载 ====================
def load_data(filepath):
    """加载Excel数据，并打印列名供核对"""
    if not os.path.exists(filepath):
        print(f"错误：文件 {filepath} 不存在！")
        return None
    df = pd.read_excel(filepath)
    print(f"数据加载成功，共 {len(df)} 行，{len(df.columns)} 列")
    print("\n数据列名如下：")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
    return df

def check_columns(df, required_cols):
    """检查所需列是否存在，若缺失则提示"""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print("\n错误：以下列不存在，请检查列名中的引号是全角还是半角：")
        for col in missing:
            print(f"  {col}")
        print("\n请根据上面打印的列名列表修改代码中的 COL_xxx 变量。")
        return False
    return True

# ==================== 信度分析 ====================
def reliability_analysis(df):
    print("\n" + "="*50)
    print("开始信度分析")
    print("="*50)
    required = [COL_Q7, COL_Q9, COL_Q10, COL_Q21, COL_Q24]
    if not check_columns(df, required):
        return

    # 提取数据并反向编码
    data = pd.DataFrame()
    # Q7: 1->5, 2->4, 3->3, 4->2, 5->1
    data['Q7'] = df[COL_Q7].map({1:5, 2:4, 3:3, 4:2, 5:1})
    # Q9: 1->5, 2->4, 3->3, 4->2, 5->1
    data['Q9'] = df[COL_Q9].map({1:5, 2:4, 3:3, 4:2, 5:1})
    # Q10: 正向，无需反向
    data['Q10'] = df[COL_Q10].copy()
    # Q21: 1->4, 2->3, 3->2, 4->1
    data['Q21'] = df[COL_Q21].map({1:4, 2:3, 3:2, 4:1})
    # Q24: 1->4, 2->3, 3->2, 4->1
    data['Q24'] = df[COL_Q24].map({1:4, 2:3, 3:2, 4:1})

    # 删除缺失值
    before = len(data)
    data = data.dropna()
    after = len(data)
    print(f"删除缺失值前样本量: {before}，删除后: {after}")

    if len(data) < 3:
        print("有效样本量不足，无法进行信度分析。")
        return

    # 计算Cronbach's α
    alpha = pg.cronbach_alpha(data)[0]
    print(f"\nCronbach's α = {alpha:.3f}")
    if alpha >= 0.9:
        print("信度非常好")
    elif alpha >= 0.8:
        print("信度较好")
    elif alpha >= 0.7:
        print("信度可接受")
    else:
        print("信度较低，题目可能需要调整")

    # 保存结果
    result = pd.DataFrame({'Cronbach_alpha': [alpha]})
    out_path = os.path.join(OUTPUT_DIR, "信度分析结果.xlsx")
    result.to_excel(out_path, index=False)
    print(f"结果已保存至: {out_path}")

# ==================== 效度分析 ====================
def validity_analysis(df):
    print("\n" + "="*50)
    print("开始效度分析（探索性因子分析）")
    print("="*50)
    required = [COL_Q7, COL_Q9, COL_Q10, COL_Q21, COL_Q24]
    if not check_columns(df, required):
        return

    data = pd.DataFrame()
    data['Q7'] = df[COL_Q7].map({1:5, 2:4, 3:3, 4:2, 5:1})
    data['Q9'] = df[COL_Q9].map({1:5, 2:4, 3:3, 4:2, 5:1})
    data['Q10'] = df[COL_Q10].copy()
    data['Q21'] = df[COL_Q21].map({1:4, 2:3, 3:2, 4:1})
    data['Q24'] = df[COL_Q24].map({1:4, 2:3, 3:2, 4:1})
    data = data.dropna()
    print(f"用于效度分析的有效样本量: {len(data)}")

    if len(data) < 5:
        print("样本量不足，无法进行因子分析。")
        return

    # KMO和Bartlett检验
    try:
        kmo_all, kmo = calculate_kmo(data)
        print(f"KMO = {kmo:.3f}")
        if kmo < 0.6:
            print("KMO值偏低，数据可能不适合因子分析")
        chi2, p = calculate_bartlett_sphericity(data)
        print(f"Bartlett's test: chi2={chi2:.2f}, p={p:.4f}")
        if p < 0.05:
            print("Bartlett检验显著，适合因子分析")
        else:
            print("Bartlett检验不显著，数据可能不适合因子分析")
    except Exception as e:
        print(f"KMO/Bartlett检验出错: {e}")
        return

    # 计算特征值
    fa = FactorAnalyzer(n_factors=5, rotation=None)
    fa.fit(data)
    ev, _ = fa.get_eigenvalues()
    ev = ev[0]  # 第一个矩阵为特征值
    print("\n特征值:")
    for i, val in enumerate(ev):
        print(f"Factor {i+1}: {val:.3f}")

    # 选择特征值>1的因子
    n_factors = sum(ev > 1)
    print(f"\n特征值>1的因子数: {n_factors}")
    if n_factors == 0:
        print("没有特征值>1的因子，无法提取因子。")
        return

    # 进行因子分析，使用varimax旋转
    fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
    fa.fit(data)
    loadings = fa.loadings_
    variance = fa.get_factor_variance()

    # 输出因子载荷
    print("\n因子载荷矩阵（旋转后）：")
    loadings_df = pd.DataFrame(loadings, index=data.columns, columns=[f'Factor{i+1}' for i in range(n_factors)])
    print(loadings_df.round(3))

    # 输出方差解释
    print("\n方差解释：")
    var_df = pd.DataFrame(variance, index=['SS Loadings', 'Proportion Var', 'Cumulative Var'],
                          columns=[f'Factor{i+1}' for i in range(n_factors)]).T
    print(var_df.round(3))

    # 保存结果
    out_path = os.path.join(OUTPUT_DIR, "效度分析结果.xlsx")
    with pd.ExcelWriter(out_path) as writer:
        loadings_df.to_excel(writer, sheet_name='因子载荷')
        var_df.to_excel(writer, sheet_name='方差解释')
        pd.DataFrame({'KMO': [kmo], 'Bartlett_chi2': [chi2], 'Bartlett_p': [p]}).to_excel(writer, sheet_name='检验结果')
    print(f"\n结果已保存至: {out_path}")

# ==================== 主程序 ====================
if __name__ == "__main__":
    print("="*50)
    print("信效度分析脚本启动")
    print("="*50)

    df = load_data(DATA_FILE)
    if df is None:
        exit()

    reliability_analysis(df)
    validity_analysis(df)

    print("\n所有分析完成！")