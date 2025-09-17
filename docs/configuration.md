# ⚙️ Configuration Guide

## 📊 Scoring Parameters Configuration

### ⚖️ Parameter Weights
*📍 Location: `Utils/structured_2_scored_data.py:117-126`*

All weights sum to 1.0 for normalized scoring:

```python
weights = {
    'Team_Quality': 0.15,          # 15% - Team background & experience
    'Market_Size': 0.15,            # 15% - Total addressable market
    'Traction': 0.15,               # 15% - User growth & engagement
    'Financials': 0.10,             # 10% - Revenue & profitability
    'Product_Uniqueness': 0.15,     # 15% - Innovation & differentiation
    'Competitive_Landscape': 0.10,  # 10% - Market competition
    'Business_Model_Clarity': 0.10, # 10% - Revenue model clarity
    'Risk_Factors': 0.10            # 10% - Operational risks
}
```

### 🎯 Scoring Details

| **📊 Parameter** | **⚖️ Weight** | **📋 Description** | **🎯 Score Range** |
|-----------|--------|-------------|-------------|
| **👥 Team Quality** | 15% | Educational background, experience | 1-10 |
| **🌍 Market Size** | 15% | Total addressable market analysis | 1-10 |
| **📈 Traction** | 15% | User growth, engagement metrics | 1-10 |
| **💰 Financials** | 10% | Revenue, profitability, burn rate | 1-10 |
| **🚀 Product Uniqueness** | 15% | Innovation, differentiation | 1-10 |
| **🏆 Competitive Landscape** | 10% | Market competition analysis | 1-10 |
| **💼 Business Model Clarity** | 10% | Revenue model, scalability | 1-10 |
| **⚠️ Risk Factors** | 10% | Regulatory, operational risks | 1-10 |

### 🚨 Risk Thresholds
*📍 Location: `Utils/structured_2_scored_data.py:128-137`*

Minimum acceptable scores for red flag detection:

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

- Default threshold: **3/10** for all parameters
- Scores below threshold trigger red flags
- Overall score < 5 generates warning

### 📊 Industry Benchmarks
*📍 Location: `Utils/structured_2_scored_data.py:106-115`*

Sector-specific performance comparisons:

```python
benchmarks = {
    'Technology': {
        'Team_Quality': 7,
        'Market_Size': 8,
        'Traction': 6,
        'Financials': 5,
        'Product_Uniqueness': 8
    },
    'Finance': {
        'Team_Quality': 8,
        'Market_Size': 7,
        'Traction': 7,
        'Financials': 6,
        'Product_Uniqueness': 7
    }
    # Add more sectors as needed
}
```

## 📄 File Processing Configuration

### 📋 Supported Formats
*📍 Location: `Utils/utils.py:15-37`*

```python
SUPPORTED_FORMATS = {
    '.pdf': 'PyPDF2',      # PDF documents
    '.docx': 'python-docx', # Word documents
    '.doc': 'python-docx',  # Legacy Word documents
    '.txt': 'UTF-8'         # Plain text files
}
```

### 📏 File Size Limits

Handled by Streamlit default settings. To modify:

Create `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200  # MB
maxMessageSize = 200 # MB
```

### 👁️ OCR Support
*📍 Location: `tools/tools.py:50-68`*

Google Cloud Vision integration for scanned documents:

```python
# Enable OCR in configuration
OCR_ENABLED = True
GOOGLE_CLOUD_CREDENTIALS = "path/to/credentials.json"
```

## 🖥️ Streamlit UI Configuration

### 🎨 Theme Settings

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### 📊 Component Configuration
*📍 Location: `app.py:5-113`*

**Main Interface Components**:
- **Upload Phase** ([lines 15-33](../app.py#L15-L33))
- **Analysis Dashboard** ([lines 35-89](../app.py#L35-L89))
- **Data Editor** ([lines 49-55](../app.py#L49-L55))
- **Visualizations** ([lines 78-89](../app.py#L78-L89))
- **Action Buttons** ([lines 92-109](../app.py#L92-L109))

### 💾 Session State Management
*📍 Location: `app.py:8-11`*

```python
# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
    st.session_state.summary_df = None
    st.session_state.results_df = None
    st.session_state.final_score = None
    st.session_state.red_flags = []
    st.session_state.recommendations = []
```

## 🔧 Advanced Configuration

### 🤖 AI/LLM Integration (Future)

```python
# config.json
{
    "llm_provider": "openai",
    "model": "gpt-4",
    "api_key": "your-api-key",
    "temperature": 0.7,
    "max_tokens": 2000
}
```

### 📊 Database Configuration (Future)

```python
# database_config.py
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'startup_analysis',
    'user': 'admin',
    'password': 'secure_password'
}
```

### 📧 Notification Settings (Future)

```python
# notification_config.py
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'notifications@example.com',
    'sender_password': 'app_password'
}
```

## 🎯 Custom Scoring Rules

### Adding New Parameters

1. **Define in `structured_2_scored_data.py`**:
```python
def parse_new_parameter(param_str):
    # Custom parsing logic
    score = calculate_score(param_str)
    return min(10, max(1, score))
```

2. **Add to weights dictionary**:
```python
weights['New_Parameter'] = 0.05
# Adjust other weights to sum to 1.0
```

3. **Set threshold**:
```python
thresholds['New_Parameter'] = 3
```

### Modifying Scoring Logic

Example: Changing team scoring bonus:
```python
def parse_team(team_str):
    base_score = extract_team_size(team_str)
    
    # Custom bonus logic
    if "MIT" in team_str or "Stanford" in team_str:
        base_score += 3
    elif "IIT" in team_str or "IIM" in team_str:
        base_score += 2
    
    return min(10, base_score)
```

## 🔍 Debugging Configuration

### Enable Debug Mode

```python
# app.py
DEBUG_MODE = True

if DEBUG_MODE:
    st.sidebar.write("Debug Info:")
    st.sidebar.json(st.session_state)
```

### Logging Configuration

```python
# logging_config.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🚀 Performance Optimization

### Caching Configuration

```python
# Enable Streamlit caching
@st.cache_data
def process_files(uploaded_files):
    return read_files(uploaded_files)

@st.cache_resource
def load_benchmarks():
    return pd.read_csv('data/sector_benchmarks.csv')
```

### Memory Management

```python
# Clear cache periodically
st.cache_data.clear()
st.cache_resource.clear()
```
