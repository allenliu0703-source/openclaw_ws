# 📧 邮件发送技能配置指南

## 🎯 配置目标
为您配置邮件发送功能，支持：
1. 发送普通文本邮件
2. 发送HTML格式邮件
3. 添加附件
4. 定时发送邮件
5. 与现有系统集成（如安霸股票报告）

## 🔧 可用方案

### 方案一：使用Himalaya CLI（推荐）
**优点：**
- 专门为命令行设计的邮件客户端
- 支持IMAP/SMTP
- 与OpenClaw技能集成
- 功能完整

**安装步骤：**
```bash
# 方法1：使用cargo（需要Rust）
cargo install himalaya

# 方法2：下载预编译二进制
# 访问：https://github.com/pimalaya/himalaya/releases
```

### 方案二：使用Python邮件库
**优点：**
- 无需额外安装
- 使用现有Python环境
- 编程灵活

**所需库：**
```bash
pip install yagmail  # 简化版
# 或
pip install smtplib email  # 标准库
```

### 方案三：使用系统邮件命令
**优点：**
- 系统自带
- 简单直接

**命令：**
```bash
# 使用mail命令
echo "邮件内容" | mail -s "主题" recipient@example.com

# 使用sendmail
sendmail recipient@example.com < email.txt
```

## 📋 配置步骤

### 第一步：选择邮件服务商
请选择您的邮件服务商：
- [ ] Gmail（需要应用专用密码）
- [ ] Outlook/Hotmail
- [ ] QQ邮箱
- [ ] 163/126邮箱
- [ ] 企业邮箱
- [ ] 其他：____________

### 第二步：获取SMTP配置信息
每种邮箱的SMTP配置不同：

**Gmail：**
```
SMTP服务器：smtp.gmail.com
端口：587（TLS）或 465（SSL）
需要开启：两步验证和应用专用密码
```

**QQ邮箱：**
```
SMTP服务器：smtp.qq.com
端口：587
需要：授权码（非登录密码）
```

**163邮箱：**
```
SMTP服务器：smtp.163.com
端口：25或465或587
```

### 第三步：创建配置文件

#### Himalaya配置示例：
```toml
# ~/.config/himalaya/config.toml
[accounts.default]
email = "your_email@example.com"
display-name = "您的名字"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "your_email@example.com"
backend.auth.type = "password"
# 使用密码管理器或直接输入

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "your_email@example.com"
message.send.backend.auth.type = "password"
```

#### Python配置示例：
```python
# email_config.py
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'username': 'your_email@example.com',
    'password': 'your_password_or_app_password',
    'use_tls': True,
    'sender_name': '您的名字'
}
```

## 🚀 快速开始方案

### 如果您想立即开始，我建议：

#### 选项A：使用Python快速配置
让我为您创建一个简单的Python邮件发送脚本：

```python
#!/usr/bin/env python3
"""
简单邮件发送脚本
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os

class EmailSender:
    def __init__(self, config_file='email_config.json'):
        self.config = self.load_config(config_file)
    
    def load_config(self, config_file):
        """加载邮件配置"""
        # 这里可以读取配置文件
        # 暂时使用示例配置
        return {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your_email@gmail.com',
            'password': 'your_app_password',
            'use_tls': True
        }
    
    def send_email(self, to_email, subject, body, html_body=None):
        """发送邮件"""
        try:
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config['username']
            msg['To'] = to_email
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 添加纯文本版本
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 如果有HTML版本，也添加
            if html_body:
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # 连接服务器并发送
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                if self.config['use_tls']:
                    server.starttls()
                server.login(self.config['username'], self.config['password'])
                server.send_message(msg)
            
            print(f"✅ 邮件发送成功：{to_email}")
            return True
            
        except Exception as e:
            print(f"❌ 邮件发送失败：{e}")
            return False

# 使用示例
if __name__ == "__main__":
    sender = EmailSender()
    
    # 发送测试邮件
    sender.send_email(
        to_email="recipient@example.com",
        subject="测试邮件",
        body="这是一封测试邮件，来自OpenClaw邮件系统。",
        html_body="<h1>测试邮件</h1><p>这是一封测试邮件，来自OpenClaw邮件系统。</p>"
    )
```

