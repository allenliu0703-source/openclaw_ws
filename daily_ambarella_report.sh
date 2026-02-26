#!/bin/bash
# Daily Ambarella Stock Analysis Report
# Runs at 8 AM daily

# Set the date
DATE=$(date +%Y-%m-%d)
REPORT_DIR="/home/allen/.openclaw/workspace/reports"
REPORT_FILE="$REPORT_DIR/ambarella_${DATE}.md"

# Create reports directory if it doesn't exist
mkdir -p "$REPORT_DIR"

# Start the report
echo "# Ambarella (AMBA) Daily Stock Analysis - $DATE" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Report generated at:** $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 📊 Current Stock Data" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Try to get stock data from Yahoo Finance (using curl)
echo "### Yahoo Finance Data" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Get current price and basic info
echo "Fetching Ambarella stock data from Yahoo Finance..." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Use curl to get stock data (Yahoo Finance API endpoint)
YAHOO_URL="https://query1.finance.yahoo.com/v8/finance/chart/AMBA?interval=1d&range=1d"
curl -s "$YAHOO_URL" > /tmp/amba_data.json 2>/dev/null

if [ -s /tmp/amba_data.json ]; then
    # Extract data from JSON response
    CURRENT_PRICE=$(cat /tmp/amba_data.json | grep -o '"regularMarketPrice":[0-9.]*' | head -1 | cut -d: -f2)
    PREV_CLOSE=$(cat /tmp/amba_data.json | grep -o '"previousClose":[0-9.]*' | head -1 | cut -d: -f2)
    DAY_HIGH=$(cat /tmp/amba_data.json | grep -o '"regularMarketDayHigh":[0-9.]*' | head -1 | cut -d: -f2)
    DAY_LOW=$(cat /tmp/amba_data.json | grep -o '"regularMarketDayLow":[0-9.]*' | head -1 | cut -d: -f2)
    VOLUME=$(cat /tmp/amba_data.json | grep -o '"regularMarketVolume":[0-9]*' | head -1 | cut -d: -f2)
    
    if [ ! -z "$CURRENT_PRICE" ] && [ ! -z "$PREV_CLOSE" ]; then
        # Calculate change
        CHANGE=$(echo "$CURRENT_PRICE - $PREV_CLOSE" | bc -l 2>/dev/null || echo "0")
        CHANGE_PERCENT=$(echo "($CHANGE / $PREV_CLOSE) * 100" | bc -l 2>/dev/null || echo "0")
        
        echo "| Metric | Value |" >> "$REPORT_FILE"
        echo "|--------|-------|" >> "$REPORT_FILE"
        echo "| **Current Price** | \$$CURRENT_PRICE |" >> "$REPORT_FILE"
        echo "| **Previous Close** | \$$PREV_CLOSE |" >> "$REPORT_FILE"
        echo "| **Daily Change** | \$$(printf "%.2f" $CHANGE) ($(printf "%.2f" $CHANGE_PERCENT)%) |" >> "$REPORT_FILE"
        
        if [ ! -z "$DAY_HIGH" ]; then
            echo "| **Day High** | \$$DAY_HIGH |" >> "$REPORT_FILE"
        fi
        if [ ! -z "$DAY_LOW" ]; then
            echo "| **Day Low** | \$$DAY_LOW |" >> "$REPORT_FILE"
        fi
        if [ ! -z "$VOLUME" ]; then
            # Format volume with commas
            FORMATTED_VOLUME=$(printf "%'d" $VOLUME 2>/dev/null || echo $VOLUME)
            echo "| **Volume** | $FORMATTED_VOLUME |" >> "$REPORT_FILE"
        fi
    else
        echo "Unable to parse stock data from Yahoo Finance." >> "$REPORT_FILE"
    fi
else
    echo "Could not fetch data from Yahoo Finance. Please check internet connection." >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

