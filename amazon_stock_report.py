#!/usr/bin/env python3
"""
Amazon股票每日报告 - 发送到邮箱
"""

import os
import sys
import json
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
except ImportError:
    print("❌ 需要安装requests库")
    sys.exit(1)

# ==================== 配置 ====================
ALPHA_VANTAGE_API_KEY = "RHSTH42HVC2YDMZB"
STOCK_SYMBOL = "AMZN"

# QQ邮箱配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
FROM_EMAIL = "allenliu0703@qq.com"
FROM_NAME = "Openclaw Assistant"
# 使用QQ邮箱授权码
AUTH_CODE = "ehpjiaterlinedfc"  # 16位授权码

# 收件人
TO_EMAIL = "allenliu0703@qq.com"

# ==================== 股票数据获取 ====================

def get_amazon_quote():
    """获取Amazon股票实时报价"""
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": STOCK_SYMBOL,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            return {
                "symbol": quote.get("01. symbol", "N/A"),
                "price": float(quote.get("05. price", 0)),
                "open": float(quote.get("02. open", 0)),
                "high": float(quote.get("03. high", 0)),
                "low": float(quote.get("04. low", 0)),
                "volume": int(quote.get("06. volume", 0)),
                "previous_close": float(quote.get("08. previous close", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": quote.get("10. change percent", "N/A"),
                "latest_day": quote.get("07. latest trading day", "N/A")
            }
    except Exception as e:
        print(f"❌ 获取股票数据失败: {e}")
    
    return None

def get_company_overview():
    """获取Amazon公司概况"""
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": STOCK_SYMBOL,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data:
            return {
                "name": data.get("Name", "Amazon.com Inc."),
                "description": data.get("Description", "N/A")[:300] + "...",
                "sector": data.get("Sector", "N/A"),
                "industry": data.get("Industry", "N/A"),
                "market_cap": data.get("MarketCapitalization", "N/A"),
                "pe_ratio": data.get("PERatio", "N/A"),
                "dividend_yield": data.get("DividendYield", "N/A"),
                "eps": data.get("EPS", "N/A"),
                "beta": data.get("Beta", "N/A"),
                "52_week_high": data.get("52WeekHigh", "N/A"),
                "52_week_low": data.get("52WeekLow", "N/A")
            }
    except Exception as e:
        print(f"⚠️ 获取公司概况失败: {e}")
    
    return None

# ==================== 邮件发送 ====================

def send_email(quote_data, overview_data):
    """发送股票报告邮件"""
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg['To'] = TO_EMAIL
    msg['Subject'] = f"📈 Amazon ({STOCK_SYMBOL}) 每日股票报告 - {datetime.datetime.now().strftime('%Y-%m-%d')}"
    
    # 提取数据
    price = quote_data.get('price', 0)
    change = quote_data.get('change', 0)
    change_percent = quote_data.get('change_percent', '0%')
    prev_close = quote_data.get('previous_close', 0)
    
    # 颜色和emoji
    if change >= 0:
        color = "#4CAF50"
        emoji = "📈"
        trend = "上涨"
    else:
        color = "#F44336"
        emoji = "📉"
        trend = "下跌"
    
    # 纯文本版本
    text_body = f"""Amazon ({STOCK_SYMBOL}) 每日股票报告
=====================================

当前价格: ${price:.2f} {emoji}
涨跌: ${change:.2f} ({change_percent}) {trend}
昨日收盘: ${prev_close:.2f}
今日开盘: ${quote_data.get('open', 0):.2f}
今日最高: ${quote_data.get('high', 0):.2f}
今日最低: ${quote_data.get('low', 0):.2f}
成交量: {quote_data.get('volume', 0):,}

52周最高: ${overview_data.get('52_week_high', 'N/A')}
52周最低: ${overview_data.get('52_week_low', 'N/A')}
市盈率: {overview_data.get('pe_ratio', 'N/A')}
市值: ${overview_data.get('market_cap', 'N/A')}

公司: {overview_data.get('name', 'Amazon.com Inc.')}
行业: {overview_data.get('industry', 'N/A')}

报告生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # HTML版本
    html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Amazon股票每日报告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #FF9900 0%, #FFB84D 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .price-section {{ background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center; }}
        .price {{ font-size: 36px; font-weight: bold; color: #333; }}
        .change {{ font-size: 18px; margin-top: 10px; }}
        .positive {{ color: #4CAF50; }}
        .negative {{ color: #F44336; }}
        .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 20px 0; }}
        .stat-box {{ background: white; padding: 15px; border-radius: 8px; border: 1px solid #eee; }}
        .stat-label {{ font-size: 12px; color: #666; }}
        .stat-value {{ font-size: 16px; font-weight: bold; color: #333; }}
        .info-section {{ background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .info-section h3 {{ margin-top: 0; color: #FF9900; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }}
        .badge {{ display: inline-block; background: #FF9900; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Amazon ({STOCK_SYMBOL}) 每日股票报告</h1>
        <div class="badge">每日自动推送</div>
    </div>
    
    <div class="price-section">
        <div class="price">${price:.2f}</div>
        <div class="change {'positive' if change >= 0 else 'negative'}">
            {emoji} ${change:+.2f} ({change_percent}) {trend}
        </div>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-label">昨日收盘</div>
            <div class="stat-value">${prev_close:.2f}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">今日开盘</div>
            <div class="stat-value">${quote_data.get('open', 0):.2f}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">今日最高</div>
            <div class="stat-value">${quote_data.get('high', 0):.2f}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">今日最低</div>
            <div class="stat-value">${quote_data.get('low', 0):.2f}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">成交量</div>
            <div class="stat-value">{quote_data.get('volume', 0):,}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">交易日</div>
            <div class="stat-value">{quote_data.get('latest_day', 'N/A')}</div>
        </div>
    </div>
    
    <div class="info-section">
        <h3>🏢 公司概况</h3>
        <p><strong>公司名称:</strong> {overview_data.get('name', 'Amazon.com Inc.')}</p>
        <p><strong>所属行业:</strong> {overview_data.get('industry', 'N/A')}</p>
        <p><strong>市值:</strong> ${overview_data.get('market_cap', 'N/A')}</p>
        <p><strong>市盈率:</strong> {overview_data.get('pe_ratio', 'N/A')}</p>
        <p><strong>52周最高:</strong> ${overview_data.get('52_week_high', 'N/A')}</p>
        <p><strong>52周最低:</strong> ${overview_data.get('52_week_low', 'N/A')}</p>
    </div>
    
    <div class="footer">
        <p>📧 本报告由OpenClaw助手自动生成</p>
        <p>⏰ 报告时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>📈 数据来源: Alpha Vantage API</p>
    </div>
</body>
</html>"""
    
    # 添加内容
    msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    # 发送邮件
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, AUTH_CODE)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")
        return False

