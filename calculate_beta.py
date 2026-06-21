#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算滚动100日Beta系数

Beta系数公式：
Beta = Cov(Ri, Rm) / Var(Rm)

其中：
- Ri 是个股的日回报率
- Rm 是市场（沪深300）的日回报率
"""

import pandas as pd
import numpy as np
from pathlib import Path


def calculate_rolling_beta():
    """
    计算滚动100日Beta系数
    """
    # 数据文件夹
    data_dir = Path("靶机数据")

    # 获取所有股票文件
    stock_files = sorted(data_dir.glob("*.xlsx"))

    # 过滤掉已经处理过的文件
    stock_files = [f for f in stock_files if '_' not in f.stem]

    print(f"找到 {len(stock_files)} 个股票数据文件")
    print("=" * 80)

    # 滚动窗口大小
    window = 100

    success_count = 0
    fail_count = 0

    for i, stock_file in enumerate(stock_files, 1):
        stock_code = stock_file.stem
        print(f"\n[{i}/{len(stock_files)}] 处理股票: {stock_code}")

        try:
            # 读取Excel文件
            df = pd.read_excel(stock_file, header=None)

            # 提取表头（前3行）
            header_df = df.iloc[:3].copy()

            # 提取数据行（从第4行开始）
            data_df = df.iloc[3:].copy()

            # 获取个股日回报率（列114）和沪深300涨跌幅（列38）
            stock_return = pd.to_numeric(data_df.iloc[:, 114], errors='coerce')
            market_return = pd.to_numeric(data_df.iloc[:, 38], errors='coerce') / 100  # 转换为小数形式

            # 计算滚动Beta系数
            # Beta = Cov(Ri, Rm) / Var(Rm)
            rolling_beta = []
            for j in range(len(data_df)):
                if j < window - 1:
                    # 窗口不足100天，Beta为NaN
                    rolling_beta.append(np.nan)
                else:
                    # 获取过去100天的数据
                    stock_window = stock_return.iloc[j - window + 1:j + 1]
                    market_window = market_return.iloc[j - window + 1:j + 1]

                    # 过滤掉NaN值
                    valid_mask = ~(stock_window.isna() | market_window.isna())
                    stock_valid = stock_window[valid_mask]
                    market_valid = market_window[valid_mask]

                    if len(stock_valid) >= 30 and market_valid.std() != 0:  # 至少需要30个有效数据点
                        # 计算协方差和方差
                        covariance = np.cov(stock_valid, market_valid)[0, 1]
                        market_variance = np.var(market_valid, ddof=0)
                        beta = covariance / market_variance
                        rolling_beta.append(beta)
                    else:
                        rolling_beta.append(np.nan)

            rolling_beta = pd.Series(rolling_beta)

            # 在表头添加新列
            new_col_beta = len(df.columns)
            header_df[new_col_beta] = ['Rolling_Beta_100d', '滚动100日Beta系数', '没有单位']

            # 在数据行中添加新列
            data_df[new_col_beta] = rolling_beta.values

            # 合并表头和数据
            final_df = pd.concat([header_df, data_df], ignore_index=True)

            # 保存回原文件
            final_df.to_excel(stock_file, index=False, header=False)

            # 计算统计信息
            valid_beta = rolling_beta.dropna()
            if len(valid_beta) > 0:
                print(f"  ✅ 计算完成")
                print(f"     Beta系数 - 均值: {valid_beta.mean():.4f}, 标准差: {valid_beta.std():.4f}")
                print(f"     有效数据点: {len(valid_beta)} / {len(rolling_beta)}")
                print(f"     最新Beta: {rolling_beta.iloc[-1]:.4f}" if not pd.isna(rolling_beta.iloc[-1]) else "     最新Beta: NaN")
            else:
                print(f"  ⚠️ 有效Beta数据不足")

            success_count += 1

        except Exception as e:
            print(f"  ❌ 处理失败: {str(e)}")
            fail_count += 1

    print("\n" + "=" * 80)
    print(f"处理完成！")
    print(f"  成功: {success_count}")
    print(f"  失败: {fail_count}")
    print("=" * 80)


if __name__ == "__main__":
    calculate_rolling_beta()