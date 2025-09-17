# 🔧 API Reference

## 📚 Core Functions

### 🚀 `create_results(uploaded_files)`
*📍 Location: `analyse_pipeline.py:7-55`*

**🎯 Purpose**: Main analysis pipeline that processes uploaded files and generates comprehensive startup evaluation.

**🔄 Process Flow**:
1. 📖 Extract content from files using [`read_files()`](../Utils/utils.py#L42-L51) 
2. 🔄 Convert to structured JSON via [`content_to_json()`](../Utils/pdf_file_reader.py#L15-L51)
3. 📊 Create parameter DataFrame ([`create_results()` lines 23-28](../analyse_pipeline.py#L23-L28))
4. 🎯 Apply scoring algorithms via [`convert_raw_to_structured()`](../Utils/structured_2_scored_data.py#L69-L146)
5. ⚖️ Calculate weighted scores and final rating
6. 🚨 Generate red flags via [`detect_red_flags()`](../analyse_pipeline.py#L88-L110) and 💡 recommendations via [`generate_recommendations()`](../analyse_pipeline.py#L112-L118)

**📥 Parameters**: 
- `uploaded_files` - List of Streamlit file objects

**📤 Returns**: 
- `summary_df` - Summary DataFrame with company info
- `results_df` - Detailed results with scores
- `final_score` - Overall weighted score (0-10)
- `flags` - List of red flags detected
- `recommendations` - List of actionable recommendations

**Example Usage**:
```python
summary_df, results_df, final_score, flags, recommendations = create_results(uploaded_files)
```

---

### 🔄 `analyze_results(structured_df)`
*📍 Location: `analyse_pipeline.py:120-135`*

**🎯 Purpose**: Re-analyzes data after user modifications in interactive dashboard.

**Operations**: 
- Recalculates weighted scores
- Refreshes red flags
- Updates recommendations

**📥 Parameters**: 
- `structured_df` - Modified DataFrame from UI

**📤 Returns**: 
- `final_score` - Updated overall score
- `flags` - Updated list of red flags
- `recommendations` - Updated recommendations

**Example Usage**:
```python
final_score, flags, recommendations = analyze_results(structured_df)
```

---

## 📚 Utility Functions

### 📖 `read_files(uploaded_files)`
*📍 Location: `Utils/utils.py:42-51`*

**🎯 Purpose**: Batch file processing for multiple document types

**📥 Parameters**: 
- `uploaded_files` - List of uploaded file objects

**📤 Returns**: 
- Combined text content from all files

**Calls**: [`read_file()`](../Utils/utils.py#L8-L39) for individual file processing

---

### 📄 `read_file(file)`
*📍 Location: `Utils/utils.py:8-39`*

**🎯 Purpose**: Reads individual file and extracts text content

**📥 Parameters**: 
- `file` - Single file object (PDF, DOCX, or TXT)

**📤 Returns**: 
- Extracted text content as string

**Supported Formats**:
- 📄 PDF - Using PyPDF2
- 📝 DOCX/DOC - Using python-docx
- 📄 TXT - UTF-8 text files

---

### 🤖 `content_to_json(content)` 🚧 **[TO BE IMPLEMENTED]**
*📍 Location: `Utils/pdf_file_reader.py:15-51`*

**🎯 Purpose**: Converts raw text to structured startup parameters using AI/LLM

**📥 Parameters**: 
- `content` - Raw text content from documents

**📤 Returns**: 
- Structured JSON with company parameters

**Current Status**: ⚠️ Uses hardcoded sample data - **AI integration pending**

**Next Steps**: Integrate with GPT-4/Claude for dynamic content analysis

---

### 🔄 `convert_raw_to_structured(raw_df)`
*📍 Location: `Utils/structured_2_scored_data.py:69-146`*

**🎯 Purpose**: Transforms parameters into scored format with benchmarks

**📥 Parameters**: 
- `raw_df` - DataFrame with raw parameter values

**📤 Returns**: 
- DataFrame with scored parameters (1-10 scale)

**Key Functions Used**: 
- [`parse_team()`](../Utils/structured_2_scored_data.py#L44-L51)
- [`parse_market_size()`](../Utils/structured_2_scored_data.py#L9-L24)
- [`parse_traction()`](../Utils/structured_2_scored_data.py#L26-L42)

---

## 🎯 Scoring Functions
*All located in [`Utils/structured_2_scored_data.py`](../Utils/structured_2_scored_data.py)*

### 👥 `parse_team(team_str)`
*📍 Location: Lines 44-51*

**🎯 Purpose**: Team background scoring with IIT/IIM bonuses

**📥 Parameters**: 
- `team_str` - String describing team composition

**📤 Returns**: 
- Score (1-10) based on team quality

**Scoring Logic**:
- Base score from team size
- +2 points for IIT/IIM backgrounds
- Maximum score: 10

---

### 🌍 `parse_market_size(market_str)`
*📍 Location: Lines 9-24*

**🎯 Purpose**: Market size analysis with B/M regex parsing

**📥 Parameters**: 
- `market_str` - String describing market size

**📤 Returns**: 
- Score (1-10) based on TAM size

**Scoring Logic**:
- $50B+ → 10 points
- $10-50B → 8 points
- $1-10B → 6 points
- <$1B → 4 points

---

### 📈 `parse_traction(traction_str)`
*📍 Location: Lines 26-42*

**🎯 Purpose**: User growth and MoM metrics evaluation

**📥 Parameters**: 
- `traction_str` - String describing traction metrics

**📤 Returns**: 
- Score (1-10) based on growth metrics

**Scoring Logic**:
- User count evaluation
- MoM growth rate assessment
- Combined weighted score

---

## 🧠 Analysis Functions

### 🚨 `detect_red_flags(df, score)`
*📍 Location: `analyse_pipeline.py:88-110`*

**🎯 Purpose**: Identifies parameters below acceptable thresholds

**📥 Parameters**: 
- `df` - DataFrame with scored parameters
- `score` - Overall weighted score

**📤 Returns**: 
- List of red flag strings with page references

**Detection Logic**:
- Checks each parameter against threshold (default: 3/10)
- Adds page references for traceability
- Includes overall score warning if < 5

---

### 💡 `generate_recommendations(df, flags)`
*📍 Location: `analyse_pipeline.py:112-118`*

**🎯 Purpose**: Generates actionable insights based on analysis

**📥 Parameters**: 
- `df` - DataFrame with scored parameters
- `flags` - List of detected red flags

**📤 Returns**: 
- List of recommendation strings

**Recommendation Logic**:
- Parameter-specific suggestions
- Priority-based ordering
- Actionable improvement steps

---

## 📊 Configuration Functions

### ⚖️ Weight & Benchmark Configs
*📍 Location: `Utils/structured_2_scored_data.py:106-137`*

**Parameter Weights** (Lines 117-126):
```python
weights = {
    'Team_Quality': 0.15,
    'Market_Size': 0.15,
    'Traction': 0.15,
    'Financials': 0.10,
    'Product_Uniqueness': 0.15,
    'Competitive_Landscape': 0.10,
    'Business_Model_Clarity': 0.10,
    'Risk_Factors': 0.10
}
```

**Risk Thresholds** (Lines 128-137):
```python
thresholds = {
    'Team_Quality': 3,
    'Market_Size': 3,
    'Traction': 3,
    'Financials': 3,
    'Product_Uniqueness': 3,
    'Competitive_Landscape': 3,
    'Business_Model_Clarity': 3,
    'Risk_Factors': 3
}
```

---

## 🖥️ UI Functions

### 📤 File Upload Handler
*📍 Location: `app.py:15-33`*

**Components**:
- Pitch deck uploader (required)
- Call transcript uploader (optional)
- Founder material uploader (optional)

### 📊 Dashboard Renderer
*📍 Location: `app.py:35-89`*

**Components**:
- Score display
- Parameter editor
- Charts and visualizations
- Red flags display
- Recommendations panel

### 🔄 Session State Manager
*📍 Location: `app.py:8-11`*

**Manages**:
- Analysis results
- User modifications
- UI state persistence
