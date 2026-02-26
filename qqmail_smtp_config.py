#!/usr/bin/env python3
"""
QQ邮箱SMTP配置和邮件发送脚本
使用Python标准库：smtplib, email, imaplib
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr
import ssl
import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
import getpass

class QQMailConfig:
    """QQ邮箱配置类"""
    
    # QQ邮箱SMTP/IMAP服务器配置
    SMTP_SERVER = "smtp.qq.com"
    SMTP_PORT = 587  # 或 465 (SSL)
    IMAP_SERVER = "imap.qq.com"
    IMAP_PORT = 993  # SSL
    
    CONFIG_FILE = os.path.expanduser("~/.openclaw/qqmail_config.json")
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """获取默认配置模板"""
        return {
            "email": "",  # QQ邮箱地址，如：123456789@qq.com
            "password": "",  # 授权码（不是登录密码！）
            "display_name": "OpenClaw助手",
            "use_ssl": True,
            "smtp_port": cls.SMTP_PORT,
            "imap_port": cls.IMAP_PORT,
            "signature": "来自OpenClaw助手的邮件",
            "last_test": None
        }
    
    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """加载配置"""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  读取配置文件失败: {e}")
        
        return cls.get_default_config()
    
    @classmethod
    def save_config(cls, config: Dict[str, Any]) -> None:
        """保存配置"""
        os.makedirs(os.path.dirname(cls.CONFIG_FILE), exist_ok=True)
        with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False, default=str)
        print(f"✅ 配置已保存到: {cls.CONFIG_FILE}")
    
    @classmethod
    def interactive_setup(cls) -> Dict[str, Any]:
        """交互式配置向导"""
        print("=" * 60)
        print("📧 QQ邮箱SMTP配置向导")
        print("=" * 60)
        print("\n重要提示：")
        print("1. 需要使用QQ邮箱授权码，不是登录密码！")
        print("2. 获取授权码：登录QQ邮箱 → 设置 → 账户 → POP3/IMAP/SMTP服务")
        print("3. 开启服务：IMAP/SMTP服务")
        print("=" * 60)
        
        config = cls.load_config()
        
        # 获取QQ邮箱地址
        while True:
            email_addr = input(f"\n请输入QQ邮箱地址 (当前: {config['email'] or '未设置'}): ").strip()
            if email_addr:
                if '@qq.com' in email_addr:
                    config['email'] = email_addr
                    break
                else:
                    print("❌ 请输入正确的QQ邮箱地址（包含@qq.com）")
            elif config['email']:
                break
            else:
                print("❌ 邮箱地址不能为空")
        
        # 获取授权码
        print(f"\n⚠️  注意：需要QQ邮箱授权码，不是登录密码！")
        print("   获取方法：QQ邮箱 → 设置 → 账户 → 开启IMAP/SMTP服务 → 生成授权码")
        password = getpass.getpass(f"请输入授权码 (当前: {'*' * len(config['password']) if config['password'] else '未设置'}): ")
        if password:
            config['password'] = password
        
        # 发件人名称
        display_name = input(f"\n请输入发件人显示名称 (当前: {config['display_name']}): ").strip()
        if display_name:
            config['display_name'] = display_name
        
        # 签名
        signature = input(f"\n请输入邮件签名 (当前: {config['signature']}): ").strip()
        if signature:
            config['signature'] = signature
        
        # 保存配置
        cls.save_config(config)
        
        print("\n✅ 配置完成！")
        print(f"   邮箱: {config['email']}")
        print(f"   发件人: {config['display_name']}")
        print(f"   SMTP服务器: {cls.SMTP_SERVER}:{config['smtp_port']}")
        print(f"   IMAP服务器: {cls.IMAP_SERVER}:{config['imap_port']}")
        
        return config

class QQMailSender:
    """QQ邮箱发送器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or QQMailConfig.load_config()
        self.smtp_server = QQMailConfig.SMTP_SERVER
        self.smtp_port = self.config.get('smtp_port', QQMailConfig.SMTP_PORT)
        self.use_ssl = self.config.get('use_ssl', True)
    
    def create_message(self, 
                      to_email: str, 
                      subject: str, 
                      body: str, 
                      html_body: Optional[str] = None,
                      attachments: Optional[List[str]] = None) -> MIMEMultipart:
        """创建邮件消息"""
        # 创建邮件
        if html_body or attachments:
            msg = MIMEMultipart('mixed' if attachments else 'alternative')
        else:
            msg = MIMEMultipart()
        
        # 设置发件人
        from_name = self.config.get('display_name', 'OpenClaw助手')
        from_email = self.config['email']
        msg['From'] = formataddr((str(Header(from_name, 'utf-8')), from_email))
        
        # 设置收件人
        msg['To'] = to_email
        
        # 设置主题
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 设置日期
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # 添加正文
        if html_body:
            # 创建alternative部分
            alternative = MIMEMultipart('alternative')
            
            # 添加纯文本版本
            text_part = MIMEText(body, 'plain', 'utf-8')
            alternative.attach(text_part)
            
            # 添加HTML版本
            html_part = MIMEText(html_body, 'html', 'utf-8')
            alternative.attach(html_part)
            
            # 将alternative添加到主消息
            msg.attach(alternative)
        else:
            # 只有纯文本
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
        
        # 添加附件
        if attachments:
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    filename = os.path.basename(attachment_path)
                    
                    with open(attachment_path, 'rb') as f:
                        attachment = MIMEApplication(f.read(), Name=filename)
                    
                    attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
                    msg.attach(attachment)
                    print(f"📎 已添加附件: {filename}")
                else:
                    print(f"⚠️  附件不存在: {attachment_path}")
        
        return msg
    
    def send(self, 
             to_email: str, 
             subject: str, 
             body: str, 
             html_body: Optional[str] = None,
             attachments: Optional[List[str]] = None) -> bool:
        """发送邮件"""
        try:
            print(f"📧 准备发送邮件...")
            print(f"   发件人: {self.config['email']}")
            print(f"   收件人: {to_email}")
            print(f"   主题: {subject}")
            
            # 创建邮件
            msg = self.create_message(to_email, subject, body, html_body, attachments)
            
            # 连接SMTP服务器
            print(f"🔗 连接SMTP服务器: {self.smtp_server}:{self.smtp_port}")
            
            if self.use_ssl and self.smtp_port == 465:
                # SSL连接
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    print("🔒 使用SSL加密连接")
                    self._login_and_send(server, msg, to_email)
            else:
                # STARTTLS连接
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.set_debuglevel(1)  # 显示调试信息
                    
                    if self.use_ssl:
                        print("🔒 启用STARTTLS加密...")
                        server.starttls()
                    
                    self._login_and_send(server, msg, to_email)
            
            # 更新最后测试时间
            self.config['last_test'] = datetime.now().isoformat()
            QQMailConfig.save_config(self.config)
            
            return True
            
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            self._print_troubleshooting(e)
            return False
    
    def _login_and_send(self, server, msg, to_email):
        """登录并发送邮件"""
        # 登录
        print(f"🔑 登录邮箱: {self.config['email']}")
        server.login(self.config['email'], self.config['password'])
        
        # 发送邮件
        print("📤 发送邮件...")
        server.send_message(msg)
        
        print(f"✅ 邮件发送成功！")
        print(f"   收件人: {to_email}")
        print(f"   主题: {msg['Subject']}")
    
    def _print_troubleshooting(self, error):
        """打印故障排除信息"""
        print("\n💡 QQ邮箱常见问题解决：")
        print("1. 授权码错误")
        print("   - 确认使用的是授权码，不是登录密码")
        print("   - 重新生成授权码：QQ邮箱 → 设置 → 账户 → 生成授权码")
        
        print("\n2. 未开启SMTP服务")
        print("   - 登录QQ邮箱网页版")
        print("   - 设置 → 账户 → POP3/IMAP/SMTP服务")
        print("   - 开启：IMAP/SMTP服务")
        
        print("\n3. 端口问题")
        print(f"   - 尝试端口 465 (SSL) 或 587 (STARTTLS)")
        print(f"   - 当前使用: {self.smtp_port}")
        
        print("\n4. 网络问题")
        print("   - 检查网络连接")
        print("   - 尝试关闭防火墙或杀毒软件")
        
        print(f"\n详细错误: {error}")
    
    def send_test_email(self, to_email: Optional[str] = None) -> bool:
        """发送测试邮件"""
        if not to_email:
            to_email = self.config['email']
        
        test_subject = "📧 QQ邮箱SMTP测试邮件"
        
        test_body = f"""这是一封QQ邮箱SMTP测试邮件。

发送信息：
- 发件人：{self.config['email']}
- 发件人名称：{self.config.get('display_name', 'OpenClaw助手')}
- 发送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- SMTP服务器：{self.smtp_server}:{self.smtp_port}

如果收到此邮件，说明QQ邮箱SMTP配置成功！

下一步：
1. 确认收到此邮件
2. 可以开始使用邮件功能
3. 如有问题，请检查配置

祝使用愉快！
{self.config.get('signature', 'OpenClaw助手')}
"""
        
        test_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>QQ邮箱SMTP测试</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #12B7F5; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ padding: 30px; background-color: #f9f9f9; }}
        .success {{ color: #52c41a; font-weight: bold; font-size: 18px; }}
        .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 QQ邮箱SMTP测试邮件</h1>
        </div>
        <div class="content">
            <p class="success">✅ 测试邮件发送成功！</p>
            
            <div class="info-box">
                <h3>发送信息：</h3>
                <ul>
                    <li><strong>发件人：</strong>{self.config['email']}</li>
                    <li><strong>发件人名称：</strong>{self.config.get('display_name', 'OpenClaw助手')}</li>
                    <li><strong>发送时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                    <li><strong>SMTP服务器：</strong>{self.smtp_server}:{self.smtp_port}</li>
                </ul>
            </div>
            
            <p>如果收到此邮件，说明QQ邮箱SMTP配置成功！</p>
            
            <div class="info-box">
                <h3>下一步：</h3>
                <ol>
                    <li>确认收到此邮件</li>
                    <li>可以开始使用邮件功能</li>
                    <li>如有问题，请检查配置</li>
                </ol>
            </div>
        </div>
        <div class="footer">
            <p>{self.config.get('signature', 'OpenClaw助手')}</p>
            <p>{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
        
        return self.send(to_email, test_subject, test_body, test_html)

class QQMailReceiver:
    """QQ邮箱接收器（使用IMAP）"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or QQMailConfig.load_config()
        self.imap_server = QQMailConfig.IMAP_SERVER
        self.imap_port = self.config.get('imap_port', QQMailConfig.IMAP_PORT)
    
    def connect(self) -> Optional[imaplib.IMAP4_SSL]:
        """连接IMAP服务器"""
        try:
            print(f"🔗 连接IMAP服务器: {self.imap_server}:{self.imap_port}")
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            
            print(f"🔑 登录邮箱: {self.config['email']}")
            mail.login(self.config['email'], self.config['password'])
            
            print("✅ IMAP连接成功")
            return mail
            
        except Exception as e:
            print(f"❌ IMAP连接失败: {e}")
            return None
    
    def get_unread_count(self, folder: str = 'INBOX') -> int:
        """获取未读邮件数量"""
        mail = self.connect()
        if not mail:
            return -1
        
        try:
            mail.select(folder)
            _, data = mail.search(None, 'UNSEEN')
            unread_ids = data[0].split()
            count = len(unread_ids)
            
            print(f"📥 {folder} 未读邮件: {count}封")
            return count
            
        except Exception as e:
            print(f"❌ 获取未读邮件失败: {e}")
            return -1
        finally:
            mail.logout()
    
    def fetch_recent_emails(self, folder: str = 'INBOX', limit: int = 5) -> List[Dict[str, Any]]:
        """获取最近邮件"""
        mail = self.connect()
        if not mail:
            return []
        
        try:
            mail.select(folder)
            
            # 搜索所有邮件，按日期排序
            _, data = mail.search(None, 'ALL')
            email_ids = data[0].split()
            
            # 获取最新的几封
            recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            emails = []
            for email_id in recent_ids:
                try:
                    _, msg_data = mail.fetch(email_id, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    email_info = {
                        'id': email_id.decode(),
                        'from': self._decode_header(msg['From']),
                        'to': self._decode_header(msg['To']),
                        'subject': self._decode_header(msg['Subject']),
                        'date': msg['Date'],
                        'has_attachments': self._has_attachments(msg)
                    }
                    
                    # 获取纯文本内容
                    body = self._get_email_body(msg)
                    if body:
                        email_info['body_preview'] = body[:200] + '...' if len(body) > 200 else body
                    
                    emails.append(email_info)
                    
                except Exception as e:
                    print(f"⚠️  解析邮件 {email_id} 失败: {e}")
            
            return emails
            
        except Exception as e:
            print(f"❌ 获取邮件失败: {e}")
            return []
        finally:
            mail.logout()
    
    def _decode_header(self, header: str) -> str:
        """解码邮件头"""
        if not header:
            return ""
        
        try:
            decoded_parts = email.header.decode_header(header)
            result = []
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        result.append(part.decode(encoding))
                    else:
                        result.append(part.decode('utf-8', errors='ignore'))
                else:
                    result.append(part)
            return ' '.join(result)
        except:
            return str(header)
    
    def _has_attachments(self, msg: email.message.Message) -> bool:
        """检查是否有附件"""
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
        return False
    
    def _get_email_body(self, msg: email.message.Message) -> Optional[str]:
        """获取邮件正文（纯文本）"""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        return part.get_payload(decode=True).decode()
                    except:
                        return part.get_payload()
        else:
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                try:
                    return msg.get_payload(decode=True).decode()
                except:
                    return msg.get_payload()
        
        return None

def main():
    """主函数"""
    import sys
    
    print("=" * 60)
    print("📧 QQ邮箱SMTP/IMAP邮件系统")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'setup':
            QQMailConfig.interactive_setup()
        
        elif command == 'test':
            config = QQMailConfig.load_config()
            if not config['email'] or not config['password']:
                print("❌ 请先运行配置向导: python qqmail_smtp_config.py setup")
                return
            
            sender = QQMailSender(config)
            sender.send_test_email()
        
        elif command == 'send':
            if len(sys.argv) < 4:
                print("用法: python qqmail_smtp_config.py send <收件人> <主题> [正文]")
                return
            
            to_email = sys.argv[2]
            subject = sys.argv[3]
            body = sys.argv[4] if len(sys.argv) > 4 else "这是一封来自QQ邮箱的测试邮件。"
            
            sender = QQMailSender()
            sender.send(to_email, subject, body)
        
        elif command == 'receive':
            receiver = QQMailReceiver()
            
            if len(sys.argv) > 2 and sys.argv[2] == 'count':
                count = receiver.get_unread_count()
                if count >= 0:
                    print(f"📥 未读邮件: {count}封")
            else:
                emails = receiver.fetch_recent_emails(limit=5)
                if emails:
                    print(f"\n📨 最近 {len(emails)} 封邮件:")
                    for i, email_info in enumerate(emails, 1):
                        print(f"\n{i}. [{email_info['date']}]")
                        print(f"   发件人: {email_info['from']}")
                        print(f"   主题: {email_info['subject']}")
                        if 'body_preview' in email_info:
                            print(f"   预览: {email_info['body_preview']}")
                        if email_info['has_attachments']:
                            print(f"   有附件: 是")
                else:
                    print("📭 没有找到邮件")
        
        elif command == 'config':
            config = QQMailConfig.load_config()
            print(json.dumps(config, indent=2, ensure_ascii=False, default=str))
        
        else:
            print(f"未知命令: {command}")
            print("\n可用命令:")
            print("  setup    - 配置QQ邮箱")
            print("  test     - 发送测试邮件")
            print("  send     - 发送邮件")
            print("  receive  - 接收邮件")
            print("  config   - 查看配置")
    
    else:
        # 交互模式
        print("\n请选择操作:")
        print("1. 配置QQ邮箱")
        print("2. 发送测试邮件")
        print("3. 发送自定义邮件")
        print("4. 查看未读邮件")
        print("5. 查看最近邮件")
        print("6. 查看当前配置")
        print("7. 退出")
        
        choice = input("\n请输入选择 (1-7): ").strip()
        
        if choice == '1':
            QQMailConfig.interactive_setup()
        
        elif choice == '2':
            sender = QQMailSender()
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
            
            sender = QQMailSender()
            sender.send(to_email, subject, body)
        
        elif choice == '4':
            receiver = QQMailReceiver()
            count = receiver.get_unread_count()
            if count >= 0:
                print(f"📥 未读邮件: {count}封")
        
        elif choice == '5':
            receiver = QQMailReceiver()
            emails = receiver.fetch_recent_emails(limit=5)
            if emails:
                print(f"\n📨 最近 {len(emails)} 封邮件:")
                for i, email_info in enumerate(emails, 1):
                    print(f"\n{i}. [{email_info['date']}]")
                    print(f"   发件人: {email_info['from']}")
                    print(f"   主题: {email_info['subject']}")
                    if 'body_preview' in email_info:
                        print(f"   预览: {email_info['body_preview']}")
                    if email_info['has_attachments']:
                        print(f"   有附件: 是")
            else:
                print("📭 没有找到邮件")
        
        elif choice == '6':
            config = QQMailConfig.load_config()
            print("\n当前配置:")
            for key, value in config.items():
                if key == 'password' and value:
                    print(f"  {key}: {'*' * len(value)}")
                else:
                    print(f"  {key}: {value}")
        
        elif choice == '7':
            print("再见！")
        
        else:
            print("无效选择")

if __name__ == "__main__":
    main()