# 📊 AI Data Analyst

An AI-powered Business Intelligence application built with **LangGraph**, **Streamlit**, **Mistral AI**, **Pandas**, and **Plotly**. Upload any CSV file and interact with your data using natural language to generate business insights, dashboards, KPI summaries, and executive reports.

---

## 🚀 Features

- 🤖 AI-powered natural language data analysis
- 📈 Interactive Plotly visualizations
- 📊 KPI Dashboard
- 📄 Executive Business Reports
- 🌍 Region, Product, Category & Profit Analysis
- 🔍 Correlation Analysis
- 📋 Dataset Statistics & Data Quality Checks
- 💬 Conversational AI interface
- ⚡ Multi-Agent Workflow using LangGraph
- 🎨 Modern Streamlit UI

---

## 🏗️ Architecture

```
                User
                  │
                  ▼
          Streamlit Frontend
                  │
                  ▼
            LangGraph Workflow
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
 Supervisor   Analyst Agent  Visualizer Agent
      │           │           │
      └───────────┼───────────┘
                  ▼
             Final Response
                  │
                  ▼
          Streamlit Dashboard
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Frontend | Streamlit |
| Workflow | LangGraph |
| AI Model | Mistral AI |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Environment | Python Dotenv |

---

## 📁 Project Structure

```
AI-Data-Analyst/
│
├── agents/
│   ├── analyst.py
│   ├── supervisor.py
│   └── visualizer.py
│
├── components/
│   ├── chat.py
│   ├── dashboard.py
│   ├── data_preview.py
│   ├── insights.py
│   ├── kpi_cards.py
│   └── styles.py
│
├── graph/
│   ├── nodes.py
│   ├── state.py
│   └── workflow.py
│
├── tools/
│   ├── chart_tool.py
│   ├── pandas_tool.py
│   └── python_tool.py
│
├── utils/
│   ├── llm.py
│   └── prompts.py
│
├── data/
│   └── sales.csv
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 💡 Example Questions

Ask questions such as:

- Total Sales
- Total Profit
- KPI Dashboard
- Sales by Region
- Sales by Product
- Profit Analysis
- Category Analysis
- Correlation Analysis
- Data Quality
- Dataset Summary
- Executive Report
- Full Report
- Dashboard

---

## 📸 Screenshots

### Dashboard



### Executive Report



### KPI Dashboard




## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/FaizullaDataVerse/AI-Data-Analyst.git

cd AI-Data-Analyst
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
MISTRAL_API_KEY="ACDRTocW3fAOX6PBU2Mae8g517gaOVLf"
```

Run the application

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This application can be deployed on **Streamlit Community Cloud**.

Add the following secret:

```toml
MISTRAL_API_KEY="ACDRTocW3fAOX6PBU2Mae8g517gaOVLf"
```

---

## 🎯 Use Cases

- Business Intelligence
- Sales Analysis
- Financial Reporting
- Data Exploration
- Executive Reporting
- KPI Monitoring
- Data Visualization
- AI-powered Analytics

---

## 🔮 Future Improvements

- PDF Report Export
- PowerPoint Export
- Excel Report Export
- Forecasting & Time-Series Analysis
- Anomaly Detection
- Database Connectivity
- Authentication & User Management
- Multi-file Analysis
- SQL Database Support
- AI Insight Recommendations

---

## 👨‍💻 Author

**Faijulla Shabbir Alas**

- GitHub: https://github.com/FaizullaDataVerse
- LinkedIn: 

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
