#!/usr/bin/env python3
"""
安霸（Ambarella）真实股票数据分析脚本
使用 Alpha Vantage API 和 Yahoo Finance API
"""

import os
import sys
import json
from datetime import datetime, timedelta
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd
import numpy as np

# 配置
ALPHA_VANTAGE_API_KEY = "RHSTH42HVC2YDMZB"
SYMBOL = "AMBA"
OUTPUT_DIR = "/home/allen/.openclaw/workspace/reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_yahoo_finance_data():
    """从 Yahoo Finance 获取数据"""
    print("📊 从 Yahoo Finance 获取安霸股票数据...")
    
    try:
        # 获取股票对象
        stock = yf.Ticker(SYMBOL)
        
        # 获取基本信息
        info = stock.info
        
        # 获取历史数据（最近30天）
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        hist = stock.history(start=start_date, end=end_date)
        
        # 获取当前数据
        current_data = stock.history(period="1d")
        
        yahoo_data = {
            "company_name": info.get("longName", "Ambarella, Inc."),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
            "previous_close": info.get("previousClose", 0),
            "open_price": info.get("open", 0),
            "day_high": info.get("dayHigh", 0),
            "day_low": info.get("dayLow", 0),
            "volume": info.get("volume", 0),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "52_week_high": info.get("fiftyTwoWeekHigh", 0),
            "52_week_low": info.get("fiftyTwoWeekLow", 0),
            "avg_volume": info.get("averageVolume", 0),
            "beta": info.get("beta", 0),
            "currency": info.get("currency", "USD"),
            "history": hist.tail(10).to_dict() if not hist.empty else {},
            "current_data": current_data.to_dict() if not current_data.empty else {}
        }
        
        print(f"✅ Yahoo Finance 数据获取成功")
        print(f"   当前价格: ${yahoo_data['current_price']:.2f}")
        print(f"   涨跌幅: {((yahoo_data['current_price'] - yahoo_data['previous_close']) / yahoo_data['previous_close'] * 100):.2f}%")
        
        return yahoo_data
        
    except Exception as e:
        print(f"❌ Yahoo Finance 数据获取失败: {e}")
        return None

