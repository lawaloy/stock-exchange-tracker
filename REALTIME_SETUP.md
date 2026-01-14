# Real-Time Dashboard Setup Guide

Your dashboard now supports **real-time data updates**! Here's how everything works.

## 🎯 Three Ways to Get Fresh Data

### 1. Manual Refresh (Immediate) ⚡

**Use the "Refresh Data" button in the dashboard header**

- Click the blue "Refresh Data" button in the top-right
- Dashboard will fetch latest data from Finnhub API
- Takes 3-5 minutes to complete
- Progress shown in real-time
- Dashboard auto-refreshes when done

**Perfect for:**
- Getting latest data right now
- Before making trading decisions
- Testing or ad-hoc updates

### 2. Scheduled Auto-Updates (Recommended) 🔄

**Set up daily automatic updates**

#### Windows:
```bash
# Run as Administrator
setup-scheduled-updates.bat
```

#### Mac/Linux:
```bash
chmod +x setup-scheduled-updates.sh
./setup-scheduled-updates.sh
```

**What it does:**
- Runs stock tracker daily at 4:30 PM (after market close)
- Fetches fresh data automatically
- No manual intervention needed
- Dashboard always shows latest data

**Perfect for:**
- Production/daily use
- Set it and forget it
- Always having current data

### 3. API Integration (Advanced) 🔴

The dashboard backend can fetch live data directly from Finnhub API.

**Configuration:**
- Add `FINNHUB_API_KEY` to backend environment
- Backend will use API for real-time quotes
- Caches data to stay within rate limits
- Updates every 15-30 minutes during market hours

## 🚀 Quick Setup (All Features)

### Step 1: Set Up Scheduled Updates

**Windows (as Administrator):**
```bash
setup-scheduled-updates.bat
```

**Mac/Linux:**
```bash
chmod +x setup-scheduled-updates.sh
./setup-scheduled-updates.sh
```

### Step 2: Verify Setup

1. Open dashboard: http://localhost:3000
2. Look at header - you'll see:
   - **Data from: [date]** - Shows when data was fetched
   - **Refresh Data button** - Click to update now

### Step 3: Test Manual Refresh

1. Click "Refresh Data" button
2. Watch the progress messages
3. Dashboard will reload with fresh data
4. Data timestamp will update

## 📊 How It Works

```
┌─────────────────────────────────────────────────┐
│  Dashboard (Browser)                            │
│  • Shows data timestamp                         │
│  • Has "Refresh Data" button                    │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  FastAPI Backend                                │
│  • Reads latest CSV/JSON files                  │
│  • Triggers stock tracker on demand             │
│  • Polls for refresh completion                 │
└────────────┬────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│  Stock Tracker (main.py)                        │
│  • Fetches from Finnhub API                     │
│  • Generates projections                        │
│  • Saves CSV/JSON files                         │
│  • Runs on schedule OR on-demand               │
└─────────────────────────────────────────────────┘
```

## ⏰ Scheduled Update Details

### Windows Task Scheduler

**Task Name:** `StockTrackerDailyUpdate`

**Schedule:** Daily at 4:30 PM

**View/Edit Task:**
```bash
# Open Task Scheduler
taskschd.msc

# Or command line
schtasks /query /tn StockTrackerDailyUpdate /v /fo list
```

**Delete Task:**
```bash
schtasks /delete /tn StockTrackerDailyUpdate /f
```

### Mac (launchd)

**Service:** `com.stocktracker.daily`

**Schedule:** Daily at 4:30 PM

**View Status:**
```bash
launchctl list | grep stocktracker
```

**Stop/Remove:**
```bash
launchctl unload ~/Library/LaunchAgents/com.stocktracker.daily.plist
rm ~/Library/LaunchAgents/com.stocktracker.daily.plist
```

### Linux (cron)

**View Cron Jobs:**
```bash
crontab -l
```

**Edit Cron Jobs:**
```bash
crontab -e
```

**Remove:**
Delete the line containing `stock-exchange-tracker/main.py`

## 🔍 Troubleshooting

### "Refresh Data" Button Not Working

**Check backend is running:**
```bash
curl http://localhost:8000/health
```

**Check logs:**
```bash
# Backend terminal
# Look for errors when clicking refresh

# Dashboard browser console
# Right-click -> Inspect -> Console tab
```

### Scheduled Task Not Running

**Windows:**
```bash
# Check task history in Task Scheduler
taskschd.msc
# Find StockTrackerDailyUpdate -> History tab
```

**Mac/Linux:**
```bash
# Check logs
cat logs/scheduled_run.log
cat logs/scheduled_run_error.log
```

**Common issues:**
- Python not in PATH
- Virtual environment not activated
- API key not set (if using .env)

### Data Not Updating

**Check data directory:**
```bash
dir data\daily_data_*.csv  # Windows
ls -la data/daily_data_*.csv  # Mac/Linux
```

**Manually run tracker:**
```bash
python main.py
```

If this works, scheduled task has permission/path issues.

## 📱 Using the Dashboard

### Header Features

```
┌─────────────────────────────────────────────────────────┐
│ 📊 Stock Exchange Tracker  Data from: Jan 14, 2026    │
│                                                         │
│                           [Refreshing...] [🔄 Refresh] │
└─────────────────────────────────────────────────────────┘
```

- **Data timestamp**: Shows when data was last fetched
- **Status messages**: Shows refresh progress
- **Refresh button**: 
  - Blue = ready to click
  - Gray + spinning = currently refreshing
  - Takes 3-5 minutes
  - Shows progress messages

### After Refresh

1. ✅ "Data refresh complete!" message appears
2. Dashboard automatically reloads
3. Timestamp updates to current date/time
4. All charts and tables show fresh data

## 🎯 Best Practices

### Daily Workflow

1. **Morning**: Open dashboard to see yesterday's data
2. **Click "Refresh Data"** if you need current prices
3. **Let scheduled task** handle daily updates at 4:30 PM
4. **Next morning**: Fresh data ready automatically

### Production Setup

1. ✅ Run setup script to enable scheduled updates
2. ✅ Test manual refresh works
3. ✅ Verify scheduled task runs successfully
4. ✅ Check logs directory for any errors
5. ✅ Monitor API usage (free tier: 60 calls/min)

### API Rate Limits

**Finnhub Free Tier:**
- 60 API calls per minute
- 250 calls per day (project uses ~241 per run)

**Recommendations:**
- Don't click "Refresh Data" more than 2-3 times per day
- Use scheduled updates instead
- Check Finnhub dashboard: https://finnhub.io/dashboard

## 🔐 Environment Variables

### Backend (.env file)

```bash
# Required for stock tracker
FINNHUB_API_KEY=your-key-here

# Optional for AI summaries
OPENAI_API_KEY=your-key-here

# Optional: Custom data directory
DATA_DIR=/path/to/data
```

## 📈 Success Metrics

After setup, you should see:

✅ Dashboard shows current date (or yesterday if after market close)  
✅ "Refresh Data" button works and shows progress  
✅ Scheduled task appears in task manager/cron  
✅ Daily data files appear in `data/` directory  
✅ Dashboard timestamp updates after refresh  

## 🆘 Need Help?

1. **Check logs**: `logs/stock_tracker_*.log`
2. **Test manually**: `python main.py`
3. **Check API status**: https://finnhub.io/status
4. **View scheduled task**: Task Scheduler (Windows) or `crontab -l` (Linux)
5. **Browser console**: Right-click dashboard -> Inspect -> Console

---

**Your dashboard is now real-time ready! 🚀**

Set up scheduled updates and you'll always have fresh data without any manual work.
