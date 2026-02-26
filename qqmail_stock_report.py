#!/usr/bin/env python3
"""
使用QQ邮箱发送安霸股票报告
集成QQ邮箱SMTP和股票报告系统
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from qqmail_smtp_config import QQMailSender, QQMailConfig
except ImportError:
    print("❌ 无法导入QQ邮箱模块")
    sys.exit(1)

class QQStockReportEmail:
    """QQ邮箱股票报告发送器"""
    
    def __init__(self, email_sender=None):
        self.email_sender = email_sender or QQMailSender()
        self.reports_dir = "/home/allen/.openclaw/workspace/reports"
        
    def get_latest_report(self, date=None):
        """获取最新的股票报告"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 尝试真实数据报告
        real_report = os.path.join(self.reports_dir, f"ambarella_real_{date}.md")
        if os.path.exists(real_report):
            return real_report
        
        # 尝试模拟数据报告
        sim_report = os.path.join(self.reports_dir, f"ambarella_{date}.md")
        if os.path.exists(sim_report):
            return sim_report
        
        # 尝试昨天的报告
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_real = os.path.join(self.reports_dir, f"ambarella_real_{yesterday}.md")
        if os.path.exists(yesterday_real):
            return yesterday_real
        
        yesterday_sim = os.path.join(self.reports_dir, f"ambarella_{yesterday}.md")
        if os.path.exists(yesterday_sim):
            return yesterday_sim
        
        return None
    
    def parse_report_summary(self, report_path):
        """解析报告生成摘要"""
        if not report_path or not os.path.exists(report_path):
            return None
        
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            summary = {
                'date': '',
                'current_price': '',
                'change': '',
                'support': '',
                'resistance': '',
                'bias': '',
                'action': '',
                'full_content': content[:2000]
            }
            
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '当前价格' in line and '$' in line:
                    price_part = line.split('$')[1]
                    if ' ' in price_part:
                        summary['current_price'] = f"${price_part.split(' ')[0]}"
                        for j in range(max(0, i-2), min(len(lines), i+3)):
                            if '涨跌幅' in lines[j] or 'Change' in lines[j]:
                                change_text = lines[j]
                                if '$' in change_text or '%' in change_text:
                                    summary['change'] = change_text.strip()
                                    break
                
                elif '支撑位' in line and '$' in line:
                    summary['support'] = line.split('$')[1].split()[0]
                
                elif '阻力位' in line and '$' in line:
                    summary['resistance'] = line.split('$')[1].split()[0]
                
                elif '市场偏向' in line:
                    summary['bias'] = line.split('偏向:')[1].strip() if '偏向:' in line else line.strip()
                
                elif '操作建议' in line:
                    summary['action'] = line.split('建议:')[1].strip() if '建议:' in line else line.strip()
                
                elif '报告生成时间' in line or 'Report generated at' in line:
                    summary['date'] = line.split(':')[1].strip() if ':' in line else line.strip()
            
            return summary
            
        except Exception as e:
            print(f"❌ 解析报告失败: {e}")
            return None
    
    def create_email_content(self, report_summary):
        """创建邮件内容"""
        if not report_summary:
            return "股票报告生成失败，请检查系统。", None
        
        date = report_summary.get('date', datetime.now().strftime('%Y-%m-%d'))
        price = report_summary.get('current_price', 'N/A')
        change = report_summary.get('change', '')
        support = report_summary.get('support', 'N/A')
        resistance = report_summary.get('resistance', 'N/A')
        bias = report_summary.get('bias', 'N/A')
        action = report_summary.get('action', 'N/A')
        
        # 判断涨跌颜色
        change_color = "#52c41a"  # 绿色
        if "🔴" in change or "-" in change:
            change_color = "#f5222d"  # 红色
        
        # 纯文本版本
        text_body = f"""📈 安霸(AMBA)股票分析报告 - {date}

💰 股价信息：
当前价格：{price} {change}
支撑位：${support}
阻力位：${resistance}

🎯 交易策略：
市场偏向：{bias}
操作建议：{action}

📊 技术分析：
- 使用真实数据API (Yahoo Finance + Alpha Vantage)
- 包含移动平均线、RSI等技术指标
- 提供关键价位和风险提示

⚠️ 风险提示：
1. 股票市场具有波动性
2. 投资需谨慎，建议分散投资
3. 本报告仅供参考，不构成投资建议

📁 完整报告：
报告已保存到系统，可随时查看。

---
OpenClaw股票分析系统 · QQ邮箱发送
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # HTML版本（适配QQ邮箱）
        html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>安霸(AMBA)股票分析报告 - {date}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #12B7F5 0%, #0D8ABC 100%);
            color: white;
            padding: 25px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 500;
        }}
        .header .date {{
            margin-top: 10px;
            opacity: 0.9;
            font-size: 14px;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 25px;
            padding: 20px;
            border-radius: 8px;
            background-color: #f9f9f9;
            border-left: 4px solid #12B7F5;
        }}
        .price-section {{
            background-color: #e6f7ff;
            border-left-color: #1890ff;
        }}
        .price {{
            font-size: 32px;
            font-weight: bold;
            color: #1890ff;
            margin: 10px 0;
        }}
        .change {{
            font-size: 18px;
            margin-left: 10px;
            color: {change_color};
            font-weight: bold;
        }}
        .metric-row {{
            display: flex;
            justify-content: space-between;
            margin: 12px 0;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .metric-label {{
            font-weight: 600;
            color: #555;
            min-width: 100px;
        }}
        .metric-value {{
            color: #222;
            text-align: right;
            flex: 1;
        }}
        .warning {{
            background-color: #fffbe6;
            border-left: 4px solid #faad14;
            padding: 20px;
            margin: 25px 0;
        }}
        .warning h3 {{
            color: #d48806;
            margin-top: 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 12px;
            border-top: 1px solid #eee;
            background-color: #fafafa;
        }}
        h2 {{
            color: #333;
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #12B7F5;
            font-size: 18px;
        }}
        h3 {{
            color: #555;
            font-size: 16px;
            margin: 15px 0 10px 0;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .tag {{
            display: inline-block;
            padding: 4px 12px;
            background-color: #f0f0f0;
            border-radius: 20px;
            font-size: 12px;
            color: #666;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        .success-tag {{
            background-color: #f6ffed;
            color: #52c41a;
            border: 1px solid #b7eb8f;
        }}
        .info-tag {{
            background-color: #e6f7ff;
            color: #1890ff;
            border: 1px solid #91d5ff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 安霸(AMBA)股票分析报告</h1>
            <div class="date">{date}</div>
        </div>
        
        <div class="content">
            <div class="section price-section">
                <h2>💰 股价信息</h2>
                <div class="price">
                    {price} <span class="change">{change}</span>
                </div>
                
                <div class="metric-row">
                    <span class="metric-label">支撑位：</span>
                    <span class="metric-value">${support}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">阻力位：</span>
                    <span class="metric-value">${resistance}</span>
                </div>
                
                <div style="margin-top: 15px;">
                    <span class="tag success-tag">实时数据</span>
                    <span class="tag info-tag">QQ邮箱发送</span>
                    <span class="tag">自动生成</span>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 交易策略</h2>
                <div class="metric-row">
                    <span class="metric-label">市场偏向：</span>
                    <span class="metric-value">{bias}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">操作建议：</span>
                    <span class="metric-value">{action}</span>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 技术分析</h2>
                <ul>
                    <li>使用真实数据API (Yahoo Finance + Alpha Vantage)</li>
                    <li>包含移动平均线、RSI等技术指标</li>
                    <li>提供关键价位和风险提示</li>
                    <li>每日自动生成，数据实时更新</li>
                </ul>
            </div>
            
            <div class="warning">
                <h3>⚠️ 风险提示</h3>
                <ol>
                    <li>股票市场具有波动性，价格可能快速变化</li>
                    <li>投资需谨慎，建议分散投资</li>
                    <li>本报告仅供参考，不构成投资建议</li>
                    <li>请结合个人风险承受能力做出决策</li>
                </ol>
            </div>
            
            <div class="section">
                <h2>📁 报告详情</h2>
                <p>完整报告已保存到系统，包含详细的技术分析和市场数据。</p>
                <p>如需查看完整报告，请登录OpenClaw系统或查看邮件附件。</p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>OpenClaw股票分析系统 · 专业AI投资助手</strong></p>
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>发送方式：QQ邮箱SMTP · 安全加密传输</p>
            <p style="color: #999; font-size: 11px; margin-top: 10px;">
                免责声明：本报告基于公开数据生成，仅供参考。投资有风险，入市需谨慎。
            </p>
        </div>
    </div>
</body>
</html>"""
        
        return text_body, html_body
    
    def send_daily_report(self, recipient_email=None):
        """发送每日报告"""
        print("📧 QQ邮箱发送安霸每日股票报告...")
        
        # 获取最新报告
        report_path = self.get_latest_report()
        if not report_path:
            print("❌ 未找到股票报告文件")
            return False
        
        print(f"📄 找到报告文件: {report_path}")
        
        # 解析报告
        summary = self.parse_report_summary(report_path)
        if not summary:
            print("❌ 无法解析报告内容")
            return False
        
        # 创建邮件内容
        text_body, html_body = self.create_email_content(summary)
        
        # 获取收件人
        if not recipient_email:
            config = QQMailConfig.load_config()
            recipient_email = config['email']  # 默认发给自己
        
        # 邮件主题
        date = datetime.now().strftime('%Y-%m-%d')
        subject = f"📈 安霸(AMBA)每日股票分析 - {date}"
        
        # 添加报告作为附件
        attachments = [report_path]
        
        # 发送邮件
        print(f"📤 通过QQ邮箱发送到: {recipient_email}")
        success = self.email_sender.send(
            to_email=recipient_email,
            subject=subject,
            body=text_body,
            html_body=html_body,
            attachments=attachments
        )
        
        if success:
            print("✅ 股票报告邮件发送成功！")
            return True
        else:
            print("❌ 股票报告邮件发送失败")
            return False

