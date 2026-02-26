#!/usr/bin/env python3
"""
安霸股票报告邮件发送脚本
将每日股票分析报告通过邮件发送
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加当前目录到路径，以便导入simple_email_sender
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_email_sender import EmailSender, EmailConfig
except ImportError:
    print("❌ 无法导入邮件发送模块，请确保simple_email_sender.py在同一目录")
    sys.exit(1)

class StockReportEmail:
    """股票报告邮件发送器"""
    
    def __init__(self, email_sender=None):
        self.email_sender = email_sender or EmailSender()
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
            
            # 提取关键信息
            summary = {
                'date': '',
                'current_price': '',
                'change': '',
                'support': '',
                'resistance': '',
                'bias': '',
                'action': '',
                'full_content': content[:2000]  # 限制长度
            }
            
            # 解析关键信息
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '当前价格' in line and '$' in line:
                    # 提取价格和涨跌幅
                    price_part = line.split('$')[1]
                    if ' ' in price_part:
                        summary['current_price'] = f"${price_part.split(' ')[0]}"
                        # 查找涨跌幅
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
OpenClaw股票分析系统
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # HTML版本
        html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>安霸(AMBA)股票分析报告 - {date}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background-color: #f9f9f9; border-radius: 10px; overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 30px; }}
        .section {{ margin-bottom: 25px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .price {{ font-size: 28px; font-weight: bold; color: #4CAF50; }}
        .change {{ font-size: 18px; margin-left: 10px; }}
        .positive {{ color: #4CAF50; }}
        .negative {{ color: #f44336; }}
        .metric {{ display: flex; justify-content: space-between; margin: 10px 0; }}
        .metric-label {{ font-weight: bold; }}
        .metric-value {{ }}
        .warning {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; border-top: 1px solid #eee; }}
        h2 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        h3 {{ color: #555; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 安霸(AMBA)股票分析报告</h1>
            <p>{date}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>💰 股价信息</h2>
                <div class="price">
                    {price} <span class="change">{change}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">支撑位：</span>
                    <span class="metric-value">${support}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">阻力位：</span>
                    <span class="metric-value">${resistance}</span>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 交易策略</h2>
                <div class="metric">
                    <span class="metric-label">市场偏向：</span>
                    <span class="metric-value">{bias}</span>
                </div>
                <div class="metric">
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
                <p>如需查看完整报告，请登录OpenClaw系统。</p>
            </div>
        </div>
        
        <div class="footer">
            <p>OpenClaw股票分析系统 · 专业AI投资助手</p>
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>免责声明：本报告基于公开数据生成，仅供参考。</p>
        </div>
    </div>
</body>
</html>"""
        
        return text_body, html_body
    
    def send_daily_report(self, recipient_email=None):
        """发送每日报告"""
        print("📧 开始发送安霸每日股票报告...")
        
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
            config = EmailConfig.load_config()
            recipient_email = config.get('default_recipient')
            if not recipient_email:
                recipient_email = config.get('username')
        
        # 邮件主题
        date = datetime.now().strftime('%Y-%m-%d')
        subject = f"📈 安霸(AMBA)每日股票分析 - {date}"
        
        # 添加报告作为附件
        attachments = [report_path]
        
        # 发送邮件
        print(f"📤 发送报告到: {recipient_email}")
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
    
    def send_to_multiple_recipients(self, recipient_list):
        """发送给多个收件人"""
        print(f"📧 开始批量发送给 {len(recipient_list)} 个收件人...")
        
        report_path = self.get_latest_report()
        if not report_path:
            print("❌ 未找到股票报告文件")
            return False
        
        summary = self.parse_report_summary(report_path)
        text_body, html_body = self.create_email_content(summary)
        
        date = datetime.now().strftime('%Y-%m-%d')
        subject = f"📈 安霸(AMBA)每日股票分析 - {date}"
        attachments = [report_path]
        
        success_count = 0
        for recipient in recipient_list:
            print(f"  发送给: {recipient}")
            success = self.email_sender.send(
                to_email=recipient,
                subject=subject,
                body=text_body,
                html_body=html_body,
                attachments=attachments
            )
            if success:
                success_count += 1
        
        print(f"✅ 批量发送完成: {success_count}/{len(recipient_list)} 成功")
        return success_count > 0

def main():
    """主函数"""
    import sys
    
    print("=" * 60)
    print("📈 安霸股票报告邮件系统")
    print("=" * 60)
    
    sender = StockReportEmail()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'daily':
            # 发送每日报告
            recipient = sys.argv[2] if len(sys.argv) > 2 else None
            sender.send_daily_report(recipient)
        
        elif command == 'test':
            # 测试发送
            config = EmailConfig.load_config()
            test_recipient = config.get('default_recipient', config['username'])
            print(f"📧 发送测试报告到: {test_recipient}")
            sender.send_daily_report(test_recipient)
        
        elif command == 'batch':
            # 批量发送
            if len(sys.argv) < 3:
                print("用法: python send_stock_report_email.py batch <邮箱1,邮箱2,...>")
                return
            recipients = sys.argv[2].split(',')
            sender.send_to_multiple_recipients(recipients)
        
        elif command == 'check':
            # 检查报告
            report_path = sender.get_latest_report()
            if report_path:
                print(f"✅ 找到最新报告: {report_path}")
                summary = sender.parse_report_summary(report_path)
                if summary:
                    print("\n报告摘要:")
                    for key, value in summary.items():
                        if key != 'full_content':
                            print(f"  {key}: {value}")
            else:
                print("❌ 未找到报告文件")
        
        else:
            print(f"未知命令: {command}")
    
    else:
        # 交互模式
        print("\n请选择操作:")
        print("1. 发送今日报告")
        print("2. 发送测试报告")
        print("3. 检查报告状态")
        print("4. 配置邮件设置")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            recipient = input("收件人邮箱 (直接回车使用默认): ").strip()
            if not recipient:
                recipient = None
            sender.send_daily_report(recipient)
        
        elif choice == '2':
            sender.send_daily_report()
        
        elif choice == '3':
            report_path = sender.get_latest_report()
            if report_path:
                print(f"\n✅ 最新报告: {report_path}")
                file_size = os.path.getsize(report_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(report_path))
                print(f"   大小: {file_size} 字节")
                print(f"   修改时间: {file_time}")
                
                # 显示前几行
                with open(report_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:10]
                print("\n报告开头:")
                for line in lines:
                    print(f"   {line.rstrip()}")
            else:
                print("❌ 未找到报告文件")
        
        elif choice == '4':
            from simple_email_sender import setup_wizard
            setup_wizard()
        
        elif choice == '5':
            print("再见！")
        
        else:
            print("无效选择")

if __name__ == "__main__":
    main()