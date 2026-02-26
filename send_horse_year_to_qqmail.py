#!/usr/bin/env python3
"""
发送马年拜年邮件到allenliu0703@qq.com
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

def send_horse_year_to_qqmail():
    """发送马年拜年邮件到QQ邮箱"""
    print("=" * 60)
    print("🐎 发送马年拜年邮件到QQ邮箱")
    print("=" * 60)
    
    # 收件人信息
    to_email = "allenliu0703@qq.com"
    recipient_name = "Allen"
    
    print(f"📧 收件人: {to_email}")
    print(f"👤 收件人姓名: {recipient_name}")
    
    # 创建邮件发送器
    email_sender = QQMailSender()
    current_year = datetime.now().year
    
    # 创建邮件内容
    print("📝 创建邮件内容...")
    
    # 纯文本版本
    text_body = f"""🐎 马年大吉，新春快乐！ 🎉

亲爱的 Allen：

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
祝福语：祝Allen新的一年大吉大利！
发送到：您的QQ邮箱
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
            font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #fff9e6;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(210, 0, 0, 0.15);
            border: 3px solid #d40000;
        }}
        .header {{
            background: linear-gradient(135deg, #d40000 0%, #ff3333 100%);
            color: gold;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 36px;
            font-weight: bold;
        }}
        .header .subtitle {{
            margin-top: 10px;
            font-size: 18px;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .greeting {{
            font-size: 20px;
            color: #d40000;
            text-align: center;
            margin-bottom: 25px;
            padding: 15px;
            background-color: #fff0f0;
            border-radius: 10px;
        }}
        .blessing-section {{
            margin: 20px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            border-left: 5px solid #d40000;
        }}
        .blessing-section h2 {{
            color: #d40000;
            margin-top: 0;
            font-size: 24px;
        }}
        .horse-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 20px 0;
        }}
        .horse-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #ff9999;
        }}
        .horse-emoji {{
            font-size: 30px;
            margin-bottom: 10px;
        }}
        .horse-title {{
            color: #d40000;
            font-weight: bold;
            margin: 5px 0;
        }}
        .wish-list {{
            list-style: none;
            padding: 0;
        }}
        .wish-list li {{
            padding: 10px;
            margin: 8px 0;
            background-color: #fff9e6;
            border-radius: 8px;
            border-left: 4px solid #d40000;
        }}
        .final-blessing {{
            text-align: center;
            padding: 25px;
            background: linear-gradient(135deg, #d40000 0%, #ff3333 100%);
            color: gold;
            border-radius: 10px;
            margin: 25px 0;
        }}
        .final-blessing h2 {{
            margin: 0 0 15px 0;
            font-size: 28px;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 14px;
            border-top: 2px solid #ffcccc;
            background-color: #f9f9f9;
        }}
        .red-text {{
            color: #d40000;
            font-weight: bold;
        }}
        .gold-text {{
            color: gold;
            font-weight: bold;
        }}
        .qq-badge {{
            display: inline-block;
            background-color: #12B7F5;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐎 {current_year}马年大吉 🎉</h1>
            <div class="subtitle">新春快乐 · 万事如意 · 阖家幸福</div>
            <div class="qq-badge">📧 QQ邮箱专送</div>
        </div>
        
        <div class="content">
            <div class="greeting">
                亲爱的 <span class="red-text">Allen</span>：<br>
                值此{current_year}年新春佳节之际，谨向您致以最诚挚的祝福！
            </div>
            
            <div class="blessing-section">
                <h2>🐴 马年吉祥话</h2>
                <div class="horse-grid">
                    <div class="horse-card">
                        <div class="horse-emoji">🏇</div>
                        <div class="horse-title">一马当先</div>
                        <div>事业腾飞，领先一步</div>
                    </div>
                    <div class="horse-card">
                        <div class="horse-emoji">🐎</div>
                        <div class="horse-title">龙马精神</div>
                        <div>身体健康，精力充沛</div>
                    </div>
                    <div class="horse-card">
                        <div class="horse-emoji">🎯</div>
                        <div class="horse-title">马到成功</div>
                        <div>万事如意，心想事成</div>
                    </div>
                    <div class="horse-card">
                        <div class="horse-emoji">💰</div>
                        <div class="horse-title">金马送福</div>
                        <div>财源广进，富贵吉祥</div>
                    </div>
                </div>
            </div>
            
            <div class="blessing-section">
                <h2>🎊 新春祝福</h2>
                <p style="text-align: center; color: #d40000; font-size: 18px;">
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
                <h2>🎁 特别祝福</h2>
                <p>祝Allen在新的一年里：</p>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 15px 0;">
                    <div style="background: #e6f7ff; padding: 10px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 20px;">💼</div>
                        <div style="font-weight: bold;">工作顺利</div>
                        <div>升职加薪，事业有成</div>
                    </div>
                    <div style="background: #f6ffed; padding: 10px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 20px;">📚</div>
                        <div style="font-weight: bold;">学习进步</div>
                        <div>金榜题名，学业有成</div>
                    </div>
                    <div style="background: #fff0f6; padding: 10px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 20px;">❤️</div>
                        <div style="font-weight: bold;">爱情甜蜜</div>
                        <div>幸福美满，白头偕老</div>
                    </div>
                    <div style="background: #f9f0ff; padding: 10px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 20px;">🏠</div>
                        <div style="font-weight: bold;">家庭和睦</div>
                        <div>其乐融融，温馨幸福</div>
                    </div>
                </div>
            </div>
            
            <div class="final-blessing">
                <h2>🎉 最后祝福</h2>
                <p style="font-size: 20px;">马年行大运，万事皆如意！</p>
                <p style="font-size: 20px;">新春快乐，阖家幸福！</p>
                <p style="font-size: 24px; margin-top: 15px;">🐎🎊🏮✨</p>
            </div>
            
            <div style="text-align: center; margin: 20px 0; padding: 15px; background: #fff9e6; border-radius: 10px; border: 2px solid #ffcccc;">
                <p style="color: #d40000; font-size: 18px;">
                    <strong>🎯 特别祝福语：</strong><br>
                    <span style="font-size: 20px; color: #d40000;">祝Allen新的一年大吉大利！</span><br>
                    愿好运常伴，幸福永随！
                </p>
            </div>
            
            <div style="text-align: center; margin: 20px 0; padding: 15px; background: #e6f7ff; border-radius: 10px;">
                <p style="color: #1890ff;">
                    <strong>📧 邮件信息：</strong><br>
                    此邮件通过QQ邮箱SMTP系统发送<br>
                    发件人：OpenClaw助手<br>
                    收件人：您的QQ邮箱 ({to_email})
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>🎊 马年新春祝福邮件 🎊</strong></p>
            <p>此邮件由OpenClaw助手自动发送</p>
            <p>发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>祝福语：祝Allen新的一年大吉大利！</p>
            <p>发送方式：QQ邮箱SMTP系统</p>
            <p style="color: #999; font-size: 12px; margin-top: 15px;">
                注：本邮件为自动生成的祝福邮件，包含传统文化元素和美好祝愿。<br>
                愿这份祝福能为您的新年带来欢乐和好运！
            </p>
        </div>
    </div>
</body>
</html>"""
    
    # 邮件主题
    subject = f"🐎 {current_year}马年新春祝福 - 祝Allen新年大吉大利！"
    
    print(f"📋 邮件主题: {subject}")
    
    # 发送邮件
    print("📤 正在发送邮件...")
    success = email_sender.send(
        to_email=to_email,
        subject=subject,
        body=text_body,
        html_body=html_body
    )
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 马年拜年邮件发送成功！")
        print("=" * 60)
        print(f"📧 收件人: {to_email}")
        print(f"📋 主题: {subject}")
        print(f"⏰ 发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 祝福语: 祝Allen新的一年大吉大利！")
        print(f"📮 发送方式: QQ邮箱到QQ邮箱")
        print("\n🎉 邮件已成功发送到您的QQ邮箱！")
        return True
    else:
        print("\n❌ 邮件发送失败")
        return False

if __name__ == "__main__":
    send_horse_year_to_qqmail()