# Alerting System Design (Proposed Feature)

## Overview

A flexible alerting system to notify users when stocks meet specific conditions, enabling timely buying decisions.

## Use Cases

### 1. Price-Based Alerts
```
"Alert me when AAPL drops below $150"
"Alert me when TSLA reaches $200"
"Alert me when any S&P 500 stock drops >5% in a day"
```

### 2. Screening-Based Alerts
```
"Alert me when high volume stocks gain >5%"
"Alert me when a stock meets my screening criteria for the first time"
"Alert me when RSI < 30 (oversold)"
```

### 3. Pattern-Based Alerts
```
"Alert me when 50-day MA crosses above 200-day MA (golden cross)"
"Alert me when a stock breaks out of 52-week high"
"Alert me when volume is 3x average"
```

---

## Architecture

```
src/
└── alerts/                          # New module
    ├── __init__.py
    ├── alert_engine.py              # Core alert evaluation
    ├── alert_rules.py               # Rule definitions
    ├── notifiers/                   # Notification channels
    │   ├── __init__.py
    │   ├── sns_notifier.py          # AWS SNS (SMS/Email)
    │   ├── email_notifier.py        # SMTP Email
    │   ├── webhook_notifier.py      # Slack/Discord/Custom
    │   └── base_notifier.py         # Abstract base
    └── alert_storage.py             # Alert history

config/
└── alerts.json                      # User-defined alert rules
```

---

## Configuration Example

### `config/alerts.json`

```json
{
  "alerts": [
    {
      "id": "alert_1",
      "name": "AAPL Price Drop",
      "enabled": true,
      "condition": {
        "type": "price_threshold",
        "symbol": "AAPL",
        "operator": "less_than",
        "value": 150.0
      },
      "notifications": ["sns", "email"],
      "cooldown_minutes": 60
    },
    {
      "id": "alert_2",
      "name": "High Volume Gainers",
      "enabled": true,
      "condition": {
        "type": "screening_match",
        "filters": {
          "volume_threshold": 5000000,
          "min_daily_change_pct": 5.0
        }
      },
      "notifications": ["webhook"],
      "cooldown_minutes": 1440
    },
    {
      "id": "alert_3",
      "name": "Oversold RSI",
      "enabled": false,
      "condition": {
        "type": "technical_indicator",
        "indicator": "RSI",
        "period": 14,
        "operator": "less_than",
        "value": 30
      },
      "notifications": ["email"],
      "cooldown_minutes": 360
    }
  ]
}
```

---

## Environment Variables

```bash
# AWS SNS
AWS_REGION=us-east-1
AWS_SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789:stock-alerts
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL_TO=recipient@example.com

# Webhook
WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## Implementation Plan

### Phase 1: Core Alert Engine (2-3 days)
- [ ] Alert rule parser
- [ ] Condition evaluator
- [ ] Alert storage (history)
- [ ] Cooldown mechanism

### Phase 2: Basic Notifications (1-2 days)
- [ ] Email notifier (SMTP)
- [ ] Webhook notifier (generic HTTP POST)
- [ ] Notification formatting

### Phase 3: AWS Integration (1-2 days)
- [ ] SNS notifier (SMS/Email)
- [ ] AWS credentials handling
- [ ] Error handling and retries

### Phase 4: Advanced Features (3-4 days)
- [ ] Technical indicators (RSI, MACD)
- [ ] Pattern detection
- [ ] Multi-condition alerts (AND/OR logic)
- [ ] Alert templates

### Phase 5: UI/UX (2-3 days)
- [ ] CLI for managing alerts
- [ ] Alert testing/dry-run mode
- [ ] Alert history viewer
- [ ] Alert performance metrics

---

## Example Usage

### CLI Commands (Proposed)

```bash
# List alerts
python main.py alerts list

# Add alert
python main.py alerts add \
  --name "AAPL Price Drop" \
  --condition "price < 150" \
  --symbol AAPL \
  --notify sns

