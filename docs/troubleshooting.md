# 🔍 Troubleshooting Guide

## 🚨 Common Issues & Solutions

### 📄 1. PDF Processing Errors

#### **Problem**: Unable to read PDF files
```
Error: PyPDF2.errors.PdfReadError: Cannot read PDF file
```

#### **Solutions**:
```bash
# Install/upgrade PDF dependencies
pip install --upgrade PyPDF2
pip install pdfplumber

# For OCR support (scanned PDFs)
pip install google-cloud-vision
```

#### **Alternative Approach**:
```python
# Use pdfplumber as fallback
import pdfplumber

def read_pdf_alternative(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text
```

---

### 🖥️ 2. Streamlit Import Errors

#### **Problem**: Module import failures
```
ModuleNotFoundError: No module named 'streamlit'
```

#### **Solutions**:
```bash
# Upgrade Streamlit
pip install --upgrade streamlit

# Clear cache
streamlit cache clear

# Verify installation
streamlit --version
```

---

### 💾 3. Memory Issues with Large Files

#### **Problem**: Application crashes with large documents
```
Error: Maximum message size exceeded
```

#### **Solution 1**: Increase upload limits
Create/edit `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500  # Increase to 500MB
maxMessageSize = 500
```

#### **Solution 2**: Implement file chunking
```python
def process_large_file(file, chunk_size=1024*1024):
    chunks = []
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        chunks.append(chunk)
    return b''.join(chunks)
```

---

### 📊 4. Data Processing Errors

#### **Problem**: DataFrame conversion failures
```
ValueError: Cannot convert to DataFrame
```

#### **Debug Steps**:
```python
# Add debugging output
print(f"Data type: {type(data)}")
print(f"Data shape: {data.shape if hasattr(data, 'shape') else 'N/A'}")
print(f"Data content: {data[:100]}")  # First 100 chars

# Validate data before processing
if not isinstance(data, pd.DataFrame):
    data = pd.DataFrame(data)
```

---

### 🔄 5. Session State Issues

#### **Problem**: Lost data after page refresh
```
KeyError: 'st.session_state has no key "analysis_complete"'
```

#### **Solution**: Initialize session state properly
```python
# Add to top of app.py
def initialize_session_state():
    defaults = {
        'analysis_complete': False,
        'summary_df': None,
        'results_df': None,
        'final_score': None,
        'red_flags': [],
        'recommendations': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Call at app start
initialize_session_state()
```

---

### 📝 6. DOCX File Reading Issues

#### **Problem**: Cannot read .docx files
```
Error: Package not found at 'document.xml'
```

#### **Solutions**:
```bash
# Reinstall python-docx
pip uninstall python-docx
pip install python-docx

# For legacy .doc files
pip install python-docx2txt
```

#### **Fallback implementation**:
```python
import docx2txt

def read_doc_fallback(file):
    try:
        text = docx2txt.process(file)
        return text
    except Exception as e:
        st.error(f"Failed to read document: {e}")
        return ""
```

---

### 🎯 7. Scoring Calculation Errors

#### **Problem**: Incorrect score calculations
```
ValueError: Score out of range (1-10)
```

#### **Debug & Fix**:
```python
def validate_score(score, param_name):
    """Ensure score is within valid range"""
    if not isinstance(score, (int, float)):
        print(f"Warning: {param_name} score is not numeric: {score}")
        return 5  # Default score
    
    if score < 1:
        print(f"Warning: {param_name} score too low: {score}")
        return 1
    elif score > 10:
        print(f"Warning: {param_name} score too high: {score}")
        return 10
    
    return score

# Apply validation
score = validate_score(calculated_score, "Team_Quality")
```

---

### 🚨 8. Red Flag Detection Issues

#### **Problem**: Red flags not showing correctly
```
No red flags displayed despite low scores
```

#### **Debug Steps**:
```python
# Add debug logging
def detect_red_flags(df, score):
    print(f"DataFrame columns: {df.columns.tolist()}")
    print(f"Score values: {df.to_dict()}")
    print(f"Overall score: {score}")
    
    flags = []
    for column in df.columns:
        value = df[column].iloc[0]
        print(f"Checking {column}: {value} against threshold 3")
        if value < 3:
            flags.append(f"{column} is below threshold")
    
    return flags
```

---

### 🌐 9. API/External Service Errors

#### **Problem**: Google Cloud Vision API failures
```
Error: Invalid credentials for Google Cloud Vision
```

#### **Solution**:
```python
# Set up credentials
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

# Verify credentials
from google.cloud import vision
client = vision.ImageAnnotatorClient()
```

---

### 📈 10. Visualization Errors

#### **Problem**: Charts not rendering
```
Error: Cannot render chart with empty data
```

#### **Fix**:
```python
# Validate data before plotting
if df is not None and not df.empty:
    st.bar_chart(df)
else:
    st.warning("No data available for visualization")
```

---

## 🛠️ Debug Mode

### Enable Comprehensive Debugging

Add this to your `app.py`:
```python
DEBUG_MODE = st.sidebar.checkbox("🔧 Debug Mode")

if DEBUG_MODE:
    st.sidebar.subheader("📊 Session State")
    st.sidebar.json(dict(st.session_state))
    
    st.sidebar.subheader("📁 Uploaded Files")
    if uploaded_files:
        for file in uploaded_files:
            st.sidebar.write(f"- {file.name} ({file.size} bytes)")
    
    st.sidebar.subheader("🎯 Current Scores")
    if st.session_state.results_df is not None:
        st.sidebar.dataframe(st.session_state.results_df)
```

---

## 📝 Logging Setup

### Configure Detailed Logging

Create `logging_config.py`:
```python
import logging
import sys
from datetime import datetime

# Create logs directory
import os
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now():%Y%m%d}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Usage in code
logger.debug("Processing file: %s", filename)
logger.info("Analysis complete. Score: %f", score)
logger.error("Failed to process: %s", error)
```

---

## 🔄 Recovery Procedures

### 1. Complete Reset
```bash
# Clear all caches and restart
streamlit cache clear
rm -rf __pycache__
rm -rf .streamlit/cache
streamlit run app.py
```

### 2. Data Recovery
```python
# Add backup mechanism
import pickle

def save_backup(data, filename='backup.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_backup(filename='backup.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
```

### 3. Environment Reset
```bash
# Recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🆘 Getting Help

### 📚 Resources
- **Documentation**: Check `/docs` folder for detailed guides
- **Code Comments**: Review inline documentation in source files
- **Sample Data**: Use files in `/input` folder for testing

### 🐛 Reporting Issues
When reporting issues, include:
1. **Error message** (full traceback)
2. **Steps to reproduce**
3. **File types and sizes** being processed
4. **Python version** (`python --version`)
5. **Package versions** (`pip freeze`)
6. **Operating system**

### 💡 Quick Fixes Checklist
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Correct Python version (3.8+)
- [ ] Virtual environment activated
- [ ] Streamlit cache cleared
- [ ] File permissions correct
- [ ] Sufficient memory available
- [ ] Network connection stable (for API calls)
