"""
DataProcessingAgent: Handles file processing and initial analysis
Sub-agent responsible for document extraction, company analysis, and evaluation
"""

import os
import json
from typing import Dict, Any, List
import sys
from google.adk.agents import Agent
from adk.tools import tool
sys.path.append('..')
from Utils.ai_startup_utility_improved import AIStartupUtility


class DataProcessingAgent(Agent):
    """
    Agent responsible for processing input files and performing initial analysis
    Handles: File extraction, company details, startup evaluation, insights
    """
    
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        super().__init__(
            name="DataProcessingAgent",
            description="Sub-agent for document processing, company analysis, and insight generation.",
            model=config['gemini_model'],
            tools=[
                self.extract_file_content,
                self.analyze_company_details,
                self.evaluate_startup,
                self.generate_insights,
                self.process_documents,
                self.enrich_with_public_data
            ]
        )

        # After super().__init__(), set utility using __dict__ to bypass Pydantic
        self.__dict__['utility'] = AIStartupUtility(model_name=config['gemini_model'], weightages=config.get('scoring_weightages', {}))
    
    @tool("Extract text content from uploaded files (PDF, DOCX, TXT)")
    async def extract_file_content(self, file_path: str, file_type: str) -> str:
        """
        Extract content from uploaded file based on file type
        
        Args:
            file_path: Path to the uploaded file
            file_type: Type of file (pdf, docx, txt)
            
        Returns:
            Extracted text content
        """
        try:
            if file_type == "application/pdf":
                return self.utility.extract_text_from_pdf(file_path)
            elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                              "application/msword"]:
                return self.utility.extract_text_from_docx(file_path)
            elif file_type == "text/plain":
                return self.utility.extract_text_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            raise Exception(f"File extraction failed: {str(e)}")
    
    @tool("Use AI to extract company information from document content")
    async def analyze_company_details(self, document_content: str) -> Dict[str, Any]:
        """
        Extract company details from document content using Gemini
        
        Args:
            document_content: Combined content from all uploaded files
            
        Returns:
            Dictionary with extracted company details
        """
        try:
            return await self.utility.get_company_json_from_gemini(document_content)
        except Exception as e:
            raise Exception(f"Company analysis failed: {str(e)}")

    @tool("Score startup on 10 key parameters (1-10 scale)")
    async def evaluate_startup(self, company_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform startup evaluation based on company details
        
        Args:
            company_json: Company details extracted from documents
            
        Returns:
            Dictionary with evaluation scores and metrics
        """
        try:
            return await self.utility.startup_evaluation(company_json)
        except Exception as e:
            raise Exception(f"Startup evaluation failed: {str(e)}")

    @tool("Generate AI-powered insights, red flags, green flags, recommendations")
    async def generate_insights(self, uploaded_content: str, company_json: Dict[str, Any],
                              evaluation_data: Dict[str, Any], final_scores: Any,
                              benchmark_score: float) -> Dict[str, Any]:
        """
        Generate insights and recommendations
        
        Args:
            uploaded_content: Original document content
            company_json: Company details
            evaluation_data: Evaluation results
            final_scores: Final calculated scores
            benchmark_score: Benchmark score for comparison
            
        Returns:
            Dictionary with insights, red flags, green flags, and recommendations
        """
        try:
            return await self.utility.derive_insight(
                uploaded_content, company_json, evaluation_data, 
                final_scores, benchmark_score
            )
        except Exception as e:
            raise Exception(f"Insight generation failed: {str(e)}")

    @tool("Complete document processing workflow orchestration")
    async def process_documents(self, pitch_deck, additional_files=None) -> Dict[str, Any]:
        """
        Main workflow: Process all uploaded documents and perform initial analysis
        
        Args:
            pitch_deck: Main pitch deck file
            additional_files: Optional additional documents
            
        Returns:
            Complete analysis results including company details and evaluation
        """
        try:
            # Step 1: Save and process pitch deck
            temp_pitch_path = "temp_pitch.pdf"
            with open(temp_pitch_path, "wb") as f:
                f.write(pitch_deck.getbuffer())
            
            # Extract content from pitch deck
            pitch_content = await self.extract_file_content(temp_pitch_path, "application/pdf")
            all_content = {pitch_deck.name: pitch_content}
            
            # Step 2: Process additional files if provided
            if additional_files:
                for add_file in additional_files:
                    temp_add_path = f"temp_{add_file.name}"
                    with open(temp_add_path, "wb") as f:
                        f.write(add_file.getbuffer())
                    
                    try:
                        file_content = await self.extract_file_content(temp_add_path, add_file.type)
                        all_content[add_file.name] = file_content
                    except ValueError as e:
                        # Skip unsupported file types
                        continue
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_add_path):
                            os.remove(temp_add_path)
            
            # Step 3: Analyze company details
            combined_content = str(all_content)
            company_json = await self.analyze_company_details(combined_content)

            # Step 3.5: Enrich company data with public sources
            enriched_data = {}
            if "error" not in company_json and "company_name" in company_json and "sector" in company_json:
                startup_name = company_json.get("company_name", "Unknown")
                sector = company_json.get("sector", "Unknown")
                if startup_name != "Unknown" and sector != "Unknown":
                    enriched_data = await self.enrich_with_public_data(startup_name, sector)
            
            # Step 4: Evaluate startup
            evaluation_data = {}
            if "error" not in company_json:
                evaluation_data = await self.evaluate_startup(company_json)
            
            # Clean up pitch deck file
            if os.path.exists(temp_pitch_path):
                os.remove(temp_pitch_path)
            
            return {
                'all_content': all_content,
                'company_json': company_json,
                'enriched_data': enriched_data,
                'evaluation_data': evaluation_data,
                'status': 'success'
            }
            
        except Exception as e:
            # Clean up files on error
            for temp_file in ["temp_pitch.pdf"] + [f"temp_{f.name}" for f in (additional_files or [])]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            # Include more detailed error information
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in process_documents: {error_details}")
            
            return {
                'error': str(e),
                'error_details': error_details,
                'status': 'failed'
            }
    
    @tool("Enrich company data with public information")
    async def enrich_with_public_data(self, startup_name: str, sector: str) -> dict:
        """
        Enriches company data by fetching information from public sources.

        Args:
            startup_name: The name of the startup.
            sector: The sector of the startup.
        
        Returns:
            A dictionary containing the enriched data.
        """
        print(f"Enriching data for {startup_name} in sector {sector}...")
        enriched_data = await self.utility.enrich_company_data(startup_name, sector)
        return enriched_data