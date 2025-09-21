# 🔄 Data Flow Documentation

## 📋 Overview
This document describes how data flows through the GenAI Hackathon startup analysis platform, from document upload to final analysis results.

## 🔄 Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant UI as 🖥️ Streamlit UI
    participant P as ⚙️ Main Pipeline
    participant FR as 📖 File Reader
    participant E as 🔍 Parameter Extractor
    participant S as 🎯 Scoring Engine
    participant A as 🧠 Analysis Engine
    participant I as 🤖 Intelligence Layer
    
    U->>UI: 📤 Upload Documents
    UI->>P: 🚀 Trigger Analysis
    P->>FR: 📄 Process Files
    FR->>E: 📊 Extract Content
    E->>S: 🔄 Convert to Parameters
    S->>A: 🎯 Apply Scoring Logic
    A->>I: 💡 Generate Insights
    I->>UI: 📋 Return Results
    UI->>U: 📊 Display Dashboard
    
    Note over U,I: ⚡ Real-time interaction loop
    U->>UI: ✏️ Modify Parameters
    UI->>I: 🔄 Recalculate
    I->>UI: 📈 Updated Results
```

## 🔄 Execution Flows

### 🚀 Initial Analysis Flow (When User Clicks "🔍 Analyse")

```mermaid
flowchart TD
    subgraph FRONTEND["🖥️ FRONTEND (app.py)"]
        START([User Clicks Analyse - Line 728]) --> VALIDATE{Pitch Deck Uploaded?<br/>Line 729}
        VALIDATE -->|No| ERROR[Show Error: Pitch Deck Required<br/>Line 730]
        VALIDATE -->|Yes| TRIGGER[Trigger Analysis<br/>Line 732]
        UPDATE_SESSION[Update Session State<br/>Lines 740-742]
        RERUN[st.rerun - Line 744]
        SHOW_DASHBOARD[Display Dashboard<br/>Lines 749-823]
    end
    
    subgraph BACKEND["⚙️ BACKEND (analyse_pipeline.py)"]
        CALL_CREATE[create_results<br/>Line 18]
        READ_FILES[read_files<br/>Line 28]
        EXTRACT_PARAMS[content_to_json<br/>Line 31]
        CREATE_DF[Create DataFrame<br/>Line 34]
        FILTER_DF[Filter Parameters<br/>Lines 39-40]
        SCORE_CONVERT[convert_raw_to_structured<br/>Line 45]
        CALC_WEIGHTED[Calculate Weighted Scores<br/>Line 49]
        FINAL_SCORE[Sum Final Score<br/>Line 52]
        DETECT_FLAGS[detect_red_flags<br/>Line 57]
        GEN_RECS[generate_recommendations<br/>Line 61]
        RETURN_RESULTS[Return Results<br/>Line 67]
    end
    
    TRIGGER -->|Line 739| CALL_CREATE
    CALL_CREATE --> READ_FILES
    READ_FILES --> EXTRACT_PARAMS
    EXTRACT_PARAMS --> CREATE_DF
    CREATE_DF --> FILTER_DF
    FILTER_DF --> SCORE_CONVERT
    SCORE_CONVERT --> CALC_WEIGHTED
    CALC_WEIGHTED --> FINAL_SCORE
    FINAL_SCORE --> DETECT_FLAGS
    DETECT_FLAGS --> GEN_RECS
    GEN_RECS --> RETURN_RESULTS
    RETURN_RESULTS -->|Line 739| UPDATE_SESSION
    UPDATE_SESSION --> RERUN
    RERUN --> SHOW_DASHBOARD
    
    ERROR --> END([End])
    SHOW_DASHBOARD --> END
    
    style START fill:#4285f4,color:#fff
    style CALL_CREATE fill:#34a853,color:#fff
    style RETURN_RESULTS fill:#fbbc05,color:#000
