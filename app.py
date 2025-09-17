import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from analyse_pipeline import create_results, recalculate_results, analyze_results
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="GenAI Exchange Hackathon - AI Analyst for Startups", 
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CONSTANTS - Google Brand Colors
# ============================================================================
GOOGLE_BLUE = "#4285F4"
GOOGLE_GREEN = "#34A853"
GOOGLE_YELLOW = "#FBBC05"
GOOGLE_RED = "#EA4335"
GOOGLE_GRAY = "#5F6368"
GOOGLE_LIGHT_GRAY = "#F8F9FA"
GOOGLE_DARK_GRAY = "#202124"

# ============================================================================
# CUSTOM CSS STYLING - Dark Theme with Google Colors
# ============================================================================
def apply_custom_css():
    """Apply comprehensive dark theme CSS with Google colors"""
    st.markdown(f"""
    <style>
        /* Google Dark mode variables */
        :root {{
            --google-blue: {GOOGLE_BLUE};
            --google-green: {GOOGLE_GREEN};
            --google-yellow: {GOOGLE_YELLOW};
            --google-red: {GOOGLE_RED};
            --bg-primary: {GOOGLE_DARK_GRAY};
            --bg-secondary: #303134;
            --bg-card: #3c4043;
            --text-primary: #e8eaed;
            --text-secondary: #9aa0a6;
            --border-color: #5f6368;
            --shadow: rgba(0, 0, 0, 0.5);
        }}
        
        /* Main app background */
        .stApp {{
            background: var(--bg-primary);
        }}
        
        /* Main container */
        .main {{
            background: var(--bg-primary);
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background: #303134;
        }}
        
        /* All text elements */
        .element-container, .stMarkdown {{
            color: var(--text-primary);
        }}
        
        /* Metric cards styling */
        [data-testid="metric-container"] {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 1px 3px var(--shadow);
            color: var(--text-primary);
        }}
        
        [data-testid="metric-container"] [data-testid="metric-label"] {{
            color: var(--text-secondary);
        }}
        
        [data-testid="metric-container"] [data-testid="metric-value"] {{
            color: var(--text-primary);
        }}
        
        /* Google-style header */
        .header-title {{
            font-family: 'Google Sans', 'Product Sans', Arial, sans-serif;
            font-size: 2.5rem;
            font-weight: 400;
            text-align: center;
            margin-bottom: 2rem;
            color: var(--text-primary);
        }}
        
        /* Color classes for text */
        .g-blue {{ color: {GOOGLE_BLUE}; }}
        .g-red {{ color: {GOOGLE_RED}; }}
        .g-yellow {{ color: {GOOGLE_YELLOW}; }}
        .g-green {{ color: {GOOGLE_GREEN}; }}
        
        /* Subheader styling */
        .subheader {{
            color: var(--text-primary);
            font-size: 1.25rem;
            font-weight: 500;
            margin: 1.5rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {GOOGLE_BLUE};
        }}
        
        /* Google-style buttons */
        .stButton > button {{
            background: {GOOGLE_BLUE};
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            border-radius: 4px;
            transition: all 0.2s ease;
            font-family: 'Google Sans', Arial, sans-serif;
            box-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}
        
        .stButton > button:hover {{
            background: #1a73e8;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}
        
        /* File uploader styling */
        .stFileUploader {{
            border: 2px dashed var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            background: var(--bg-card);
            transition: all 0.2s ease;
        }}
        
        .stFileUploader label {{
            color: var(--text-primary) !important;
        }}
        
        .stFileUploader:hover {{
            border-color: {GOOGLE_BLUE};
            background: #3c4043;
        }}
        
        /* Tabs Google style */
        .stTabs [data-baseweb="tab-list"] {{
            background: transparent;
            gap: 0;
            border-bottom: 1px solid var(--border-color);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: var(--text-secondary);
            border-bottom: 2px solid transparent;
            background: transparent;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
        }}
        
        .stTabs [aria-selected="true"] {{
            color: {GOOGLE_BLUE};
            border-bottom: 2px solid {GOOGLE_BLUE};
            background: transparent;
        }}
        
        /* Expander styling */
        .streamlit-expanderHeader {{
            background: var(--bg-card);
            color: var(--text-primary);
            border-radius: 8px;
            font-weight: 500;
        }}
        
        /* Data editor/frame styling */
        .stDataFrame {{
            background: var(--bg-card);
        }}
        
        [data-testid="stDataFrame"] {{
            background: var(--bg-card);
            color: var(--text-primary);
        }}
        
        /* Success alert */
        .stSuccess {{
            background: rgba(52, 168, 83, 0.15);
            border-left: 4px solid {GOOGLE_GREEN};
            color: var(--text-primary);
        }}
        
        /* Error alert */
        .stError {{
            background: rgba(234, 67, 53, 0.15);
            border-left: 4px solid {GOOGLE_RED};
            color: var(--text-primary);
        }}
        
        /* Warning/Info alert */
        .stWarning, .stInfo {{
            background: rgba(66, 133, 244, 0.15);
            border-left: 4px solid {GOOGLE_BLUE};
            color: var(--text-primary);
        }}
        
        /* Progress bar */
        .stProgress > div > div > div {{
            background: {GOOGLE_BLUE};
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
        }}
        
        /* Plotly charts dark theme */
        .js-plotly-plot .plotly {{
            background: transparent !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HEADER COMPONENT
# ============================================================================
def display_header():
    """Display the main application header with team name prominence"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 0.5rem; 
                   background: linear-gradient(90deg, #4285f4, #ea4335, #fbbc05, #34a853);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   background-clip: text;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            🚀 AI-Powered Startup Analysis Platform
        </h1>
        <h2 style="font-size: 2.5rem; font-weight: 600; margin: 0.5rem 0;
                   color: #4285f4; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
            ✨ Team Gen AI Crew ✨
        </h2>
        <p style="font-size: 1rem; color: #9aa0a6; font-style: italic; margin-top: 0.5rem;">
            <span class="g-blue">Gen</span><span class="g-red">AI</span>
            <span style="color: var(--text-secondary);"> Exchange</span>
            <span class="g-yellow"> Hackathon</span> 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER COMPONENT
# ============================================================================
def display_footer():
    """Display the application footer with team name prominence"""
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem;'>
        <p style='font-size: 1.5rem; font-weight: 600; color: {GOOGLE_BLUE}; margin-bottom: 0.5rem;'>
            🏆 Team Gen AI Crew
        </p>
        <small style='color: #9aa0a6;'>
            Built for <span style='color: {GOOGLE_BLUE};'>Gen</span><span style='color: {GOOGLE_RED};'>AI</span>
            <span style='color: #9aa0a6;'> Exchange</span>
            <span style='color: {GOOGLE_YELLOW};'> Hackathon</span> 2025
        </small>
        <br>
        <small style='color: #9aa0a6;'>
            <a href="https://vision.hack2skill.com/event/genaiexchangehackathon/" target="_blank" style="color: {GOOGLE_BLUE}; text-decoration: none;">
                hack2skill.com/genaiexchangehackathon
            </a>
        </small>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CHART CREATION FUNCTIONS
# ============================================================================

def create_gauge_chart(value, title, max_value=100):
    """
    Create a Google-styled gauge chart for dark theme
    
    Args:
        value: Current score value
        title: Chart title  
        max_value: Maximum possible value (default 100)
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 18, 'color': '#e8eaed', 'family': 'Google Sans, Arial'}},
        delta = {'reference': max_value * 0.7, 'font': {'color': '#e8eaed'}},
        number = {'font': {'color': GOOGLE_BLUE, 'size': 40}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': '#e8eaed'},
            'bar': {'color': GOOGLE_BLUE},
            'bgcolor': "#303134",
            'borderwidth': 2,
            'bordercolor': "#5f6368",
            'steps': [
                {'range': [0, max_value * 0.5], 'color': 'rgba(234, 67, 53, 0.3)'},  # Red zone
                {'range': [max_value * 0.5, max_value * 0.75], 'color': 'rgba(251, 188, 5, 0.3)'},  # Yellow zone
                {'range': [max_value * 0.75, max_value], 'color': 'rgba(52, 168, 83, 0.3)'}  # Green zone
            ],
            'threshold': {
                'line': {'color': GOOGLE_GREEN, 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(48,49,52,0)",
        font={'color': '#e8eaed', 'family': "Google Sans, Arial"}
    )
    return fig

def create_comparison_chart(df):
    """
    Create a Google-styled comparison chart for dark theme
    
    Args:
        df: DataFrame with Score, Threshold, and Benchmark columns
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'Score' not in df.columns:
        fig.add_annotation(
            text="No data available for visualization",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#999")
        )
        fig.update_layout(
            template="plotly_dark",
            showlegend=False,
            height=400
        )
        return fig
    
    # Add Score line with Google Blue
    if 'Score' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Score'],
            mode='lines+markers',
            name='Score',
            line=dict(color=GOOGLE_BLUE, width=3),
            marker=dict(size=8, symbol='circle', color=GOOGLE_BLUE),
            hovertemplate='<b>Score: %{y:.1f}</b><extra></extra>'
        ))
    
    # Add Threshold line with Google Red
    if 'Threshold' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Threshold'],
            mode='lines+markers',
            name='Threshold',
            line=dict(color=GOOGLE_RED, width=2, dash='dash'),
            marker=dict(size=6, symbol='square', color=GOOGLE_RED),
            hovertemplate='<b>Threshold: %{y:.1f}</b><extra></extra>'
        ))
    
    # Add Benchmark line with Google Green
    if 'Benchmark_normalized' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Benchmark_normalized'],
            mode='lines+markers',
            name='Benchmark',
            line=dict(color=GOOGLE_GREEN, width=2),
            marker=dict(size=6, symbol='diamond', color=GOOGLE_GREEN),
            hovertemplate='<b>Benchmark: %{y:.1f}</b><extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': "Performance Analysis",
            'font': {'family': 'Google Sans, Arial', 'size': 20, 'color': '#e8eaed'}
        },
        xaxis_title="Parameters",
        yaxis_title="Values",
        hovermode='x unified',
        showlegend=True,
        height=400,
        template='plotly_dark',
        plot_bgcolor='rgba(48,49,52,0)',
        paper_bgcolor='rgba(48,49,52,0)',
        xaxis=dict(showgrid=True, gridcolor='#5f6368', color='#e8eaed'),
        yaxis=dict(showgrid=True, gridcolor='#5f6368', color='#e8eaed'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font={'family': 'Google Sans, Arial', 'color': '#e8eaed'}
        ),
        font={'family': 'Google Sans, Arial', 'color': '#e8eaed'}
    )
    
    return fig

