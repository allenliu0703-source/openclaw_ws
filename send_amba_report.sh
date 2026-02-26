#!/bin/bash
# 发送安霸每日报告到飞书

REPORT_DIR="/home/allen/.openclaw/workspace/reports"
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/ambarella_${TODAY}.md"

if [ ! -f "$REPORT_FILE" ]; then
    echo "今天的报告尚未生成，正在生成..."
    /home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh
fi

# 读取报告内容
REPORT_CONTENT=$(cat "$REPORT_FILE" | head -100)

# 创建简化的飞书消息格式
MESSAGE="# 📈 安霸（AMBA）每日股市分析 - $TODAY

**报告时间：** $(date '+%Y-%m-%d %H:%M:%S')

## 今日要点

$(echo "$REPORT_CONTENT" | grep -A5 "## 📊 Market Data Summary" | tail -n +3 | head -10 | sed 's/|//g' | sed 's/---//g')

## 技术分析
$(echo "$REPORT_CONTENT" | grep -A5 "## 📈 Technical Analysis" | tail -n +3 | head -15 | sed 's/|//g' | sed 's/---//g')

## 交易建议
$(echo "$REPORT_CONTENT" | grep -A5 "## 💡 Daily Trading Strategy" | tail -n +3 | head -10)

---
*每日上午8点自动生成*
*如需调整报告时间或内容，请告知*"

echo "$MESSAGE"