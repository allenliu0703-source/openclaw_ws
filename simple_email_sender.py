#!/usr/bin/env python3
"""
简单邮件发送脚本 - OpenClaw邮件技能
支持：文本邮件、HTML邮件、附件、多收件人
"""

import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from datetime import datetime
from pathlib import Path

class EmailConfig:
    """邮件配置类"""
    
    CONFIG_FILE = os.path.expanduser("~/.openclaw/email_config.json")
    
    @classmethod
    def load_config(cls):
        """加载邮件配置"""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认配置模板
        default_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "your_email@gmail.com",
            "password": "",  # 使用应用专用密码
            "use_tls": True,
            "sender_name": "OpenClaw助手",
            "default_recipient": "your_email@gmail.com"
        }
        
        # 保存默认配置
        cls.save_config(default_config)
        return default_config
    
    @classmethod
    def save_config(cls, config):
        """保存邮件配置"""
        os.makedirs(os.path.dirname(cls.CONFIG_FILE), exist_ok=True)
        with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置已保存到: {cls.CONFIG_FILE}")
    
    @classmethod
    def update_config(cls, **kwargs):
        """更新配置"""
        config = cls.load_config()
        config.update(kwargs)
        cls.save_config(config)
        return config

class EmailSender:
    """邮件发送器"""
    
    def __init__(self, config=None):
        self.config = config or EmailConfig.load_config()
    
    def create_message(self, to_email, subject, body, html_body=None, attachments=None):
        """创建邮件消息"""
        # 创建多部分消息
        if html_body or attachments:
            msg = MIMEMultipart('mixed' if attachments else 'alternative')
        else:
            msg = MIMEMultipart()
        
        # 设置邮件头
        sender_name = self.config.get('sender_name', 'OpenClaw助手')
        msg['From'] = f"{Header(sender_name, 'utf-8').encode()} <{self.config['username']}>"
        
        # 处理收件人（支持多个）
        if isinstance(to_email, list):
            msg['To'] = ', '.join(to_email)
        else:
            msg['To'] = to_email
        
        msg['Subject'] = Header(subject, 'utf-8')
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # 添加正文
        if html_body:
            # 添加HTML版本
            html_part = MIMEText(html_body, 'html', 'utf-8')
            if attachments:
                # 如果有附件，需要嵌套
                alternative = MIMEMultipart('alternative')
                alternative.attach(MIMEText(body, 'plain', 'utf-8'))
                alternative.attach(html_part)
                msg.attach(alternative)
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
                msg.attach(html_part)
        else:
            # 只有纯文本
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
        
        # 添加附件
        if attachments:
            for attachment in attachments:
                if isinstance(attachment, str):
                    filepath = attachment
                    filename = os.path.basename(filepath)
                else:
                    filepath, filename = attachment
                
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        attachment_part = MIMEApplication(f.read(), Name=filename)
                    
                    attachment_part['Content-Disposition'] = f'attachment; filename="{filename}"'
                    msg.attach(attachment_part)
                    print(f"📎 已添加附件: {filename}")
                else:
                    print(f"⚠️  附件不存在: {filepath}")
        
        return msg
    
    def send(self, to_email, subject, body, html_body=None, attachments=None):
        """发送邮件"""
        try:
            # 创建邮件
            msg = self.create_message(to_email, subject, body, html_body, attachments)
            
            # 连接SMTP服务器
            print(f"🔗 连接SMTP服务器: {self.config['smtp_server']}:{self.config['smtp_port']}")
            
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.set_debuglevel(1)  # 启用调试信息
                
                # TLS加密
                if self.config.get('use_tls', True):
                    print("🔒 启用TLS加密...")
                    server.starttls()
                
                # 登录
                print(f"🔑 登录邮箱: {self.config['username']}")
                server.login(self.config['username'], self.config['password'])
                
                # 发送邮件
                recipients = to_email if isinstance(to_email, list) else [to_email]
                server.send_message(msg)
                
                print(f"✅ 邮件发送成功！")
                print(f"   收件人: {', '.join(recipients)}")
                print(f"   主题: {subject}")
                if attachments:
                    print(f"   附件: {len(attachments)}个")
                
                return True
                
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            print("\n💡 可能的原因：")
            print("1. 用户名或密码错误")
            print("2. SMTP服务器地址或端口错误")
            print("3. 未开启SMTP服务（需要到邮箱设置中开启）")
            print("4. 需要应用专用密码（如Gmail）")
            print("5. 网络连接问题")
            return False
    
    def send_test_email(self):
        """发送测试邮件"""
        test_subject = "📧 OpenClaw邮件系统测试"
        test_body = """这是一封测试邮件，来自OpenClaw邮件系统。

如果收到此邮件，说明邮件配置成功！

发送时间：{time}

配置信息：
- SMTP服务器：{server}:{port}
- 发件人：{sender}

下一步：
1. 确认收到此邮件
2. 根据需要调整配置
3. 开始使用邮件功能

祝使用愉快！
OpenClaw助手
""".format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            server=self.config['smtp_server'],
            port=self.config['smtp_port'],
            sender=self.config['username']
        )
        
        test_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OpenClaw邮件测试</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #4CAF50; color: white; padding: 10px; text-align: center; }
        .content { padding: 20px; background-color: #f9f9f9; }
        .footer { margin-top: 20px; padding: 10px; text-align: center; color: #666; font-size: 12px; }
        .success { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 OpenClaw邮件系统测试</h1>
        </div>
        <div class="content">
            <p class="success">✅ 邮件发送成功！</p>
            <p>这是一封测试邮件，来自OpenClaw邮件系统。</p>
            <p>如果收到此邮件，说明邮件配置成功！</p>
            
            <h3>发送信息：</h3>
            <ul>
                <li><strong>时间：</strong>{time}</li>
                <li><strong>SMTP服务器：</strong>{server}:{port}</li>
                <li><strong>发件人：</strong>{sender}</li>
            </ul>
            
            <h3>下一步：</h3>
            <ol>
                <li>确认收到此邮件</li>
                <li>根据需要调整配置</li>
                <li>开始使用邮件功能</li>
            </ol>
        </div>
        <div class="footer">
            <p>OpenClaw助手 · {time}</p>
        </div>
    </div>
</body>
</html>""".format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            server=self.config['smtp_server'],
            port=self.config['smtp_port'],
            sender=self.config['username']
        )
        
        # 发送给自己
        recipient = self.config.get('default_recipient', self.config['username'])
        return self.send(recipient, test_subject, test_body, test_html)

def setup_wizard():
    """配置向导"""
    print("=" * 60)
    print("📧 OpenClaw邮件系统配置向导")
    print("=" * 60)
    
    config = EmailConfig.load_config()
    
    print("\n当前配置：")
    for key, value in config.items():
        if key == 'password' and value:
            print(f"  {key}: {'*' * len(value)}")
        else:
            print(f"  {key}: {value}")
    
    print("\n请选择邮箱服务商：")
    print("1. Gmail (推荐)")
    print("2. QQ邮箱")
    print("3. 163/126邮箱")
    print("4. Outlook/Hotmail")
    print("5. 其他")
    
    choice = input("\n请输入选择 (1-5): ").strip()
    
    smtp_configs = {
        '1': {'server': 'smtp.gmail.com', 'port': 587, 'note': '需要应用专用密码'},
        '2': {'server': 'smtp.qq.com', 'port': 587, 'note': '需要授权码'},
        '3': {'server': 'smtp.163.com', 'port': 25, 'note': '或端口465/587'},
        '4': {'server': 'smtp.office365.com', 'port': 587, 'note': '或smtp-mail.outlook.com'},
        '5': {'server': '', 'port': 587, 'note': '请手动输入SMTP服务器'}
    }
    
    if choice in smtp_configs:
        smtp_info = smtp_configs[choice]
        if choice == '5':
            smtp_info['server'] = input("请输入SMTP服务器地址: ").strip()
            smtp_info['port'] = int(input("请输入端口号 (默认587): ") or "587")
        
        config['smtp_server'] = smtp_info['server']
        config['smtp_port'] = smtp_info['port']
        
        print(f"\n✅ 已设置SMTP服务器: {smtp_info['server']}:{smtp_info['port']}")
        print(f"   提示: {smtp_info['note']}")
    
    # 更新其他配置
    config['username'] = input(f"\n请输入邮箱地址 (当前: {config['username']}): ").strip() or config['username']
    config['password'] = input(f"请输入密码/授权码 (当前: {'*' * len(config['password']) if config['password'] else '空'}): ").strip() or config['password']
    config['sender_name'] = input(f"请输入发件人名称 (当前: {config['sender_name']}): ").strip() or config['sender_name']
    config['default_recipient'] = input(f"请输入默认收件人 (当前: {config['default_recipient']}): ").strip() or config['default_recipient']
    
    # 保存配置
    EmailConfig.save_config(config)
    
    print("\n✅ 配置完成！")
    print("下一步：发送测试邮件验证配置")
    
    test = input("\n是否发送测试邮件？ (y/n): ").strip().lower()
    if test == 'y':
        sender = EmailSender(config)
        sender.send_test_email()
    
    return config

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'setup':
            setup_wizard()
        
        elif command == 'test':
            sender = EmailSender()
            sender.send_test_email()
        
        elif command == 'send':
            if len(sys.argv) < 4:
                print("用法: python simple_email_sender.py send <收件人> <主题> [正文文件]")
                return
            
            to_email = sys.argv[2]
            subject = sys.argv[3]
            body = sys.argv[4] if len(sys.argv) > 4 else "这是一封来自OpenClaw的邮件。"
            
            # 如果body是文件路径，读取文件内容
            if os.path.exists(body):
                with open(body, 'r', encoding='utf-8') as f:
                    body = f.read()
            
            sender = EmailSender()
            sender.send(to_email, subject, body)
        
        elif command == 'config':
            config = EmailConfig.load_config()
            print(json.dumps(config, indent=2, ensure_ascii=False))
        
        else:
            print(f"未知命令: {command}")
            print("\n可用命令:")
            print("  setup    - 运行配置向导")
            print("  test     - 发送测试邮件")
            print("  send     - 发送邮件")
            print("  config   - 查看当前配置")
    
    else:
        # 交互模式
        print("📧 OpenClaw邮件发送系统")
        print("=" * 40)
        
        config = EmailConfig.load_config()
        
        print("\n请选择操作:")
        print("1. 运行配置向导")
        print("2. 发送测试邮件")
        print("3. 发送自定义邮件")
        print("4. 查看当前配置")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            setup_wizard()
        elif choice == '2':
            sender = EmailSender()
            sender.send_test_email()
        elif choice == '3':
            to_email = input("收件人邮箱: ").strip()
            subject = input("邮件主题: ").strip()
            print("邮件正文 (输入空行结束):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            body = "\n".join(lines)
            
            sender = EmailSender()
            sender.send(to_email, subject, body)
        elif choice == '4':
            config = EmailConfig.load_config()
            print("\n当前配置:")
            for key, value in config.items():
                if key == 'password' and value:
                    print(f"  {key}: {'*' * len(value)}")
                else:
                    print(f"  {key}: {value}")
        elif choice == '5':
            print("再见！")
        else:
            print("无效选择")

if __name__ == "__main__":
    main()