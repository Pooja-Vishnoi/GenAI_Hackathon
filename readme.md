Run - streamlit run app.py

🚀 AI-Powered Startup Investment Analysis (ADK Agents)
📌 Project Overview

This project demonstrates an AI-driven pipeline for evaluating startups and generating investor-ready recommendations using ADK (Agent Development Kit).

The system integrates:

🤖 AI Agents (ADK) for red/green flag detection & recommendations

🔥 Firebase for authentication, storage, and user-facing app layer

📊 BigQuery for sector benchmarks, startup analytics, and portfolio tracking

The solution helps investors quickly assess startups based on scores, benchmarks, red/green flags, and generate actionable insights for decision-making.

⚙️ Features

✅ Red Flag Agent – Identifies risks in startup data (financial, hiring, traction).

✅ Green Flag Agent – Highlights positive signals.

✅ Recommendation Agent – Produces final investor recommendations & action items.

🔥 Firebase Integration – Store structured results, handle authentication, sync reports.

📊 BigQuery Integration – Compare startups against sector benchmarks, track historical trends.

📈 Extensible Pipeline – Modular design to add more agents (fraud detection, market analysis, etc.).

🏗️ Project Architecture
flowchart TD
    A[Startup Data Input] --> B[Red Flag Agent]
    A --> C[Green Flag Agent]
    B --> D[Recommendation Agent]
    C --> D
    D --> E[Firebase Firestore]
    D --> F[BigQuery Analytics]
    E --> G[Investor Dashboard]
    F --> G

📂 Project Structure
ai-investment-analysis/
│── agents/
│   ├── red_flag_agent.py
│   ├── green_flag_agent.py
│   ├── recommendation_agent.py
│── utils/
│   ├── firebase_utils.py
│   ├── bigquery_utils.py
│── main_pipeline.py
│── prompt.py
│── requirements.txt
│── README.md

🛠️ Tech Stack

Languages/Frameworks: Python, ADK (Agent Development Kit)

AI/ML: LLM-powered reasoning, scoring, recommendations

Cloud: Firebase (Firestore, Auth, Hosting), BigQuery (Analytics)

Visualization: Streamlit (optional investor dashboard)

🚀 Getting Started
1️⃣ Clone Repo
git clone https://github.com/yourusername/ai-investment-analysis.git
cd ai-investment-analysis

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Setup Firebase

Create Firebase project → enable Firestore & Auth

Download service account JSON → save as firebase_key.json

4️⃣ Setup BigQuery

Create dataset & tables for sector_benchmarks and startup_analysis

Download service account JSON → save as gcp_key.json

5️⃣ Run Pipeline
python main_pipeline.py

📊 Example Output
{
  "startup_id": "fintech_123",
  "overall_score": 82,
  "red_flags": ["High burn rate", "Founder churn risk"],
  "green_flags": ["Strong revenue growth", "Top-tier VCs backing"],
  "recommendations": [
    "Proceed with due diligence on financial sustainability",
    "Consider co-investment with lead VC"
  ]
}

🌟 Use Cases

Investor due diligence

VC portfolio analysis

Startup accelerators evaluating cohorts

Financial analysts exploring risk & opportunity

🧑‍💻 Author

Built by Pooja Vishnoi – AI/ML/GenAI Engineer | Hugging Face AI Agents Certified | AWS Certified AI Practitioner | 10+ years in AI & Software Engineering

🔗 LinkedIn
 | Topmate

📝 License

MIT License – free to use & extend.