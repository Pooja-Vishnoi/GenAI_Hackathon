import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Utils.ai_startup_utility_improved import AIStartupUtility
import json
from datetime import datetime
import io
import base64
from io import BytesIO
import plotly.io as pio

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
    .blinking {
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.85; transform: scale(1.01); }
        100% { opacity: 1; transform: scale(1); }
    }
    .highlight-button {
        background: linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%);
        border-radius: 3px;
        box-shadow: 0 3px 5px 2px rgba(255, 105, 135, .3);
        color: white;
        padding: 8px 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🚀 AI Startup Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload a startup pitch deck (PDF) to analyze key details, evaluate performance, and generate actionable insights with comprehensive visualizations</p>', unsafe_allow_html=True)


# Initialize AIStartupUtility
utility = AIStartupUtility()

# Initialize session state for storing analysis data
if 'evaluation_data' not in st.session_state:
    st.session_state.evaluation_data = None
if 'company_json' not in st.session_state:
    st.session_state.company_json = None
if 'all_content' not in st.session_state:
    st.session_state.all_content = None
if 'edited_eval_data' not in st.session_state:
    st.session_state.edited_eval_data = None
if 'final_scores' not in st.session_state:
    st.session_state.final_scores = None
if 'insights' not in st.session_state:
    st.session_state.insights = None
if 'has_unsaved_changes' not in st.session_state:
    st.session_state.has_unsaved_changes = False




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
    
    # Store in session state
    st.session_state.all_content = all_content
    
    # Extract company details
    if all_content:
        with st.spinner("Analyzing company details..."):
            company_document_str = str(all_content)
            company_json = utility.get_company_json_from_gemini(company_document_str)
            st.session_state.company_json = company_json
        
        # Evaluate startup if extraction was successful
        if "error" not in company_json:
            with st.spinner("Evaluating startup..."):
                evaluation_data = utility.startup_evaluation(company_json)
                st.session_state.evaluation_data = evaluation_data
                st.session_state.edited_eval_data = None  # Reset edited data
    
    # Clean up temporary file
    if os.path.exists(temp_pitch_path):
        os.remove(temp_pitch_path)

