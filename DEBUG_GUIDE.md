# 🔍 Debugging Guide for Startup Analysis API

## Issue: Empty Results After File Upload

Your API is working but returning empty analysis results. Here's how to fix it:

## 1. Test the Pipeline First

```bash
# Test with dummy data (no file upload needed)
curl http://localhost:8000/analyze-test
```

This should return analysis results with dummy data. If this works, the analysis pipeline is OK.

## 2. Check Server Logs

When you upload files, the server will now print detailed debug logs:

```
[API] Analyzing 2 files: ['/tmp/file1.pdf', '/tmp/file2.pdf']
[DEBUG] Processing file: /tmp/file1.pdf
[DEBUG] Extracting text from PDF: /tmp/file1.pdf
[DEBUG] Extracted 5000 characters from PDF
[DEBUG] Calling content_to_json with 2 files
[DEBUG] Extracted data: {...}
[DEBUG] Final score: 8.2
```

## 3. Common Issues & Solutions

### Issue 1: PDF Extraction Failing
**Symptom:** `[ERROR] Error reading file: ...`

**Solution:**
```bash
# Install PDF dependencies
pip install PyPDF2
pip install pdfplumber
```

### Issue 2: Google API Not Configured
**Symptom:** `content_to_json` returns None

**Solution:**
1. Check if Google API credentials are configured:
```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
```

2. If not set, configure them:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
```

### Issue 3: Missing Dependencies
**Symptom:** `ModuleNotFoundError`

**Solution:**
```bash
cd GenAI_Hackathon
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Test PDF Extraction Directly

Run the test script:
```bash
cd GenAI_Hackathon
source venv/bin/activate
python test_extraction.py
```

This will show you if PDF extraction is working.

## 5. Fallback to Dummy Data

The code now includes dummy data when extraction fails. You should see:
```
[WARNING] No data extracted from files, using dummy data
```

This ensures you get some results even if extraction fails.

## 6. Check File Upload

Verify files are being uploaded correctly:
```bash
# In the API logs, you should see:
[API] Analyzing 2 files: ['/tmp/filename1.pdf', '/tmp/filename2.pdf']
```

## 7. Manual Testing with cURL

Test with a simple text file first:
```bash
echo "Test startup content" > test.txt
curl -X POST "http://localhost:8000/analyze" \
     -F "files=@test.txt" \
     -F "startup_name=Test" \
     -F "sector=Technology"
```

## 8. Check Utils Module

Ensure the Utils module is working:
```python
# In Python shell
from Utils.ai_startup_utility import AIStartupUtility
from Utils.pdf_file_reader import content_to_json
```

## Expected Flow

1. **File Upload** → Files saved to temp directory
2. **Text Extraction** → PDF/DOCX/TXT content extracted
3. **Content Processing** → `content_to_json()` extracts parameters
4. **Scoring** → Parameters scored and weighted
5. **Analysis** → Red/green flags and recommendations generated

## Debug Output Explained

- `[API]` - API server messages
- `[DEBUG]` - Detailed processing steps
- `[WARNING]` - Non-critical issues
- `[ERROR]` - Critical failures

## Quick Fix Checklist

✅ Virtual environment activated  
✅ All dependencies installed  
✅ Google API credentials configured (if using)  
✅ PDF extraction libraries installed  
✅ Server running with debug logs visible  
✅ Test endpoint working (`/analyze-test`)  

## Still Not Working?

1. **Use the test endpoint** to verify the pipeline:
   ```
   http://localhost:8000/analyze-test
   ```

2. **Check the actual error** in server logs when uploading

3. **Try with different file types** (TXT first, then PDF)

4. **Verify file content** is being read:
   Look for: `[DEBUG] Extracted XXX characters from PDF`

5. **Check if content_to_json is working**:
   Look for: `[DEBUG] Extracted data: {...}`

The API now has comprehensive debugging that will help identify exactly where the process is failing.
