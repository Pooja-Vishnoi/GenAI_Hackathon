import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import asyncio
import nest_asyncio

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from agents import StartupAnalyzerAgent
from agents.root_agent import StartupAnalyzerAgent


# Allow nested event loops (needed for Streamlit + asyncio)
nest_asyncio.apply()

# Helper function to run async functions safely in Streamlit
def run_async(coro):
    """
    Run an async coroutine safely in Streamlit environment.
    Uses a new event loop with proper cleanup handling.
    """
    import warnings
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    
    try:
        # Try to get existing event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run the coroutine
        result = loop.run_until_complete(coro)
        
        # Don't close the loop - let it be reused
        return result
    except Exception as e:
        print(f"Error in run_async: {e}")
        raise

# Streamlit App Configuration
st.set_page_config(
    page_title="AI Startup Analyzer", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
            
    /* Ensure the parent container centers the header */
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        padding: 0;
        background: #f0f2f5;
    }

    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 4rem;
        font-family: 'Poppins', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 800;
        margin: 2rem auto;
        padding: 1.5rem 2rem;
        background: linear-gradient(45deg, #2a5298 0%, #e94057 50%, #8a2be2 100%);
        background-size: 200% 200%;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
        max-width: 90%;
        overflow: hidden;
        transform: translateX(55px);
    }

    @media (max-width: 768px) {
        .main-header {
            font-size: 2.8rem;
            padding: 1rem 1.5rem;
            margin: 1.5rem auto;
            transform: translateX(55px);
        }
    }

    @media (max-width: 480px) {
        .main-header {
            font-size: 2rem;
            padding: 0.75rem 1rem;
            letter-spacing: 0.05em;
            transform: translateX(55px);
        }
    }
