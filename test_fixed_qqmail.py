#!/usr/bin/env python3
"""
修复后的QQ邮箱测试脚本
"""

import smtplib
import ssl
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from datetime import datetime

def test_fixed_smtp():
    """测试修复后的SMTP发送"""
    config_file = os.path.expanduser('~/.openclaw/qqmail_config.json')
    
    if not os.path.exists(config_file):
        print("❌ 配置文件不存在")
        return False
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 60)
    print("🔧 测试修复后的QQ邮箱SMTP")
    print("=" * 60)
    
    email = config.get('email', '')
    password = config.get('password', '')
    display_name = config.get('display_name', 'OpenClaw助手')
    smtp_server = "smtp.qq.com"
    smtp_port = config.get('smtp_port', 587)
    
    print(f"发件人: {display_name} <{email}>")
    print(f"收件人: {email} (发送给自己)")
    print(f"SMTP服务器: {smtp_server}:{smtp_port}")
    
    try:
        # 1. 创建邮件
        print("\n1. 创建邮件...")
        msg = MIMEMultipart('alternative')
        
        # 设置邮件头
        msg['From'] = formataddr((str(Header(display_name, 'utf-8')), email))
        msg['To'] = email
        msg['Subject'] = Header('📧 修复测试邮件', 'utf-8')
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # 纯文本版本
        text_content = """这是一封修复测试邮件。

如果收到此邮件，说明QQ邮箱SMTP配置已修复成功！

发送信息：
- 时间：{time}
- 发件人：{sender}
- 收件人：{recipient}

修复的问题：
1. 邮件创建逻辑错误
2. From字段格式问题
3. 编码处理优化

祝使用愉快！
OpenClaw助手
""".format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            sender=email,
            recipient=email
        )
        
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # HTML版本
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>修复测试邮件</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .success {{ color: #4CAF50; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 修复测试邮件</h1>
        </div>
        <div class="content">
            <p class="success">✅ QQ邮箱SMTP配置已修复成功！</p>
            <p>如果收到此邮件，说明所有问题已解决。</p>
            
            <h3>发送信息：</h3>
            <ul>
                <li><strong>时间：</strong>{time}</li>
                <li><strong>发件人：</strong>{sender}</li>
                <li><strong>收件人：</strong>{recipient}</li>
            </ul>
            
            <h3>修复的问题：</h3>
            <ol>
                <li>邮件创建逻辑错误</li>
                <li>From字段格式问题</li>
                <li>编码处理优化</li>
            </ol>
            
            <p>现在可以正常使用QQ邮箱SMTP功能了！</p>
        </div>
    </div>
</body>
</html>""".format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            sender=email,
            recipient=email
        )
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        print("   ✅ 邮件创建成功")
        
        # 2. 连接SMTP服务器
        print("\n2. 连接SMTP服务器...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.set_debuglevel(1)  # 显示基本调试信息
        
        print("   启动STARTTLS...")
        server.starttls()
        
        # 3. 登录
        print("\n3. 登录邮箱...")
        server.login(email, password)
        print("   ✅ 登录成功")
        
        # 4. 发送邮件
        print("\n4. 发送邮件...")
        server.send_message(msg)
        print("   ✅ 邮件发送成功")
        
        # 5. 退出
        server.quit()
        print("\n🎉 所有测试通过！邮件已发送到您的QQ邮箱")
        
        # 更新配置
        config['last_test'] = datetime.now().isoformat()
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ 认证失败: {e}")
        print("\n请检查：")
        print("1. 是否使用QQ邮箱授权码（不是登录密码）")
        print("2. 授权码是否正确（16位字符）")
        print("3. 是否在QQ邮箱中开启了SMTP服务")
        return False
        
    except Exception as e:
        print(f"\n❌ 发送失败: {type(e).__name__}: {e}")
        return False

def check_email_format():
    """检查邮件格式"""
    config_file = os.path.expanduser('~/.openclaw/qqmail_config.json')
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    email = config.get('email', '')
    
    print("\n" + "=" * 60)
    print("📋 邮件格式检查")
    print("=" * 60)
    
    print(f"邮箱地址: {email}")
    
    if not email:
        print("❌ 邮箱地址为空")
        return False
    
    if '@qq.com' not in email:
        print("⚠️  不是QQ邮箱地址")
    
    # 测试formataddr
    from_name = config.get('display_name', 'Test')
    formatted = formataddr((str(Header(from_name, 'utf-8')), email))
    print(f"格式化发件人: {formatted}")
    
    return True

def main():
    """主函数"""
    print("🔧 QQ邮箱SMTP修复测试")
    print("=" * 60)
    
    # 检查配置文件
    config_file = os.path.expanduser('~/.openclaw/qqmail_config.json')
    if not os.path.exists(config_file):
        print("❌ 配置文件不存在")
        print("请先运行: python3 qqmail_smtp_config.py setup")
        return
    
    # 检查邮件格式
    check_email_format()
    
    # 运行测试
    print("\n" + "=" * 60)
    success = test_fixed_smtp()
    
    if success:
        print("\n✅ 修复成功！")
        print("现在可以正常使用：")
        print("1. python3 qqmail_smtp_config.py test")
        print("2. python3 qqmail_stock_report.py daily")
    else:
        print("\n❌ 测试失败，请检查以上错误信息")

if __name__ == "__main__":
    main()