def create_radar_chart(df):
    """
    Create a Google-styled radar chart for multi-parameter analysis
    
    Args:
        df: DataFrame with Parameter, Score, and Threshold columns
    
    Returns:
        Plotly figure object or None if data insufficient
    """
    if 'Parameter' in df.columns:
        # Take top 8 parameters for radar chart
        parameters = df['Parameter'].tolist()[:8]
        scores = df['Score'].tolist()[:8]
        thresholds = df['Threshold'].tolist()[:8]
        
        fig = go.Figure()
        
        # Add actual scores trace
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=parameters,
            fill='toself',
            name='Actual Score',
            line_color=GOOGLE_BLUE,
            fillcolor='rgba(66, 133, 244, 0.25)',
            marker=dict(color=GOOGLE_BLUE)
        ))
        
        # Add threshold trace
        fig.add_trace(go.Scatterpolar(
            r=thresholds,
            theta=parameters,
            fill='toself',
            name='Threshold',
            line_color=GOOGLE_RED,
            fillcolor='rgba(234, 67, 53, 0.12)',
            marker=dict(color=GOOGLE_RED)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont={'family': 'Google Sans, Arial', 'color': '#e8eaed'},
                    gridcolor='#5f6368'
                ),
                angularaxis=dict(
                    tickfont={'family': 'Google Sans, Arial', 'color': '#e8eaed'},
                    gridcolor='#5f6368'
                ),
                bgcolor='rgba(48,49,52,0)'
            ),
            showlegend=True,
            height=400,
            title={
                'text': "Multi-Parameter Analysis",
                'font': {'family': 'Google Sans, Arial', 'size': 20, 'color': '#e8eaed'}
            },
            template='plotly_dark',
            paper_bgcolor='rgba(48,49,52,0)',
            legend=dict(font={'family': 'Google Sans, Arial', 'color': '#e8eaed'}),
            font={'family': 'Google Sans, Arial', 'color': '#e8eaed'}
        )
        
        return fig
    return None

