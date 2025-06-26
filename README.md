# Indium-Project-Smart-Dashboard
A Smart Slack Dashboard Using SlackAPI streamlit psycopg2 and PostgreSQL

project/
│
├── slack_bot/
│   ├── app.py                  # Slack event handler
│   ├── slack_utils.py          # Slack auth, formatting, response handling
│   └── queries.py              # Shared query functions used by bot
│
├── flask_api/
│   ├── app.py                  # Main Flask app
│   ├── endpoints/
│   │   ├── fraud_summary.py    # /fraud-summary
│   │   └── account_summary.py  # /account-summary/<account_id>
│   └── utils.py                # DB connection, helpers
│
├── streamlit_dashboard/
│   ├── app.py                  # Main Streamlit UI
│   └── charts.py               # Graphs like fraud trends, transaction volume
│
├── db/
│   ├── schema.sql              # Optional: DB schema for reference
│   └── db_conn.py              # Connection pool/shared engine
│
├── requirements.txt            # All required packages
└── README.md                   # Setup and run instructions


👥 DIVISION OF WORK
👤 Person 1 – Slack Bot & Query Integration
Tasks:
Create Slack Bot and connect it to a Slack workspace.

Implement parsing of simple commands:
get fraud report for today,
show top transactions for ACC123

Integrate queries.py to fetch data and format Slack responses.

Files to own:
slack_bot/app.py

slack_bot/slack_utils.py

slack_bot/queries.py

Key Skills:
Slack API, Python, string parsing, formatting JSON/text

👤 Person 2 – Flask API Development
Tasks:
Design two endpoints:

/fraud-summary: Aggregate fraud data by date/state/etc.

/account-summary/<account_id>: Detailed report for account/card.

Return JSON responses (or text/HTML if triggered by Slack).

Connect Flask to PostgreSQL using db_conn.py.

Files to own:
flask_api/app.py

flask_api/endpoints/*

db/db_conn.py

Optional: db/schema.sql for DB reference

Key Skills:
Flask, REST APIs, PostgreSQL, JSON formatting

👤 Person 3 – Streamlit Dashboard
Tasks:
Build lightweight UI:

Dropdown for account or card types

Graphs (fraud trend, volume)

Button: "Send this report to Slack"

Use charts.py for visualizations via Plotly/Altair/Matplotlib.

Files to own:
streamlit_dashboard/app.py

streamlit_dashboard/charts.py

Key Skills:
Streamlit, Plotly/Altair, pandas, visualization
