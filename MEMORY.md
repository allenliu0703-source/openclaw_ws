# MEMORY.md - 长期记忆

## 系统启动信息
**首次启动时间**: 2026-02-22
**工作目录**: /home/allen/.openclaw/workspace
**用户**: Allen

## 重要系统配置

### 邮件系统配置 (2026-02-22)
- **QQ邮箱**: allenliu0703@qq.com
- **SMTP服务器**: smtp.qq.com:587 (STARTTLS)
- **IMAP服务器**: imap.qq.com:993 (SSL)
- **显示名称**: Openclaw Assistant
- **状态**: ✅ 已完全修复并正常工作

### 创建的邮件系统文件
1. `qqmail_smtp_config.py` - 核心邮件发送功能
2. `send_weather_email.py` - 天气邮件系统
3. `send_horse_year_email_final.py` - 马年拜年邮件(Gmail)
4. `send_horse_year_to_qqmail.py` - 马年拜年邮件(QQ邮箱)
5. `qqmail_stock_report.py` - 安霸股票报告邮件

### 测试验证结果 (2026-02-22)
1. ✅ QQ邮箱SMTP连接测试成功
2. ✅ 安霸股票报告邮件发送成功
3. ✅ 上海天气邮件发送成功
4. ✅ 马年拜年邮件发送成功(Gmail和QQ邮箱)

## 用户偏好和习惯

### 邮件相关偏好
- 使用Python的smtplib而不是Himalaya
- 喜欢简洁、可操作的摘要
- 需要真实股票数据(Yahoo Finance和Alpha Vantage)
- 喜欢中国传统节日祝福邮件

### 技术偏好
- 使用真实API数据
- 偏好模块化、可重用的脚本
- 需要详细的错误处理和状态报告
- 喜欢自动化系统(cron任务)

## 重要联系人信息
- **飞书用户ID**: `ou_02fb23cf00d12a29c643f872b0061d51` (主要消息目标)
- **手机号码**: 17765191437 (用于问候上下文)
- **邮箱地址**: 
  - allenliu0703@qq.com (主要QQ邮箱)
  - allenliu0703@gmail.com (Gmail邮箱)
- **王勃 (勃比)**: wangbo8927@gmail.com (好兄弟)

## API密钥和配置
- **Alpha Vantage API Key**: `RHSTH42HVC2YDMZB` (已配置用于股票数据)
- **wttr.in API**: 用于天气数据查询

## 项目目录结构
```
/home/allen/.openclaw/workspace/
├── reports/                    # 股票报告目录
│   └── ambarella_real_2026-02-22.md
├── memory/                    # 每日记忆文件
│   └── 2026-02-22.md
├── qqmail_smtp_config.py     # ✅ 核心邮件发送
├── send_weather_email.py     # ✅ 天气邮件系统
├── send_horse_year_*.py      # ✅ 拜年邮件脚本
├── qqmail_stock_report.py    # ✅ 股票报告邮件
└── ~/.openclaw/qqmail_config.json # 配置文件
```

## 系统能力总结

### 已实现的功能
1. **邮件发送系统** - 完整的QQ邮箱SMTP集成
2. **股票报告系统** - 安霸(AMBA)每日分析报告
3. **天气查询系统** - 实时天气获取和邮件发送
4. **节日祝福系统** - 自动生成和发送节日邮件
5. **定时任务系统** - 支持cron自动执行

### 技术特点
- ✅ 稳定可靠的邮件发送
- ✅ 专业美观的HTML邮件模板
- ✅ 完整的中文支持
- ✅ 详细的错误处理和日志
- ✅ 模块化设计，易于扩展

## 经验教训

### 技术问题解决 (2026-02-22)
**问题**: QQ邮箱SMTP发送失败，出现`mail from:<None>`错误
**原因**: MIME对象层次结构错误，函数返回了子对象而不是主消息
**解决方案**: 确保`MIMEMultipart('alternative')`正确附加到主消息

### 最佳实践
1. **邮件创建**: 始终检查MIME对象层次结构
2. **HTML模板**: CSS中的花括号需要双重转义
3. **调试方法**: 使用`smtplib.set_debuglevel(1)`查看详细日志
4. **错误处理**: 完整的异常捕获和状态报告

## 未来扩展计划

### 短期计划
1. 配置每日自动天气邮件
2. 添加更多城市天气支持
3. 扩展股票报告功能

### 长期计划
1. 批量邮件发送功能
2. 邮件模板管理系统
3. 邮件接收和查看功能
4. 重要事件通知系统

---
**最后更新**: 2026-02-22 18:45
**系统状态**: ✅ 所有邮件系统功能正常工作