.sub-header {
    text-align: center;
    color: #333;
    font-size: 1.5rem;
    font-family: 'Poppins', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    font-weight: 400;
    margin: 0.5rem auto;
    padding: 0.5rem 1rem;
    max-width: 80%;
    transform: translateX(55px);
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid #333;
    animation: 
        typing 3s steps(30, end) forwards,
        blink-caret 0.75s step-end 4, /* Runs 4 times to match typing duration */
        hide-caret 3s steps(1, end) forwards; /* Hides cursor at the end */
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes blink-caret {
    from, to { border-color: transparent; }
    50% { border-color: #333; }
}

@keyframes hide-caret {
    to { border-right: transparent; }
}

@media (max-width: 768px) {
    .main-header {
        font-size: 2.8rem;
        padding: 1rem 1.5rem;
        margin: 1.5rem auto;
        transform: translateX(55px);
    }

    .sub-header {
        font-size: 1.2rem;
        padding: 0.5rem 1rem;
        margin: 0.5rem auto;
        transform: translateX(55px);
        animation: 
            typing 2.5s steps(25, end) forwards,
            blink-caret 0.75s step-end 4, /* Adjusted to match 2.5s typing */
            hide-caret 2.5s steps(1, end) forwards;
    }
}

@media (max-width: 480px) {
    .main-header {
        font-size: 2rem;
        padding: 0.75rem 1rem;
        letter-spacing: 0.05em;
        transform: translateX(55px);
    }

    .sub-header {
        font-size: 1rem;
        padding: 0.5rem 0.75rem;
        margin: 0.5rem auto;
        letter-spacing: 0.03em;
        transform: translateX(55px);
        animation: 
            typing 2s steps(20, end) forwards,
            blink-caret 0.75s step-end 3, /* Adjusted to match 2s typing */
            hide-caret 2s steps(1, end) forwards;
    }
}

</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">    AI Startup Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload a startup pitch deck and generate actionable insights with comprehensive visualizations</p>', unsafe_allow_html=True)


# Initialize ADK Root Agent
analyzer_agent = StartupAnalyzerAgent()

# Custom CSS for enhanced UI/UX
st.markdown("""
<style>
    /* Animated button */
    .questionnaire-button {
        display: inline-block;
        padding: 14px 28px;
        font-size: 16px;
        font-weight: 600;
        color: white !important;
        background: linear-gradient(45deg, #3B82F6, #60A5FA);
        border-radius: 8px;
        text-decoration: none !important;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .questionnaire-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
        background: linear-gradient(45deg, #60A5FA, #3B82F6);
    }
    .questionnaire-button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }
    .questionnaire-button:hover::before {
        width: 300px;
        height: 300px;
    }
    }
    /* Tooltip */
    .questionnaire-button[data-tooltip]:hover:after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #1F2937;
        color: white;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 13px;
        line-height: 1.5;
        white-space: normal;
        width: 260px;
        z-index: 100;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    }




    /* Responsive columns */
    .stColumn > div {
        padding: 10px;
    }
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .questionnaire-button {
            padding: 12px 20px;
            font-size: 14px;
            color: white;
        }
        .questionnaire-button[data-tooltip]:hover:after {
            width: 200px;
            font-size: 12px;
            color: white;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main container for cohesive layout
with st.container():
    # Animated questionnaire button
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <a href="https://forms.gle/vqjYzPUBjad5jiyy8" target="_blank" class="questionnaire-button" 
           data-tooltip="Fill out this optional questionnaire to share insights about your AI startup venture. It helps us tailor our support to your needs!">
            AI Startup Founder Questionnaire
        </a>
    </div>
    """, unsafe_allow_html=True)
    
# File Uploaders in a modern layout using columns
col1, col2 = st.columns(2)
with col1:
    pitch_deck = st.file_uploader("Upload Mandatory Startup Pitch Deck (PDF Recommended)", type=["pdf", "docx", "doc", "txt"], help="Upload a PDF file (max 200MB)")
with col2:
    additional_files = st.file_uploader("Upload Optional Documents (e.g., call transcript, founder copy, email document)", type=["pdf", "docx", "doc", "txt"], accept_multiple_files=True, help="Upload multiple files if needed")



# Apply enhanced CSS styling for the analyze button
st.markdown(
    """
    <style>
    /* Enhanced button styling */
    div.stButton > button {
        display: block;
        margin: 20px auto;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: 600;
        padding: 12px 48px;
        border: none;
        border-radius: 30px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a container for better button positioning and visual feedback
button_container = st.container()
with button_container:
    # Add visual separator and spacing
    st.markdown("""
    <div style='
        margin: 30px 0; 
        text-align: center;
        position: relative;
    '>
        <div style='
            width: 100px; 
            height: 2px; 
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 0 auto 20px auto;
        '></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the button using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Submit button to start analysis with icon
        analyze_clicked = st.button(" Start Analyzing", type="primary", use_container_width=True)
        
        # Add helpful hint below button
        if pitch_deck:
            st.markdown("""
            <div style='
                text-align: center; 
                margin-top: 10px; 
                font-size: 12px; 
                color: #667eea;
                font-style: italic;
            '>
                ✨ Click to analyze your startup pitch deck
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='
                text-align: center; 
                margin-top: 10px; 
                font-size: 12px; 
                color: #ff6b6b;
                font-style: italic;
            '>
                ⚠️ Please upload a pitch deck first
            </div>
            """, unsafe_allow_html=True)
    
    # Initialize session state for analysis results
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    if analyze_clicked and pitch_deck:
        # Process documents using ADK DataProcessingAgent
        with st.spinner("🤖 Processing documents with AI agents..."):
            # Use async function with event loop
            # Use run_async helper for proper event loop handling
            try:
                result = run_async(
                    analyzer_agent.process_startup_documents(pitch_deck, additional_files)
                )
                
                if 'error' in result:
                    st.error(f"Analysis failed: {result['error']}")
                else:
                    st.success("✅ Document processing completed successfully!")
                    
            except Exception as e:
                st.error(f"Agent processing error: {str(e)}")

    # Check analysis status using agent
    analysis_status = analyzer_agent.get_analysis_status()
    
    # Show tabs if analysis has been completed at least once
    if analysis_status['analysis_complete'] and analysis_status['has_company_data']:
        # Tabbed Interface
        tab1, tab2, tab3, tab4 = st.tabs(["Company Details", "Evaluation Scores", "Final Scores", "Insights"])
        
        # Get data from agent session
        session_data = analysis_status['session_data']
        all_content = session_data['all_content']
    
        # Get company analysis from agent session
        company_json = session_data.get('company_json', {})
        
        # Tab 1: Company Details
        with tab1:
            st.subheader("📋 Company Details")
            if company_json and "error" not in company_json:
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
    
        # Get evaluation data from agent session
        evaluation_data = session_data.get('evaluation_data', {})
        
        # Tab 2: Evaluation Scores
        with tab2:
            if evaluation_data and "error" not in evaluation_data:
                st.subheader("Evaluation Scores")
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
    
        # Get or calculate final scores using CalculationAgent
        final_scores = session_data.get('final_scores', [])
        if not final_scores and evaluation_data and "error" not in evaluation_data:
            with st.spinner("🤖 Calculating weighted scores with AI agent..."):
                try:
                    score_result = run_async(
                        analyzer_agent.calculate_scores(evaluation_data)
                    )
                    if 'error' not in score_result:
                        final_scores = score_result['final_scores']
                except Exception as e:
                    st.error(f"Score calculation error: {str(e)}")
        
        # Tab 3: Final Weighted Scores
        with tab3:
            if final_scores:
                st.subheader("🏅 Final Weighted Scores")
                final_scores_df = pd.DataFrame(final_scores)
                
                # Add info message about editable columns
                st.info("💡 You can edit the **Threshold** and **Weightage** columns below. Charts will update only after you click **Recalculate**.")
                
                # Initialize original scores tracking if not exists
                if session_data.get('original_final_scores') is None:
                    analyzer_agent.update_session_data('original_final_scores', final_scores_df.copy())
                
                # Create editable data editor with specific column configuration
                st.caption("You can edit multiple cells below. No processing will occur until you click 'Recalculate'.")
                column_config = {}
                
                # Configure each column - make Threshold and Weightage editable
                for col in final_scores_df.columns:
                    if col.lower() in ['threshold', 'weightage']:
                        if col.lower() == 'threshold':
                            column_config[col] = st.column_config.NumberColumn(
                                label="Threshold",
                                help="Minimum acceptable score (0-10)",
                                min_value=0.0,
                                max_value=10.0,
                                step=0.1,
                                format="%.1f"
                            )
                        elif col.lower() == 'weightage':
                            column_config[col] = st.column_config.NumberColumn(
                                label="Weightage", 
                                help="Relative importance (0-1)",
                                min_value=0.0,
                                max_value=1.0,
                                step=0.01,
                                format="%.2f"
                            )
                    else:
                        # Make all other columns read-only
                        column_config[col] = st.column_config.Column(
                            label=col,
                            disabled=True
                        )
                
                # Get current results from agent session
                # Only set results_df in session if it doesn't exist (first load)
                current_results_df = session_data.get('results_df')
                if current_results_df is None:
                    current_results_df = final_scores_df.copy()
                    # Do NOT update session here; only after recalculation
                
                # Display editable data editor
                edited_df = st.data_editor(
                    current_results_df,
                    column_config=column_config,
                    use_container_width=True,
                    hide_index=True,
                    key="final_scores_editor",
                    num_rows="fixed"
                )

                # Show validation for edited data (but don't calculate weighted scores yet)
                if 'Weightage' in edited_df.columns:
                    weightage_sum = edited_df['Weightage'].sum()
                    if abs(weightage_sum - 1.0) > 0.01:
                        st.warning(f"⚠️ Weightage values sum to {weightage_sum:.3f}. For optimal results, they should sum to 1.0")
                    else:
                        st.success(f"✅ Weightage values sum to {weightage_sum:.3f} - Good!")

                # Check if user has made changes
                has_changes = not edited_df.equals(current_results_df)
                if has_changes:
                    st.info("📝 You have unsaved changes. Click 'Recalculate' to apply them.")

                # Action button - centered
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    recalculate_clicked = st.button("🔄 Recalculate", type="primary", use_container_width=True, key="save_scores", disabled=not has_changes)

                # Only run recalculation and update session if button was explicitly clicked
                if recalculate_clicked and has_changes:
                    # Use CalculationAgent to recalculate scores with edited data
                    with st.spinner("🤖 Recalculating scores with AI agent..."):
                        try:
                            recalc_result = run_async(
                                analyzer_agent.recalculate_scores(edited_df)
                            )
                            if 'error' not in recalc_result:
                                # The agent already updated session with recalculated scores
                                # No need to update again here
                                st.success("✅ Recalculated successfully!")
                                st.rerun()  # Refresh to show updated charts
                            else:
                                st.error(f"Recalculation failed: {recalc_result['error']}")
                        except Exception as e:
                            st.error(f"Agent recalculation error: {str(e)}")

                # Use saved calculated data for charts (only updates after Recalculate)
                _results_df = session_data.get('results_df')
                if _results_df is not None:
                    display_df = _results_df.copy()
                else:
                    display_df = final_scores_df.copy()
                # Show status of displayed data
                if has_changes:
                    st.warning("📊 Charts show previously saved data. Click 'Recalculate' to see updated results.")
                else:
                    st.success("📊 Charts are up-to-date with your current data.")
                
                # Bar Chart for Weighted Score vs Benchmark
                fig_final = px.bar(
                    display_df,
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
                            text=f"Total Weighted Score: {display_df['Weighted_Score'].sum():.3f} | Total Benchmark: {display_df['benchmark_weighted_score'].sum():.3f}",
                            showarrow=False,
                            font=dict(size=14)
                        )
                    ]
                )
                st.plotly_chart(fig_final, use_container_width=True)
                
                # Gauge Chart for Total Score vs Benchmark
                total_score = display_df['Weighted_Score'].sum()
                total_benchmark = display_df['benchmark_weighted_score'].sum()
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=total_score,
                    number={'valueformat': '.3f'},  # Format to 3 decimal places
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Total Score (out of 10)"},
                    delta={
                        'reference': total_benchmark, 
                        'increasing': {'color': "green"}, 
                        'decreasing': {'color': "red"},
                        'valueformat': '.3f'  # Format delta to 3 decimal places
                    },
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
                with st.spinner("🤖 Generating insights with AI agent..."):
                    uploaded_content_str = str(all_content)
                    # Use updated scores from session state if available, otherwise use original
                    current_results_df = session_data.get('results_df')
                    scores_for_insights = current_results_df.to_dict('records') if current_results_df is not None else final_scores
                    
                    # Generate insights using agent - use run_async helper
                    try:
                        insights = run_async(
                            analyzer_agent.generate_insights(
                                uploaded_content_str, company_json, evaluation_data, 
                                scores_for_insights, 8.0
                            )
                        )
                    except Exception as e:
                        st.error(f"❌ Insight generation failed: {str(e)}")
                        insights = {'error': f'Insight generation failed: {str(e)}'}
                
                # Only show insights if generation was successful
                if 'error' not in insights:
                    st.subheader("💡 Insights and Recommendations")
                    
                    # Red Flags
                    st.markdown("### 🚨 Red Flags")
                    red_flags = insights.get("red_flags", [])
                    if red_flags:
                        for flag in red_flags:
                            with st.expander(flag.get("description", "N/A")):
                                st.markdown(f"**Reference**: {flag.get('reference', 'N/A')}")
                    else:
                        st.info("No red flags identified.")
                    
                    # Green Flags
                    st.markdown("### ✅ Green Flags")
                    green_flags = insights.get("green_flags", [])
                    if green_flags:
                        for flag in green_flags:
                            with st.expander(flag.get("description", "N/A")):
                                st.markdown(f"**Reference**: {flag.get('reference', 'N/A')}")
                    else:
                        st.info("No green flags identified.")
                    
                    # Recommendations
                    st.markdown("### 📝 Recommendations")
                    recommendations = insights.get("recommendations", [])
                    if recommendations:
                        for i, rec in enumerate(recommendations):
                            st.markdown(f"{i+1}. {rec}")
                    else:
                        st.info("No recommendations available.")
                else:
                    st.error(f"Failed to generate insights: {insights.get('error', 'Unknown error')}")
            else:
                # Show why insights can't be generated
                if "error" in company_json:
                    st.error(f"❌ Cannot generate insights due to company analysis error: {company_json.get('error')}")
                elif not evaluation_data:
                    st.error("❌ Cannot generate insights: Evaluation data is missing")
                elif "error" in evaluation_data:
                    st.error(f"❌ Cannot generate insights due to evaluation error: {evaluation_data.get('error')}")
                else:
                    st.warning("⚠️ Insights cannot be generated at this time.")
    
    # Show message when no analysis has been done yet
    elif not analysis_status['analysis_complete']:
        st.info("👆 Please upload a pitch deck and click 'Start Analyzing' to begin the analysis.")

# Add a button to start new analysis (clear session state)
if analysis_status['analysis_complete']:
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🆕 Start New Analysis", type="secondary", use_container_width=True):
            # Use agent to reset analysis
            analyzer_agent.reset_analysis()
            st.success("✅ Ready for new analysis! Upload a new pitch deck above.")
            st.rerun()

st.markdown("---")

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
    font-weight: bold;
    font-size: 18px;
}
</style>
<div class="cool-footer">
    Developed by GenAI Crew for Gen AI Exchange Hackathon
</div>
""", unsafe_allow_html=True)
