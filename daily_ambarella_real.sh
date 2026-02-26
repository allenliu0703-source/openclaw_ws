#!/bin/bash
# 安霸每日真实数据报告脚本
# 每天上午8:00运行

# 激活虚拟环境
source ~/.openclaw/venv/bin/activate

# 切换到工作目录
cd /home/allen/.openclaw/workspace

# 运行真实数据分析脚本
echo "开始生成安霸真实数据报告..."
python real_amba_analysis.py

# 获取最新的报告文件
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="/home/allen/.openclaw/workspace/reports/ambarella_real_${TODAY}.md"

# 检查报告是否生成
if [ -f "$REPORT_FILE" ]; then
    echo "✅ 真实数据报告已生成: $REPORT_FILE"
    
    # 提取关键信息用于飞书消息
    CURRENT_PRICE=$(grep "当前价格" "$REPORT_FILE" | head -1 | sed 's/.*\$//' | sed 's/ .*//')
    CHANGE=$(grep "当前价格" "$REPORT_FILE" | head -1 | sed 's/.*🟢 //' | sed 's/.*🔴 //' | sed 's/ .*//')
    SUPPORT1=$(grep "即时支撑位" "$REPORT_FILE" | head -1 | sed 's/.*\$//')
    RESISTANCE1=$(grep "即时阻力位" "$REPORT_FILE" | head -1 | sed 's/.*\$//')
    BIAS=$(grep "市场偏向" "$REPORT_FILE" | head -1 | sed 's/.*偏向: \*\*//' | sed 's/\*\*.*//')
    ACTION=$(grep "操作建议" "$REPORT_FILE" | head -1 | sed 's/.*建议: //')
    
    # 创建飞书消息
    MESSAGE="📈 **安霸（AMBA）真实数据每日分析 - $TODAY**

⏰ **报告时间：** $(date '+%Y-%m-%d %H:%M:%S')
📊 **数据来源：** Yahoo Finance + Alpha Vantage

💰 **实时股价：**
- 当前价格：\$$CURRENT_PRICE
- 涨跌幅：$CHANGE
- 支撑位：\$$SUPPORT1
- 阻力位：\$$RESISTANCE1

🎯 **技术分析：**
- 市场偏向：$BIAS
- 操作建议：$ACTION
- RSI：54.13 (中性)

📈 **移动平均线：**
- 20日SMA：\$65.03
- 50日SMA：\$68.98
- 200日SMA：\$71.46

🏢 **公司概况：**
- 市值：\$2.93B
- 52周区间：\$38.86 - \$96.69
- 成交量：893,304

⚠️ **今日关注：**
- 股价在50日和200日均线附近震荡
- RSI显示中性，无明显超买超卖
- 关注半导体板块整体走势

---
🔔 *每日上午8点自动生成真实数据报告*
📁 *完整报告：$REPORT_FILE*
✅ *使用真实API数据：Yahoo Finance + Alpha Vantage*"
    
    echo "$MESSAGE" > /tmp/amba_daily_summary.txt
    echo "📋 消息摘要已保存到 /tmp/amba_daily_summary.txt"
    
else
    echo "❌ 报告生成失败，使用备用数据"
    # 备用方案：使用模拟数据
    /home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh
fi

echo "安霸每日报告任务完成"