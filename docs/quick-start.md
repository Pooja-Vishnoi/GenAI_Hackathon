# 🚀 Quick Start Guide

## ⚡ 5-Minute Setup

### 📋 Prerequisites
- Python 3.8 or higher
- pip package manager
- 2GB free disk space

### 🎯 Quick Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd GenAI_Hackathon

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run app.py
```

### 🌐 Access the Application
Open your browser and navigate to: `http://localhost:8501`

## 🎪 Demo Mode

### 🎯 Quick Test with Sample Data

1. **Start the app**:
   ```bash
   streamlit run app.py
   ```

2. **Upload sample files** (found in `input/` folder):
   - 📊 **Pitch Deck**: `startup_ptch_deck.pdf` (Required)
   - 📝 **Call Transcript**: `transcript.txt` (Optional)
   - 👤 **Founder Material**: `founder_material.docx` (Optional)

3. **Click "🔍 Analyse"** button

4. **View Results**:
   - 📊 Overall score (0-10)
   - 🎯 Parameter scores
   - 🚨 Red flags
   - 💡 Recommendations

## 📤 Your First Analysis

### Step 1: Prepare Documents
Gather your startup documents:
- **Pitch Deck** (PDF format) - **Required**
- **Call Transcripts** (TXT format) - Optional
- **Founder Profiles** (DOCX format) - Optional

### Step 2: Upload Files
1. Click on **"📊 Upload Pitch Deck"**
2. Select your PDF file
3. Optionally add transcript and founder materials

### Step 3: Run Analysis
1. Click **"🔍 Analyse Documents"**
2. Wait for processing (typically 5-10 seconds)

### Step 4: Review Results
- **📊 Score Dashboard**: View overall and parameter scores
- **✏️ Edit Parameters**: Modify scores in real-time
- **🔄 Re-analyze**: Update analysis after edits

## 🎯 Understanding the Output

### Score Interpretation
| **Score Range** | **Investment Signal** | **Meaning** |
|-----------------|----------------------|-------------|
| 8.0 - 10.0 | 🟢 **Strong Buy** | Excellent investment opportunity |
| 6.0 - 7.9 | 🟡 **Consider** | Good potential with some concerns |
| 4.0 - 5.9 | 🟠 **Caution** | Significant risks, needs improvement |
| 1.0 - 3.9 | 🔴 **Pass** | High risk, not recommended |

### Key Parameters Evaluated
1. **👥 Team Quality** (15% weight) - Founder experience & education
2. **🌍 Market Size** (15% weight) - Total addressable market
3. **📈 Traction** (15% weight) - User growth & engagement
4. **💰 Financials** (10% weight) - Revenue & profitability
5. **🚀 Product Uniqueness** (15% weight) - Innovation & differentiation
6. **🏆 Competition** (10% weight) - Competitive landscape
7. **💼 Business Model** (10% weight) - Revenue model clarity
8. **⚠️ Risk Factors** (10% weight) - Operational risks

## 🔄 Interactive Features

### ✏️ Real-time Editing
1. Click on any score in the data editor
2. Modify the value (1-10)
3. See instant impact on final score

### 🔄 Re-analysis
1. After editing parameters
2. Click **"🔄 Analyse Again"**
3. Get updated recommendations

## 🆘 Quick Troubleshooting

### Issue: App won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: File upload fails
- Ensure file size < 200MB
- Check file format (PDF, DOCX, TXT only)
- Try with sample files first

### Issue: Analysis errors
```bash
# Clear Streamlit cache
streamlit cache clear

# Restart application
streamlit run app.py
```

## 📚 Next Steps

### Explore Documentation
- 📖 [Full Setup Guide](./SETUP_INSTRUCTIONS.md)
- 🏗️ [Architecture Overview](./architecture.md)
- 🔧 [API Reference](./api-reference.md)
- 🎨 [UI/UX Guide](./UI-UX.md)

### Advanced Features
- Customize scoring weights
- Add new parameters
- Integrate with APIs
- Export analysis reports

### Get Help
- Check [Troubleshooting Guide](./troubleshooting.md)
- Review [Configuration Options](./configuration.md)
- Explore [Sample Data](../input/)

## 🎉 Success Checklist

- [ ] ✅ Python 3.8+ installed
- [ ] ✅ Virtual environment created
- [ ] ✅ Dependencies installed
- [ ] ✅ App running on localhost:8501
- [ ] ✅ Sample analysis completed
- [ ] ✅ Results displayed correctly

**🚀 You're ready to analyze startups!**
