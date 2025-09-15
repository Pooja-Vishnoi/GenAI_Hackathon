import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from analyse_pipeline import create_results, recalculate_results, analyze_results
from Utils.company_data_loader import (
    get_available_companies,
    get_company_files,
    load_company_documents,
    get_company_metadata,
    get_benchmark_companies,
    generate_analysis_context,
    get_document_summary
)
import time
import io
import base64
import zipfile
import tempfile

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
    """Display the main application header with hackathon context"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 0.5rem; 
                   background: linear-gradient(90deg, #4285f4, #ea4335, #fbbc05, #34a853);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   background-clip: text;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            🚀 AI Analyst for Startup Evaluation
        </h1>
        <h2 style="font-size: 2.5rem; font-weight: 600; margin: 0.5rem 0;
                   color: #4285f4; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">
            ✨ Team Gen AI Crew ✨
        </h2>
        <p style="font-size: 1.2rem; color: #e8eaed; margin-top: 0.5rem;">
            <b>Synthesizing founder materials & public data → Actionable investment insights</b>
        </p>
        <p style="font-size: 1rem; color: #9aa0a6; font-style: italic; margin-top: 0.5rem;">
            <span class="g-blue">Gen</span><span class="g-red">AI</span>
            <span style="color: var(--text-secondary);"> Exchange</span>
            <span class="g-yellow"> Hackathon</span> 2024
            | Powered by Google AI Technologies
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
            <span style='color: {GOOGLE_YELLOW};'> Hackathon</span> 2024
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
    Handle document uploads with company selector and manual upload options
    
    Returns:
        tuple: (pitch_deck, uploaded_files_list, selected_company)
    """
    st.markdown('<div class="subheader">📁 Document Selection</div>', unsafe_allow_html=True)
    
    # Initialize session state for upload mode
    if 'upload_mode' not in st.session_state:
        st.session_state.upload_mode = 'company_selector'
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = None
    
    # Upload mode selector
    st.markdown("#### 🎯 Choose Data Source")
    upload_mode = st.radio(
        "Select how you want to provide startup data:",
        ["📊 Select from Available Companies", "📤 Upload Custom Documents"],
        key="upload_mode_radio",
        horizontal=True,
        help="Choose to analyze existing company data or upload your own documents"
    )
    
    st.markdown("---")
    
    pitch_deck = None
    uploaded_files = []
    selected_company = None
    
    if upload_mode == "📊 Select from Available Companies":
        # Company selector mode
        companies = get_available_companies()
        
        if companies:
            # Quick selection cards
            st.markdown("##### 🎯 Quick Selection - Featured Startups")
            
            # Featured companies with special badges
            featured_companies = {
                "We360 AI": "🤖 AI Leader",
                "Kredily": "💰 Fintech",
                "Dr.Doodley": "🏥 Healthcare",
                "Ctruh": "🥽 XR Tech",
                "Sensesemi": "🔧 Hardware",
                "Naario": "👩 Social Impact"
            }
            
            # Create a grid of company cards (3 columns)
            company_list = list(companies.keys())
            cols = st.columns(3)
            
            # Create clickable cards for featured companies
            featured_idx = 0
            for company_name, badge in featured_companies.items():
                if company_name in company_list:
                    with cols[featured_idx % 3]:
                        button_label = f"🏢 {company_name}\n{badge}"
                        if st.button(
                            button_label,
                            key=f"quick_select_{featured_idx}",
                            use_container_width=True,
                            help=f"Quick select {company_name} - {badge}"
                        ):
                            st.session_state.selected_company = company_name
                            st.rerun()
                    featured_idx += 1
            
            st.markdown("---")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("##### 🏢 All Available Companies")
                
                # Create company selector with preview
                selected_company = st.selectbox(
                    "Choose a company to analyze:",
                    ["-- Select a Company --"] + company_list,
                    key="company_selector",
                    index=company_list.index(st.session_state.selected_company) + 1 if st.session_state.selected_company in company_list else 0,
                    help="Select from 14 pre-loaded startup companies"
                )
                
                if selected_company and selected_company != "-- Select a Company --":
                    st.session_state.selected_company = selected_company
                    
                    # Load and display company files
                    company_folder = companies[selected_company]
                    files = get_company_files(company_folder)
                    
                    # Display file information
                    st.success(f"✅ **{selected_company}** selected")
                    
                    # Show available documents with preview and download options
                    with st.expander(f"📋 Available Documents for {selected_company}", expanded=True):
                        doc_count = 0
                        
                        # Create tabs for better organization
                        doc_tabs = st.tabs(["📄 Documents", "👁️ Preview", "📥 Downloads"])
                        
                        with doc_tabs[0]:
                            # List all documents
                            if files['pitch_deck']:
                                st.markdown(f"✓ **Pitch Deck:** `{files['pitch_deck'].name}`")
                                doc_count += 1
                            if files['founders_checklist']:
                                st.markdown(f"✓ **Founders Checklist:** `{files['founders_checklist'].name}`")
                                doc_count += 1
                            if files['investment_memo']:
                                st.markdown(f"✓ **Investment Memo:** `{files['investment_memo'].name}`")
                                doc_count += 1
                            if files['financials']:
                                st.markdown(f"✓ **Financial Documents:** `{files['financials'].name}`")
                                doc_count += 1
                            for doc in files['other_docs']:
                                st.markdown(f"✓ **Additional:** `{doc.name}`")
                                doc_count += 1
                            
                            st.info(f"📊 Total documents available: **{doc_count}**")
                        
                        with doc_tabs[1]:
                            # Document preview section
                            st.markdown("**Preview Documents:**")
                            
                            # Create a selectbox for document selection
                            preview_options = []
                            preview_files = {}
                            
                            if files['pitch_deck']:
                                preview_options.append(f"Pitch Deck - {files['pitch_deck'].name}")
                                preview_files[f"Pitch Deck - {files['pitch_deck'].name}"] = files['pitch_deck']
                            if files['founders_checklist']:
                                preview_options.append(f"Founders Checklist - {files['founders_checklist'].name}")
                                preview_files[f"Founders Checklist - {files['founders_checklist'].name}"] = files['founders_checklist']
                            if files['investment_memo']:
                                preview_options.append(f"Investment Memo - {files['investment_memo'].name}")
                                preview_files[f"Investment Memo - {files['investment_memo'].name}"] = files['investment_memo']
                            
                            if preview_options:
                                selected_doc = st.selectbox(
                                    "Select document to preview:",
                                    preview_options,
                                    key=f"preview_select_{selected_company}"
                                )
                                
                                if selected_doc and selected_doc in preview_files:
                                    file_path = preview_files[selected_doc]
                                    
                                    # For PDF files, show embedded viewer
                                    if file_path.suffix.lower() == '.pdf':
                                        try:
                                            with open(file_path, 'rb') as pdf_file:
                                                pdf_data = pdf_file.read()
                                                pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
                                                
                                                # Show file info
                                                file_size_mb = len(pdf_data) / (1024 * 1024)
                                                st.caption(f"📄 File Size: {file_size_mb:.2f} MB")
                                                
                                                # Option to view inline or download
                                                view_option = st.radio(
                                                    "View Option:",
                                                    ["Embedded Viewer", "Download to View"],
                                                    horizontal=True,
                                                    key=f"view_option_{selected_company}_{selected_doc}"
                                                )
                                                
                                                if view_option == "Embedded Viewer":
                                                    # Create iframe for PDF viewing
                                                    pdf_display = f'''
                                                    <iframe 
                                                        src="data:application/pdf;base64,{pdf_base64}" 
                                                        width="100%" 
                                                        height="600" 
                                                        type="application/pdf"
                                                        style="border: 1px solid #5f6368; border-radius: 8px;">
                                                        <p>Your browser doesn't support embedded PDFs. 
                                                        <a href="data:application/pdf;base64,{pdf_base64}" download="{file_path.name}">
                                                        Download PDF</a> instead.</p>
                                                    </iframe>
                                                    '''
                                                    st.markdown(pdf_display, unsafe_allow_html=True)
                                                else:
                                                    st.download_button(
                                                        label=f"⬇️ Download {file_path.name}",
                                                        data=pdf_data,
                                                        file_name=file_path.name,
                                                        mime="application/pdf",
                                                        key=f"preview_download_{selected_company}_{selected_doc}",
                                                        use_container_width=True
                                                    )
                                        except Exception as e:
                                            st.error(f"Error loading PDF: {str(e)}")
                                            st.info("Please use the Downloads tab to access this document.")
                                    
                                    elif file_path.suffix.lower() in ['.docx', '.doc']:
                                        st.info("📝 Word documents cannot be previewed directly. Please download to view.")
                                        with open(file_path, 'rb') as f:
                                            st.download_button(
                                                label=f"⬇️ Download {file_path.name}",
                                                data=f.read(),
                                                file_name=file_path.name,
                                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                key=f"preview_word_{selected_company}_{selected_doc}",
                                                use_container_width=True
                                            )
                                    else:
                                        st.info(f"Preview not available for {file_path.suffix} files. Please download to view.")
                            else:
                                st.info("No documents available for preview")
                        
                        with doc_tabs[2]:
                            # Download section
                            st.markdown("**Download Documents:**")
                            
                            download_cols = st.columns(2)
                            col_idx = 0
                            
                            # Pitch Deck download
                            if files['pitch_deck']:
                                with download_cols[col_idx % 2]:
                                    with open(files['pitch_deck'], 'rb') as f:
                                        st.download_button(
                                            label=f"📄 Pitch Deck",
                                            data=f.read(),
                                            file_name=files['pitch_deck'].name,
                                            mime="application/pdf" if files['pitch_deck'].suffix.lower() == '.pdf' else "application/octet-stream",
                                            key=f"download_pitch_{selected_company}",
                                            use_container_width=True
                                        )
                                col_idx += 1
                            
                            # Founders Checklist download
                            if files['founders_checklist']:
                                with download_cols[col_idx % 2]:
                                    with open(files['founders_checklist'], 'rb') as f:
                                        mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document" if files['founders_checklist'].suffix.lower() == '.docx' else "application/pdf"
                                        st.download_button(
                                            label=f"📋 Founders Checklist",
                                            data=f.read(),
                                            file_name=files['founders_checklist'].name,
                                            mime=mime_type,
                                            key=f"download_checklist_{selected_company}",
                                            use_container_width=True
                                        )
                                col_idx += 1
                            
                            # Investment Memo download
                            if files['investment_memo']:
                                with download_cols[col_idx % 2]:
                                    with open(files['investment_memo'], 'rb') as f:
                                        st.download_button(
                                            label=f"📑 Investment Memo",
                                            data=f.read(),
                                            file_name=files['investment_memo'].name,
                                            mime="application/pdf",
                                            key=f"download_memo_{selected_company}",
                                            use_container_width=True
                                        )
                                col_idx += 1
                            
                            # Financial Documents download
                            if files['financials']:
                                with download_cols[col_idx % 2]:
                                    with open(files['financials'], 'rb') as f:
                                        st.download_button(
                                            label=f"💰 Financial Docs",
                                            data=f.read(),
                                            file_name=files['financials'].name,
                                            mime="application/pdf",
                                            key=f"download_financials_{selected_company}",
                                            use_container_width=True
                                        )
                                col_idx += 1
                            
                            # Download all as ZIP
                            if doc_count > 1:
                                st.markdown("---")
                                
                                # Create a temporary ZIP file
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip:
                                    with zipfile.ZipFile(tmp_zip.name, 'w') as zipf:
                                        # Add all available documents to ZIP
                                        if files['pitch_deck']:
                                            zipf.write(files['pitch_deck'], files['pitch_deck'].name)
                                        if files['founders_checklist']:
                                            zipf.write(files['founders_checklist'], files['founders_checklist'].name)
                                        if files['investment_memo']:
                                            zipf.write(files['investment_memo'], files['investment_memo'].name)
                                        if files['financials']:
                                            zipf.write(files['financials'], files['financials'].name)
                                        for doc in files['other_docs']:
                                            zipf.write(doc, doc.name)
                                    
                                    # Read the ZIP file for download
                                    tmp_zip.seek(0)
                                    zip_data = open(tmp_zip.name, 'rb').read()
                                    
                                    st.download_button(
                                        label=f"📦 Download All Documents ({doc_count} files)",
                                        data=zip_data,
                                        file_name=f"{selected_company}_documents.zip",
                                        mime="application/zip",
                                        key=f"download_all_{selected_company}",
                                        use_container_width=True,
                                        type="primary"
                                    )
                    
                    # Load the documents
                    pitch_deck_data, other_docs = load_company_documents(selected_company)
                    
                    # Convert to file-like objects for compatibility
                    if pitch_deck_data:
                        pitch_deck = io.BytesIO(pitch_deck_data)
                        pitch_deck.name = files['pitch_deck'].name if files['pitch_deck'] else "pitch_deck.pdf"
                    
                    for doc in other_docs:
                        file_obj = io.BytesIO(doc['data'])
                        file_obj.name = doc['name']
                        file_obj.type = doc['type']
                        uploaded_files.append(file_obj)
            
            with col2:
                # Company statistics
                st.markdown("##### 📈 Quick Stats")
                st.metric("Total Companies", len(companies))
                st.metric("Selected", selected_company if selected_company != "-- Select a Company --" else "None")
                
                # Suggestions based on selection
                if selected_company and selected_company != "-- Select a Company --":
                    st.markdown("##### 💡 AI Analysis Preview")
                    
                    # Get company metadata and analysis context
                    metadata = get_company_metadata(selected_company)
                    benchmark_companies = get_benchmark_companies(selected_company)
                    doc_summary = get_document_summary(selected_company)
                    
                    # Display sector and stage
                    st.info(f"**Sector:** {metadata.get('sector', 'Unknown')}")
                    st.info(f"**Stage:** {metadata.get('stage', 'Unknown')}")
                    
                    # Display benchmark companies if available
                    if benchmark_companies:
                        st.markdown("**📊 Benchmark Against:**")
                        for comp in benchmark_companies[:3]:
                            st.caption(f"• {comp}")
                    
                    # Document readiness indicator
                    if doc_summary.get('has_required_docs'):
                        st.success(f"✅ Ready for AI Analysis")
                    else:
                        st.warning(f"⚠️ Missing: {', '.join(doc_summary.get('missing_docs', []))}")
        else:
            st.warning("⚠️ No companies found in the data directory")
    
    else:
        # Manual upload mode
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.container():
                st.markdown("##### 📎 Required Documents")
                pitch_deck = st.file_uploader(
                    "Pitch Deck (PDF)",
                    type=["pdf"],
                    key="pitch_deck_manual",
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
    
    # Add helpful tips
    with st.expander("💡 Tips for Best Results", expanded=False):
        st.markdown("""
        **For Company Selection:**
        - All 14 companies have pre-loaded pitch decks and supporting documents
        - Documents are automatically categorized for optimal analysis
        - No need to upload files manually
        
        **For Manual Upload:**
        - Ensure pitch deck is in PDF format
        - Include founders checklist for comprehensive analysis
        - Add financial documents for better investment insights
        """)
    
    return pitch_deck, uploaded_files, selected_company

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
        # Count flags properly - handle list of lists format
        if isinstance(flags, (list, tuple)) and len(flags) >= 2 and isinstance(flags[0], list):
            flag_count = len(flags[0])  # Count actual risk points
        elif isinstance(flags, list):
            flag_count = len(flags)
        else:
            flag_count = 0
            
        st.metric(
            "Red Flags",
            flag_count,
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
# INSIGHTS DISPLAY SECTION - Enhanced for AI Analyst Platform
# ============================================================================
def display_insights(flags, recommendations, company_name=None):
    """
    Display AI-powered risk assessment and investment recommendations
    
    Args:
        flags: List of red flags detected by AI analysis
        recommendations: AI-generated investment recommendations
        company_name: Name of the analyzed company for context
    """
    st.markdown('<div class="subheader">🔍 AI Analysis Insights</div>', unsafe_allow_html=True)
    
    # Get analysis context if company is specified
    analysis_context = {}
    if company_name:
        analysis_context = generate_analysis_context(company_name)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🚨 Risk Assessment & Red Flags")
        
        # Display detected risks
        if flags:
            # Handle both list of lists and single list format
            if isinstance(flags, (list, tuple)) and len(flags) >= 2 and isinstance(flags[0], list):
                # flags is [red_flags_points, red_flags_reference]
                risk_points = flags[0] if isinstance(flags[0], list) else [flags[0]]
                risk_references = flags[1] if isinstance(flags[1], list) else [flags[1]] if len(flags) > 1 else []
                
                for i, (flag_point, flag_ref) in enumerate(zip(risk_points, risk_references)):
                    # Convert to string if needed
                    flag_text = str(flag_point) if not isinstance(flag_point, str) else flag_point
                    ref_text = str(flag_ref) if not isinstance(flag_ref, str) else flag_ref
                    
                    # Determine risk level based on flag content
                    risk_level = "High" if any(word in flag_text.lower() for word in ['critical', 'severe', 'major', 'high', 'low revenue']) else "Medium"
                    risk_color = GOOGLE_RED if risk_level == "High" else GOOGLE_YELLOW
                    
                    with st.expander(f"⚠️ Risk {i+1}: {flag_text[:30]}...", expanded=(i < 2)):
                        st.markdown(f"**{flag_text}**")
                        st.markdown(f"📄 {ref_text}")
                        st.markdown(f"<span style='color: {risk_color};'>Impact: {risk_level}</span>", unsafe_allow_html=True)
                        st.markdown("**Mitigation:** Review financial metrics and market validation")
            
            elif isinstance(flags, list):
                # Handle simple list of flags
                for i, flag in enumerate(flags):
                    # Convert to string if needed
                    flag_text = str(flag) if not isinstance(flag, str) else flag
                    
                    # Determine risk level based on flag content
                    risk_level = "High" if any(word in flag_text.lower() for word in ['critical', 'severe', 'major', 'high']) else "Medium"
                    risk_color = GOOGLE_RED if risk_level == "High" else GOOGLE_YELLOW
                    
                    with st.expander(f"⚠️ Risk {i+1}: {flag_text[:30]}...", expanded=(i < 2)):
                        st.markdown(f"**{flag_text}**")
                        st.markdown(f"<span style='color: {risk_color};'>Impact: {risk_level}</span>", unsafe_allow_html=True)
                        st.markdown("**Mitigation:** Review financial metrics and market validation")
        
        # Add sector-specific risks if available
        if analysis_context.get('risk_flags'):
            st.markdown("**🎯 Sector-Specific Risks:**")
            for risk in analysis_context['risk_flags'][:3]:
                st.caption(f"• {risk.replace('_', ' ').title()}")
        
        if not flags:
            st.success("✅ No critical risks detected in initial screening")
    
    with col2:
        st.markdown("#### 💡 AI Investment Recommendations")
        
        # Display AI recommendations
        if recommendations:
            if isinstance(recommendations, str):
                st.info(recommendations)
            elif isinstance(recommendations, list):
                for rec in recommendations[:3]:
                    st.info(f"• {rec}")
            
            # Add focus areas from context
            if analysis_context.get('analysis_focus'):
                st.markdown("**🎯 Key Analysis Areas:**")
                for focus in analysis_context['analysis_focus'][:3]:
                    st.caption(f"• {focus.replace('_', ' ').title()}")
            
            # Add implementation timeline
            col_impl1, col_impl2 = st.columns(2)
            with col_impl1:
                st.markdown(f"<span style='color: {GOOGLE_BLUE};'>📅 Due Diligence: 2-3 weeks</span>", unsafe_allow_html=True)
            with col_impl2:
                st.markdown(f"<span style='color: {GOOGLE_GREEN};'>📈 Investment Horizon: 3-5 years</span>", unsafe_allow_html=True)
        else:
            st.info("🤖 AI analysis will generate investment recommendations based on:")
            st.caption("• Pitch deck analysis")
            st.caption("• Sector benchmarking")
            st.caption("• Financial metrics evaluation")
            st.caption("• Market opportunity assessment")

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
        # Handle file uploads (now returns 3 values)
        pitch_deck, uploaded_files, selected_company = handle_file_uploads()
        
        # Upload summary and analyze button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Show document status
            if selected_company and selected_company != "-- Select a Company --":
                st.success(f"🏢 **{selected_company}** ready for analysis")
                if uploaded_files:
                    st.info(f"📎 {len(uploaded_files) + 1} document(s) loaded")
            elif uploaded_files:
                st.info(f"📎 {len(uploaded_files)} document(s) ready")
            
            # Analyze button with dynamic text
            button_text = f"🔍 Analyze {selected_company}" if (selected_company and selected_company != "-- Select a Company --") else "🔍 Analyze Documents"
            
            if st.button(button_text, use_container_width=True):
                if pitch_deck is None:
                    st.error("⚠️ Please select a company or upload a Pitch Deck (PDF)")
                else:
                    with st.spinner(f"🤖 Analyzing {selected_company if selected_company else 'documents'} with GenAI Exchange Platform..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Simulate analysis steps
                        steps = [
                            "📄 Loading documents...",
                            "🔍 Extracting key information...",
                            "📊 Analyzing financial metrics...",
                            "🎯 Evaluating investment potential...",
                            "💡 Generating recommendations..."
                        ]
                        
                        for i, step in enumerate(steps):
                            status_text.text(step)
                            for j in range(20):
                                time.sleep(0.005)
                                progress_bar.progress((i * 20 + j + 1))
                        
                        st.session_state.show_results = True
                        st.session_state.analyzed_company = selected_company
                        summary_df, results_df, score, flags, recommendations = create_results(uploaded_files)
                        st.session_state.summary_df = summary_df
                        st.session_state.results_df = results_df
                        status_text.empty()
                        st.success(f"✅ Analysis complete for {selected_company if selected_company else 'uploaded documents'}!")
                        time.sleep(1)
                        st.rerun()
    
    # ========================================================================
    # RESULTS SECTION (Show after analysis)
    # ========================================================================
    else:
        # Display which company is being analyzed
        if 'analyzed_company' in st.session_state and st.session_state.analyzed_company:
            st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, rgba(66,133,244,0.1), rgba(52,168,83,0.1)); 
                        border-radius: 10px; margin-bottom: 1rem; border: 1px solid rgba(66,133,244,0.3);'>
                <h3 style='color: {GOOGLE_BLUE}; margin: 0;'>🏢 Analyzing: {st.session_state.analyzed_company}</h3>
            </div>
            """, unsafe_allow_html=True)
        
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
        
        # Insights Section with AI Analysis Context
        st.markdown("---")
        company_for_insights = st.session_state.get('analyzed_company', None)
        display_insights(flags, recommendations, company_for_insights)
        
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
                st.session_state.selected_company = None
                st.session_state.analyzed_company = None
                st.rerun()
    
    # Display footer
    display_footer()

# ============================================================================
# RUN APPLICATION
# ============================================================================
if __name__ == "__main__":
    main()