#### 选项B：使用系统mail命令（最简单）
```bash
# 安装mailutils（如果尚未安装）
sudo apt-get install mailutils

# 发送测试邮件
echo "测试邮件内容" | mail -s "测试主题" recipient@example.com
```

## 📊 与现有系统集成

### 集成安霸股票报告
我可以将邮件发送功能与您的安霸股票分析系统集成：

```python
# 发送每日股票报告
def send_daily_stock_report(email_address):
    """发送每日安霸股票报告"""
    
    # 读取今日报告
    with open('/home/allen/.openclaw/workspace/reports/ambarella_real_2026-02-22.md', 'r') as f:
        report_content = f.read()
    
    # 创建邮件内容
    subject = f"📈 安霸(AMBA)每日股票分析 - {datetime.today().strftime('%Y-%m-%d')}"
    
    # 简化版内容
    simple_content = f"""
安霸(AMBA)今日分析：

{report_content[:500]}...

完整报告请查看附件或登录系统查看。
"""
    
    # 发送邮件
    email_sender.send_email(
        to_email=email_address,
        subject=subject,
        body=simple_content
    )
```

### 定时发送功能
可以配置cron任务定时发送：

```bash
# 每天上午9点发送股票报告
0 9 * * * /home/allen/.openclaw/workspace/send_stock_report.py
```

## 🔐 安全注意事项

### 密码安全
1. **不要将密码硬编码在脚本中**
2. **使用环境变量：**
   ```bash
   export EMAIL_PASSWORD="your_password"
   ```
3. **使用配置文件（加密）：**
   ```python
   import keyring
   password = keyring.get_password("email_system", "username")
   ```
4. **使用应用专用密码（Gmail等）**

### 隐私保护
1. 加密存储联系人信息
2. 遵守反垃圾邮件法规
3. 提供退订选项
4. 保护收件人隐私

## 🎯 下一步行动

### 请告诉我：
1. **您使用哪个邮箱服务商？**
   - Gmail / Outlook / QQ邮箱 / 其他

2. **主要用途是什么？**
   - 发送股票报告
   - 日常沟通
   - 自动化通知
   - 其他：____________

3. **发送频率？**
   - 每日
   - 每周
   - 每月
   - 按需

4. **收件人范围？**
   - 仅自己
   - 小团队
   - 客户/订阅者

### 根据您的回答，我将：
1. 创建相应的配置模板
2. 编写发送脚本
3. 测试发送功能
4. 集成到现有系统

## 📞 技术支持

### 常见问题解决：
1. **认证失败**
   - 检查用户名密码
   - 确认是否开启SMTP服务
   - 检查是否需要应用专用密码

2. **连接超时**
   - 检查网络连接
   - 确认SMTP服务器地址和端口
   - 检查防火墙设置

3. **被标记为垃圾邮件**
   - 优化邮件内容
   - 配置SPF/DKIM记录
   - 避免敏感词汇

### 调试命令：
```bash
# 测试SMTP连接
telnet smtp.gmail.com 587

# 查看邮件日志
tail -f /var/log/mail.log

# 测试发送
echo "test" | mail -s "test" your_email@example.com
```

## 🚀 立即开始

### 最简单的方式（使用Gmail）：
1. 开启Gmail两步验证
2. 生成应用专用密码
3. 运行我的配置脚本

### 让我为您创建完整的邮件系统：
请提供以下信息：
```
邮箱服务商：_________
邮箱地址：___________
主要用途：___________
```

我将为您创建完整的邮件发送解决方案！

---
*配置指南版本：1.0*
*更新日期：2026年2月22日*
*适用于：OpenClaw邮件技能配置*