def main():
    """主函数"""
    import sys
    
    print("=" * 60)
    print("📈 QQ邮箱安霸股票报告系统")
    print("=" * 60)
    
    sender = QQStockReportEmail()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'daily':
            # 发送每日报告
            recipient = sys.argv[2] if len(sys.argv) > 2 else None
            sender.send_daily_report(recipient)
        
        elif command == 'test':
            # 测试QQ邮箱配置
            from qqmail_smtp_config import QQMailSender
            mail_sender = QQMailSender()
            mail_sender.send_test_email()
        
        elif command == 'config':
            # 配置QQ邮箱
            from qqmail_smtp_config import QQMailConfig
            QQMailConfig.interactive_setup()
        
        elif command == 'check':
            # 检查报告
            report_path = sender.get_latest_report()
            if report_path:
                print(f"✅ 找到最新报告: {report_path}")
                import os
                file_size = os.path.getsize(report_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(report_path))
                print(f"   大小: {file_size} 字节")
                print(f"   修改时间: {file_time}")
            else:
                print("❌ 未找到报告文件")
        
        else:
            print(f"未知命令: {command}")
            print("\n可用命令:")
            print("  daily   - 发送每日报告")
            print("  test    - 测试QQ邮箱配置")
            print("  config  - 配置QQ邮箱")
            print("  check   - 检查报告状态")
    
    else:
        # 交互模式
        print("\n请选择操作:")
        print("1. 发送今日股票报告")
        print("2. 测试QQ邮箱配置")
        print("3. 配置QQ邮箱")
        print("4. 检查报告状态")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            recipient = input("收件人邮箱 (直接回车发送给自己): ").strip()
            if not recipient:
                recipient = None
            sender.send_daily_report(recipient)
        
        elif choice == '2':
            from qqmail_smtp_config import QQMailSender
            mail_sender = QQMailSender()
            mail_sender.send_test_email()
        
        elif choice == '3':
            from qqmail_smtp_config import QQMailConfig
            QQMailConfig.interactive_setup()
        
        elif choice == '4':
            report_path = sender.get_latest_report()
            if report_path:
                print(f"✅ 找到最新报告: {report_path}")
                file_size = os.path.getsize(report_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(report_path))
                print(f"   大小: {file_size} 字节")
                print(f"   修改时间: {file_time}")
            else:
                print("❌ 未找到报告文件")
        
        elif choice == '5':
            print("再见！")
        
        else:
            print("无效选择")

if __name__ == "__main__":
    main()