import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Utils.ai_startup_utility3 import AIStartupUtility

# Streamlit App Configuration
# st.set_page_config(page_title="AI Startup Analyzer", layout="centered")

# Streamlit App Configuration
st.set_page_config(
    page_title="AI Startup Analyzer", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .success-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .danger-card {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🚀 AI Startup Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload a startup pitch deck (PDF) to analyze key details, evaluate performance, and generate actionable insights with comprehensive visualizations</p>', unsafe_allow_html=True)


# Initialize AIStartupUtility
utility = AIStartupUtility()




# st.markdown("""
# <div style="text-align: center; font-size: 12px;">
# <a href="https://forms.gle/vqjYzPUBjad5jiyy8">AI Startup Founder Initial Screening Questionnaire</a><br>
# This step is optional but highly recommended to help us better understand your venture
# </div>
# """, unsafe_allow_html=True)


st.markdown("""
<div style="text-align: center; font-size: 14px; margin-bottom: 24px;">
<a href="https://forms.gle/vqjYzPUBjad5jiyy8">AI Startup Founder Initial Screening Questionnaire</a><br>
This step is optional but highly recommended to help us better understand your venture
</div>
""", unsafe_allow_html=True)

# File Uploaders in a modern layout using columns
col1, col2 = st.columns(2)
with col1:
    pitch_deck = st.file_uploader("Upload Mandatory Startup Pitch Deck (PDF)", type=["pdf"], help="Upload a PDF file (max 200MB)")
with col2:
    additional_files = st.file_uploader("Upload Optional Documents (e.g., call transcript, founder copy, email document)", type=["pdf", "docx", "doc", "txt"], accept_multiple_files=True, help="Upload multiple files if needed")


# Apply CSS to center the button
st.markdown(
    """
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Submit button to start analysis
if st.button("Start Analyzing", type="primary") and pitch_deck:
    # Save pitch deck temporarily
    temp_pitch_path = "temp_pitch.pdf"
    with open(temp_pitch_path, "wb") as f:
        f.write(pitch_deck.getbuffer())
    
    # Process pitch deck
    with st.spinner("Processing Pitch Deck PDF..."):
        pitch_result = utility.extract_text_from_pdf(temp_pitch_path)
    
    # Initialize all_content dict with pitch deck
    all_content = {pitch_deck.name: pitch_result}
    
    # Process additional files if any
    for add_file in additional_files or []:
        temp_add_path = f"temp_{add_file.name}"
        with open(temp_add_path, "wb") as f:
            f.write(add_file.getbuffer())
        
        if add_file.type == "application/pdf":
            all_content[add_file.name] = utility.extract_text_from_pdf(temp_add_path)
        elif add_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            all_content[add_file.name] = utility.extract_text_from_docx(temp_add_path)
        elif add_file.type == "text/plain":
            all_content[add_file.name] = utility.extract_text_from_txt(temp_add_path)
        else:
            st.warning(f"Unsupported file type for {add_file.name}. Skipping.")
        
        if os.path.exists(temp_add_path):
            os.remove(temp_add_path)
    
    # Tabbed Interface
    tab1, tab2, tab3, tab4 = st.tabs(["Company Details", "Evaluation Scores", "Final Scores", "Insights"])
    
    # Tab 1: Company Details
    with tab1:
        if all_content:
            with st.spinner("Analyzing company details..."):
                company_document_str = str(all_content)
                company_json = utility.get_company_json_from_gemini(company_document_str)
            
            st.subheader("📋 Company Details")
            if "error" not in company_json:
                # Format company details as a table for better readability
                company_data = {
                    "Field": ["Company Name", "Sector", "Founded", "Team", "Market", "Traction", "Revenue", "Unique Selling Point", "Competition", "Risks"],
                    "Details": [
                        company_json.get("company_name", "N/A"),
                        company_json.get("sector", "N/A"),
                        company_json.get("founded", "N/A"),
                        company_json.get("team", "N/A"),
                        company_json.get("market", "N/A"),
                        company_json.get("traction", "N/A"),
                        company_json.get("revenue", "N/A"),
                        company_json.get("unique_selling_point", "N/A"),
                        company_json.get("competition", "N/A"),
                        company_json.get("risks", "N/A")
                    ]
                }
                company_df = pd.DataFrame(company_data)
                st.dataframe(company_df, use_container_width=True, hide_index=True)
            else:
                st.error("Failed to extract company details.")
    
    # Tab 2: Evaluation Scores
    with tab2:
        if "error" not in company_json:
            with st.spinner("Evaluating startup..."):
                evaluation_data = utility.startup_evaluation(company_json)
            
            if evaluation_data and "error" not in evaluation_data:
                st.subheader("📊 Evaluation Scores")
                # Convert evaluation data to DataFrame
                eval_list = evaluation_data.get("startup_score", [])
                eval_df = pd.DataFrame([
                    {
                        "Parameter": item["Parameter"],
                        "Score": item["Score"],
                        "Threshold": item["Threshold"],
                        "Benchmark Normalized": item["Benchmark_normalized"]
                    } for item in eval_list
                ])
                
                # Display table
                st.dataframe(eval_df, use_container_width=True, hide_index=True)
                
                # Bar Chart for Scores vs Threshold vs Benchmark
                fig_bar = px.bar(
                    eval_df,
                    x="Parameter",
                    y=["Score", "Threshold", "Benchmark Normalized"],
                    barmode="group",
                    title="Evaluation Scores Comparison",
                    labels={"value": "Score", "variable": "Metric"},
                    height=400
                )
                fig_bar.update_layout(xaxis_title="Parameters", yaxis_title="Scores", legend_title="Metrics")
                st.plotly_chart(fig_bar, use_container_width=True)
                
                # Radar Chart for Scores
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=eval_df["Score"],
                    theta=eval_df["Parameter"],
                    fill="toself",
                    name="Score"
                ))
                fig_radar.add_trace(go.Scatterpolar(
                    r=eval_df["Benchmark Normalized"],
                    theta=eval_df["Parameter"],
                    fill="toself",
                    name="Benchmark Normalized"
                ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                    showlegend=True,
                    title="Evaluation Scores Radar Chart",
                    height=400
                )
                st.plotly_chart(fig_radar, use_container_width=True)
                
                # Additional Chart: Line Chart for Cumulative Scores
                eval_df['Cumulative Score'] = eval_df['Score'].cumsum()
                eval_df['Cumulative Benchmark'] = eval_df['Benchmark Normalized'].cumsum()
                fig_line = px.line(
                    eval_df,
                    x="Parameter",
                    y=["Cumulative Score", "Cumulative Benchmark"],
                    title="Cumulative Scores Comparison",
                    height=400
                )
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.error("Failed to evaluate startup due to invalid evaluation data.")
    
    # Tab 3: Final Weighted Scores
    with tab3:
        if "error" not in company_json and evaluation_data and "error" not in evaluation_data:
            with st.spinner("Calculating weighted scores..."):
                final_scores = utility.calculate_final_score_updated(evaluation_data)
            
            st.subheader("🏅 Final Weighted Scores")
            final_scores_df = pd.DataFrame(final_scores)
            st.dataframe(final_scores_df, use_container_width=True, hide_index=True)
            
            # Bar Chart for Weighted Score vs Benchmark
            fig_final = px.bar(
                final_scores_df,
                x="Parameter",
                y=["Weighted_Score", "benchmark_weighted_score"],
                barmode="group",
                title="Weighted Score vs Benchmark Weighted Score",
                labels={"value": "Weighted Score", "variable": "Metric"},
                height=400
            )
            fig_final.update_layout(
                xaxis_title="Parameters",
                yaxis_title="Weighted Scores",
                legend_title="Metrics",
                annotations=[
                    dict(
                        x=0.5,
                        y=1.1,
                        xref="paper",
                        yref="paper",
                        text=f"Total Weighted Score: {final_scores_df['Weighted_Score'].sum():.2f} | Total Benchmark: {final_scores_df['benchmark_weighted_score'].sum():.2f}",
                        showarrow=False,
                        font=dict(size=14)
                    )
                ]
            )
            st.plotly_chart(fig_final, use_container_width=True)
            
            # Gauge Chart for Total Score vs Benchmark
            total_score = final_scores_df['Weighted_Score'].sum()
            total_benchmark = final_scores_df['benchmark_weighted_score'].sum()
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=total_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Total Score (out of 10)"},
                delta={'reference': total_benchmark, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                gauge={
                    'axis': {'range': [0, 10]},
                    'bar': {'color': "darkblue"},
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': total_benchmark
                    }
                }
            ))
            fig_gauge.update_layout(height=400)
            st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Tab 4: Insights and Recommendations
    with tab4:
        if "error" not in company_json and evaluation_data and "error" not in evaluation_data:
            with st.spinner("Generating insights..."):
                uploaded_content_str = str(all_content)
                insights = utility.derive_insight(uploaded_content_str, company_json, evaluation_data, final_scores, 8.0)
            
            st.subheader("💡 Insights and Recommendations")
            
            # Red Flags
            st.markdown("### 🚨 Red Flags")
            for flag in insights.get("red_flags", []):
                with st.expander(flag["description"]):
                    st.markdown(f"**Reference**: {flag['reference']}")
            
            # Green Flags
            st.markdown("### ✅ Green Flags")
            for flag in insights.get("green_flags", []):
                with st.expander(flag["description"]):
                    st.markdown(f"**Reference**: {flag['reference']}")
            
            # Recommendations
            st.markdown("### 📝 Recommendations")
            for i, rec in enumerate(insights.get("recommendations", [])):
                st.markdown(f"{i+1}. {rec}")
    
    # Clean up temporary file
    if os.path.exists(temp_pitch_path):
        os.remove(temp_pitch_path)
else:
    if not pitch_deck:
        st.info("Please upload a PDF pitch deck to begin the analysis.")

st.markdown("---")
# st.markdown("Developed by GenAi_Crew | Powered by Gemini ")

st.markdown("""
<style>
.cool-footer {
    font-family: 'Arial', sans-serif;
    font-size: 16px;
    color: #ffffff;
    background: linear-gradient(90deg, #4b6cb7, #182848);
    padding: 10px 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.cool-footer span.developers {
    font-weight: bold;
    font-size: 18px;
}
.cool-footer span.separator {
    color: #ffd700;
    margin: 0 10px;
}
.cool-footer span.powered {
    font-style: italic;
}
</style>
<div class="cool-footer">
    <span class="developers">Developed by GenAI Crew</span>
    <span class="separator">|</span>
    <span class="powered">Powered by Google's Gemini AI</span>
</div>
""", unsafe_allow_html=True)