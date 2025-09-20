# 🎯 Complete Guide: Using the Startup Analysis System

## ✅ Current Status

Your **Startup Analysis API is now fully integrated** with the UI! The API successfully:
- ✅ Extracts data from uploaded documents (PDF, DOCX, TXT)
- ✅ Analyzes startup metrics and generates scores (you got 6.3/10 for Datastride Analytics)
- ✅ Returns structured data with parameters, benchmarks, and recommendations
- ✅ Integrates seamlessly with the frontend UI

## 🚀 Quick Start Guide

### Step 1: Start the API Server
```bash
cd /home/neosoft/test/GenAI_Hackathon
./run_api.sh
```
The server will run on `http://localhost:8000`

### Step 2: Open the UI
```bash
cd /home/neosoft/test/startup-analysis-ui-exp
python3 -m http.server 8080
```
Navigate to `http://localhost:8080/index.html`

### Step 3: Upload and Analyze Documents
1. Click the **"Add"** button in the Sources panel (left sidebar)
2. Upload your pitch deck or business documents (PDF, DOCX, TXT)
3. Click **"Add sources"**
4. The analysis will automatically run and display results

## 📊 What You'll See

### Your Current Results (Datastride Analytics / Sia):

#### 1. **Overall Score: 6.3/10**
   - Team Quality: 5.0 (Below Benchmark)
   - Market Size: 10.0 (Above Benchmark) ⭐
   - Traction: 5.0 (Below Benchmark)
   - Financials: 5.0 (Below Benchmark)
   - Product Uniqueness: 8.0 (Near Benchmark)
   - Competitive Landscape: 5.0 (Below Benchmark)
   - Business Model: 7.0 (Above Benchmark)
   - Risk Factors: 4.0 (Below Threshold) ⚠️

#### 2. **Investment Recommendation**
   - Status: **Moderate Investment Potential**
   - Sector Benchmark: 7.81
   - Your Score: 6.3 (Below Average)

#### 3. **Key Strengths**
   - Strong founding team
   - Large market size ($300B TAM)
   - Innovative AI platform (Sia)
   - Clear revenue model

#### 4. **Risk Factors**
   - High burn rate (₹14L/month)
   - Intense competitive pressure
   - Need for talent acquisition
   - Regional regulatory risks

## 🎨 UI Features

### Tabs Available:
1. **Scoring Matrix** - Detailed parameter scores with benchmarks
2. **Risk Analysis** - Red flags and mitigation strategies  
3. **AI Insights** - Investment recommendations
4. **Founder Analysis** - Team evaluation
5. **Visualize** - Charts and graphs
6. **Agent** - AI chat interface

### Key Metrics Displayed:
- Final weighted score
- Parameter-wise scoring
- Benchmark comparisons
- Investment recommendation
- Risk assessment
- Growth projections

## 🔧 API Endpoints

### Main Endpoints:
- `GET /` - Health check
- `POST /analyze` - Upload and analyze documents
- `GET /analyze/{session_id}` - Get previous analysis
- `GET /score/{session_id}` - Get investment score
- `GET /red-flags/{session_id}` - Get risk factors
- `GET /recommendations/{session_id}` - Get AI recommendations

### Test Endpoints:
- `GET /analyze-test` - Test with dummy data
- `GET /docs` - Interactive API documentation

## 📁 File Structure

```
GenAI_Hackathon/
├── api_server.py           # FastAPI server
├── analyse_pipeline.py     # Analysis logic
├── run_api.sh             # Startup script
├── requirements.txt        # All dependencies
└── Utils/                 # Utility functions

startup-analysis-ui-exp/
├── index.html             # Main UI
├── js/
│   └── api-client.js      # API integration
└── styles/                # CSS files
```

## 🐛 Troubleshooting

### If Analysis Returns Empty:
1. Check server logs for errors
2. Verify file format (PDF, DOCX, TXT)
3. Ensure files are not corrupted
4. Check if Gemini API is configured

### If UI Not Updating:
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify API is running
4. Clear browser cache

### Common Fixes:
```bash
# Install missing dependencies
cd GenAI_Hackathon
source venv/bin/activate
pip install -r requirements.txt

# Check API status
curl http://localhost:8000/

# Test with dummy data
curl http://localhost:8000/analyze-test
```

## 📈 Current Analysis Details

Your uploaded documents were successfully processed:
- **Company**: Datastride Analytics (Product: Sia)
- **Sector**: AI for Data Analytics
- **Founded**: 2021
- **Team**: 8+ years experience, Data & Domain expertise
- **Market**: $300B global data analytics industry
- **Traction**: Booked customers (Abha Hospital, IDBI Bank)
- **Revenue**: $400k booked, $400k pipeline
- **Burn Rate**: ₹14L/month
- **USP**: Agentic AI platform with chat interface

## 🎯 Next Steps

1. **Improve Score**: Focus on areas below benchmark
2. **Add More Documents**: Upload financial models, customer testimonials
3. **Customize Analysis**: Modify scoring weights in `analyse_pipeline.py`
4. **Export Results**: Use API to export as JSON/CSV
5. **Share Analysis**: Generate investment memo

## 💡 Pro Tips

1. **Batch Upload**: Upload multiple documents at once for comprehensive analysis
2. **Real-time Updates**: Use WebSocket connection for live updates
3. **Custom Scoring**: Adjust weights in `Utils/structured_2_scored_data.py`
4. **API Testing**: Use `/docs` endpoint for interactive testing
5. **Debug Mode**: Check server logs for detailed processing info

## 📞 Support

If you encounter issues:
1. Check server logs in terminal
2. Verify all dependencies installed
3. Ensure virtual environment activated
4. Check API documentation at `/docs`

---

**Your system is ready and working!** The API successfully analyzed your documents and generated a comprehensive investment analysis with a score of 6.3/10. 🚀
