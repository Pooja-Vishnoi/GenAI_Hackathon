# 🚀 Startup Analysis API Integration Guide

## Overview
This guide explains how to integrate the Startup Analysis FastAPI backend with your UI (index.html).

## Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌────────────────┐
│                 │         │                  │         │                │
│   Frontend UI   │ <-----> │  FastAPI Server  │ <-----> │ Analysis       │
│  (index.html)   │  HTTP   │  (api_server.py) │         │ Pipeline       │
│                 │         │                  │         │(analyse_pipeline.py)
└─────────────────┘         └──────────────────┘         └────────────────┘
```

## Quick Setup (3 Steps)

### Step 1: Start the API Server
```bash
cd GenAI_Hackathon
./run_api.sh

# Server will run on http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Step 2: Open the UI
```bash
# Open in browser
cd startup-analysis-ui-exp
python3 -m http.server 8080

# Navigate to http://localhost:8080/index.html
```

### Step 3: Test the Integration
1. Click "Add" button in Sources panel
2. Upload your pitch deck/documents
3. Click "Add sources"
4. Results will appear in the Scoring Matrix tab

## Key Integration Points

### 1. File Upload Flow
```javascript
// Frontend (index.html)
uploadSources() → analysisAPI.analyzeDocuments() → API Server → analyse_pipeline.py
```

### 2. API Endpoints Used
- **POST /analyze** - Main document analysis
- **GET /score/{session_id}** - Investment score
- **GET /red-flags/{session_id}** - Risk factors
- **GET /green-flags/{session_id}** - Positive indicators
- **POST /recommendations/{session_id}** - AI recommendations

### 3. Data Flow

1. **Upload Documents**
   ```javascript
   // Frontend
   const results = await analysisAPI.analyzeDocuments(files, {
       startup_name: 'Datastride Analytics',
       sector: 'Technology'
   });
   ```

2. **Server Processing**
   ```python
   # api_server.py
   @app.post("/analyze")
   async def analyze_documents():
       # Calls analyse_pipeline.create_results()
       df, structured_df, final_score, flags, recommendations = create_results(files)
   ```

3. **UI Update**
   ```javascript
   // Frontend receives and displays
   updateUIWithAnalysis(results);
   updateScoringTable(results.analysis.structured_data);
   updateFinalScore(results.analysis.final_score);
   ```

## Testing the Integration

### Test Page
Open `startup-analysis-ui-exp/api-test.html` for a simplified testing interface.

### Manual Testing with cURL
```bash
# Test API health
curl http://localhost:8000/

# Upload and analyze
curl -X POST "http://localhost:8000/analyze" \
     -F "files=@your_pitch_deck.pdf" \
     -F "startup_name=Test Startup" \
     -F "sector=Technology"
```

## UI Components Integration

### Scoring Matrix Tab
```javascript
// Automatically populated from API response
updateScoringTable(data.analysis.structured_data);
```

### Risk Analysis Tab
```javascript
// Red flags from API
updateRedFlags(data.analysis.red_flags);
// Green flags
updateGreenFlags(data.analysis.green_flags);
```

### AI Insights Tab
```javascript
// Recommendations from API
updateRecommendations(data.analysis.recommendations);
```

### Agent Tab (Chat Interface)
```javascript
// Can query the API for specific insights
const response = await analysisAPI.getRecommendations(sessionId, 'financial');
```

## Configuration

### API Server Configuration
Edit `api_server.py`:
```python
# CORS settings for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend Configuration
Edit `js/api-client.js`:
```javascript
// Change API URL for production
const analysisAPI = new StartupAnalysisAPI('https://api.your-domain.com');
```

## Common Issues & Solutions

### Issue: CORS Error
**Solution:** Ensure API server is running and CORS is configured correctly.

### Issue: File Upload Fails
**Solution:** Check file size (max 10MB) and format (PDF, DOC, DOCX, etc.).

### Issue: No Analysis Results
**Solution:** 
1. Check API server logs
2. Verify file content extraction is working
3. Check if all required Python packages are installed

### Issue: UI Not Updating
**Solution:** 
1. Open browser console for errors
2. Verify API response format
3. Check if updateUIWithAnalysis function is called

## Advanced Features

### Real-time Updates with WebSocket
```javascript
// Connect WebSocket for live updates
const ws = analysisAPI.connectWebSocket(sessionId, (data) => {
    console.log('Real-time update:', data);
    updateUIWithAnalysis(data);
});
```

### Export Results
```javascript
// Export as JSON
const jsonData = await analysisAPI.exportAnalysis(sessionId, 'json');

// Export as CSV
const csvData = await analysisAPI.exportAnalysis(sessionId, 'csv');
```

### Recalculate with Modified Data
```javascript
// User edits scores in UI
const updatedData = getModifiedTableData();
const newResults = await analysisAPI.recalculateAnalysis(sessionId, updatedData);
```

## Production Deployment

### Using Docker
```dockerfile
# Dockerfile for API
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using PM2
```bash
pm2 start ecosystem.config.js
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }
}
```

## API Response Format

### Success Response
```json
{
  "status": "success",
  "session_id": "analysis_20240120_143022",
  "analysis": {
    "final_score": 8.2,
    "structured_data": [...],
    "red_flags": [...],
    "green_flags": [...],
    "recommendations": {...}
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "details": "Detailed error information"
}
```

## Performance Tips

1. **Cache Results**: API caches analysis results by session ID
2. **Batch Requests**: Use parallel API calls where possible
3. **File Compression**: Compress large documents before upload
4. **Lazy Loading**: Load UI components as needed

## Security Considerations

1. **API Key Authentication** (for production)
2. **Rate Limiting** to prevent abuse
3. **File Validation** to prevent malicious uploads
4. **HTTPS** for production deployment
5. **Input Sanitization** for all user inputs

## Support & Debugging

### Check API Status
```javascript
// In browser console
fetch('http://localhost:8000/')
  .then(r => r.json())
  .then(console.log);
```

### View API Logs
```bash
# In terminal running API server
# Logs will show all requests and errors
```

### Browser DevTools
1. Network tab - Check API calls
2. Console - JavaScript errors
3. Application - Check localStorage/sessionStorage

## Next Steps

1. ✅ API Server is running
2. ✅ Frontend is connected
3. ✅ Documents can be analyzed
4. 🔄 Customize scoring algorithms in `analyse_pipeline.py`
5. 🔄 Add more visualization in UI
6. 🔄 Implement user authentication
7. 🔄 Deploy to production

## Contact & Support

For issues or questions:
- Check API documentation at `/docs`
- Review error messages in console
- Check server logs for detailed errors

---

**Built for GenAI Exchange Hackathon** 🚀
