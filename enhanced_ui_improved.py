import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Utils.ai_startup_utility_improved import AIStartupUtility



# Since we're using st.data_editor directly in the main code, we no longer need this function


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


# Initialize AIStartupUtility
utility = AIStartupUtility()

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
        
        # Store analysis data in session state
        st.session_state.all_content = all_content
        st.session_state.analysis_complete = True
        
        # Clean up temporary file
        if os.path.exists(temp_pitch_path):
            os.remove(temp_pitch_path)

    # Show tabs if analysis has been completed at least once
    if st.session_state.analysis_complete and 'all_content' in st.session_state:
        # Tabbed Interface
        tab1, tab2, tab3, tab4 = st.tabs(["Company Details", "Evaluation Scores", "Final Scores", "Insights"])
        
        # Get all_content from session state
        all_content = st.session_state.all_content
    
        # Get or calculate company analysis (cached in session state)
        if 'company_json' not in st.session_state:
            if all_content:
                with st.spinner("Analyzing company details..."):
                    company_document_str = str(all_content)
                    st.session_state.company_json = utility.get_company_json_from_gemini(company_document_str)
        
        company_json = st.session_state.get('company_json', {})
        
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
    
        # Get or calculate evaluation data (cached in session state)
        if 'evaluation_data' not in st.session_state and company_json and "error" not in company_json:
            with st.spinner("Evaluating startup..."):
                st.session_state.evaluation_data = utility.startup_evaluation(company_json)
        
        evaluation_data = st.session_state.get('evaluation_data', {})
        
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
    
        # Get or calculate final scores (cached in session state)
        if 'final_scores' not in st.session_state and evaluation_data and "error" not in evaluation_data:
            with st.spinner("Calculating weighted scores..."):
                st.session_state.final_scores = utility.calculate_final_score_updated(evaluation_data)
        
        final_scores = st.session_state.get('final_scores', [])
        
        # Tab 3: Final Weighted Scores
        with tab3:
            if final_scores:
                st.subheader("🏅 Final Weighted Scores")
                final_scores_df = pd.DataFrame(final_scores)
                
                # Store original data in session state for editing
                if 'results_df' not in st.session_state:
                    st.session_state.results_df = final_scores_df.copy()
                
                # Initialize original scores tracking if not exists
                if 'original_final_scores' not in st.session_state:
                    st.session_state.original_final_scores = final_scores_df.copy()
                
                # Initialize edited_pending flag to track unsaved changes
                if 'edits_pending' not in st.session_state:
                    st.session_state.edits_pending = False
                
                # Add info message about editable columns
                st.info("💡 You can edit the **Threshold** and **Weightage** columns below. Make all your changes, then click **Save Changes** to recalculate scores.")
                
                # Create editable data editor with specific column configuration
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
                
                # Display editable data editor
                edited_df = st.data_editor(
                    st.session_state.results_df,
                    column_config=column_config,
                    use_container_width=True,
                    hide_index=True,
                    key="final_scores_editor",
                    num_rows="fixed"
                )
                
                # Check if there are any changes between edited_df and results_df
                if not edited_df.equals(st.session_state.results_df):
                    st.session_state.edits_pending = True
                    st.warning("⚠️ You have unsaved changes. Click **Save Changes** to recalculate scores with your edits.")
                
                # Use the saved results_df for display (not the edited_df until saved)
                display_df = st.session_state.results_df.copy()
                
                # Validation for Weightage column (using current edited data)
                if 'Weightage' in display_df.columns:
                    weightage_sum = display_df['Weightage'].sum()
                    if abs(weightage_sum - 1.0) > 0.01:
                        st.warning(f"⚠️ Weightage values sum to {weightage_sum:.3f}. For optimal results, they should sum to 1.0")
                    else:
                        st.success(f"✅ Weightage values sum to {weightage_sum:.3f} - Good!")
                
                # Update session state only when explicitly requested (avoid automatic updates)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("💾 Save Changes", type="primary", use_container_width=True, key="save_scores"):
                        with st.spinner("🔄 Recalculating scores... Please wait."):
                            # Recalculate weighted scores with the edited values
                            updated_df = edited_df.copy()
                            if 'Weightage' in updated_df.columns and 'Score' in updated_df.columns:
                                updated_df['Weighted_Score'] = updated_df['Score'] * updated_df['Weightage']
                            
                            if 'Weightage' in updated_df.columns and 'Benchmark_normalized' in updated_df.columns:
                                updated_df['benchmark_weighted_score'] = updated_df['Benchmark_normalized'] * updated_df['Weightage']
                            
                            # Update session state with recalculated values
                            st.session_state.results_df = updated_df.copy()
                            st.session_state.edits_pending = False
                            # Clear cached insights to force regeneration with new scores
                            if 'cached_insights' in st.session_state:
                                del st.session_state['cached_insights']
                        st.success("✅ Changes saved and scores recalculated successfully!")
                        st.rerun()
                
                with col3:
                    if st.button("🔄 Reset to Original", type="secondary", use_container_width=True, key="reset_scores"):
                        # Reset to original values
                        if 'original_final_scores' in st.session_state:
                            st.session_state.results_df = st.session_state.original_final_scores.copy()
                        else:
                            st.session_state.results_df = final_scores_df.copy()
                        st.session_state.edits_pending = False
                        # Clear cached insights to force regeneration with new scores
                        if 'cached_insights' in st.session_state:
                            del st.session_state['cached_insights']
                        st.success("✅ Values reset to original!")
                        st.rerun()
                
                # Always use display_df for charts (shows saved state only)
                
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
                # Check if insights are already cached
                if 'cached_insights' not in st.session_state:
                    with st.spinner("Generating insights..."):
                        uploaded_content_str = str(all_content)
                        # Use updated scores from session state if available, otherwise use original
                        scores_for_insights = st.session_state.results_df.to_dict('records') if 'results_df' in st.session_state else final_scores
                        total_score = st.session_state.results_df['Weighted_Score'].sum() if 'results_df' in st.session_state and 'Weighted_Score' in st.session_state.results_df.columns else sum(item.get('Weighted_Score', 0) for item in final_scores)
                        total_benchmark = st.session_state.results_df['benchmark_weighted_score'].sum() if 'results_df' in st.session_state and 'benchmark_weighted_score' in st.session_state.results_df.columns else 8.0
                        
                        insights = utility.derive_insight(uploaded_content_str, company_json, evaluation_data, scores_for_insights, total_benchmark)
                        # Cache the insights
                        st.session_state.cached_insights = insights
                        st.session_state.insights_score_state = st.session_state.results_df.copy() if 'results_df' in st.session_state else final_scores_df.copy()
                else:
                    # Use cached insights
                    insights = st.session_state.cached_insights
                
                # Check if insights are based on modified scores
                insights_modified = False
                if 'results_df' in st.session_state and 'original_final_scores' in st.session_state:
                    if not st.session_state.results_df.equals(st.session_state.original_final_scores):
                        insights_modified = True
                
                st.subheader("💡 Insights and Recommendations")
                
                # Show indicator if insights are based on modified scores
                if insights_modified:
                    st.info("ℹ️ These insights are based on your modified scores from the Final Scores tab.")
                else:
                    st.success("✅ These insights are based on the original calculated scores.")
                
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
    
    # Show message when no analysis has been done yet
    elif not st.session_state.analysis_complete:
        st.info("👆 Please upload a pitch deck and click 'Start Analyzing' to begin the analysis.")

# Add a button to start new analysis (clear session state)
if st.session_state.analysis_complete:
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🆕 Start New Analysis", type="secondary", use_container_width=True):
            # Clear all analysis-related session state
            keys_to_clear = ['analysis_complete', 'all_content', 'company_json', 'evaluation_data', 'final_scores', 'results_df', 'original_final_scores', 'edits_pending', 'cached_insights', 'insights_score_state']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
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
