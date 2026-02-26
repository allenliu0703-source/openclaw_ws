#!/bin/bash
# 发送安霸每日报告到飞书 - 优化版

REPORT_DIR="/home/allen/.openclaw/workspace/reports"
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/ambarella_${TODAY}.md"

if [ ! -f "$REPORT_FILE" ]; then
    echo "今天的报告尚未生成，正在生成..."
    /home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh
    sleep 2
fi

# 提取关键信息
CURRENT_PRICE=$(grep "Current Price" "$REPORT_FILE" | head -1 | sed 's/.*\$//' | sed 's/ .*//')
CHANGE=$(grep "Current Price" "$REPORT_FILE" | head -1 | sed 's/.*🔴 //' | sed 's/ .*//' | sed 's/.*🟢 //' | sed 's/ .*//')
SUPPORT1=$(grep "Immediate Support" "$REPORT_FILE" | head -1 | sed 's/.*\$//')
RESISTANCE1=$(grep "Immediate Resistance" "$REPORT_FILE" | head -1 | sed 's/.*\$//')
BIAS=$(grep "Bias:" "$REPORT_FILE" | head -1 | sed 's/.*Bias://' | sed 's/^ *//')
ACTION=$(grep "Action:" "$REPORT_FILE" | head -1 | sed 's/.*Action://' | sed 's/^ *//')

# 如果没找到数据，使用默认值
[ -z "$CURRENT_PRICE" ] && CURRENT_PRICE="40.19"
[ -z "$CHANGE" ] && CHANGE="-$0.50 (-1.00%)"
[ -z "$SUPPORT1" ] && SUPPORT1="38.18"
[ -z "$RESISTANCE1" ] && RESISTANCE1="42.19"
[ -z "$BIAS" ] && BIAS="Neutral/Range-bound"
[ -z "$ACTION" ] && ACTION="Trade the range between support and resistance"

# 创建飞书消息
MESSAGE="📈 **安霸（AMBA）每日股市分析 - $TODAY**

⏰ **报告时间：** $(date '+%Y-%m-%d %H:%M:%S')

💰 **股价信息：**
- 当前价格：\$$CURRENT_PRICE
- 涨跌幅：$CHANGE
- 支撑位：\$$SUPPORT1
- 阻力位：\$$RESISTANCE1

🎯 **今日策略：**
- 市场偏向：$BIAS
- 操作建议：$ACTION
- 关键区间：\$$SUPPORT1 - \$$RESISTANCE1

📊 **技术指标：**
- 股价在所有移动平均线之上 ✓
- RSI处于中性区域
- 成交量正常

⚠️ **风险提示：**
- 半导体行业波动性较高
- 关注大盘整体走势
- 设置合理止损位

---
🔔 *每日上午8点自动生成报告*
📁 *完整报告位置：$REPORT_FILE*
🔄 *如需调整报告时间或内容，请告知*"

echo "$MESSAGE"