```

### 🔄 Re-Analysis Flow (When User Clicks "🔄 Analyse Again")

```mermaid
flowchart TD
    subgraph FRONTEND2["🖥️ FRONTEND (app.py)"]
        START([User Clicks Re-analyze<br/>Line 862]) --> TRIGGER[Button Click Event]
        UPDATE_SESSION[Update Session Variables<br/>Lines 865-867]
        RERUN[st.rerun - Line 870]
        UPDATED_DASHBOARD[Updated Dashboard Display<br/>Lines 749-823]
    end
    
    subgraph BACKEND2["⚙️ BACKEND (analyse_pipeline.py)"]
        CALL_ANALYZE[analyze_results<br/>Line 151]
        GET_DF[Process DataFrame<br/>Line 153]
        RECALC_WEIGHTED[Recalculate Weighted Scores<br/>Line 154]
        NEW_FINAL[New Final Score<br/>Line 157]
        REFRESH_FLAGS[detect_red_flags<br/>Line 162]
        REFRESH_RECS[generate_recommendations<br/>Line 166]
    end
    
    TRIGGER -->|Line 864| CALL_ANALYZE
    CALL_ANALYZE --> GET_DF
    GET_DF --> RECALC_WEIGHTED
    RECALC_WEIGHTED --> NEW_FINAL
    NEW_FINAL --> REFRESH_FLAGS
    REFRESH_FLAGS --> REFRESH_RECS
    REFRESH_RECS -->|Return| UPDATE_SESSION
    UPDATE_SESSION --> RERUN
    RERUN --> UPDATED_DASHBOARD
    UPDATED_DASHBOARD --> END([End])
    
    style START fill:#4285f4,color:#fff
    style CALL_ANALYZE fill:#fbbc05,color:#000
```

### ✏️ Interactive Parameter Editing Flow (Real-time Updates)

```mermaid
flowchart TD
    subgraph FRONTEND3["🖥️ FRONTEND (app.py)"]
        START([User Edits in Data Editor<br/>Line 812]) --> STREAMLIT_UPDATE[Streamlit Auto-Update<br/>Line 819]
        SESSION_UPDATE[Session State Updated<br/>Line 819]
        DISPLAY_UPDATE[Display Updates]
    end
    
    subgraph BACKEND3["⚙️ BACKEND (analyse_pipeline.py)"]
        CALL_ANALYZE[analyze_results<br/>Line 762]
        INSTANT_RECALC[Instant Recalculation<br/>Lines 153-167]
    end
    
    STREAMLIT_UPDATE --> SESSION_UPDATE
    SESSION_UPDATE --> CALL_ANALYZE
    CALL_ANALYZE --> INSTANT_RECALC
    INSTANT_RECALC --> DISPLAY_UPDATE
    DISPLAY_UPDATE --> END([Real-time UI Update])
    
    style START fill:#4285f4,color:#fff
    style CALL_ANALYZE fill:#34a853,color:#fff
