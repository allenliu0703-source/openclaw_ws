#!/usr/bin/env python3
"""
发送马年拜年邮件
"""

import os
import sys
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from qqmail_smtp_config import QQMailSender, QQMailConfig
except ImportError:
    print("❌ 无法导入QQ邮箱模块")
    sys.exit(1)

class HorseYearEmailSender:
    """马年拜年邮件发送器"""
    
    def __init__(self, email_sender=None):
        self.email_sender = email_sender or QQMailSender()
        
    def create_horse_year_email(self, recipient_name="Allen"):
        """创建马年拜年邮件内容"""
        current_year = datetime.now().year
        chinese_zodiac = "马"  # 马年
        
        # 纯文本版本
        text_body = f"""🐎 马年大吉，新春快乐！ 🎉

亲爱的 {recipient_name}：

值此{current_year}年新春佳节之际，谨向您致以最诚挚的祝福！

🐴 **马年吉祥话**：
一马当先，事业腾飞！
龙马精神，身体健康！
马到成功，万事如意！
金马送福，财源广进！

🎊 **新春祝福**：
愿您在新的一年里：
1. 事业如骏马奔腾，一往无前
2. 健康如千里马，活力无限
3. 财运如天马行空，源源不断
4. 家庭如马厩温馨，幸福美满
5. 友情如万马奔腾，热闹非凡

🌟 **马年特色**：
马象征着力量、速度和成功。在马年：
- 像骏马一样勇往直前，追逐梦想
- 像战马一样坚韧不拔，克服困难
- 像千里马一样才华横溢，展现自我
- 像宝马一样珍贵稀有，珍惜拥有

📅 **新春时节**：
春节是阖家团圆的日子，也是新的开始。
愿您扫去旧年的尘埃，迎接新年的阳光。
愿您放下过去的烦恼，拥抱未来的希望。

🎁 **特别祝福**：
祝您在新的一年里：
- 工作顺利，升职加薪
- 学习进步，金榜题名
- 爱情甜蜜，幸福美满
- 家庭和睦，其乐融融
- 朋友众多，欢乐常在

🏮 **传统习俗**：
记得：
- 贴春联，迎福气
- 放鞭炮，驱邪气
- 吃饺子，聚财气
- 拜大年，收红包
- 看春晚，享欢乐

最后，再次祝福您：
**马年行大运，万事皆如意！
新春快乐，阖家幸福！**

🐎🎉🎊🏮✨

---
此邮件由OpenClaw助手自动发送
发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
祝福来自：您的朋友
"""
        
        # HTML版本
        html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐎 {current_year}马年新春祝福</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'SimHei', 'STHeiti', sans-serif;
            line-height: 1.8;
            color: #333;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #fff9e6 0%, #ffe6e6 100%);
            background-attachment: fixed;
        }}
        .container {{
            max-width: 700px;
            margin: 30px auto;
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 50px rgba(210, 0, 0, 0.2);
            border: 5px solid #d40000;
            position: relative;
        }}
        .red-envelope {{
            position: absolute;
            top: -30px;
            right: -30px;
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #d40000 0%, #ff3333 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: gold;
            font-size: 40px;
            transform: rotate(15deg);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            z-index: 10;
        }}
        .header {{
            background: linear-gradient(135deg, #d40000 0%, #ff6b6b 100%);
            color: gold;
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: "🐎";
            font-size: 100px;
            position: absolute;
            top: 10px;
            left: 20px;
            opacity: 0.2;
            transform: rotate(-15deg);
        }}
        .header::after {{
            content: "🎉";
            font-size: 100px;
            position: absolute;
            bottom: 10px;
            right: 20px;
            opacity: 0.2;
            transform: rotate(15deg);
        }}
        .header h1 {{
            margin: 0;
            font-size: 42px;
            font-weight: bold;
            text-shadow: 3px 3px 5px rgba(0,0,0,0.3);
            position: relative;
            z-index: 2;
        }}
        .header .subtitle {{
            margin-top: 15px;
            font-size: 22px;
            opacity: 0.9;
            position: relative;
            z-index: 2;
        }}
        .content {{
            padding: 40px;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="%23fff9e6"/><path d="M20,20 L80,80 M80,20 L20,80" stroke="%23ffcccc" stroke-width="1" opacity="0.1"/></svg>');
        }}
        .greeting {{
            font-size: 24px;
            color: #d40000;
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #fff9e6 0%, #ffe6e6 100%);
            border-radius: 15px;
            border-left: 8px solid #d40000;
            border-right: 8px solid #d40000;
        }}
        .blessing-section {{
            margin: 30px 0;
            padding: 25px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(210, 0, 0, 0.1);
            border: 2px solid #ffcccc;
        }}
        .blessing-section h2 {{
            color: #d40000;
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 3px solid gold;
            font-size: 28px;
            display: flex;
            align-items: center;
        }}
        .blessing-section h2::before {{
            content: "🎊";
            margin-right: 10px;
            font-size: 24px;
        }}
        .horse-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}
        .horse-card {{
            background: linear-gradient(135deg, #fff9e6 0%, #ffe6e6 100%);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid #ff9999;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .horse-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(210, 0, 0, 0.2);
        }}
        .horse-emoji {{
            font-size: 40px;
            margin-bottom: 15px;
        }}
        .horse-title {{
            color: #d40000;
            font-size: 20px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .horse-desc {{
            color: #666;
            font-size: 16px;
            line-height: 1.6;
        }}
        .wish-list {{
            list-style: none;
            padding: 0;
        }}
        .wish-list li {{
            padding: 12px 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #fff9e6 0%, #ffe6e6 100%);
            border-radius: 10px;
            border-left: 5px solid #d40000;
            font-size: 18px;
            display: flex;
            align-items: center;
        }}
        .wish-list li::before {{
            content: "✓";
            color: #d40000;
            font-weight: bold;
            margin-right: 15px;
            font-size: 20px;
        }}
        .tradition-section {{
            background: linear-gradient(135deg, #fff9e6 0%, #e6f7ff 100%);
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
            border: 2px dashed #d40000;
        }}
        .tradition-section h3 {{
            color: #d40000;
            text-align: center;
            font-size: 24px;
            margin-top: 0;
        }}
        .tradition-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .tradition-item {{
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
        .tradition-emoji {{
            font-size: 30px;
            margin-bottom: 10px;
        }}
        .tradition-name {{
            color: #d40000;
            font-weight: bold;
            margin: 5px 0;
        }}
        .tradition-desc {{
            color: #666;
            font-size: 14px;
        }}
        .final-blessing {{
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #d40000 0%, #ff3333 100%);
            color: gold;
            border-radius: 15px;
            margin: 30px 0;
        }}
        .final-blessing h2 {{
            margin: 0 0 15px 0;
            font-size: 32px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .final-blessing p {{
            margin: 10px 0;
            font-size: 20px;
            opacity: 0.9;
        }}
        .footer {{
            text-align: center;
            padding: 25px;
            color: #666;
            font-size: 14px;
            border-top: 3px solid #ffcccc;
            background: #fff9e6;
        }}
        .fireworks {{
            position: absolute;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }}
        .firework {{
            position: absolute;
            width: 5px;
            height: 5px;
            background: gold;
            border-radius: 50%;
            animation: firework 2s infinite;
        }}
        @keyframes firework {{
            0% {{ transform: translateY(100px) scale(0); opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ transform: translateY(-100px) scale(1.5); opacity: 0; }}
        }}
        .gold-text {{
            color: gold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: bold;
        }}
        .red-text {{
            color: #d40000;
            font-weight: bold;
        }}
        .highlight {{
            background: linear-gradient(135deg, gold 0%, #ffd700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="red-envelope">🧧</div>
        
        <div class="header">
            <h1>🐎 {current_year}马年大吉 🎉</h1>
            <div class="subtitle">新春快乐 · 万事如意 · 阖家幸福</div>
        </div>
        
        <div class="content">
            <div class="greeting">
                亲爱的 <span class="highlight">{recipient_name}</span>：<br>
                值此{current_year}年新春佳节之际，谨向您致以最诚挚的祝福！
            </div>
            
            <div class="blessing-section">
                <h2>🐴 马年吉祥话</h2>
                <div class="horse-grid">
                    <div class="horse-card">
                        <div class="horse-emoji">🏇</div>
                        <div class="horse-title">一马当先</div>
                        <div class="horse-desc">事业腾飞，领先一步</div>
                    </div>
                    <div class="horse-card">
                        <div class="horse-emoji">🐎</div>
                        <div class="horse-title">龙马精神</div>
                        <div class="horse-desc">身体健康，精力充沛</div>
                    </div>
                    <div class="horse-card">
                        <div class="horse-emoji">🎯</div>
                        <div class="horse-title">马到成功</div>
                        <div class="horse-desc">万事如意，心想事成</div>
                    </div>
                    <div class="horse-card">
                        <div class="horse-emoji">💰</div>
                        <div class="horse-title">金马送福</div>
                        <div class="horse-desc">财源广进，富贵吉祥</div>
                    </div>
                </div>
            </div>
            
            <div class="blessing-section">
                <h2>🎊 新春祝福</h2>
                <p style="font-size: 20px; color: #d40000; text-align: center; margin: 20px 0;">
                    愿您在新的一年里：
                </p>
                <ul class="wish-list">
                    <li>事业如骏马奔腾，一往无前</li>
                    <li>健康如千里马，活力无限</li>
                    <li>财运如天马行空，源源不断</li>
                    <li>家庭如马厩温馨，幸福美满</li>
                    <li>友情如万马奔腾，热闹非凡</li>
                </ul>
            </div>
            
            <div class="blessing-section">
                <h2>🌟 马年特色</h2>
                <p style="font-size: 18px; line-height: 1.8; color: #555;">
                    马象征着<span class="red-text">力量、速度和成功</span>。在马年：
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
                    <div style="text-align: center; padding: 15px; background: #fff9e6; border-radius: 10px;">
                        <div style="font-size: 30px;">🏃</div>
                        <div style="color: #d40000; font-weight: bold; margin: 10px 0;">像骏马一样</div>
                        <div>勇往直前，追逐梦想</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #fff9e6; border-radius: 10px;">
                        <div style="font-size: 30px;">💪</div>
                        <div style="color: #d40000; font-weight: bold; margin: 10px 0;">像战马一样</div>
                        <div>坚韧不拔，克服困难</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #fff9e6; border-radius: 10px;">
                        <div style="font-size: 30px;">🎓</div>
                        <div style="color: #d40000; font-weight: bold; margin: 10px 0;">像千里马一样</div>
                        <div>才华横溢，展现自我</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: #fff9e6; border-radius: 10px;">
                        <