# Test alert
python main.py alerts test alert_1

# Enable/disable
python main.py alerts enable alert_1
python main.py alerts disable alert_1

# View history
python main.py alerts history --days 7
```

### Programmatic Usage

```python
from src.alerts import AlertEngine, PriceThresholdAlert, SNSNotifier

# Create alert
alert = PriceThresholdAlert(
    symbol="AAPL",
    threshold=150.0,
    operator="less_than"
)

# Add notifier
notifier = SNSNotifier(topic_arn=os.getenv("AWS_SNS_TOPIC_ARN"))
alert.add_notifier(notifier)

# Evaluate
engine = AlertEngine()
engine.add_alert(alert)
engine.evaluate(stock_data)  # Checks all alerts
```

---

## Notification Examples

### SMS (via AWS SNS)
```
🚨 Stock Alert: AAPL Price Drop

Apple Inc (AAPL) is now $148.50
Condition: Price < $150.00
Change: -2.5% today

Time: 2026-01-04 14:30:00 UTC
```

### Email
```
Subject: 🚨 Stock Alert: High Volume Gainers

You have 3 stocks matching your "High Volume Gainers" alert:

1. NVDA (NVIDIA) - $450.25 (+5.8%, vol: 52M)
2. AMD (AMD) - $125.80 (+6.2%, vol: 48M)
3. INTC (Intel) - $42.10 (+5.1%, vol: 65M)

View details: [link to dashboard]
Manage alerts: [link to settings]
```

### Slack Webhook
```json
{
  "text": "🚨 Stock Alert Triggered",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*AAPL Price Drop Alert*\nApple Inc (AAPL) is now $148.50\nCondition: Price < $150.00"
      }
    }
  ]
}
```

---

## Technical Considerations

### Rate Limiting
- Cooldown periods prevent alert spam
- Per-alert cooldown configuration
- Global rate limits for notifications

### Data Requirements
- Real-time or near-real-time data needed
- May require WebSocket or streaming API
- Consider API call costs for frequent checks

### Reliability
- Alert evaluation should be idempotent
- Retry failed notifications
- Store alert history for audit

### Security
- Secure credential storage
- Encrypted notification channels
- Alert access control (if multi-user)

---

## Testing Strategy

```python
# Unit tests
def test_price_threshold_alert_triggers():
    alert = PriceThresholdAlert("AAPL", 150, "less_than")
    stock = {"symbol": "AAPL", "close": 148.0}
    assert alert.evaluate(stock) == True

# Integration tests
def test_sns_notification_sent():
    notifier = SNSNotifier(topic_arn="test-topic")
    result = notifier.send("Test message")
    assert result.status_code == 200

# End-to-end tests
def test_full_alert_workflow():
    # Create alert → evaluate → notify → verify history
    pass
```

---

## Future Enhancements

- **AI-powered alerts**: "Alert me when this stock is a good buy"
- **Portfolio alerts**: Track entire portfolio performance
- **Social alerts**: Alert when a stock is trending on Twitter/Reddit
- **Backtest alerts**: Test alert rules against historical data
- **Mobile app**: Push notifications to mobile devices

---

## Cost Considerations

### AWS SNS Pricing (as of 2026)
- SMS: $0.00645 per message (US)
- Email: $2 per 100,000 emails
- Very affordable for personal use

### Alternative Free Options
- SMTP email (Gmail, Outlook)
- Webhook to free services (Discord, Telegram)
- Local notifications (desktop/mobile)

---

## Priority: HIGH

This feature directly enables the core use case: **making timely buy/sell decisions**.

**Estimated Effort**: 2-3 weeks for full implementation
**Impact**: Very High - enables proactive trading
**Dependencies**: None (can be built independently)

---

## Contributing

Want to implement this feature? See [CONTRIBUTING.md](../CONTRIBUTING.md) and start with Phase 1!

**Contact**: Open an issue with tag `feature: alerting` to discuss implementation details.

