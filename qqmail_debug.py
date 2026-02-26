#!/usr/bin/env python3
"""
QQ邮箱SMTP调试脚本
"""

import smtplib
import ssl
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

def debug_smtp_connection():
    """调试SMTP连接"""
    config_file = os.path.expanduser('~/.openclaw/qqmail_config.json')
    
    if not os.path.exists(config_file):
        print("❌ 配置文件不存在")
        return False
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 60)
    print("🔧 QQ邮箱SMTP连接调试")
    print("=" * 60)
    
    email = config.get('email', '')
    password = config.get('password', '')
    smtp_server = "smtp.qq.com"
    smtp_port = config.get('smtp_port', 587)
    
    print(f"邮箱: {email}")
    print(f"密码长度: {len(password)}")
    print(f"SMTP服务器: {smtp_server}:{smtp_port}")
    
    if not email:
        print("❌ 邮箱地址为空")
        return False
    
    if not password:
        print("❌ 密码为空")
        return False
    
    try:
        print(f"\n1. 尝试连接SMTP服务器...")
        
        if smtp_port == 465:
            # SSL连接
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
            print("   ✅ SSL连接成功")
        else:
            # STARTTLS连接
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            server.set_debuglevel(2)  # 显示详细调试信息
            print("   ✅ TCP连接成功")
            
            if smtp_port == 587:
                print("   尝试STARTTLS...")
                server.starttls()
                print("   ✅ STARTTLS成功")
        
        print(f"\n2. 尝试登录...")
        server.login(email, password)
        print("   ✅ 登录成功")
        
        print(f"\n3. 创建测试邮件...")
        msg = MIMEMultipart()
        msg['From'] = formataddr((str(Header(config.get('display_name', 'Test')), 'utf-8'), email))
        msg['To'] = email  # 发送给自己
        msg['Subject'] = Header('📧 SMTP连接测试', 'utf-8')
        
        body = "这是一封SMTP连接测试邮件。如果收到，说明连接成功！"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        print(f"\n4. 发送测试邮件...")
        server.send_message(msg)
        print("   ✅ 邮件发送成功")
        
        server.quit()
        print("\n🎉 所有测试通过！")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ 认证失败: {e}")
        print("\n可能原因：")
        print("1. 密码错误 - 请使用QQ邮箱授权码，不是登录密码")
        print("2. 未开启SMTP服务 - 登录QQ邮箱网页版开启")
        print("3. 授权码过期 - 重新生成授权码")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ 连接失败: {e}")
        print("\n可能原因：")
        print("1. 网络问题 - 检查网络连接")
        print("2. 防火墙阻止 - 检查防火墙设置")
        print("3. 端口被屏蔽 - 尝试不同端口")
        return False
        
    except Exception as e:
        print(f"\n❌ 其他错误: {type(e).__name__}: {e}")
        return False

def test_different_ports():
    """测试不同端口"""
    config_file = os.path.expanduser('~/.openclaw/qqmail_config.json')
    
    if not os.path.exists(config_file):
        print("❌ 配置文件不存在")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    email = config.get('email', '')
    password = config.get('password', '')
    
    print("\n" + "=" * 60)
    print("🔌 测试不同SMTP端口")
    print("=" * 60)
    
    ports_to_test = [
        (587, "STARTTLS (推荐)"),
        (465, "SSL"),
        (25, "传统SMTP"),
    ]
    
    for port, description in ports_to_test:
        print(f"\n测试端口 {port} ({description})...")
        try:
            if port == 465:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL("smtp.qq.com", port, context=context, timeout=10)
            else:
                server = smtplib.SMTP("smtp.qq.com", port, timeout=10)
                if port == 587:
                    server.starttls()
            
            server.login(email, password)
            print(f"   ✅ 端口 {port} 可用")
            server.quit()
            
        except Exception as e:
            print(f"   ❌ 端口 {port} 失败: {e}")

def check_qqmail_service():
    """检查QQ邮箱服务状态"""
    print("\n" + "=" * 60)
    print("🔍 QQ邮箱服务状态检查")
    print("=" * 60)
    
    print("\n请确认以下事项：")
    print("1. ✅ 已登录QQ邮箱网页版: https://mail.qq.com")
    print("2. ✅ 已进入设置 → 账户")
    print("3. ✅ 已找到 'POP3/IMAP/SMTP服务'")
    print("4. ✅ 已开启 'IMAP/SMTP服务'")
    print("5. ✅ 已生成16位授权码（不是QQ密码）")
    print("6. ✅ 授权码已复制保存")
    
    print("\n授权码获取步骤：")
    print("1. 登录QQ邮箱网页版")
    print("2. 点击顶部 '设置'")
    print("3. 选择 '账户' 选项卡")
    print("4. 找到 'POP3/IMAP/SMTP服务'")
    print("5. 点击 '开启'")
    print("6. 按照提示发送短信验证")
    print("7. 获取16位授权码")
    
    print("\n常见问题：")
    print("• 授权码以 '#' 开头和结尾，需要去掉")
    print("• 授权码包含字母和数字，区分大小写")
    print("• 每个授权码只能用于一个应用")
    print("• 可以随时生成新的授权码，旧的会失效")

def main():
    """主函数"""
    print("📧 QQ邮箱SMTP调试工具")
    print("=" * 60)
    
    print("\n请选择调试选项：")
    print("1. 测试SMTP连接")
    print("2. 测试不同端口")
    print("3. 检查QQ邮箱服务状态")
    print("4. 重新配置")
    print("5. 退出")
    
    choice = input("\n请输入选择 (1-5): ").strip()
    
    if choice == '1':
        debug_smtp_connection()
    elif choice == '2':
        test_different_ports()
    elif choice == '3':
        check_qqmail_service()
    elif choice == '4':
        # 重新配置
        from qqmail_smtp_config import QQMailConfig
        QQMailConfig.interactive_setup()
    elif choice == '5':
        print("再见！")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()