def create_heatmap(df):
    """
    Create a Google-styled correlation heatmap
    
    Args:
        df: DataFrame with numeric columns for correlation
    
    Returns:
        Plotly figure object or None if insufficient data
    """
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        
        # Dark theme colorscale
        colorscale = [
            [0, '#8B1A1A'],      # Dark red
            [0.25, '#8B6914'],   # Dark yellow
            [0.5, '#5F6368'],    # Gray
            [0.75, '#2E7D32'],   # Dark green
            [1, GOOGLE_GREEN]    # Bright green
        ]
        
        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Parameters", y="Parameters", color="Correlation"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            color_continuous_scale=colorscale,
            aspect="auto",
            title="Parameter Correlation Matrix",
            template='plotly_dark'
        )
        
        fig.update_layout(
            height=400,
            title={'font': {'family': 'Google Sans, Arial', 'size': 20, 'color': '#e8eaed'}},
            font={'family': 'Google Sans, Arial', 'color': '#e8eaed'},
            paper_bgcolor='rgba(48,49,52,0)'
        )
        return fig
    return None

# ============================================================================
# FILE UPLOAD SECTION
# ============================================================================
def handle_file_uploads():
    """
    Handle document uploads and display upload interface
    
    Returns:
        tuple: (pitch_deck, uploaded_files_list)
    """
    st.markdown('<div class="subheader">📁 Document Upload</div>', unsafe_allow_html=True)
    
    # Create two columns for upload interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        with st.container():
            st.markdown("##### 📎 Required Documents")
            pitch_deck = st.file_uploader(
                "Pitch Deck (PDF)",
                type=["pdf"],
                key="pitch_deck",
                help="Upload your startup's pitch deck in PDF format"
            )
            if pitch_deck:
                st.success(f"✅ {pitch_deck.name} uploaded")
    
    with col2:
        with st.container():
            st.markdown("##### 📄 Optional Documents")
            call_transcript = st.file_uploader(
                "Call Transcript",
                type=["doc", "docx", "txt"],
                key="call_transcript"
            )
            email_copy = st.file_uploader(
                "Email Copy",
                type=["doc", "docx", "txt"],
                key="email_copy"
            )
            founders_doc = st.file_uploader(
                "Founders Document",
                type=["doc", "docx", "txt"],
                key="founders_doc"
            )
    
    # Collect all uploaded files
    uploaded_files = [f for f in [pitch_deck, call_transcript, email_copy, founders_doc] if f is not None]
    
    return pitch_deck, uploaded_files

