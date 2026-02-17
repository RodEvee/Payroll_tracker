[README.md](https://github.com/user-attachments/files/25374003/README.md)
# 💼 Secure Pay & Benefits Tracker - Streamlit Version

A Python/Streamlit conversion of the React-based payroll tracking application. Track time, calculate pay with overtime, manage benefits, and generate reports.

## ✨ Features

- 🔐 **Authentication System** - Simulated biometric login
- ⏱️ **Time Tracking** - Clock in/out with precise time recording
- 💰 **Salary Calculator** - Automatic calculation with overtime support
- 📊 **Benefits Tracking** - Health, dental, vision, and 401(k) management
- 📈 **Weekly Pay Summary** - Detailed breakdown of gross pay, deductions, and net pay
- 📅 **History & Reports** - View and export time entries (CSV/JSON)
- 🔒 **Session Storage** - Data persists during your browser session
- 📱 **Responsive Design** - Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd payroll-tracker-streamlit
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   
   The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
payroll-tracker-streamlit/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── components/                 # UI Components
│   ├── auth.py                # Authentication screen
│   ├── dashboard.py           # Main dashboard
│   ├── history.py             # History and reports
│   └── settings.py            # Settings page
├── services/                   # Business Logic
│   └── calc_service.py        # Calculation service
└── utils/                      # Utilities
    ├── session.py             # Session management
    └── styles.py              # Custom CSS styles
```

## 📖 Usage Guide

### Authentication

1. Launch the app
2. Enter any username/password OR click "Biometric Login"
3. Demo mode - all logins succeed

### Time Tracking

1. **Dashboard** → Click **"Clock In"**
2. Work timer shows elapsed time
3. Click **"Clock Out"** to record entry
4. View weekly summary automatically

### Viewing History

1. **History** tab from sidebar
2. Filter by date range
3. View statistics and detailed entries
4. Export to CSV or JSON

### Configuring Settings

**Settings** → Three tabs:

#### 💰 Compensation
- Hourly rate
- Overtime threshold (hours/week)
- Overtime multiplier (e.g., 1.5x)

#### 🏥 Benefits
- Health insurance (employee + employer)
- Dental insurance
- Vision insurance
- 401(k) (percentage or fixed amount)

#### 🔒 Security
- Authentication options
- Clear all data
- Logout

## 💻 Development

### Adding Features

The modular structure makes it easy to extend:

- **New calculations**: Edit `services/calc_service.py`
- **New UI components**: Add to `components/`
- **New utilities**: Add to `utils/`

### Adding Database Persistence

Current version uses session state. To add permanent storage:

**Option 1: SQLite (Simplest)**

```python
import sqlite3

def init_db():
    conn = sqlite3.connect('payroll.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS time_entries
                 (id INTEGER PRIMARY KEY, clock_in TEXT, 
                  clock_out TEXT, hours REAL, date TEXT)''')
    conn.commit()
    conn.close()
```

**Option 2: JSON Files**

```python
import json

def save_entries():
    with open('entries.json', 'w') as f:
        json.dump(st.session_state.time_entries, f)

def load_entries():
    try:
        with open('entries.json', 'r') as f:
            return json.load(f)
    except:
        return []
```

## 🌐 Deployment

### Streamlit Cloud (FREE)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Click "Deploy"
5. Done! Get a public URL

### Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create
git push heroku main
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Local Network

```bash
streamlit run app.py --server.address=0.0.0.0
```

Access from other devices: `http://YOUR_IP:8501`

## ⚙️ Configuration

### Port Configuration

```bash
streamlit run app.py --server.port 8502
```

### Custom Config

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#3b82f6"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
headless = true
```

## 🔒 Security Notes

- **Demo Application**: For educational purposes
- **Production Requirements**:
  - Real authentication (OAuth, SAML)
  - Database backend
  - HTTPS encryption
  - Audit logging
  - Input validation
  - Role-based access control

## 🐛 Troubleshooting

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

### Module Import Errors

Make sure you're in the project directory:
```bash
cd payroll-tracker-streamlit
python -m streamlit run app.py
```

### Data Not Saving

Session state is temporary. To persist data:
- Add database (see Development section)
- Or use file storage

## 📊 Calculations Reference

### Hours
- **Regular**: Up to overtime threshold
- **Overtime**: Hours beyond threshold

### Gross Pay
- Regular: `hours × hourly_rate`
- Overtime: `hours × hourly_rate × multiplier`

### Deductions
- Health, Dental, Vision: Fixed weekly amounts
- 401(k): Percentage or fixed amount
- Federal Tax: 15% (demo)
- State Tax: 5% (demo)
- Social Security: 6.2%
- Medicare: 1.45%

### Net Pay
- `Gross Pay - Total Deductions`

## 🤝 Contributing

Contributions welcome! Ideas:
- Database integration
- Data visualizations
- PDF report generation
- Multi-user support
- API integrations
- Email notifications

## 📄 License

MIT License - Free to use and modify

## 🆘 Support

- Check this README
- Review code comments
- Open GitHub issue

## 🎯 Future Enhancements

- [ ] SQLite database persistence
- [ ] Data visualization charts
- [ ] PDF report generation
- [ ] Email weekly summaries
- [ ] Multi-user support
- [ ] API integrations
- [ ] Mobile app version
- [ ] Dark mode theme

---

**Built with Streamlit 🎈 | Python 🐍**

For questions or issues, please open a GitHub issue.