echo "## 📈 Technical Analysis" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Add technical analysis section
echo "### Key Levels to Watch" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "1. **Support Levels:**" >> "$REPORT_FILE"
echo "   - Immediate: \$$(echo "$CURRENT_PRICE * 0.95" | bc -l 2>/dev/null | xargs printf "%.2f" 2>/dev/null || echo "N/A")" >> "$REPORT_FILE"
echo "   - Strong: \$$(echo "$CURRENT_PRICE * 0.90" | bc -l 2>/dev/null | xargs printf "%.2f" 2>/dev/null || echo "N/A")" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "2. **Resistance Levels:**" >> "$REPORT_FILE"
echo "   - Immediate: \$$(echo "$CURRENT_PRICE * 1.05" | bc -l 2>/dev/null | xargs printf "%.2f" 2>/dev/null || echo "N/A")" >> "$REPORT_FILE"
echo "   - Strong: \$$(echo "$CURRENT_PRICE * 1.10" | bc -l 2>/dev/null | xargs printf "%.2f" 2>/dev/null || echo "N/A")" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "### Market Sentiment" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
if [ ! -z "$CHANGE" ]; then
    if (( $(echo "$CHANGE > 0" | bc -l 2>/dev/null || echo 0) )); then
        echo "🟢 **Bullish** - Stock is trading above previous close" >> "$REPORT_FILE"
    elif (( $(echo "$CHANGE < 0" | bc -l 2>/dev/null || echo 0) )); then
        echo "🔴 **Bearish** - Stock is trading below previous close" >> "$REPORT_FILE"
    else
        echo "⚪ **Neutral** - No change from previous close" >> "$REPORT_FILE"
    fi
else
    echo "Market sentiment data unavailable." >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

echo "## 🏢 Company Overview" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Ambarella, Inc.** is a semiconductor design company known for its high-definition video compression and image processing solutions." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Key Products/Services:**" >> "$REPORT_FILE"
echo "- Computer Vision SoCs" >> "$REPORT_FILE"
echo "- Video Processing Chips" >> "$REPORT_FILE"
echo "- AI-powered camera solutions" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Target Markets:**" >> "$REPORT_FILE"
echo "- Automotive (ADAS, autonomous driving)" >> "$REPORT_FILE"
echo "- Security cameras" >> "$REPORT_FILE"
echo "- Robotics" >> "$REPORT_FILE"
echo "- IoT devices" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 📰 Recent News & Events" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "*(Note: Automated news fetching would require API access)*" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Check for recent:**" >> "$REPORT_FILE"
echo "- Earnings reports" >> "$REPORT_FILE"
echo "- Product announcements" >> "$REPORT_FILE"
echo "- Partnership deals" >> "$REPORT_FILE"
echo "- Analyst upgrades/downgrades" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 💡 Investment Considerations" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "### Bullish Factors" >> "$REPORT_FILE"
echo "1. Growing demand for AI and computer vision chips" >> "$REPORT_FILE"
echo "2. Expansion in automotive sector (ADAS, autonomous vehicles)" >> "$REPORT_FILE"
echo "3. Strong IP portfolio in video processing" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "### Bearish Factors" >> "$REPORT_FILE"
echo "1. Competition from larger semiconductor companies" >> "$REPORT_FILE"
echo "2. Cyclical nature of semiconductor industry" >> "$REPORT_FILE"
echo "3. Dependence on few key customers" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 📅 Next Important Dates" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "1. **Next Earnings Report:** Typically quarterly (check investor relations)" >> "$REPORT_FILE"
echo "2. **Dividend:** Ambarella does not currently pay dividends" >> "$REPORT_FILE"
echo "3. **Analyst Days:** Check company calendar" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 📊 Analyst Consensus" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "*(Note: Analyst data would require financial data API)*" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Typical metrics to track:**" >> "$REPORT_FILE"
echo "- Price targets" >> "$REPORT_FILE"
echo "- Buy/Hold/Sell ratings" >> "$REPORT_FILE"
echo "- Earnings estimates" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Disclaimer:** This report is for informational purposes only and should not be considered financial advice. Always do your own research before making investment decisions." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "*Report generated automatically by OpenClaw Daily Stock Analysis System*" >> "$REPORT_FILE"

# Clean up
rm -f /tmp/amba_data.json

# Make the script executable
chmod +x "$0"

echo "Daily Ambarella report generated: $REPORT_FILE"