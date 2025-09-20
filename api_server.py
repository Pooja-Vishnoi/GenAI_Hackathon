"""
FastAPI server for Startup Analysis Pipeline
Exposes the analysis functions as REST API endpoints
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import pandas as pd
import json
import os
import tempfile
from datetime import datetime
import traceback

# Import analysis functions from analyse_pipeline
from analyse_pipeline import (
    create_results,
    create_results_from_paths,  # New function for file paths
    recalculate_results,
    calculate_score,
    detect_red_flags,
    detect_green_flags,
    generate_recommendations,
    analyze_results
)

# Import utility functions for file reading
from Utils.ai_startup_utility import AIStartupUtility
from docx import Document

# Initialize FastAPI app
app = FastAPI(
    title="Startup Analysis API",
    description="API for analyzing startup pitch decks and business documents",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store analysis results in memory (use Redis/Database in production)
analysis_cache = {}

# Helper function to convert DataFrame to JSON-serializable format
def df_to_dict(df):
    """Convert pandas DataFrame to dictionary with proper JSON serialization"""
    if df.empty:
        return []
    return json.loads(df.to_json(orient='records'))

# Helper function to read files from disk paths
def read_files_from_paths(file_paths):
    """
    Read files from disk paths and return content dict
    Similar to Utils.utils.read_files but for file paths instead of UploadedFile objects
    """
    results = {}
    analyst = AIStartupUtility()
    
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()
        text = ""
        
        try:
            if ext == ".pdf":
                # Use AIStartupUtility to extract text from PDF
                text = analyst.extract_text_from_pdf(file_path)
                
            elif ext == ".docx":
                # Read DOCX file
                doc = Document(file_path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
                
            elif ext == ".txt":
                # Read plain text file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    
            elif ext in [".csv", ".xls", ".xlsx"]:
                # For spreadsheets, read as dataframe and convert to text
                import pandas as pd
                if ext == ".csv":
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                text = df.to_string()
                
            else:
                text = f"[Unsupported file type: {ext}]"
                
            results[filename] = text
            
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            results[filename] = f"[Error reading file: {e}]"
    
    return results

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "message": "Startup Analysis API is running",
        "version": "1.0.0",
        "endpoints": [
            "/analyze",
            "/analyze/{session_id}",
            "/analyze-test",
            "/recalculate",
            "/score/{session_id}",
            "/red-flags/{session_id}",
            "/green-flags/{session_id}",
            "/recommendations/{session_id}"
        ]
    }

@app.get("/analyze-test")
async def analyze_test():
    """Test endpoint with dummy data to verify the analysis pipeline"""
    try:
        # Create dummy data directly
        dummy_data = {
            "Startup": "Test Startup",
            "Sector": "Technology",
            "Team Quality": "Strong founding team",
            "Market Size": "$300B TAM", 
            "Traction": "42 customers",
            "Financials": "₹14L monthly burn",
            "Risk Factors": "High competition"
        }
        
        # Process dummy data
        import pandas as pd
        from analyse_pipeline import convert_raw_to_structured, detect_red_flags, detect_green_flags
        
        # Create DataFrame
        df = pd.DataFrame(list(dummy_data.items()), columns=["Parameters", "Details"])
        df = df[~df["Parameters"].isin(["Startup", "Sector"])].reset_index(drop=True)
        
        # Generate structured data
        structured_df = convert_raw_to_structured(df)
        structured_df["Weighted_Score"] = structured_df["Score"] * structured_df["Weightage"]
        final_score = structured_df["Weighted_Score"].sum()
        
        # Generate flags
        red_flags = detect_red_flags(structured_df)
        green_flags = detect_green_flags(structured_df)
        
        return {
            "status": "success",
            "message": "Test analysis completed",
            "data": {
                "raw_data": df_to_dict(df),
                "structured_data": df_to_dict(structured_df),
                "final_score": float(final_score),
                "red_flags": red_flags,
                "green_flags": green_flags
            }
        }
        
    except Exception as e:
        import traceback
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc()
            },
            status_code=500
        )

@app.post("/analyze")
async def analyze_documents(
    files: List[UploadFile] = File(None),
    startup_name: Optional[str] = Form(None),
    sector: Optional[str] = Form(None)
):
    """
    Main endpoint to analyze uploaded documents
    Returns complete analysis including scores, flags, and recommendations
    """
    try:
        # Generate session ID for this analysis
        session_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save uploaded files temporarily
        temp_files = []
        if files and files[0].filename:  # Check if files are actually uploaded
            for file in files:
                temp_path = os.path.join(tempfile.gettempdir(), file.filename)
                content = await file.read()
                with open(temp_path, 'wb') as f:
                    f.write(content)
                temp_files.append(temp_path)
            
            # Run analysis using the new function that handles file paths
            print(f"[API] Analyzing {len(temp_files)} files: {temp_files}")
            df, structured_df, final_score, flags, recommendations = create_results_from_paths(temp_files)
            print(f"[API] Analysis complete - Score: {final_score}, DF rows: {len(df)}, Structured DF rows: {len(structured_df)}")
            
            # Clean up temp files
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                    print(f"[API] Cleaned up temp file: {temp_file}")
                except Exception as e:
                    print(f"[API] Failed to clean up {temp_file}: {e}")
        else:
            # No files uploaded, return dummy data or error
            df, structured_df, final_score, flags, recommendations = create_results(None)
        
        # Convert DataFrames to dict for JSON serialization
        result = {
            "session_id": session_id,
            "status": "success",
            "startup_name": startup_name or "Unknown Startup",
            "sector": sector or "Technology",
            "analysis": {
                "raw_data": df_to_dict(df),
                "structured_data": df_to_dict(structured_df),
                "final_score": float(final_score) if final_score else 0.0,
                "red_flags": flags if isinstance(flags, (list, dict)) else [],
                "green_flags": detect_green_flags(structured_df) if not structured_df.empty else [],
                "recommendations": recommendations if recommendations else {}
            },
            "metadata": {
                "analyzed_at": datetime.now().isoformat(),
                "files_processed": len(temp_files) if files else 0
            }
        }
        
        # Cache the results
        analysis_cache[session_id] = result
        
        return JSONResponse(content=result, status_code=200)
        
    except Exception as e:
        print(f"Error in analyze_documents: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e),
                "details": traceback.format_exc()
            },
            status_code=500
        )

@app.get("/analyze/{session_id}")
async def get_analysis(session_id: str):
    """
    Retrieve previously analyzed results by session ID
    """
    if session_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    return JSONResponse(content=analysis_cache[session_id], status_code=200)

@app.post("/recalculate")
async def recalculate_analysis(
    session_id: str = Form(...),
    updated_data: str = Form(...)  # JSON string of updated DataFrame
):
    """
    Recalculate analysis with updated data
    """
    try:
        if session_id not in analysis_cache:
            raise HTTPException(status_code=404, detail="Analysis session not found")
        
        # Parse updated data
        updated_df_dict = json.loads(updated_data)
        updated_df = pd.DataFrame(updated_df_dict)
        
        # Recalculate
        recalculated_df = recalculate_results(updated_df)
        
        # Update cache
        analysis_cache[session_id]["analysis"]["structured_data"] = df_to_dict(recalculated_df)
        
        # Recalculate dependent values
        final_score, red_flags, recommendations = analyze_results(recalculated_df)
        
        analysis_cache[session_id]["analysis"]["final_score"] = float(final_score)
        analysis_cache[session_id]["analysis"]["red_flags"] = red_flags
        analysis_cache[session_id]["analysis"]["recommendations"] = recommendations
        
        return JSONResponse(
            content={
                "status": "success",
                "session_id": session_id,
                "updated_data": df_to_dict(recalculated_df),
                "final_score": float(final_score),
                "red_flags": red_flags,
                "recommendations": recommendations
            },
            status_code=200
        )
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )

@app.get("/score/{session_id}")
async def get_score(session_id: str):
    """
    Get the investment score for a specific analysis session
    """
    if session_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    score = analysis_cache[session_id]["analysis"]["final_score"]
    
    # Determine investment recommendation based on score
    if score >= 8:
        recommendation = "STRONG BUY"
        confidence = "High"
    elif score >= 6:
        recommendation = "BUY"
        confidence = "Medium"
    elif score >= 4:
        recommendation = "HOLD"
        confidence = "Low"
    else:
        recommendation = "PASS"
        confidence = "Very Low"
    
    return {
        "session_id": session_id,
        "final_score": score,
        "recommendation": recommendation,
        "confidence": confidence,
        "score_breakdown": {
            "max_score": 10,
            "min_score": 0,
            "benchmark": 7.0,
            "percentile": (score / 10) * 100
        }
    }

@app.get("/red-flags/{session_id}")
async def get_red_flags(session_id: str):
    """
    Get red flags for a specific analysis session
    """
    if session_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    red_flags = analysis_cache[session_id]["analysis"]["red_flags"]
    
    # Format red flags for frontend consumption
    formatted_flags = []
    if isinstance(red_flags, list) and len(red_flags) > 0:
        # Handle the format from detect_red_flags function
        if len(red_flags) == 2 and isinstance(red_flags[0], list):
            # Format: [[flag_texts], [references]]
            for i, flag_text in enumerate(red_flags[0]):
                formatted_flags.append({
                    "text": flag_text,
                    "severity": "high" if "High" in flag_text else "medium",
                    "reference": red_flags[1][i] if i < len(red_flags[1]) else "",
                    "category": "risk"
                })
    
    return {
        "session_id": session_id,
        "red_flags": formatted_flags,
        "total_count": len(formatted_flags),
        "high_priority_count": sum(1 for f in formatted_flags if f.get("severity") == "high")
    }

@app.get("/green-flags/{session_id}")
async def get_green_flags(session_id: str):
    """
    Get positive indicators for a specific analysis session
    """
    if session_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    green_flags = analysis_cache[session_id]["analysis"]["green_flags"]
    
    # Format green flags for frontend
    formatted_flags = []
    for flag in green_flags:
        formatted_flags.append({
            "text": flag,
            "category": "strength",
            "impact": "positive"
        })
    
    return {
        "session_id": session_id,
        "green_flags": formatted_flags,
        "total_count": len(formatted_flags)
    }

@app.post("/recommendations/{session_id}")
async def get_recommendations(
    session_id: str,
    focus_area: Optional[str] = Form(None)
):
    """
    Get AI-generated recommendations for the startup
    """
    if session_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    recommendations = analysis_cache[session_id]["analysis"]["recommendations"]
    
    # Structure recommendations by category
    structured_recommendations = {
        "investment_decision": recommendations.get("decision", "Conditional Invest"),
        "key_recommendations": [],
        "action_items": [],
        "focus_areas": []
    }
    
    # Parse recommendations if they're in string format
    if isinstance(recommendations, dict):
        for key, value in recommendations.items():
            if "recommendation" in key.lower():
                structured_recommendations["key_recommendations"].append(value)
            elif "action" in key.lower():
                structured_recommendations["action_items"].append(value)
            elif "focus" in key.lower():
                structured_recommendations["focus_areas"].append(value)
    
    # Add default recommendations if empty
    if not structured_recommendations["key_recommendations"]:
        structured_recommendations["key_recommendations"] = [
            "Focus on revenue growth and customer acquisition",
            "Strengthen competitive positioning",
            "Optimize burn rate and extend runway"
        ]
    
    return {
        "session_id": session_id,
        "recommendations": structured_recommendations,
        "focus_area": focus_area,
        "generated_at": datetime.now().isoformat()
    }

@app.post("/export/{session_id}")
async def export_analysis(
    session_id: str,
    format: str = Form("json")  # json, csv, or pdf
):
    """
    Export analysis results in different formats
    """
    if session_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    analysis = analysis_cache[session_id]
    
    if format == "json":
        return JSONResponse(content=analysis, status_code=200)
    
    elif format == "csv":
        # Convert to CSV (simplified version)
        df = pd.DataFrame(analysis["analysis"]["structured_data"])
        csv_content = df.to_csv(index=False)
        return JSONResponse(
            content={
                "format": "csv",
                "content": csv_content,
                "filename": f"{session_id}.csv"
            },
            status_code=200
        )
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported export format")

@app.delete("/analyze/{session_id}")
async def delete_analysis(session_id: str):
    """
    Delete a specific analysis session from cache
    """
    if session_id not in analysis_cache:
        raise HTTPException(status_code=404, detail="Analysis session not found")
    
    del analysis_cache[session_id]
    
    return {
        "status": "success",
        "message": f"Analysis session {session_id} deleted successfully"
    }

# WebSocket endpoint for real-time updates (optional)
from fastapi import WebSocket

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket for real-time analysis updates
    """
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Send analysis updates
            if session_id in analysis_cache:
                await websocket.send_json(analysis_cache[session_id])
            else:
                await websocket.send_json({"error": "Session not found"})
                
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)