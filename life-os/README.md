```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    ██╗     ██╗███████╗███████╗      ██████╗ ███████╗            ║
║    ██║     ██║██╔════╝██╔════╝     ██╔═══██╗██╔════╝            ║
║    ██║     ██║█████╗  █████╗       ██║   ██║███████╗            ║
║    ██║     ██║██╔══╝  ██╔══╝       ██║   ██║╚════██║            ║
║    ███████╗██║██║     ███████╗     ╚██████╔╝███████║            ║
║    ╚══════╝╚═╝╚═╝     ╚══════╝      ╚═════╝ ╚══════╝            ║
║                                                                  ║
║    Wellbeing Dashboard  |  MirAI School of Technology           ║
║    Virtual Summer Internship 2026  |  AI Builder Track          ║
╚══════════════════════════════════════════════════════════════════╝
```

## > ABOUT

Life-OS is a personal wellbeing dashboard that visualizes daily screen
time patterns and deploys a Gemini-powered AI life coach to provide
brutally honest, personalized productivity and lifestyle guidance.

## > STACK

| Component     | Technology               |
|---------------|--------------------------|
| Frontend      | Streamlit                |
| Data Layer    | Pandas + CSV             |
| AI Engine     | Google Gemini (genai)    |
| Avatar Gen    | Pollinations AI          |
| Visualization | Streamlit native charts  |

## > FEATURES

- [x] 14-day synthetic screen time dataset (CSV)
- [x] Interactive sidebar controls (day selector, goal slider)
- [x] KPI metrics row with delta indicators
- [x] Bar chart: today's breakdown by category
- [x] Line chart: 14-day trend over time
- [x] Gemini AI holistic life coach analysis
- [x] Guilt-Trip Avatar (Phase 4 Innovation)
- [x] Severity-aware output (st.warning / st.success)

## > QUICK START

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export GOOGLE_API_KEY=your_key_here

# 3. Run the dashboard
streamlit run app.py --server.port 3000
```

## > PROJECT STRUCTURE

```
life-os/
├── app.py              # Main Streamlit application
├── screentime.csv      # 14-day synthetic screen time data
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Server + theme configuration
└── README.md           # This file
```

## > ENVIRONMENT

```bash
GOOGLE_API_KEY=<your_gemini_api_key>   # Required for AI coaching
```

> Note: Never commit your .env file or API keys to version control.

---
*Built for MirAI School of Technology — AI Builder Capstone 2026*