# ============================================================================
# METRICS DISPLAY SECTION
# ============================================================================
def display_metrics(score, flags, recommendations):
    """
    Display key metrics in executive summary
    
    Args:
        score: Overall analysis score
        flags: List of red flags
        recommendations: AI recommendations (string or list)
    """
    st.markdown('<div class="subheader">📊 Executive Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Score",
            f"{score:.1f}",
            delta=f"{score - 70:.1f} vs benchmark",
            delta_color="normal"
        )
    
    with col2:
        # Determine risk level based on score
        risk_level = "Medium" if 50 < score < 75 else ("Low" if score >= 75 else "High")
        st.metric(
            "Risk Level",
            risk_level,
            delta=None
        )
    
    with col3:
        st.metric(
            "Red Flags",
            len(flags),
            delta=None,
            delta_color="inverse"
        )
    
    with col4:
        # Count recommendations properly
        if isinstance(recommendations, str):
            rec_count = 1 if recommendations.strip() else 0
        elif isinstance(recommendations, list):
            rec_count = len([r for r in recommendations if r and len(str(r)) > 5])
        else:
            rec_count = 0
        
        st.metric(
            "Recommendations",
            rec_count if rec_count > 0 else "Generated",
            delta=None
        )

# ============================================================================
# INSIGHTS DISPLAY SECTION
# ============================================================================
def display_insights(flags, recommendations):
    """
    Display risk assessment and recommendations
    
    Args:
        flags: List of red flags
        recommendations: AI recommendations
    """
    st.markdown('<div class="subheader">🔍 Analysis Insights</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🚨 Risk Assessment")
        if flags:
            for i, flag in enumerate(flags):
                with st.expander(f"⚠️ Issue {i+1}", expanded=True):
                    st.markdown(f"**{flag}**")
                    st.markdown(f"<span style='color: {GOOGLE_RED};'>Impact: High</span>", unsafe_allow_html=True)
                    st.markdown("Priority: Critical")
        else:
            st.success("✅ No critical risks detected")
    
    with col2:
        st.markdown("#### 💡 Recommendations")
        
        # Display recommendations as in original
        if recommendations:
            st.info(recommendations)
            
            # Add implementation details
            col_impl1, col_impl2 = st.columns(2)
            with col_impl1:
                st.markdown(f"<span style='color: {GOOGLE_BLUE};'>📅 Implementation: Medium-term</span>", unsafe_allow_html=True)
            with col_impl2:
                st.markdown(f"<span style='color: {GOOGLE_GREEN};'>📈 Expected Impact: Positive</span>", unsafe_allow_html=True)
        else:
            st.info("📝 Upload and analyze documents to get AI-powered investment recommendations")

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    """Main application function - orchestrates the entire app flow"""
    
    # Apply custom CSS styling
    apply_custom_css()
    
    # ========================================================================
    # INITIALIZE SESSION STATE
    # ========================================================================
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    
    if "results_df" not in st.session_state:
        # create_results returns tuple: (df, structured_df, score, flags, recommendations)
        result_tuple = create_results()
        if isinstance(result_tuple, tuple) and len(result_tuple) >= 2:
            st.session_state.results_df = result_tuple[1]  # structured_df is at index 1
        else:
            st.session_state.results_df = pd.DataFrame()
    
    if "analysis_progress" not in st.session_state:
        st.session_state.analysis_progress = 0
    
    # Display header
    display_header()
    
    # ========================================================================
    # UPLOAD SECTION (Show when no results)
    # ========================================================================
    if not st.session_state.show_results:
        # Handle file uploads
        pitch_deck, uploaded_files = handle_file_uploads()
        
        # Upload summary and analyze button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if uploaded_files:
                st.info(f"📎 {len(uploaded_files)} document(s) ready")
            
            if st.button("🔍 Analyze Documents", use_container_width=True):
                if pitch_deck is None:
                    st.error("⚠️ Pitch Deck (PDF) is required")
                else:
                    with st.spinner("🤖 Analyzing with GenAI Exchange Platform..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        st.session_state.show_results = True
                        summary_df, results_df, score, flags, recommendations = create_results(uploaded_files)
                        st.session_state.summary_df = summary_df
                        st.session_state.results_df = results_df
                        st.success("✅ Analysis complete!")
                        time.sleep(1)
                        st.rerun()
    
    # ========================================================================
    # RESULTS SECTION (Show after analysis)
    # ========================================================================
    else:
        # Ensure results_df is a DataFrame
        if isinstance(st.session_state.results_df, tuple):
            if len(st.session_state.results_df) >= 2:
                st.session_state.results_df = st.session_state.results_df[1]
            else:
                st.session_state.results_df = pd.DataFrame()
        
        if not isinstance(st.session_state.results_df, pd.DataFrame):
            st.session_state.results_df = pd.DataFrame()
        
        # Analyze results if DataFrame is not empty
        if not st.session_state.results_df.empty:
            score, flags, recommendations = analyze_results(st.session_state.results_df)
        else:
            score = 0
            flags = []
            recommendations = ["Upload files to get AI-powered investment recommendations"]
        
        # Display top metrics
        display_metrics(score, flags, recommendations)
        
        # Main content area
        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("##### 🎯 Investment Readiness")
            gauge_fig = create_gauge_chart(score, "Overall Score", 100)
            st.plotly_chart(gauge_fig, use_container_width=True)
            
            if hasattr(st.session_state, 'summary_df'):
                st.markdown("##### 📋 Key Metrics")
                st.dataframe(
                    st.session_state.summary_df,
                    use_container_width=True,
                    hide_index=True
                )
        
        with col2:
            # ALL CHARTS IN TABS - KEEPING ALL 4 TABS
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🎯 Radar", "🔥 Heatmap", "📊 Data"])
            
            with tab1:
                comparison_fig = create_comparison_chart(st.session_state.results_df)
                st.plotly_chart(comparison_fig, use_container_width=True)
            
            with tab2:
                radar_fig = create_radar_chart(st.session_state.results_df)
                if radar_fig:
                    st.plotly_chart(radar_fig, use_container_width=True)
                else:
                    st.info("Radar chart requires parameter data")
            
            with tab3:
                heatmap_fig = create_heatmap(st.session_state.results_df)
                if heatmap_fig:
                    st.plotly_chart(heatmap_fig, use_container_width=True)
                else:
                    st.info("Insufficient data for correlation matrix")
            
            with tab4:
                st.markdown("##### ✏️ Edit Analysis Data")
                edited_df = st.data_editor(
                    st.session_state.results_df,
                    use_container_width=True,
                    hide_index=False,
                    num_rows="dynamic",
                    key="data_editor"
                )
                st.session_state.results_df = edited_df
        
        # Insights Section
        st.markdown("---")
        display_insights(flags, recommendations)
        
        # Performance Breakdown Expander
        with st.expander("📊 Detailed Performance Analysis", expanded=False):
            if 'Weighted_Score' in st.session_state.results_df.columns:
                # Use Google colors for bar chart
                colors = [GOOGLE_BLUE, GOOGLE_RED, GOOGLE_YELLOW, GOOGLE_GREEN] * 10
                
                fig_bar = go.Figure(data=[
                    go.Bar(
                        x=st.session_state.results_df['Parameter'] if 'Parameter' in st.session_state.results_df.columns else st.session_state.results_df.index,
                        y=st.session_state.results_df['Weighted_Score'],
                        marker_color=colors[:len(st.session_state.results_df)],
                        text=st.session_state.results_df['Weighted_Score'].round(1),
                        textposition='auto',
                        textfont=dict(color='white')
                    )
                ])
                
                fig_bar.update_layout(
                    title={'text': 'Weighted Score Distribution', 'font': {'color': '#e8eaed'}},
                    xaxis_title='Parameters',
                    yaxis_title='Weighted Score',
                    height=400,
                    showlegend=False,
                    template='plotly_dark',
                    paper_bgcolor='rgba(48,49,52,0)',
                    plot_bgcolor='rgba(48,49,52,0)',
                    font={'family': 'Google Sans, Arial', 'color': '#e8eaed'},
                    xaxis=dict(color='#e8eaed'),
                    yaxis=dict(color='#e8eaed')
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Action Buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Re-analyze", use_container_width=True):
                with st.spinner("Recalculating..."):
                    final_score, flags, recommendations = analyze_results(st.session_state.results_df)
                    st.session_state.score = final_score
                    st.session_state.flags = flags
                    st.session_state.recommendations = recommendations
                    st.success("✅ Updated")
                    time.sleep(1)
                    st.rerun()
        
        with col2:
            csv = st.session_state.results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download",
                data=csv,
                file_name="startup_analysis.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            if st.button("📧 Share", use_container_width=True):
                st.info("Google Drive integration coming soon!")
        
        with col4:
            if st.button("➕ New Analysis", use_container_width=True):
                st.session_state.show_results = False
                st.session_state.results_df = pd.DataFrame()
                st.rerun()
    
    # Display footer
    display_footer()

# ============================================================================
# RUN APPLICATION
# ============================================================================
if __name__ == "__main__":
    main()