```

## 📤 1. Input Processing

### 📁 File Upload & Validation
- **🖥️ UI Components**: See [`app.py:18-23`](../app.py#L18-L23) for Streamlit file uploaders
- **📖 File Processing**: [`read_files()`](../Utils/utils.py#L42-L51) function in `Utils/utils.py`
- **📄 Individual File Reading**: [`read_file()`](../Utils/utils.py#L8-L39) function in `Utils/utils.py`

### ⚙️ Supported Operations:
- **📄 PDF Processing**: PyPDF2-based text extraction ([`read_file()` lines 18-24](../Utils/utils.py#L18-L24))
- **📝 DOCX/DOC Processing**: python-docx integration ([`read_file()` lines 26-32](../Utils/utils.py#L26-L32)) 
- **📄 TXT Processing**: UTF-8 decoding ([`read_file()` lines 34-35](../Utils/utils.py#L34-L35))

## 🤖 2. AI Analysis & Content Extraction 🚧 **[PARTIALLY IMPLEMENTED]**

### 🔄 Content Structure Conversion
- **🧠 Main Function**: [`content_to_json()`](../Utils/pdf_file_reader.py#L15-L51) 🚧 **[TO BE IMPLEMENTED]** - Currently uses sample data
- **📊 DataFrame Creation**: See [`analyse_pipeline.py:23-28`](../analyse_pipeline.py#L23-L28) ✅ **[WORKING]** - Parameter extraction pipeline
- **🔍 Data Filtering**: Non-evaluating parameters removed ([lines 29-30](../analyse_pipeline.py#L29-L30)) ✅ **[WORKING]**

**📋 Output Format**: Structured JSON with company parameters (name, sector, team, market, traction, revenue, USP, competition, risks)

**⚠️ Note**: Currently uses hardcoded sample data - AI integration needed for production use

## 🎯 3. Scoring Pipeline

### 🔧 Parameter Scoring Functions
All functions located in [`Utils/structured_2_scored_data.py`](../Utils/structured_2_scored_data.py):

- **👥 Team Quality**: [`parse_team()`](../Utils/structured_2_scored_data.py#L44-L51) function - IIT/IIM bonus scoring
- **🌍 Market Size**: [`parse_market_size()`](../Utils/structured_2_scored_data.py#L9-L24) function - Billion/Million market analysis  
- **📈 Traction**: [`parse_traction()`](../Utils/structured_2_scored_data.py#L26-L42) function - User growth and MoM metrics
- **📊 Other Parameters**: [Lines 84-94](../Utils/structured_2_scored_data.py#L84-L94) for Financials, Product Uniqueness, Competition, etc.

### ⚖️ Weighted Calculation:
- **🎯 Weights Definition**: [Lines 117-126](../Utils/structured_2_scored_data.py#L117-L126) in structured_2_scored_data.py
- **🧮 Score Calculation**: [`analyse_pipeline.py:38-43`](../analyse_pipeline.py#L38-L43) for weighted final score

## 📊 4. Analysis Output & Risk Detection

### 🚨 Red Flag Detection
- **⚙️ Function**: [`detect_red_flags()`](../analyse_pipeline.py#L88-L110) in `analyse_pipeline.py`
- **🎯 Logic**: Compares scores against thresholds with page references

### 💡 Recommendation Engine
- **⚙️ Function**: [`generate_recommendations()`](../analyse_pipeline.py#L112-L118) in `analyse_pipeline.py`
- **📋 Output**: Parameter-specific actionable insights

## ⚡ Key Execution Points

| **🎯 Execution Stage** | **🔧 Function Called** | **📁 File Location** |
|---------------------|-------------------|------------------|
| **📤 File Upload Validation** | File upload check | [`app.py:26-27`](../app.py#L26-L27) |
| **📖 File Content Reading** | [`read_files()`](../Utils/utils.py#L42-L51) | `Utils/utils.py` |
| **🔍 Parameter Extraction** | [`content_to_json()`](../Utils/pdf_file_reader.py#L15-L51) | `Utils/pdf_file_reader.py` |
| **🎯 Scoring Conversion** | [`convert_raw_to_structured()`](../Utils/structured_2_scored_data.py#L69-L146) | `Utils/structured_2_scored_data.py` |
| **📊 Individual Parameter Scoring** | [`parse_team()`](../Utils/structured_2_scored_data.py#L44-L51), [`parse_market_size()`](../Utils/structured_2_scored_data.py#L9-L24), etc. | `Utils/structured_2_scored_data.py` |
| **🧮 Final Score Calculation** | Weighted sum | [`analyse_pipeline.py:38-41`](../analyse_pipeline.py#L38-L41) |
| **🚨 Red Flag Detection** | [`detect_red_flags()`](../analyse_pipeline.py#L88-L110) | `analyse_pipeline.py` |
| **💡 Recommendation Generation** | [`generate_recommendations()`](../analyse_pipeline.py#L112-L118) | `analyse_pipeline.py` |
| **📊 Dashboard Display** | Streamlit rendering | [`app.py:35-89`](../app.py#L35-L89) |

## ⚠️ Error Handling Points

- **📤 File Upload Validation** - [`app.py:26-28`](../app.py#L26-L28) - Missing pitch deck check
- **📖 File Reading Errors** - [`Utils/utils.py:30-31`](../Utils/utils.py#L30-L31) - DOCX processing exceptions  
- **🔍 Content Extraction** - [`Utils/pdf_file_reader.py`](../Utils/pdf_file_reader.py) - Malformed document handling
- **🎯 Scoring Validation** - [`Utils/structured_2_scored_data.py`](../Utils/structured_2_scored_data.py) - Invalid parameter values
