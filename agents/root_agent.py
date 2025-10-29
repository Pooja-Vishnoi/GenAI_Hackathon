"""
Root Agent: StartupAnalyzerAgent
Orchestrates the startup analysis workflow using two sub-agents
"""

import json
from typing import Dict, Any, List, ClassVar
import streamlit as st
from google.adk.agents import Agent
from adk.tools import tool
from .data_processing_agent import DataProcessingAgent
from .calculation_agent import CalculationAgent


class StartupAnalyzerAgent(Agent):
    """
    Root agent that orchestrates startup analysis workflow
    Manages session state and coordinates between DataProcessingAgent and CalculationAgent
    """
    
    # ClassVar to avoid Pydantic validation issues
    session_key: ClassVar[str] = "startup_analyzer_session"
    
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        super().__init__(
            name="StartupAnalyzerAgent",
            description="Root agent for orchestrating startup analysis.",
            model=config['gemini_model'],
            tools=[
                self.process_startup_documents,
                self.calculate_scores,
                self.recalculate_scores,
                self.generate_insights,
                self.reset_analysis,
                self.get_analysis_status
            ]
        )

        # After super().__init__(), set attributes using __dict__ to bypass Pydantic
        self.__dict__['_data_agent'] = DataProcessingAgent()
        self.__dict__['_calculation_agent'] = CalculationAgent()
    
    @property
    def data_agent(self):
        """Property to access data_agent, bypassing Pydantic validation"""
        return self.__dict__['_data_agent']
    
    @property
    def calculation_agent(self):
        """Property to access calculation_agent, bypassing Pydantic validation"""
        return self.__dict__['_calculation_agent']
        
    def get_session_data(self) -> Dict[str, Any]:
        """Get session data from Streamlit session state"""
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                'analysis_complete': False,
                'all_content': None,
                'company_json': None,
                'evaluation_data': None,
                'final_scores': None,
                'results_df': None,
                'original_final_scores': None
            }
        return st.session_state[self.session_key]
    
    def update_session_data(self, key: str, value: Any):
        """Update specific key in session data"""
        session_data = self.get_session_data()
        session_data[key] = value
        st.session_state[self.session_key] = session_data
    
    @tool("Process uploaded documents using DataProcessingAgent")
    async def process_startup_documents(self, pitch_deck, additional_files=None) -> Dict[str, Any]:
        """
        Process uploaded documents using DataProcessingAgent
        Returns: Dictionary with analysis results
        """
        try:
            # Use DataProcessingAgent to process files
            result = await self.data_agent.process_documents(pitch_deck, additional_files)
            
            # Check if result contains an error
            if 'error' in result:
                return result
            
            # Store results in session
            self.update_session_data('all_content', result['all_content'])
            self.update_session_data('company_json', result['company_json'])
            self.update_session_data('evaluation_data', result['evaluation_data'])
            self.update_session_data('analysis_complete', True)
            
            return result
            
        except Exception as e:
            return {'error': f"Document processing failed: {str(e)}"}
    
    @tool("Calculate final scores using CalculationAgent")
    async def calculate_scores(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate final scores using CalculationAgent
        Returns: Dictionary with calculated scores
        """
        try:
            # Use CalculationAgent for score calculation
            result = await self.calculation_agent.calculate_final_scores(evaluation_data)
            
            # Store results in session
            self.update_session_data('final_scores', result['final_scores'])
            if 'results_df' not in self.get_session_data():
                self.update_session_data('results_df', result['final_scores_df'])
                self.update_session_data('original_final_scores', result['final_scores_df'])
            
            return result
            
        except Exception as e:
            return {'error': f"Score calculation failed: {str(e)}"}
    
    @tool("Recalculate scores after table edits using CalculationAgent")
    async def recalculate_scores(self, edited_data: Any) -> Dict[str, Any]:
        """
        Recalculate scores after table edits using CalculationAgent
        This only calls CalculationAgent, not DataProcessingAgent
        """
        try:
            # Use CalculationAgent for recalculation (lightweight operation)
            result = await self.calculation_agent.recalculate_weighted_scores(edited_data)
            
            # Update session with new calculated scores
            self.update_session_data('results_df', result['updated_df'])
            
            return result
            
        except Exception as e:
            return {'error': f"Score recalculation failed: {str(e)}"}
    
    @tool("Generate insights using DataProcessingAgent")
    async def generate_insights(self, uploaded_content: str, company_json: Dict, 
                              evaluation_data: Dict, final_scores: Any, 
                              benchmark_score: float) -> Dict[str, Any]:
        """
        Generate insights using DataProcessingAgent
        """
        try:
            result = await self.data_agent.generate_insights(
                uploaded_content, company_json, evaluation_data, 
                final_scores, benchmark_score
            )
            return result
            
        except Exception as e:
            return {'error': f"Insight generation failed: {str(e)}"}
    
    @tool("Clear all analysis data for fresh start")
    def reset_analysis(self):
        """Clear all analysis data for fresh start"""
        keys_to_clear = [
            'analysis_complete', 'all_content', 'company_json', 
            'evaluation_data', 'final_scores', 'results_df', 'original_final_scores'
        ]
        session_data = self.get_session_data()
        for key in keys_to_clear:
            session_data[key] = None
        session_data['analysis_complete'] = False
        st.session_state[self.session_key] = session_data
    
    @tool("Get current analysis status and data")
    def get_analysis_status(self) -> Dict[str, Any]:
        """Get current analysis status and data"""
        session_data = self.get_session_data()
        return {
            'analysis_complete': session_data.get('analysis_complete', False),
            'has_company_data': session_data.get('company_json') is not None,
            'has_evaluation_data': session_data.get('evaluation_data') is not None,
            'has_final_scores': session_data.get('final_scores') is not None,
            'session_data': session_data
        }
    
    @tool("Get comprehensive agent information for ADK framework")
    def get_agent_info(self) -> Dict[str, Any]:
        """Get comprehensive agent information for ADK framework"""
        return {
            'name': self.name,
            'description': self.description,
            'role': self.role,
            'instructions': self.instructions,
            'tools': {
                name: {
                    'description': tool['description'],
                    'parameters': tool['parameters'],
                    'returns': tool['returns'],
                    'delegates_to': tool.get('delegates_to', 'self')
                }
                for name, tool in self.tools.items()
            },
            'subagents': {
                name: {
                    'name': info['agent'].name,
                    'description': info['description'],
                    'role': info['role'],
                    'tools': info['tools']
                }
                for name, info in self.subagents.items()
            },
            'session_management': {
                'session_key': self.session_key,
                'managed_data': [
                    'analysis_complete', 'all_content', 'company_json',
                    'evaluation_data', 'final_scores', 'results_df', 'original_final_scores'
                ]
            }
        }
    
    @tool("Get detailed workflow status across all agents")
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get detailed workflow status across all agents"""
        session_data = self.get_session_data()
        return {
            'root_agent': {
                'status': 'active',
                'session_initialized': self.session_key in st.session_state,
                'available_tools': list(self.tools.keys()),
                'tools_used': self._get_tools_used_status(session_data)
            },
            'data_processing_agent': {
                'status': 'completed' if session_data.get('company_json') else 'pending',
                'tools_used': [
                    'extract_file_content', 'analyze_company_details', 'evaluate_startup'
                ] if session_data.get('evaluation_data') else [],
                'available_tools': list(self.data_agent.tools.keys())
            },
            'calculation_agent': {
                'status': 'completed' if session_data.get('final_scores') else 'pending',
                'tools_used': [
                    'calculate_final_scores'
                ] if session_data.get('results_df') is not None else [],
                'available_tools': list(self.calculation_agent.tools.keys())
            },
            'overall_progress': {
                'analysis_complete': session_data.get('analysis_complete', False),
                'ready_for_insights': all([
                    session_data.get('company_json'),
                    session_data.get('evaluation_data'),
                    session_data.get('final_scores')
                ]),
                'workflow_stage': self._get_current_workflow_stage(session_data)
            }
        }
    
    def _get_tools_used_status(self, session_data: Dict) -> List[str]:
        """Helper method to determine which root agent tools have been used"""
        tools_used = []
        if session_data.get('analysis_complete'):
            tools_used.append('process_startup_documents')
        if session_data.get('final_scores'):
            tools_used.append('calculate_scores')
        # Note: recalculate_scores and generate_insights are called on-demand
        return tools_used
    
    def _get_current_workflow_stage(self, session_data: Dict) -> str:
        """Helper method to determine current workflow stage"""
        if not session_data.get('all_content'):
            return 'awaiting_upload'
        elif not session_data.get('company_json'):
            return 'processing_documents'
        elif not session_data.get('evaluation_data'):
            return 'analyzing_company'
        elif not session_data.get('final_scores'):
            return 'calculating_scores'
        else:
            return 'analysis_complete'
    
    @tool("Get comprehensive tool registry across all agents in the framework")
    def get_all_tools(self) -> Dict[str, Any]:
        """Get comprehensive tool registry across all agents in the framework"""
        return {
            'root_agent_tools': self.tools,
            'subagent_tools': {
                agent_name: {
                    'agent_info': {
                        'name': info['agent'].name,
                        'role': info['role'],
                        'description': info['description']
                    },
                    'tools': info['tools']
                }
                for agent_name, info in self.subagents.items()
            },
            'total_tools': len(self.tools) + sum(len(info['tools']) for info in self.subagents.values()),
            'tool_categories': {
                'orchestration': list(self.tools.keys()),
                'data_processing': list(self.data_agent.tools.keys()),
                'calculation': list(self.calculation_agent.tools.keys())
            }
        }