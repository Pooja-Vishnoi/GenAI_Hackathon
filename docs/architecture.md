# 🏗️ Architecture Documentation

## 🎯 Frontend-Backend Separation

The application follows a clear **Frontend-Backend architecture**:

- **🖥️ Frontend (`app.py`)**: Streamlit-based UI that handles user interactions, file uploads, and data visualization
- **⚙️ Backend (`analyse_pipeline.py`)**: Core processing engine that performs analysis, scoring, and recommendation generation

```mermaid
graph TB
    subgraph FRONTEND["🖥️ FRONTEND - app.py"]
        UI[Streamlit UI]
        FU[File Upload Interface]
        DE[Data Editor]
        VIZ[Visualizations]
        BTN[Action Buttons]
    end
    
    subgraph BACKEND["⚙️ BACKEND - analyse_pipeline.py"]
        CR[create_results]
        AR[analyze_results]
        DF[detect_red_flags]
        GR[generate_recommendations]
    end
    
    UI --> FU
    FU -->|Uploaded Files| CR
    CR -->|Results DataFrame| DE
    DE -->|Modified Data| AR
    AR -->|Updated Scores| VIZ
    BTN -->|Re-analyze| AR
    
    style UI fill:#4285f4,color:#fff
    style CR fill:#34a853,color:#fff
```

## 🔄 Complete Application Flow

```mermaid
flowchart TD
    subgraph FRONTEND["🖥️ FRONTEND (app.py)"]
        START([User Opens App]) --> UPLOAD[File Upload UI]
        UPLOAD --> VALIDATE{Files Valid?}
        VALIDATE -->|No| ERROR[Show Error]
        VALIDATE -->|Yes| ANALYZE_BTN[Click Analyze Button]
        
        RESULTS_UI[Display Results Dashboard]
        EDIT_UI[Data Editor Interface]
        REANALYZE_BTN[Re-analyze Button]
    end
    
    subgraph BACKEND["⚙️ BACKEND (analyse_pipeline.py)"]
        CREATE_RESULTS[create_results]
        ANALYZE_RESULTS[analyze_results]
        
        subgraph UTILS["📚 Utils Functions"]
            READ_FILES[read_files]
            CONTENT_JSON[content_to_json]
            CONVERT_STRUCT[convert_raw_to_structured]
        end
        
        subgraph ANALYSIS["🧠 Analysis Functions"]
            DETECT_RED[detect_red_flags]
            DETECT_GREEN[detect_green_flags]
            GEN_REC[generate_recommendations]
        end
    end
    
    ANALYZE_BTN -->|Call| CREATE_RESULTS
    CREATE_RESULTS --> READ_FILES
    READ_FILES --> CONTENT_JSON
    CONTENT_JSON --> CONVERT_STRUCT
    CONVERT_STRUCT --> DETECT_RED
    CONVERT_STRUCT --> DETECT_GREEN
    DETECT_RED --> GEN_REC
    DETECT_GREEN --> GEN_REC
    
    CREATE_RESULTS -->|Return Results| RESULTS_UI
    RESULTS_UI --> EDIT_UI
    EDIT_UI --> REANALYZE_BTN
    REANALYZE_BTN -->|Call| ANALYZE_RESULTS
    ANALYZE_RESULTS -->|Update| RESULTS_UI
    
    style UPLOAD fill:#4285f4,color:#fff
    style CREATE_RESULTS fill:#34a853,color:#fff
    style ANALYZE_RESULTS fill:#fbbc05,color:#000
```

## 🏛️ High-Level System Overview

```mermaid
graph LR
    A[📄 Documents] --> B[🖥️ Frontend<br/>app.py]
    B --> C[⚙️ Backend<br/>analyse_pipeline.py]
    C --> D[🧠 Analysis Engine]
    D --> B
    B --> E[📊 Interactive Dashboard]
```

## 📋 Key Function Calls Between Frontend & Backend

| **Frontend Action (app.py)** | **Backend Function Called** | **Purpose** | **Returns** |
|------------------------------|----------------------------|------------|-------------|
| **User clicks "🔍 Analyze"** | `create_results(uploaded_files)` | Initial document analysis | summary_df, results_df, score, flags, recommendations |
| **User edits data in UI** | `analyze_results(structured_df)` | Re-calculate scores | final_score, flags, recommendations |
| **User clicks "🔄 Re-analyze"** | `analyze_results(structured_df)` | Refresh analysis | final_score, flags, recommendations |
| **Dashboard loads** | Uses returned DataFrames | Display results | N/A - uses stored session state |

## 🔧 Detailed Architecture Layers

