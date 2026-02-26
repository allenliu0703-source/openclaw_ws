# Daily Ambarella Stock Report Setup

## Option 1: System Cron Job (Recommended)

Add this line to your crontab to run the report daily at 8:00 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 8 * * * /home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh
```

## Option 2: Systemd Service & Timer (More Robust)

### 1. Create the service file:

```bash
sudo nano /etc/systemd/system/ambarella-daily-report.service
```

Content:
```ini
[Unit]
Description=Daily Ambarella Stock Analysis Report
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=allen
WorkingDirectory=/home/allen/.openclaw/workspace
ExecStart=/home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh
StandardOutput=journal
StandardError=journal
```

### 2. Create the timer file:

```bash
sudo nano /etc/systemd/system/ambarella-daily-report.timer
```

Content:
```ini
[Unit]
Description=Run Ambarella report daily at 8:00 AM

[Timer]
OnCalendar=*-*-* 08:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

### 3. Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ambarella-daily-report.timer
sudo systemctl start ambarella-daily-report.timer
sudo systemctl status ambarella-daily-report.timer
```

## Option 3: OpenClaw Cron (If Gateway is Working)

Once the OpenClaw gateway authentication is fixed, you can use:

```bash
openclaw cron add --name "ambarella-daily" --schedule "0 8 * * *" --command "/home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh"
```

## Report Location

- **Reports:** `/home/allen/.openclaw/workspace/reports/`
- **Logs:** `/home/allen/.openclaw/workspace/reports/ambarella_report.log`
- **Script:** `/home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh`

## Testing

Test the script manually:
```bash
cd /home/allen/.openclaw/workspace
./daily_ambarella_report_v2.sh
```

View the latest report:
```bash
cat /home/allen/.openclaw/workspace/reports/ambarella_$(date +%Y-%m-%d).md
```

## Next Steps for Real Data

To get real stock data instead of simulated data:

1. **Get Alpha Vantage API Key** (free tier available):
   - Sign up at https://www.alphavantage.co/support/#api-key
   - Free: 5 API calls per minute, 500 per day

2. **Update the script** to use real API data
3. **Add news integration** from financial news APIs
4. **Add email/SMS notifications** for significant price movements

## Features of Current Implementation

✅ **Daily report generation** at 8:00 AM  
✅ **Comprehensive analysis** including:
   - Simulated market data
   - Technical analysis with support/resistance levels
   - Moving averages
   - Company fundamentals
   - Market context
   - Trading strategy
   - Monitoring checklist
✅ **Logging system** for tracking
✅ **Historical tracking** (compares with previous reports)
✅ **Timezone-aware** (GMT+8/Asia Shanghai)

## Manual Setup Instructions

If you prefer to set up the cron job manually right now:

```bash
# 1. Make sure script is executable
chmod +x /home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh

# 2. Add to crontab
(crontab -l 2>/dev/null; echo "0 8 * * * /home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh") | crontab -

# 3. Verify
crontab -l

# 4. Test immediately (optional)
/home/allen/.openclaw/workspace/daily_ambarella_report_v2.sh
```

The report will now run automatically every day at 8:00 AM!