def get_alpha_vantage_data():
    """从 Alpha Vantage 获取数据"""
    print("📈 从 Alpha Vantage 获取技术分析数据...")
    
    try:
        # 时间序列数据
        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        
        # 获取日线数据
        data, meta_data = ts.get_daily(symbol=SYMBOL, outputsize='compact')
        
        # 获取技术指标 - SMA
        from alpha_vantage.techindicators import TechIndicators
        ti = TechIndicators(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        
        # 获取移动平均线
        sma_20, _ = ti.get_sma(symbol=SYMBOL, interval='daily', time_period=20)
        sma_50, _ = ti.get_sma(symbol=SYMBOL, interval='daily', time_period=50)
        sma_200, _ = ti.get_sma(symbol=SYMBOL, interval='daily', time_period=200)
        
        # 获取RSI
        rsi, _ = ti.get_rsi(symbol=SYMBOL, interval='daily', time_period=14)
        
        alpha_data = {
            "latest_price": float(data.iloc[0]['4. close']),
            "latest_volume": int(data.iloc[0]['5. volume']),
            "latest_open": float(data.iloc[0]['1. open']),
            "latest_high": float(data.iloc[0]['2. high']),
            "latest_low": float(data.iloc[0]['3. low']),
            "sma_20": float(sma_20.iloc[0]['SMA']) if not sma_20.empty else 0,
            "sma_50": float(sma_50.iloc[0]['SMA']) if not sma_50.empty else 0,
            "sma_200": float(sma_200.iloc[0]['SMA']) if not sma_200.empty else 0,
            "rsi": float(rsi.iloc[0]['RSI']) if not rsi.empty else 50,
            "historical_data": data.head(10).to_dict()
        }
        
        print(f"✅ Alpha Vantage 数据获取成功")
        print(f"   SMA20: ${alpha_data['sma_20']:.2f}")
        print(f"   SMA50: ${alpha_data['sma_50']:.2f}")
        print(f"   RSI: {alpha_data['rsi']:.2f}")
        
        return alpha_data
        
    except Exception as e:
        print(f"❌ Alpha Vantage 数据获取失败: {e}")
        return None

def calculate_technical_levels(price_data):
    """计算技术分析水平"""
    if not price_data:
        return {}
    
    current_price = price_data.get("current_price", 0)
    
    # 计算支撑位和阻力位
    support_1 = current_price * 0.95  # -5%
    support_2 = current_price * 0.90  # -10%
    resistance_1 = current_price * 1.05  # +5%
    resistance_2 = current_price * 1.10  # +10%
    
    # 计算波动率
    volatility = abs(current_price - price_data.get("previous_close", current_price)) / current_price * 100
    
    return {
        "support_1": round(support_1, 2),
        "support_2": round(support_2, 2),
        "resistance_1": round(resistance_1, 2),
        "resistance_2": round(resistance_2, 2),
        "volatility": round(volatility, 2)
    }

def generate_trading_strategy(yahoo_data, alpha_data, tech_levels):
    """生成交易策略"""
    if not yahoo_data or not alpha_data:
        return "数据不足，无法生成策略"
    
    current_price = yahoo_data.get("current_price", 0)
    rsi = alpha_data.get("rsi", 50)
    sma_20 = alpha_data.get("sma_20", 0)
    sma_50 = alpha_data.get("sma_50", 0)
    
    # 分析市场情绪
    bias = "中性"
    action = "观望"
    reasoning = []
    
    # RSI分析
    if rsi > 70:
        bias = "超买"
        action = "考虑减仓或等待回调"
        reasoning.append("RSI超过70，显示超买状态")
    elif rsi < 30:
        bias = "超卖"
        action = "考虑逢低买入"
        reasoning.append("RSI低于30，显示超卖状态")
    else:
        bias = "中性"
        action = "区间交易"
        reasoning.append("RSI在正常范围内")
    
    # 移动平均线分析
    if current_price > sma_20 and current_price > sma_50:
        reasoning.append("股价在短期和中期均线之上，趋势偏多")
        if bias == "中性":
            bias = "偏多"
    elif current_price < sma_20 and current_price < sma_50:
        reasoning.append("股价在短期和中期均线之下，趋势偏空")
        if bias == "中性":
            bias = "偏空"
    
    # 成交量分析
    volume = yahoo_data.get("volume", 0)
    avg_volume = yahoo_data.get("avg_volume", volume)
    if volume > avg_volume * 1.5:
        reasoning.append("成交量显著放大，关注突破方向")
    
    return {
        "bias": bias,
        "action": action,
        "reasoning": reasoning,
        "stop_loss": round(tech_levels.get("support_2", current_price * 0.90), 2),
        "take_profit": round(tech_levels.get("resistance_1", current_price * 1.05), 2)
    }

def generate_report(yahoo_data, alpha_data, strategy):
    """生成报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = os.path.join(OUTPUT_DIR, f"ambarella_real_{today}.md")
    
    tech_levels = calculate_technical_levels(yahoo_data)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# Ambarella (AMBA) 真实数据股票分析 - {today}\n\n")
        f.write(f"**报告生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**时区:** Asia/Shanghai (GMT+8)\n")
        f.write(f"**数据来源:** Yahoo Finance + Alpha Vantage\n\n")
        
        f.write("## 📊 实时市场数据\n\n")
        
        if yahoo_data:
            price_change = ((yahoo_data['current_price'] - yahoo_data['previous_close']) / 
                           yahoo_data['previous_close'] * 100)
            change_symbol = "🟢" if price_change >= 0 else "🔴"
            
            f.write("| 指标 | 数值 | 变化 |\n")
            f.write("|------|------|------|\n")
            f.write(f"| **当前价格** | ${yahoo_data['current_price']:.2f} | {change_symbol} ${yahoo_data['current_price'] - yahoo_data['previous_close']:.2f} ({price_change:.2f}%) |\n")
            f.write(f"| **前收盘价** | ${yahoo_data['previous_close']:.2f} | — |\n")
            f.write(f"| **开盘价** | ${yahoo_data['open_price']:.2f} | — |\n")
            f.write(f"| **当日最高** | ${yahoo_data['day_high']:.2f} | — |\n")
            f.write(f"| **当日最低** | ${yahoo_data['day_low']:.2f} | — |\n")
            f.write(f"| **成交量** | {yahoo_data['volume']:,} | — |\n")
            f.write(f"| **平均成交量** | {yahoo_data['avg_volume']:,} | — |\n")
            f.write(f"| **市值** | ${yahoo_data['market_cap']/1e9:.2f}B | — |\n")
            f.write(f"| **市盈率(PE)** | {yahoo_data['pe_ratio']:.2f} | — |\n")
            f.write(f"| **52周最高** | ${yahoo_data['52_week_high']:.2f} | — |\n")
            f.write(f"| **52周最低** | ${yahoo_data['52_week_low']:.2f} | — |\n\n")
        
        f.write("## 📈 技术分析\n\n")
        
        if alpha_data:
            f.write("### 移动平均线\n")
            f.write(f"- **20日SMA:** ${alpha_data['sma_20']:.2f}\n")
            f.write(f"- **50日SMA:** ${alpha_data['sma_50']:.2f}\n")
            f.write(f"- **200日SMA:** ${alpha_data['sma_200']:.2f}\n\n")
            
            f.write("### 技术指标\n")
            f.write(f"- **RSI(14):** {alpha_data['rsi']:.2f} ")
            if alpha_data['rsi'] > 70:
                f.write("(超买)")
            elif alpha_data['rsi'] < 30:
                f.write("(超卖)")
            else:
                f.write("(中性)")
            f.write("\n\n")
        
        f.write("### 关键技术位\n")
        f.write(f"- **即时支撑位:** ${tech_levels.get('support_1', 0):.2f}\n")
        f.write(f"- **强支撑位:** ${tech_levels.get('support_2', 0):.2f}\n")
        f.write(f"- **即时阻力位:** ${tech_levels.get('resistance_1', 0):.2f}\n")
        f.write(f"- **强阻力位:** ${tech_levels.get('resistance_2', 0):.2f}\n")
        f.write(f"- **波动率:** {tech_levels.get('volatility', 0):.2f}%\n\n")
        
        f.write("## 🎯 交易策略\n\n")
        if strategy:
            f.write(f"### 市场偏向: **{strategy['bias']}**\n\n")
            f.write(f"### 操作建议: {strategy['action']}\n\n")
            f.write("### 分析依据:\n")
            for reason in strategy['reasoning']:
                f.write(f"- {reason}\n")
            f.write(f"\n### 风险管理:\n")
            f.write(f"- **止损位:** ${strategy['stop_loss']:.2f}\n")
            f.write(f"- **止盈位:** ${strategy['take_profit']:.2f}\n\n")
        
        f.write("## 🏢 公司基本面\n\n")
        if yahoo_data:
            f.write(f"**公司名称:** {yahoo_data.get('company_name', 'Ambarella, Inc.')}\n")
            f.write(f"**行业:** 半导体/计算机视觉\n")
            f.write(f"**Beta系数:** {yahoo_data.get('beta', 'N/A')}\n")
            f.write(f"**股息率:** {yahoo_data.get('dividend_yield', 0)*100:.2f}%\n\n")
        
        f.write("## ⚠️ 风险提示\n\n")
        f.write("1. **市场风险:** 股票市场具有波动性，价格可能快速变化\n")
        f.write("2. **行业风险:** 半导体行业受全球经济周期影响较大\n")
        f.write("3. **公司风险:** 技术竞争激烈，研发投入压力大\n")
        f.write("4. **流动性风险:** 成交量不足时可能影响交易执行\n\n")
        
        f.write("---\n\n")
        f.write("**免责声明:** 本报告基于公开数据生成，仅供参考，不构成投资建议。投资有风险，入市需谨慎。\n")
        f.write(f"*数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    print(f"✅ 报告已生成: {report_file}")
    return report_file

def main():
    """主函数"""
    print("=" * 60)
    print("安霸（AMBA）真实股票数据分析系统")
    print("=" * 60)
    
    # 获取数据
    yahoo_data = get_yahoo_finance_data()
    alpha_data = get_alpha_vantage_data()
    
    if not yahoo_data and not alpha_data:
        print("❌ 无法获取任何数据，请检查网络连接和API配置")
        return
    
    # 生成交易策略
    strategy = generate_trading_strategy(yahoo_data, alpha_data, {})
    
    # 生成报告
    report_file = generate_report(yahoo_data, alpha_data, strategy)
    
    # 显示摘要
    print("\n" + "=" * 60)
    print("📋 分析摘要")
    print("=" * 60)
    
    if yahoo_data:
        price_change = ((yahoo_data['current_price'] - yahoo_data['previous_close']) / 
                       yahoo_data['previous_close'] * 100)
        print(f"💰 当前价格: ${yahoo_data['current_price']:.2f} ({price_change:+.2f}%)")
    
    if strategy:
        print(f"🎯 市场偏向: {strategy['bias']}")
        print(f"📝 操作建议: {strategy['action']}")
    
    print(f"📄 详细报告: {report_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()