### 🎨 Layer 1: Frontend User Interface (`app.py`)
```mermaid
graph TB
    UI[Streamlit Web App - app.py]
    UP[File Upload - Lines 538-584]
    DA[Dashboard Display - Lines 749-823]
    ME[Metrics Display - Lines 589-640]
    IN[Insights Display - Lines 645-682]
    
    UI --> UP
    UI --> DA
    UI --> ME
    UI --> IN
```

### ⚙️ Layer 2: Backend Processing Pipeline (`analyse_pipeline.py`)
```mermaid
graph LR
    INPUT[Input Files] --> CR[create_results - Lines 18-67]
    CR --> RF[read_files]
    RF --> PE[content_to_json]
    PE --> SC[convert_raw_to_structured]
    SC --> AR[analyze_results - Lines 151-167]
```

### 🧠 Layer 3: Analysis Engine (8 Parameters)
```mermaid
graph TB
    SC[Scoring Engine] --> PARAMS{Parameter Analysis}
    
    PARAMS --> TS[Team Quality]
    PARAMS --> MS[Market Size]
    PARAMS --> TR[Traction]
    PARAMS --> FS[Financials]
    PARAMS --> PS[Product Uniqueness]
    PARAMS --> CS[Competition Analysis]
    PARAMS --> BS[Business Model]
    PARAMS --> RS[Risk Factors]
```

### 🤖 Layer 4: Intelligence & Output
```mermaid
graph TB
    SCORES[Parameter Scores] --> RF_ENGINE[Red Flag Detector]
    SCORES --> REC_ENGINE[Recommendation Engine]
    BENCH[Benchmarks] --> REC_ENGINE
    
    RF_ENGINE --> OUTPUT[Final Results]
    REC_ENGINE --> OUTPUT
    
    OUTPUT --> DASHBOARD[Return to Frontend]
```

## 🧩 Detailed Component Architecture

### 🎨 1. User Interface Layer
- **🖥️ [`Streamlit Web App`](../app.py)** - Main application interface
  - **📤 [File Upload Interface](../app.py#L18-L23)**: Multi-format document upload with validation
  - **📊 [Interactive Dashboard](../app.py#L35-L89)**: Real-time results display and editing
  - **📈 [Data Visualizations](../app.py#L78-L89)**: Charts, trends, and benchmark comparisons

### ⚙️ 2. Processing Pipeline Layer
- **🔄 [`Main Pipeline`](../analyse_pipeline.py#L7-L55)** - Orchestrates entire analysis workflow
  - **📖 [`File Reader`](../Utils/utils.py#L42-L51)** - Batch processing of uploaded documents
  - **🔍 [`Parameter Extractor`](../Utils/pdf_file_reader.py#L15-L51)** - AI-powered content analysis
  - **🎯 [`Scoring Engine`](../Utils/structured_2_scored_data.py#L69-L146)** - Transforms text to numerical scores

### 🧠 3. Analysis Engine - 8-Parameter Evaluation System
- **👥 [`Team Scorer`](../Utils/structured_2_scored_data.py#L44-L51)** - Educational background + experience analysis
- **🌍 [`Market Analyzer`](../Utils/structured_2_scored_data.py#L9-L24)** - TAM size evaluation with regex parsing
- **📈 [`Traction Evaluator`](../Utils/structured_2_scored_data.py#L26-L42)** - User growth + MoM metrics
- **💰 [Financial Scorer](../Utils/structured_2_scored_data.py#L87)** - Revenue, ARR, burn rate assessment
- **🚀 [Product Scorer](../Utils/structured_2_scored_data.py#L88)** - Innovation, differentiation, AI/tech analysis
- **🏆 [Competition Analyzer](../Utils/structured_2_scored_data.py#L89-L91)** - Market saturation and competitive positioning
- **💼 [Business Model Scorer](../Utils/structured_2_scored_data.py#L92)** - Revenue model clarity and scalability
- **⚠️ [Risk Assessor](../Utils/structured_2_scored_data.py#L93)** - Regulatory, operational, market risk evaluation

### 🤖 4. Intelligence Layer - Advanced Analytics
- **🚨 [`Red Flag Detector`](../analyse_pipeline.py#L88-L110)** - Threshold-based risk identification
- **💡 [`Recommendation Engine`](../analyse_pipeline.py#L112-L118)** - Actionable insights generation
- **📊 [`Benchmark Comparator`](../data/sector_benchmarks.csv)** - Industry-specific performance analysis

### 📚 5. Data Layer - Information Management
- **📄 Input Documents** - Multi-format file processing (PDF, DOCX, TXT)
- **📊 Benchmark Data** - Sector-specific performance metrics
- **⚙️ Configuration** - Parameter weights, thresholds, scoring rules
- **📋 Analysis Results** - Structured output with scores, flags, recommendations