# Display analysis results if data is available in session state
if st.session_state.company_json is not None:
    # Show status indicators with auto-dismiss
    if st.session_state.has_unsaved_changes:
        # Create a placeholder that will auto-clear
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("""
            <div style='background-color: #ffc107; color: #000000; padding: 12px; border-radius: 8px; border-left: 6px solid #ff6b35; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); animation: fadeOut 5s ease-in-out forwards;' class='blinking'>
                <strong style='color: #000000; font-size: 16px;'>⚠️ Unsaved Changes Detected</strong>
                <span style='color: #000000; font-size: 14px;'> - Navigate to the "Evaluation Scores" tab and click "Recalculate" to apply your changes.</span>
            </div>
            <style>
                @keyframes fadeOut {
                    0% { opacity: 1; }
                    70% { opacity: 1; }
                    100% { opacity: 0; display: none; }
                }
            </style>
            """, unsafe_allow_html=True)
    elif st.session_state.edited_eval_data is not None:
        st.markdown("""
        <div style='background-color: #28a745; color: #ffffff; padding: 12px; border-radius: 8px; border-left: 6px solid #155724; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <strong style='color: #ffffff; font-size: 16px;'>✅ Using Custom Values</strong>
            <span style='color: #ffffff; font-size: 14px;'> - Analysis is currently using your edited scores and weights.</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Download buttons row - no extra heading needed
    st.markdown("---")
    download_col1, download_col2, download_col3 = st.columns([3, 3, 3])
    
    if st.session_state.evaluation_data and st.session_state.company_json:
        # Prepare complete analysis data
        download_data = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company_details": st.session_state.company_json,
            "evaluation_scores": st.session_state.edited_eval_data if st.session_state.edited_eval_data else st.session_state.evaluation_data.get("startup_score", []),
            "final_scores": st.session_state.final_scores if st.session_state.final_scores else [],
            "insights": st.session_state.insights if st.session_state.insights else {},
            "analysis_type": "Modified" if st.session_state.edited_eval_data else "Original"
        }
        
        # Convert to JSON
        json_str = json.dumps(download_data, indent=2)
        
        # Generate comprehensive HTML report with charts
        def generate_html_report():
            # Get evaluation data
            eval_data = st.session_state.edited_eval_data if st.session_state.edited_eval_data else st.session_state.evaluation_data.get("startup_score", []) if st.session_state.evaluation_data else []
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Startup Analysis Report - {st.session_state.company_json.get('company_name', 'N/A')}</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    @page {{ size: A4; margin: 2cm; }}
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                        background: #f8f9fa;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 40px;
                        border-radius: 15px;
                        text-align: center;
                        margin-bottom: 30px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    }}
                    .header h1 {{ margin: 0; font-size: 3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }}
                    .header p {{ margin: 10px 0 0 0; font-size: 1.3em; opacity: 0.95; }}
                    .section {{
                        background: white;
                        border: 1px solid #e0e0e0;
                        border-radius: 12px;
                        padding: 25px;
                        margin-bottom: 25px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    .section h2 {{
                        color: #667eea;
                        border-bottom: 3px solid #667eea;
                        padding-bottom: 12px;
                        margin-bottom: 25px;
                        font-size: 1.8em;
                    }}
                    .section h3 {{
                        color: #764ba2;
                        margin-top: 20px;
                        margin-bottom: 15px;
                        font-size: 1.4em;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    }}
                    th {{
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        color: white;
                        padding: 12px;
                        text-align: left;
                        font-weight: 600;
                    }}
                    td {{
                        padding: 12px;
                        border-bottom: 1px solid #e0e0e0;
                    }}
                    tr:hover {{ background: #f5f5f5; }}
                    .metric-card {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        margin: 10px 0;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                    }}
                    .metric-value {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
                    .metric-label {{ font-size: 1.1em; opacity: 0.95; text-transform: uppercase; letter-spacing: 1px; }}
                    .red-flag {{
                        background: #ffebee;
                        border-left: 5px solid #f44336;
                        padding: 15px;
                        margin: 12px 0;
                        border-radius: 6px;
                        box-shadow: 0 2px 4px rgba(244,67,54,0.1);
                    }}
                    .green-flag {{
                        background: #e8f5e9;
                        border-left: 5px solid #4caf50;
                        padding: 15px;
                        margin: 12px 0;
                        border-radius: 6px;
                        box-shadow: 0 2px 4px rgba(76,175,80,0.1);
                    }}
                    .recommendation {{
                        background: #e3f2fd;
                        border-left: 5px solid #2196f3;
                        padding: 15px;
                        margin: 12px 0;
                        border-radius: 6px;
                        box-shadow: 0 2px 4px rgba(33,150,243,0.1);
                        counter-increment: rec-counter;
                    }}
                    .recommendation:before {{
                        content: counter(rec-counter) ". ";
                        font-weight: bold;
                        color: #2196f3;
                    }}
                    .chart-container {{
                        margin: 30px 0;
                        padding: 20px;
                        background: #fafafa;
                        border-radius: 8px;
                        text-align: center;
                    }}
                    .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
                    .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
                    .score-bar {{
                        height: 30px;
                        background: #e0e0e0;
                        border-radius: 15px;
                        overflow: hidden;
                        margin: 10px 0;
                        position: relative;
                    }}
                    .score-fill {{
                        height: 100%;
                        background: linear-gradient(90deg, #4caf50, #8bc34a);
                        border-radius: 15px;
                        display: flex;
                        align-items: center;
                        justify-content: flex-end;
                        padding-right: 10px;
                        color: white;
                        font-weight: bold;
                        transition: width 1s ease;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 40px;
                        padding: 25px;
                        background: linear-gradient(135deg, #f5f5f5, #e0e0e0);
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    }}
                    .insights-summary {{
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 10px;
                        margin: 20px 0;
                    }}
                    .parameter-score {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 10px 0;
                        border-bottom: 1px solid #e0e0e0;
                    }}
                    .parameter-name {{
                        font-weight: 600;
                        color: #333;
                    }}
                    .parameter-value {{
                        display: flex;
                        gap: 20px;
                        align-items: center;
                    }}
                    .badge {{
                        padding: 4px 12px;
                        border-radius: 20px;
                        font-size: 0.9em;
                        font-weight: 600;
                    }}
                    .badge-high {{ background: #c8e6c9; color: #2e7d32; }}
                    .badge-medium {{ background: #fff3cd; color: #856404; }}
                    .badge-low {{ background: #ffcdd2; color: #c62828; }}
                    @media print {{
                        .section {{ page-break-inside: avoid; }}
                        body {{ background: white; }}
                    }}
                    .recommendations-section {{ counter-reset: rec-counter; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🚀 Startup Analysis Report</h1>
                    <p>{st.session_state.company_json.get('company_name', 'N/A')}</p>
                    <p style="font-size: 0.9em;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <div class="section">
                    <h2>📋 Company Overview</h2>
                    <table>
                        <tr><td width="30%"><strong>Company Name</strong></td><td>{st.session_state.company_json.get('company_name', 'N/A')}</td></tr>
                        <tr><td><strong>Sector</strong></td><td>{st.session_state.company_json.get('sector', 'N/A')}</td></tr>
                        <tr><td><strong>Founded</strong></td><td>{st.session_state.company_json.get('founded', 'N/A')}</td></tr>
                        <tr><td><strong>Team</strong></td><td>{st.session_state.company_json.get('team', 'N/A')}</td></tr>
                        <tr><td><strong>Market</strong></td><td>{st.session_state.company_json.get('market', 'N/A')}</td></tr>
                        <tr><td><strong>Traction</strong></td><td>{st.session_state.company_json.get('traction', 'N/A')}</td></tr>
                        <tr><td><strong>Revenue</strong></td><td>{st.session_state.company_json.get('revenue', 'N/A')}</td></tr>
                        <tr><td><strong>Unique Selling Point</strong></td><td>{st.session_state.company_json.get('unique_selling_point', 'N/A')}</td></tr>
                        <tr><td><strong>Competition</strong></td><td>{st.session_state.company_json.get('competition', 'N/A')}</td></tr>
                        <tr><td><strong>Risks</strong></td><td>{st.session_state.company_json.get('risks', 'N/A')}</td></tr>
                    </table>
                </div>
            """
            
            # Add evaluation scores section (raw scores before weighting)
            if eval_data:
                html_content += f"""
                <div class="section">
                    <h2>📊 Initial Evaluation Scores</h2>
                    <h3>Raw Scores Assessment</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Parameter</th>
                                <th>Score</th>
                                <th>Threshold</th>
                                <th>Benchmark</th>
                                <th>Performance</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                for item in eval_data:
                    score_val = float(item.get('Score', 0))
                    threshold_val = float(item.get('Threshold', 0))
                    benchmark_val = float(item.get('Benchmark_normalized', 0))
                    
                    # Determine performance badge
                    if score_val >= benchmark_val:
                        badge = '<span class="badge badge-high">Above Benchmark</span>'
                    elif score_val >= threshold_val:
                        badge = '<span class="badge badge-medium">Meets Threshold</span>'
                    else:
                        badge = '<span class="badge badge-low">Below Threshold</span>'
                    
                    html_content += f"""
                            <tr>
                                <td><strong>{item.get('Parameter', 'N/A')}</strong></td>
                                <td>{score_val:.1f}/10</td>
                                <td>{threshold_val:.1f}/10</td>
                                <td>{benchmark_val:.1f}/10</td>
                                <td>{badge}</td>
                            </tr>
                    """
                html_content += """
                        </tbody>
                    </table>
                    
                    <h3>Score Visualization</h3>
                    <div class="chart-container">
                """
                
                # Add visual score bars
                for item in eval_data:
                    score_val = float(item.get('Score', 0))
                    score_percent = (score_val / 10) * 100
                    html_content += f"""
                        <div style="margin: 15px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span class="parameter-name">{item.get('Parameter', 'N/A')}</span>
                                <span>{score_val:.1f}/10</span>
                            </div>
                            <div class="score-bar">
                                <div class="score-fill" style="width: {score_percent}%;">
                                    {score_val:.1f}
                                </div>
                            </div>
                        </div>
                    """
                
                html_content += """
                    </div>
                </div>
                """
            
            # Add weighted scores section
            if st.session_state.final_scores:
                total_score = sum(score['Weighted_Score'] for score in st.session_state.final_scores)
                total_benchmark = sum(score['benchmark_weighted_score'] for score in st.session_state.final_scores)
                
                html_content += f"""
                <div class="section">
                    <h2>🏆 Overall Performance Summary</h2>
                    <div class="grid">
                        <div class="metric-card">
                            <div class="metric-value">{total_score:.2f}/10</div>
                            <div class="metric-label">Total Score</div>
                        </div>
                        <div class="metric-card" style="background: linear-gradient(135deg, #ffa726, #ff7043);">
                            <div class="metric-value">{total_benchmark:.2f}/10</div>
                            <div class="metric-label">Benchmark</div>
                        </div>
                        <div class="metric-card" style="background: linear-gradient(135deg, {'#26a69a' if total_score > total_benchmark else '#ef5350'}, {'#00897b' if total_score > total_benchmark else '#c62828'});">
                            <div class="metric-value">{total_score - total_benchmark:+.2f}</div>
                            <div class="metric-label">{'Above' if total_score > total_benchmark else 'Below'} Benchmark</div>
                        </div>
                    </div>
                    
                    <div class="insights-summary">
                        <h3>Investment Recommendation</h3>
                        <p style="font-size: 1.1em;">
                """
                
                # Add investment recommendation based on score
                if total_score >= 8.0:
                    html_content += "<strong style='color: #2e7d32;'>✅ STRONG BUY - Excellent investment opportunity with high growth potential</strong>"
                elif total_score >= 7.0:
                    html_content += "<strong style='color: #388e3c;'>✅ BUY - Good investment opportunity with solid fundamentals</strong>"
                elif total_score >= 6.0:
                    html_content += "<strong style='color: #f57c00;'>⚠️ HOLD - Moderate opportunity, requires careful consideration</strong>"
                elif total_score >= 5.0:
                    html_content += "<strong style='color: #ff6f00;'>⚠️ CAUTIOUS - Below average, significant improvements needed</strong>"
                else:
                    html_content += "<strong style='color: #d32f2f;'>❌ AVOID - High risk investment with poor fundamentals</strong>"
                    
                html_content += f"""
                        </p>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📈 Final Weighted Scores</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Parameter</th>
                                <th>Raw Score</th>
                                <th>Weight</th>
                                <th>Weighted Score</th>
                                <th>Benchmark Weighted</th>
                                <th>Gap</th>
                            </tr>
                        </thead>
                        <tbody>
                """
                for score in st.session_state.final_scores:
                    gap = score['Weighted_Score'] - score['benchmark_weighted_score']
                    gap_color = '#4caf50' if gap >= 0 else '#f44336'
                    html_content += f"""
                            <tr>
                                <td><strong>{score['Parameter']}</strong></td>
                                <td>{score['Score']:.1f}/10</td>
                                <td>{score['Weightage']:.0%}</td>
                                <td><strong>{score['Weighted_Score']:.2f}</strong></td>
                                <td>{score['benchmark_weighted_score']:.2f}</td>
                                <td style="color: {gap_color}; font-weight: bold;">{gap:+.2f}</td>
                            </tr>
                    """
                html_content += f"""
                        </tbody>
                        <tfoot>
                            <tr style="background: #f5f5f5; font-weight: bold;">
                                <td>TOTAL</td>
                                <td>-</td>
                                <td>100%</td>
                                <td>{total_score:.2f}/10</td>
                                <td>{total_benchmark:.2f}/10</td>
                                <td style="color: {'#4caf50' if total_score >= total_benchmark else '#f44336'};">{total_score - total_benchmark:+.2f}</td>
                            </tr>
                        </tfoot>
                    </table>
                    
                    <h3>Top Performing Areas</h3>
                    <div class="grid-2">
                """
                
                # Add top and bottom performers
                sorted_scores = sorted(st.session_state.final_scores, key=lambda x: x['Score'], reverse=True)
                top_3 = sorted_scores[:3]
                bottom_3 = sorted_scores[-3:]
                
                html_content += """
                        <div>
                            <h4 style="color: #4caf50;">💪 Strengths</h4>
                """
                for score in top_3:
                    html_content += f"""
                            <div class="parameter-score">
                                <span class="parameter-name">✅ {score['Parameter']}</span>
                                <span class="badge badge-high">{score['Score']:.1f}/10</span>
                            </div>
                """
                
                html_content += """
                        </div>
                        <div>
                            <h4 style="color: #f44336;">📈 Areas for Improvement</h4>
                """
                for score in bottom_3:
                    html_content += f"""
                            <div class="parameter-score">
                                <span class="parameter-name">⚠️ {score['Parameter']}</span>
                                <span class="badge badge-low">{score['Score']:.1f}/10</span>
                            </div>
                """
                
                html_content += """
                        </div>
                    </div>
                </div>
                """
            
            # Add insights section
            if st.session_state.insights:
                # Red Flags section
                red_flags = st.session_state.insights.get('red_flags', [])
                if red_flags:
                    html_content += f"""
                    <div class="section">
                        <h2>🚨 Red Flags - Risk Factors ({len(red_flags)} identified)</h2>
                    """
                    for i, flag in enumerate(red_flags, 1):
                        html_content += f"""
                        <div class="red-flag">
                            <strong>{i}. {flag.get('description', 'N/A')}</strong><br>
                            <small style="color: #666; margin-top: 5px; display: block;">
                                📌 Reference: {flag.get('reference', 'N/A')}
                            </small>
                        </div>
                        """
                    html_content += "</div>"
                
                # Green Flags section
                green_flags = st.session_state.insights.get('green_flags', [])
                if green_flags:
                    html_content += f"""
                    <div class="section">
                        <h2>✅ Green Flags - Positive Indicators ({len(green_flags)} identified)</h2>
                    """
                    for i, flag in enumerate(green_flags, 1):
                        html_content += f"""
                        <div class="green-flag">
                            <strong>{i}. {flag.get('description', 'N/A')}</strong><br>
                            <small style="color: #666; margin-top: 5px; display: block;">
                                📌 Reference: {flag.get('reference', 'N/A')}
                            </small>
                        </div>
                        """
                    html_content += "</div>"
                
                # Recommendations section
                recommendations = st.session_state.insights.get('recommendations', [])
                if recommendations:
                    html_content += f"""
                    <div class="section">
                        <h2>📝 Strategic Recommendations ({len(recommendations)} action items)</h2>
                        <div class="recommendations-section">
                    """
                    for rec in recommendations:
                        html_content += f"""
                        <div class="recommendation">
                            {rec}
                        </div>
                        """
                    html_content += """
                        </div>
                    </div>
                    """
            
            # Add summary insights if not already present
            if not st.session_state.insights or (not st.session_state.insights.get('red_flags') and not st.session_state.insights.get('green_flags')):
                html_content += """
                <div class="section">
                    <h2>📋 Analysis Summary</h2>
                    <div class="insights-summary">
                        <p>Complete analysis has been performed on all available data. Please review the scores and metrics above for detailed insights.</p>
                    </div>
                </div>
                """
            
            # Add charts section with JavaScript
            html_content += """
                <div class="section">
                    <h2>📊 Visual Analytics</h2>
                    <div class="grid-2">
                        <div>
                            <canvas id="barChart"></canvas>
                        </div>
                        <div>
                            <canvas id="radarChart"></canvas>
                        </div>
                    </div>
                </div>
                
                <script>
            """
            
            if eval_data:
                # Prepare data for charts
                labels = [item['Parameter'] for item in eval_data]
                scores = [float(item['Score']) for item in eval_data]
                benchmarks = [float(item['Benchmark_normalized']) for item in eval_data]
                thresholds = [float(item['Threshold']) for item in eval_data]
                
                html_content += f"""
                    // Bar Chart
                    const barCtx = document.getElementById('barChart').getContext('2d');
                    new Chart(barCtx, {{
                        type: 'bar',
                        data: {{
                            labels: {labels},
                            datasets: [{{
                                label: 'Score',
                                data: {scores},
                                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                                borderColor: 'rgba(102, 126, 234, 1)',
                                borderWidth: 2
                            }}, {{
                                label: 'Benchmark',
                                data: {benchmarks},
                                backgroundColor: 'rgba(255, 167, 38, 0.8)',
                                borderColor: 'rgba(255, 167, 38, 1)',
                                borderWidth: 2
                            }}, {{
                                label: 'Threshold',
                                data: {thresholds},
                                backgroundColor: 'rgba(156, 39, 176, 0.8)',
                                borderColor: 'rgba(156, 39, 176, 1)',
                                borderWidth: 2
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: 'Evaluation Scores Comparison'
                                }},
                                legend: {{
                                    display: true,
                                    position: 'top'
                                }}
                            }},
                            scales: {{
                                y: {{
                                    beginAtZero: true,
                                    max: 10
                                }}
                            }}
                        }}
                    }});
                    
                    // Radar Chart
                    const radarCtx = document.getElementById('radarChart').getContext('2d');
                    new Chart(radarCtx, {{
                        type: 'radar',
                        data: {{
                            labels: {labels},
                            datasets: [{{
                                label: 'Score',
                                data: {scores},
                                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                                borderColor: 'rgba(102, 126, 234, 1)',
                                borderWidth: 2,
                                pointBackgroundColor: 'rgba(102, 126, 234, 1)'
                            }}, {{
                                label: 'Benchmark',
                                data: {benchmarks},
                                backgroundColor: 'rgba(255, 167, 38, 0.2)',
                                borderColor: 'rgba(255, 167, 38, 1)',
                                borderWidth: 2,
                                pointBackgroundColor: 'rgba(255, 167, 38, 1)'
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: 'Performance Radar Chart'
                                }}
                            }},
                            scales: {{
                                r: {{
                                    beginAtZero: true,
                                    max: 10
                                }}
                            }}
                        }}
                    }});
                """
            
            html_content += """
                </script>
            """
            
            html_content += f"""
                <div class="footer">
                    <h3>Report Metadata</h3>
                    <p><strong>Company:</strong> {st.session_state.company_json.get('company_name', 'N/A')}</p>
                    <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Analysis Type:</strong> {'Modified (User Adjusted)' if st.session_state.edited_eval_data else 'Original (System Generated)'}</p>
                    <p><strong>Powered by:</strong> AI Startup Analyzer</p>
                    <p><strong>Developed by:</strong> GenAI Crew</p>
                </div>
            </body>
            </html>
            """
            
            return html_content
        
        # Generate professional HTML report
        html_report = generate_html_report()
        
        with download_col1:
            st.download_button(
                label="📑 PROFESSIONAL REPORT",
                data=html_report,
                file_name=f"professional_report_{st.session_state.company_json.get('company_name', 'report').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                help="✅ Beautiful HTML report with all data, charts, and professional formatting - Open in browser to view/print",
                width='stretch',
                type="primary"
            )
        
        with download_col2:
            st.download_button(
                label="📊 Complete Data (JSON)",
                data=json_str,
                file_name=f"complete_analysis_{st.session_state.company_json.get('company_name', 'report').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Raw data in JSON format for integration",
                width='stretch',
                type="secondary"
            )
        
        with download_col3:
            # Comprehensive Excel download
            try:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    # Company Details
                    company_df = pd.DataFrame({
                        'Attribute': ['Company Name', 'Sector', 'Founded', 'Team', 'Market', 'Traction', 
                                     'Revenue', 'USP', 'Competition', 'Risks'],
                        'Value': [
                            st.session_state.company_json.get('company_name', 'N/A'),
                            st.session_state.company_json.get('sector', 'N/A'),
                            st.session_state.company_json.get('founded', 'N/A'),
                            st.session_state.company_json.get('team', 'N/A'),
                            st.session_state.company_json.get('market', 'N/A'),
                            st.session_state.company_json.get('traction', 'N/A'),
                            st.session_state.company_json.get('revenue', 'N/A'),
                            st.session_state.company_json.get('unique_selling_point', 'N/A'),
                            st.session_state.company_json.get('competition', 'N/A'),
                            st.session_state.company_json.get('risks', 'N/A')
                        ]
                    })
                    company_df.to_excel(writer, sheet_name='Company Details', index=False)
                    
                    # Evaluation Scores
                    if st.session_state.evaluation_data:
                        eval_data = st.session_state.edited_eval_data if st.session_state.edited_eval_data else st.session_state.evaluation_data.get("startup_score", [])
                        if eval_data:
                            pd.DataFrame(eval_data).to_excel(writer, sheet_name='Evaluation Scores', index=False)
                    
                    # Final Scores
                    if st.session_state.final_scores:
                        pd.DataFrame(st.session_state.final_scores).to_excel(writer, sheet_name='Final Scores', index=False)
                    
                    # Red and Green Flags
                    if st.session_state.insights:
                        flags_data = []
                        for flag in st.session_state.insights.get('red_flags', []):
                            flags_data.append({
                                'Type': '🚨 Red Flag',
                                'Description': flag.get('description', ''),
                                'Reference': flag.get('reference', '')
                            })
                        for flag in st.session_state.insights.get('green_flags', []):
                            flags_data.append({
                                'Type': '✅ Green Flag',
                                'Description': flag.get('description', ''),
                                'Reference': flag.get('reference', '')
                            })
                        if flags_data:
                            pd.DataFrame(flags_data).to_excel(writer, sheet_name='Flags', index=False)
                        
                        # Recommendations
                        if st.session_state.insights.get('recommendations'):
                            rec_data = [{'Recommendation': rec} for rec in st.session_state.insights['recommendations']]
                            pd.DataFrame(rec_data).to_excel(writer, sheet_name='Recommendations', index=False)
                    
                    writer.close()
                buffer.seek(0)
                
                st.download_button(
                    label="📊 Complete Excel Report",
                    data=buffer,
                    file_name=f"complete_excel_{st.session_state.company_json.get('company_name', 'report').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="✅ Excel with ALL sheets: Company, Scores, Flags, Recommendations",
                    width='stretch',
                    type="secondary"
                )
            except:
                st.button("📊 Excel (Install openpyxl)", disabled=True, width='stretch')
    
    st.divider()
    
    # Tabbed Interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Company Details", "📊 Evaluation Scores (Editable)", "🏅 Final Scores", "💡 Insights", "📥 Export Data"])
    
    # Tab 1: Company Details
    with tab1:
        st.subheader("📋 Company Details")
        company_json = st.session_state.company_json
        if "error" not in company_json:
            # Add export button for company details - styled consistently
            company_export_data = json.dumps(company_json, indent=2)
            st.download_button(
                "📋 Export Company Details",
                data=company_export_data,
                file_name=f"company_details_{company_json.get('company_name', 'report').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                help="Download company details as JSON",
                width='content',
                type="secondary"
            )
            
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
            st.dataframe(company_df, width='stretch', hide_index=True)
        else:
            st.error("Failed to extract company details.")
    
    # Tab 2: Evaluation Scores (Editable)
    with tab2:
        evaluation_data = st.session_state.evaluation_data
        if evaluation_data and "error" not in evaluation_data:
            st.subheader("📊 Evaluation Scores")
            
            # Use edited data if available, otherwise use original data
            if st.session_state.edited_eval_data is not None:
                eval_list = st.session_state.edited_eval_data
            else:
                eval_list = evaluation_data.get("startup_score", [])
            
            # Define weightages for each parameter
            default_weightages = {
                "Team_Quality": 0.15,
                "Market_Size": 0.15,
                "Traction": 0.15,
                "Financials": 0.10,
                "Product_Uniqueness": 0.15,
                "Competitive_Landscape": 0.10,
                "Business_Model_Clarity": 0.10,
                "Risk_Factors": 0.10
            }
            
            # Convert evaluation data to DataFrame with weights
            eval_df_data = []
            for item in eval_list:
                eval_df_data.append({
                    "Parameter": item["Parameter"],
                    "Score": float(item["Score"]),
                    "Threshold": float(item["Threshold"]),
                    "Benchmark_normalized": float(item["Benchmark_normalized"]),
                    "Weight": float(default_weightages.get(item["Parameter"], 0.10))
                })
            
            eval_df = pd.DataFrame(eval_df_data)
            
            # Create instructions container
            instruction_container = st.container()
            
            # Create editable dataframe
            edited_df = st.data_editor(
                eval_df,
                column_config={
                    "Parameter": st.column_config.TextColumn("Parameter", disabled=True),
                    "Score": st.column_config.NumberColumn("Score", min_value=0, max_value=10, step=0.1),
                    "Threshold": st.column_config.NumberColumn("Threshold", min_value=0, max_value=10, step=0.1),
                    "Benchmark_normalized": st.column_config.NumberColumn("Benchmark", min_value=0, max_value=10, step=0.1),
                    "Weight": st.column_config.NumberColumn("Weight", min_value=0, max_value=1, step=0.01, format="%.2f")
                },
                width='stretch',
                hide_index=True,
                key="eval_editor",
                on_change=lambda: setattr(st.session_state, 'has_unsaved_changes', True)
            )
            
            # Check if data has been modified
            data_modified = False
            if not edited_df.equals(eval_df):
                data_modified = True
                st.session_state.has_unsaved_changes = True
            
            # Show warning if there are unsaved changes
            with instruction_container:
                if st.session_state.has_unsaved_changes or data_modified:
                    st.markdown("""
                    <div style='background-color: #ffc107; color: #000000; padding: 15px; border-radius: 8px; border-left: 6px solid #ff6b35; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); animation: pulse 2s ease-in-out infinite;'>
                        <strong style='color: #000000; font-size: 18px;'>⚠️ You have unsaved changes!</strong><br>
                        <span style='color: #000000; font-size: 15px;'>Click the <strong>'🔄 Recalculate'</strong> button below to apply your changes and update the analysis.</span>
                    </div>
                    <style>
                        @keyframes pulse {
                            0% { transform: scale(1); }
                            50% { transform: scale(1.005); }
                            100% { transform: scale(1); }
                        }
                    </style>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #17a2b8; color: #ffffff; padding: 15px; border-radius: 8px; border-left: 6px solid #0c5460; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <strong style='color: #ffffff; font-size: 16px;'>ℹ️ How to edit:</strong><br>
                        <span style='color: #ffffff; font-size: 14px;'>Modify any values in the table below, then click <strong>'🔄 Recalculate'</strong> to update the entire analysis with your changes.</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add buttons for recalculation
            col1, col2, col3 = st.columns([2, 2, 6])
            with col1:
                # Highlight button if there are unsaved changes
                if st.session_state.has_unsaved_changes or data_modified:
                    recalculate_btn = st.button("🔄 **Recalculate Now**", type="primary", help="Apply changes and update analysis", width='stretch')
                else:
                    recalculate_btn = st.button("🔄 Recalculate", type="secondary", help="No changes to apply", width='stretch')
            with col2:
                reset_btn = st.button("🔙 Reset to Original", help="Reset all values to original", width='stretch')
            with col3:
                if st.session_state.has_unsaved_changes or data_modified:
                    st.markdown("<div style='padding: 8px 0;'>👈 <b>Click to apply changes</b></div>", unsafe_allow_html=True)
            
            # Handle recalculation
            if recalculate_btn:
                # Show progress container
                progress_container = st.container()
                
                with progress_container:
                    st.markdown("""
                    <div style='background-color: #007bff; color: #ffffff; padding: 12px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                        <strong style='color: #ffffff; font-size: 16px;'>🔄 Processing your changes...</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Convert edited dataframe back to evaluation data format
                    with st.spinner("📊 Saving edited values..."):
                        edited_eval_list = []
                        for _, row in edited_df.iterrows():
                            edited_eval_list.append({
                                "Parameter": row["Parameter"],
                                "Score": row["Score"],
                                "Threshold": row["Threshold"],
                                "Benchmark_normalized": row["Benchmark_normalized"]
                            })
                        
                        # Store edited data and weights
                        st.session_state.edited_eval_data = edited_eval_list
                        
                        # Create evaluation data dict with edited values
                        edited_evaluation_data = {"startup_score": edited_eval_list}
                        
                        # Update weightages based on edited values
                        edited_weightages = {}
                        for _, row in edited_df.iterrows():
                            edited_weightages[row["Parameter"]] = row["Weight"]
                    
                    # Recalculate final scores with new weightages
                    with st.spinner("🧮 Recalculating weighted scores..."):
                        # Temporarily override the calculate_final_score_updated method to use custom weights
                        original_method = utility.calculate_final_score_updated
                        
                        def custom_calculate_final_score(eval_data):
                            # Use custom weightages
                            result = []
                            input_data = eval_data["startup_score"] if isinstance(eval_data, dict) and "startup_score" in eval_data else eval_data
                            for item in input_data:
                                parameter = item["Parameter"]
                                weight = edited_weightages.get(parameter, 0.10)
                                weighted_score = item["Score"] * weight
                                benchmark_weighted_score = item["Benchmark_normalized"] * weight
                                result.append({
                                    "Parameter": parameter,
                                    "Score": item["Score"],
                                    "Threshold": item["Threshold"],
                                    "Benchmark_normalized": item["Benchmark_normalized"],
                                    "Weightage": weight,
                                    "Weighted_Score": round(weighted_score, 2),
                                    "benchmark_weighted_score": round(benchmark_weighted_score, 2)
                                })
                            return result
                        
                        utility.calculate_final_score_updated = custom_calculate_final_score
                        final_scores = utility.calculate_final_score_updated(edited_evaluation_data)
                        utility.calculate_final_score_updated = original_method  # Restore original method
                        
                        st.session_state.final_scores = final_scores
                    
                    # Regenerate insights with new scores
                    with st.spinner("💡 Regenerating insights and recommendations..."):
                        uploaded_content_str = str(st.session_state.all_content)
                        insights = utility.derive_insight(
                            uploaded_content_str, 
                            st.session_state.company_json, 
                            edited_evaluation_data, 
                            final_scores, 
                            8.0
                        )
                        st.session_state.insights = insights
                    
                    # Reset the unsaved changes flag
                    st.session_state.has_unsaved_changes = False
                    
                    # Show success message with auto-dismiss
                    success_placeholder = st.empty()
                    with success_placeholder.container():
                        st.markdown("""
                        <div style='background-color: #28a745; color: #ffffff; padding: 15px; border-radius: 8px; border-left: 6px solid #155724; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.2); animation: successFade 3s ease-in-out forwards;'>
                            <strong style='color: #ffffff; font-size: 18px;'>✅ Analysis updated successfully!</strong><br>
                            <span style='color: #ffffff; font-size: 14px;'>All scores, insights, and recommendations have been recalculated.</span>
                        </div>
                        <style>
                            @keyframes successFade {
                                0% { opacity: 0; transform: translateY(-10px); }
                                10% { opacity: 1; transform: translateY(0); }
                                80% { opacity: 1; transform: translateY(0); }
                                100% { opacity: 0; }
                            }
                        </style>
                        """, unsafe_allow_html=True)
                    st.balloons()
                    st.rerun()
            
            # Handle reset
            if reset_btn:
                with st.spinner("🔄 Resetting to original values..."):
                    st.session_state.edited_eval_data = None
                    st.session_state.final_scores = None
                    st.session_state.insights = None
                    st.session_state.has_unsaved_changes = False
                
                # Show reset success message with auto-dismiss
                reset_placeholder = st.empty()
                with reset_placeholder.container():
                    st.markdown("""
                    <div style='background-color: #17a2b8; color: #ffffff; padding: 12px; border-radius: 8px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.2); animation: resetFade 2s ease-in-out forwards;'>
                        <strong style='color: #ffffff; font-size: 16px;'>✅ Successfully reset to original values!</strong>
                    </div>
                    <style>
                        @keyframes resetFade {
                            0% { opacity: 0; }
                            20% { opacity: 1; }
                            80% { opacity: 1; }
                            100% { opacity: 0; }
                        }
                    </style>
                    """, unsafe_allow_html=True)
                st.rerun()
            
            # Export options for evaluation scores
            st.divider()
            # Create button layout similar to Recalculate/Reset style
            col1, col2 = st.columns(2)
            with col1:
                # Export current evaluation data as CSV
                current_eval_data = edited_df.to_dict('records')
                csv_data = pd.DataFrame(current_eval_data).to_csv(index=False)
                st.download_button(
                    "📊 Export as CSV",
                    data=csv_data,
                    file_name=f"evaluation_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    help="Download current evaluation scores as CSV",
                    width='stretch',
                    type="secondary"
                )
            with col2:
                # Export evaluation data as JSON
                eval_json = json.dumps(current_eval_data, indent=2)
                st.download_button(
                    "📋 Export as JSON",
                    data=eval_json,
                    file_name=f"evaluation_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    help="Download evaluation scores as JSON",
                    width='stretch',
                    type="secondary"
                )
            
            # Display charts
            st.divider()
            
            # Bar Chart for Scores vs Threshold vs Benchmark
            fig_bar = px.bar(
                edited_df,
                x="Parameter",
                y=["Score", "Threshold", "Benchmark_normalized"],
                barmode="group",
                title="Evaluation Scores Comparison",
                labels={"value": "Score", "variable": "Metric"},
                height=400
            )
            fig_bar.update_layout(xaxis_title="Parameters", yaxis_title="Scores", legend_title="Metrics")
            st.plotly_chart(fig_bar, width='stretch')
            
            # Radar Chart for Scores
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=edited_df["Score"],
                theta=edited_df["Parameter"],
                fill="toself",
                name="Score"
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=edited_df["Benchmark_normalized"],
                theta=edited_df["Parameter"],
                fill="toself",
                name="Benchmark Normalized"
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=True,
                title="Evaluation Scores Radar Chart",
                height=400
            )
            st.plotly_chart(fig_radar, width='stretch')
            
            # Line Chart for Cumulative Scores
            edited_df['Cumulative Score'] = edited_df['Score'].cumsum()
            edited_df['Cumulative Benchmark'] = edited_df['Benchmark_normalized'].cumsum()
            fig_line = px.line(
                edited_df,
                x="Parameter",
                y=["Cumulative Score", "Cumulative Benchmark"],
                title="Cumulative Scores Comparison",
                height=400
            )
            st.plotly_chart(fig_line, width='stretch')
        else:
            st.error("No evaluation data available. Please run the analysis first.")
    
    # Tab 3: Final Weighted Scores
    with tab3:
        if st.session_state.final_scores is not None:
            final_scores = st.session_state.final_scores
        elif st.session_state.evaluation_data and "error" not in st.session_state.evaluation_data:
            # Calculate final scores if not already calculated
            evaluation_data = st.session_state.evaluation_data
            with st.spinner("Calculating weighted scores..."):
                final_scores = utility.calculate_final_score_updated(evaluation_data)
                st.session_state.final_scores = final_scores
        else:
            final_scores = None
        
        if final_scores:
            st.subheader("🏅 Final Weighted Scores")
            
            
            final_scores_df = pd.DataFrame(final_scores)
            
            # Export options for final scores - styled like Recalculate buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                csv_final = final_scores_df.to_csv(index=False)
                st.download_button(
                    "📊 Export Final as CSV",
                    data=csv_final,
                    file_name=f"final_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    help="Download final weighted scores as CSV",
                    width='stretch',
                    type="secondary"
                )
            with col2:
                json_final = json.dumps(final_scores, indent=2)
                st.download_button(
                    "📋 Export Final as JSON",
                    data=json_final,
                    file_name=f"final_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    help="Download final scores as JSON",
                    width='stretch',
                    type="secondary"
                )
            with col3:
                # Create summary text
                total_score = final_scores_df['Weighted_Score'].sum()
                total_benchmark = final_scores_df['benchmark_weighted_score'].sum()
                summary_text = f"FINAL SCORES SUMMARY\n{'='*50}\n"
                summary_text += f"Company: {st.session_state.company_json.get('company_name', 'N/A')}\n"
                summary_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                summary_text += f"Total Score: {total_score:.2f}/10\n"
                summary_text += f"Benchmark: {total_benchmark:.2f}/10\n"
                summary_text += f"Difference: {total_score - total_benchmark:+.2f}\n\n"
                summary_text += "DETAILED SCORES:\n"
                for _, row in final_scores_df.iterrows():
                    summary_text += f"{row['Parameter']}: {row['Score']:.1f} (Weight: {row['Weightage']:.0%}, Weighted: {row['Weighted_Score']:.2f})\n"
                
                st.download_button(
                    "📝 Export Summary Text",
                    data=summary_text,
                    file_name=f"final_scores_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    help="Download summary as text",
                    width='stretch',
                    type="secondary"
                )
            
            st.dataframe(final_scores_df, width='stretch', hide_index=True)
            
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
            st.plotly_chart(fig_final, width='stretch')
            
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
            st.plotly_chart(fig_gauge, width='stretch')
        else:
            st.info("No weighted scores available. Please complete the evaluation first.")
    
    # Tab 4: Insights and Recommendations
    with tab4:
        if st.session_state.insights is not None:
            insights = st.session_state.insights
        elif st.session_state.final_scores is not None:
            # Generate insights if not already generated
            with st.spinner("Generating insights..."):
                uploaded_content_str = str(st.session_state.all_content)
                evaluation_data = {"startup_score": st.session_state.edited_eval_data} if st.session_state.edited_eval_data else st.session_state.evaluation_data
                insights = utility.derive_insight(
                    uploaded_content_str, 
                    st.session_state.company_json, 
                    evaluation_data, 
                    st.session_state.final_scores, 
                    8.0
                )
                st.session_state.insights = insights
        else:
            insights = None
        
        if insights:
            st.subheader("💡 Insights and Recommendations")
            
            # Export options for insights - styled like Recalculate buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                insights_json = json.dumps(insights, indent=2)
                st.download_button(
                    "📋 Export Insights as JSON",
                    data=insights_json,
                    file_name=f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    help="Download all insights as JSON",
                    width='stretch',
                    type="secondary"
                )
            with col2:
                # Create text version of insights
                insights_text = f"INSIGHTS REPORT\n{'='*50}\n"
                insights_text += f"Company: {st.session_state.company_json.get('company_name', 'N/A')}\n"
                insights_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                insights_text += f"RED FLAGS ({len(insights.get('red_flags', []))} identified):\n{'-'*30}\n"
                for i, flag in enumerate(insights.get('red_flags', []), 1):
                    insights_text += f"{i}. {flag.get('description', 'N/A')}\n"
                    insights_text += f"   Reference: {flag.get('reference', 'N/A')}\n\n"
                
                insights_text += f"\nGREEN FLAGS ({len(insights.get('green_flags', []))} identified):\n{'-'*30}\n"
                for i, flag in enumerate(insights.get('green_flags', []), 1):
                    insights_text += f"{i}. {flag.get('description', 'N/A')}\n"
                    insights_text += f"   Reference: {flag.get('reference', 'N/A')}\n\n"
                
                insights_text += f"\nRECOMMENDATIONS ({len(insights.get('recommendations', []))} items):\n{'-'*30}\n"
                for i, rec in enumerate(insights.get('recommendations', []), 1):
                    insights_text += f"{i}. {rec}\n"
                
                st.download_button(
                    "📝 Export Insights as Text",
                    data=insights_text,
                    file_name=f"insights_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    help="Download insights as formatted text",
                    width='stretch',
                    type="secondary"
                )
            with col3:
                # Export as CSV for easy analysis
                insights_list = []
                for flag in insights.get('red_flags', []):
                    insights_list.append({
                        'Type': 'Red Flag',
                        'Description': flag.get('description', ''),
                        'Reference': flag.get('reference', '')
                    })
                for flag in insights.get('green_flags', []):
                    insights_list.append({
                        'Type': 'Green Flag',
                        'Description': flag.get('description', ''),
                        'Reference': flag.get('reference', '')
                    })
                for rec in insights.get('recommendations', []):
                    insights_list.append({
                        'Type': 'Recommendation',
                        'Description': rec,
                        'Reference': ''
                    })
                
                if insights_list:
                    insights_df = pd.DataFrame(insights_list)
                    csv_insights = insights_df.to_csv(index=False)
                    st.download_button(
                        "📊 Export Insights as CSV",
                        data=csv_insights,
                        file_name=f"insights_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download insights as CSV",
                        width='stretch',
                        type="secondary"
                    )
            
            st.divider()
            
            # Red Flags
            st.markdown("### 🚨 Red Flags")
            red_flags = insights.get("red_flags", [])
            if red_flags:
                for flag in red_flags:
                    with st.expander(flag.get("description", "No description")):
                        st.markdown(f"**Reference**: {flag.get('reference', 'N/A')}")
            else:
                st.write("No red flags identified")
            
            # Green Flags
            st.markdown("### ✅ Green Flags")
            green_flags = insights.get("green_flags", [])
            if green_flags:
                for flag in green_flags:
                    with st.expander(flag.get("description", "No description")):
                        st.markdown(f"**Reference**: {flag.get('reference', 'N/A')}")
            else:
                st.write("No green flags identified")
            
            # Recommendations
            st.markdown("### 📝 Recommendations")
            recommendations = insights.get("recommendations", [])
            if recommendations:
                for i, rec in enumerate(recommendations):
                    st.markdown(f"{i+1}. {rec}")
            else:
                st.write("No recommendations available")
        else:
            st.info("No insights available. Please complete the evaluation and score calculation first.")
    
    # Tab 5: Export Data
    with tab5:
        st.subheader("📥 Export Analysis Data")
        st.info("Download your analysis in various formats for reporting and further analysis.")
        
        # Export options
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            st.markdown("### 📄 Export as Excel")
            if st.session_state.evaluation_data and st.session_state.company_json:
                try:
                    # Create Excel buffer
                    buffer = io.BytesIO()
                    
                    # Create Excel writer
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        # Company Details sheet
                        company_data = {
                            "Field": ["Company Name", "Sector", "Founded", "Team", "Market", "Traction", "Revenue", "USP", "Competition", "Risks"],
                            "Details": [
                                st.session_state.company_json.get("company_name", "N/A"),
                                st.session_state.company_json.get("sector", "N/A"),
                                st.session_state.company_json.get("founded", "N/A"),
                                st.session_state.company_json.get("team", "N/A"),
                                st.session_state.company_json.get("market", "N/A"),
                                st.session_state.company_json.get("traction", "N/A"),
                                st.session_state.company_json.get("revenue", "N/A"),
                                st.session_state.company_json.get("unique_selling_point", "N/A"),
                                st.session_state.company_json.get("competition", "N/A"),
                                st.session_state.company_json.get("risks", "N/A")
                            ]
                        }
                        pd.DataFrame(company_data).to_excel(writer, sheet_name='Company Details', index=False)
                        
                        # Evaluation Scores sheet
                        eval_data = st.session_state.edited_eval_data if st.session_state.edited_eval_data else st.session_state.evaluation_data.get("startup_score", [])
                        if eval_data:
                            eval_df = pd.DataFrame(eval_data)
                            eval_df.to_excel(writer, sheet_name='Evaluation Scores', index=False)
                        
                        # Final Scores sheet
                        if st.session_state.final_scores:
                            final_df = pd.DataFrame(st.session_state.final_scores)
                            final_df.to_excel(writer, sheet_name='Final Weighted Scores', index=False)
                        
                        # Insights sheet
                        if st.session_state.insights:
                            insights_data = []
                            for flag in st.session_state.insights.get("red_flags", []):
                                insights_data.append({"Type": "Red Flag", "Description": flag.get("description", ""), "Reference": flag.get("reference", "")})
                            for flag in st.session_state.insights.get("green_flags", []):
                                insights_data.append({"Type": "Green Flag", "Description": flag.get("description", ""), "Reference": flag.get("reference", "")})
                            for i, rec in enumerate(st.session_state.insights.get("recommendations", [])):
                                insights_data.append({"Type": "Recommendation", "Description": rec, "Reference": f"Item {i+1}"})
                            if insights_data:
                                pd.DataFrame(insights_data).to_excel(writer, sheet_name='Insights', index=False)
                        
                        writer.close()
                        
                    buffer.seek(0)
                    
                    st.download_button(
                        label="📊 Download Excel Report",
                        data=buffer,
                        file_name=f"startup_analysis_{st.session_state.company_json.get('company_name', 'report').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Download complete analysis as Excel file with multiple sheets"
                    )
                except Exception as e:
                    st.error(f"Excel export requires 'openpyxl' library. Using JSON export instead.")
                    # Fallback to JSON export
                    download_data = {
                        "company_details": st.session_state.company_json,
                        "evaluation_scores": st.session_state.edited_eval_data if st.session_state.edited_eval_data else st.session_state.evaluation_data.get("startup_score", []),
                        "final_scores": st.session_state.final_scores if st.session_state.final_scores else [],
                        "insights": st.session_state.insights if st.session_state.insights else {}
                    }
                    json_str = json.dumps(download_data, indent=2)
                    st.download_button(
                        label="📄 Download JSON Report",
                        data=json_str,
                        file_name=f"startup_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json",
                        help="Download complete analysis as JSON"
                    )
            else:
                st.warning("Please complete the analysis first.")
        
        with export_col2:
            st.markdown("### 📊 Export as CSV")
            if st.session_state.evaluation_data:
                # Evaluation scores CSV
                eval_data = st.session_state.edited_eval_data if st.session_state.edited_eval_data else st.session_state.evaluation_data.get("startup_score", [])
                if eval_data:
                    eval_df = pd.DataFrame(eval_data)
                    csv = eval_df.to_csv(index=False)
                    st.download_button(
                        label="📈 Download Evaluation Scores CSV",
                        data=csv,
                        file_name=f"evaluation_scores_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download evaluation scores as CSV"
                    )
                
                # Final scores CSV
                if st.session_state.final_scores:
                    final_df = pd.DataFrame(st.session_state.final_scores)
                    csv_final = final_df.to_csv(index=False)
                    st.download_button(
                        label="📉 Download Final Scores CSV",
                        data=csv_final,
                        file_name=f"final_scores_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download final weighted scores as CSV"
                    )
            else:
                st.warning("Please complete the analysis first.")
        
        st.divider()
        
        # Summary Statistics
        st.markdown("### 📊 Summary Statistics")
        if st.session_state.final_scores:
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            final_df = pd.DataFrame(st.session_state.final_scores)
            
            with summary_col1:
                st.metric("Total Score", f"{final_df['Weighted_Score'].sum():.2f} / 10")
            with summary_col2:
                st.metric("Benchmark Score", f"{final_df['benchmark_weighted_score'].sum():.2f} / 10")
            with summary_col3:
                difference = final_df['Weighted_Score'].sum() - final_df['benchmark_weighted_score'].sum()
                st.metric("Difference", f"{difference:+.2f}", delta_color="normal")
            
            # Top performing areas
            st.markdown("#### 🏆 Top Performing Areas")
            top_performers = final_df.nlargest(3, 'Score')[['Parameter', 'Score']]
            for _, row in top_performers.iterrows():
                st.write(f"• **{row['Parameter']}**: {row['Score']:.1f}/10")
            
            # Areas for improvement
            st.markdown("#### 📈 Areas for Improvement")
            bottom_performers = final_df.nsmallest(3, 'Score')[['Parameter', 'Score']]
            for _, row in bottom_performers.iterrows():
                st.write(f"• **{row['Parameter']}**: {row['Score']:.1f}/10")
            
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
