# 📧 QQ邮箱SMTP配置快速指南

## 🎯 目标
使用Python的smtplib和imaplib库，通过QQ邮箱SMTP/IMAP服务发送和接收邮件。

## 🔧 核心文件
1. **`qqmail_smtp_config.py`** - QQ邮箱SMTP/IMAP基础功能
2. **`qqmail_stock_report.py`** - 安霸股票报告邮件发送

## 🚀 快速开始

### 第一步：获取QQ邮箱授权码
**重要：不是QQ登录密码！**

1. 登录QQ邮箱网页版：https://mail.qq.com
2. 点击 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP服务**
4. 开启 **IMAP/SMTP服务**
5. 点击 **生成授权码**
6. 复制生成的16位授权码

### 第二步：运行配置向导
```bash
cd /home/allen/.openclaw/workspace
python3 qqmail_smtp_config.py setup
```

按照提示输入：
- QQ邮箱地址（如：123456789@qq.com）
- **授权码**（刚才生成的16位码）
- 发件人显示名称
- 邮件签名

### 第三步：测试发送
```bash
# 发送测试邮件到自己的QQ邮箱
python3 qqmail_smtp_config.py test

# 或发送自定义邮件
python3 qqmail_smtp_config.py send recipient@example.com "测试主题" "邮件内容"
```

### 第四步：发送安霸股票报告
```bash
# 发送今日安霸股票报告
python3 qqmail_stock_report.py daily

# 发送给指定收件人
python3 qqmail_stock_report.py daily recipient@example.com
```

## 📊 功能特性

### 发送功能
- ✅ 纯文本邮件
- ✅ HTML格式邮件（支持中文）
- ✅ 附件支持
- ✅ 多收件人支持
- ✅ 自动编码处理

### 接收功能
- ✅ 查看未读邮件数量
- ✅ 获取最近邮件列表
- ✅ 解析邮件头信息
- ✅ 提取邮件正文

### 股票报告集成
- ✅ 自动读取最新安霸分析报告
- ✅ 生成专业HTML邮件模板
- ✅ 附加完整报告文件
- ✅ 适配QQ邮箱显示

## ⚙️ 技术配置

### SMTP服务器配置
```
服务器：smtp.qq.com
端口：587 (推荐) 或 465
加密：STARTTLS (587) 或 SSL (465)
认证：需要QQ邮箱授权码
```

### IMAP服务器配置
```
服务器：imap.qq.com
端口：993
加密：SSL
用途：接收邮件
```

## 🎯 使用示例

### 1. 交互式使用
```bash
python3 qqmail_smtp_config.py
```
选择菜单操作：
- 1: 配置QQ邮箱
- 2: 发送测试邮件
- 3: 发送自定义邮件
- 4: 查看未读邮件
- 5: 查看最近邮件

### 2. 命令行使用
```bash
# 配置
python3 qqmail_smtp_config.py setup

# 测试
python3 qqmail_smtp_config.py test

# 发送
python3 qqmail_smtp_config.py send friend@qq.com "你好" "这是一封测试邮件"

# 接收
python3 qqmail_smtp_config.py receive count  # 查看未读数量
python3 qqmail_smtp_config.py receive        # 查看最近邮件

# 查看配置
python3 qqmail_smtp_config.py config
```

### 3. 股票报告系统
```bash
# 发送今日报告
python3 qqmail_stock_report.py daily

# 测试QQ邮箱配置
python3 qqmail_stock_report.py test

# 重新配置
python3 qqmail_stock_report.py config

# 检查报告
python3 qqmail_stock_report.py check
```

## 🔄 与现有系统集成

### 定时发送股票报告
```bash
# 每天上午9点发送
0 9 * * * cd /home/allen/.openclaw/workspace && python3 qqmail_stock_report.py daily

# 每天上午8点和下午4点发送
0 8,16 * * * cd /home/allen/.openclaw/workspace && python3 qqmail_stock_report.py daily
```

### 价格突破提醒
可以扩展脚本，当安霸股价突破关键价位时自动发送提醒邮件。

## 🛠️ 故障排除

### 常见问题

#### 1. 授权码错误
```
错误：535 b'Login Fail. Please enter your authorization code to login.'
解决：使用正确的授权码，不是QQ登录密码
```

#### 2. 未开启SMTP服务
```
错误：535 b'Error: authentication failed'
解决：登录QQ邮箱网页版开启IMAP/SMTP服务
```

#### 3. 端口问题
```
错误：Connection refused
解决：尝试不同端口：587 或 465
```

#### 4. 编码问题
```
错误：UnicodeEncodeError
解决：脚本已自动处理中文编码
```

### 调试命令
```bash
# 测试SMTP连接
telnet smtp.qq.com 587

# 查看详细错误
python3 -c "import smtplib; server = smtplib.SMTP('smtp.qq.com', 587); server.set_debuglevel(1)"
```

## 📁 文件结构

```
/home/allen/.openclaw/workspace/
├── qqmail_smtp_config.py      # 核心QQ邮箱功能
├── qqmail_stock_report.py     # 股票报告邮件
├── qqmail_quick_start.md      # 本指南
├── ~/.openclaw/qqmail_config.json  # 配置文件
└── reports/                   # 股票报告目录
    ├── ambarella_real_*.md    # 真实数据报告
    └── ambarella_*.md         # 模拟数据报告
```

## 🔐 安全提示

1. **保护授权码**
   - 授权码相当于密码，不要泄露
   - 不要硬编码在脚本中
   - 使用配置文件存储

2. **定期更新**
   - 可以定期重新生成授权码
   - 旧授权码会自动失效

3. **安全存储**
   - 配置文件权限：600
   - 建议加密存储敏感信息

## 🚀 高级功能

### 自定义邮件模板
可以修改 `qqmail_stock_report.py` 中的 `create_email_content` 函数，自定义邮件样式。

### 批量发送
扩展脚本支持批量发送给多个收件人。

### 邮件过滤
使用IMAP功能实现邮件过滤和自动回复。

### 集成其他服务
将QQ邮箱与新闻摘要、天气提醒等服务集成。

## 📞 技术支持

### 官方文档
- QQ邮箱帮助中心：https://service.mail.qq.com
- Python smtplib文档：https://docs.python.org/3/library/smtplib.html
- Python imaplib文档：https://docs.python.org/3/library/imaplib.html

### 问题反馈
遇到问题时：
1. 检查授权码是否正确
2. 确认SMTP服务已开启
3. 尝试不同端口（587/465）
4. 查看错误信息详细内容

## 🎉 开始使用

### 最简单的流程：
```bash
# 1. 配置
python3 qqmail_smtp_config.py setup

# 2. 测试
python3 qqmail_smtp_config.py test

# 3. 发送股票报告
python3 qqmail_stock_report.py daily

# 4. 设置定时任务（可选）
crontab -e
# 添加：0 9 * * * cd /home/allen/.openclaw/workspace && python3 qqmail_stock_report.py daily
```

### 验证成功：
1. 收到测试邮件
2. 收到股票报告邮件
3. 邮件格式正确显示
4. 附件可以正常下载

现在您的QQ邮箱SMTP系统已经配置完成，可以开始使用了！ 🚀

---
*最后更新：2026年2月22日*
*适用于：OpenClaw QQ邮箱SMTP配置*