# ==================== 主程序 ====================

def main():
    print("=" * 60)
    print("📈 Amazon股票每日报告")
    print("=" * 60)
    
    # 获取股票数据
    print("\n📊 正在获取Amazon股票数据...")
    quote_data = get_amazon_quote()
    
    if not quote_data:
        print("❌ 无法获取股票数据")
        sys.exit(1)
    
    print(f"✅ 获取成功!")
    print(f"   股票代码: {quote_data['symbol']}")
    print(f"   当前价格: ${quote_data['price']:.2f}")
    print(f"   涨跌: ${quote_data['change']:.2f} ({quote_data['change_percent']})")
    
    # 获取公司概况
    print("\n📋 正在获取公司概况...")
    overview_data = get_company_overview()
    
    if overview_data:
        print(f"   公司名称: {overview_data.get('name', 'N/A')}")
        print(f"   市值: ${overview_data.get('market_cap', 'N/A')}")
    else:
        overview_data = {
            "name": "Amazon.com Inc.",
            "industry": "N/A",
            "market_cap": "N/A",
            "pe_ratio": "N/A",
            "52_week_high": "N/A",
            "52_week_low": "N/A"
        }
    
    # 发送邮件
    print(f"\n📧 正在发送邮件到 {TO_EMAIL}...")
    
    if len(sys.argv) > 1 and sys.argv[1] == "send":
        success = send_email(quote_data, overview_data)
        if success:
            print("\n" + "=" * 60)
            print("✅ 邮件发送成功!")
            print("=" * 60)
        else:
            print("\n❌ 邮件发送失败")
            sys.exit(1)
    else:
        # 只显示数据，不发送
        print("\n📝 使用 'send' 参数发送邮件")
        print(f"   示例: python3 {sys.argv[0]} send")

if __name__ == "__main__":
    main()