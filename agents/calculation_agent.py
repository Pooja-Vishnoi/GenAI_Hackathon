"""
CalculationAgent: Handles scoring calculations and recalculations
Sub-agent responsible for final score calculations and weighted score updates
"""
import json
import pandas as pd
from typing import Dict, Any
import sys
from google.adk.agents import Agent
from adk.tools import tool
sys.path.append('..')
from Utils.ai_startup_utility_improved import AIStartupUtility


class CalculationAgent(Agent):
    """
    Agent responsible for scoring calculations and recalculations
    Handles: Final score calculation, weighted score updates, table edit processing
    """
    
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        super().__init__(
            name="CalculationAgent",
            description="Sub-agent for scoring, weighted computations, and recalculations.",
            model=config['gemini_model'],
            tools=[
                self.calculate_final_scores,
                self.recalculate_weighted_scores,
                self.validate_weightage_sum,
                self.prepare_chart_data,
                self.process_table_edit
            ]
        )

        # After super().__init__(), set utility using __dict__ to bypass Pydantic
        self.__dict__['utility'] = AIStartupUtility(model_name=config['gemini_model'], weightages=config.get('scoring_weightages', {}))
    
    @tool("Calculate final weighted scores from evaluation data")
    async def calculate_final_scores(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate final weighted scores from evaluation data
        
        Args:
            evaluation_data: Results from startup evaluation
            
        Returns:
            Dictionary with final scores and DataFrame
        """
        try:
            if not evaluation_data or "error" in evaluation_data:
                raise ValueError("Invalid evaluation data provided")
            
            # Use utility function to calculate final scores
            final_scores = self.utility.calculate_final_score_updated(evaluation_data)
            
            # Convert to DataFrame for UI
            final_scores_df = pd.DataFrame(final_scores)
            
            return {
                'final_scores': final_scores,
                'final_scores_df': final_scores_df,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    @tool("Recalculate scores after user table edits (real-time)")
    async def recalculate_weighted_scores(self, edited_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Recalculate weighted scores after table edits
        This is the lightweight operation called when user edits the table
        
        Args:
            edited_df: DataFrame with user edits (Threshold/Weightage changes)
            
        Returns:
            Dictionary with updated DataFrame and calculations
        """
        try:
            # Create a copy for calculations
            updated_df = edited_df.copy()
            
            # Recalculate weighted scores if weightage was changed
            if 'Weightage' in updated_df.columns and 'Score' in updated_df.columns:
                updated_df['Weighted_Score'] = updated_df['Score'] * updated_df['Weightage']
            
            # Recalculate benchmark weighted scores
            if 'Weightage' in updated_df.columns and 'benchmark_score' in updated_df.columns:
                updated_df['benchmark_weighted_score'] = (
                    updated_df['benchmark_score'] * updated_df['Weightage']
                )
            
            # Calculate totals
            total_score = updated_df['Weighted_Score'].sum() if 'Weighted_Score' in updated_df.columns else 0
            total_benchmark = updated_df['benchmark_weighted_score'].sum() if 'benchmark_weighted_score' in updated_df.columns else 0
            
            return {
                'updated_df': updated_df,
                'total_score': total_score,
                'total_benchmark': total_benchmark,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    @tool("Validate that weightage values sum to approximately 1.0")
    async def validate_weightage_sum(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate that weightage values sum to approximately 1.0
        
        Args:
            df: DataFrame with Weightage column
            
        Returns:
            Validation result with sum and status
        """
        try:
            if 'Weightage' not in df.columns:
                return {
                    'valid': True,
                    'message': 'No weightage column found',
                    'sum': 0
                }
            
            weightage_sum = df['Weightage'].sum()
            is_valid = abs(weightage_sum - 1.0) <= 0.01
            
            return {
                'valid': is_valid,
                'sum': weightage_sum,
                'message': f"Weightage sum: {weightage_sum:.3f}" + 
                          (" ✅ Good!" if is_valid else " ⚠️ Should sum to 1.0"),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    @tool("Prepare data for charts and visualizations")
    async def prepare_chart_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Prepare data for charts and visualizations
        
        Args:
            df: DataFrame with calculated scores
            
        Returns:
            Dictionary with chart-ready data
        """
        try:
            chart_data = {
                'parameters': df.get('Parameter', []).tolist() if 'Parameter' in df.columns else [],
                'weighted_scores': df.get('Weighted_Score', []).tolist() if 'Weighted_Score' in df.columns else [],
                'benchmark_scores': df.get('benchmark_weighted_score', []).tolist() if 'benchmark_weighted_score' in df.columns else [],
                'total_weighted_score': df['Weighted_Score'].sum() if 'Weighted_Score' in df.columns else 0,
                'total_benchmark_score': df['benchmark_weighted_score'].sum() if 'benchmark_weighted_score' in df.columns else 0
            }
            
            return {
                'chart_data': chart_data,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    @tool("Main workflow for processing table edits")
    async def process_table_edit(self, original_df: pd.DataFrame, 
                               edited_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Main workflow for processing table edits
        Called when user modifies Threshold or Weightage values
        
        Args:
            original_df: Original DataFrame before edits
            edited_df: DataFrame with user modifications
            
        Returns:
            Complete results with recalculated scores and validation
        """
        try:
            # Step 1: Recalculate weighted scores
            recalc_result = await self.recalculate_weighted_scores(edited_df)
            if recalc_result['status'] == 'failed':
                return recalc_result
            
            updated_df = recalc_result['updated_df']
            
            # Step 2: Validate weightage sum
            validation_result = await self.validate_weightage_sum(updated_df)
            
            # Step 3: Prepare chart data
            chart_result = await self.prepare_chart_data(updated_df)
            
            return {
                'updated_df': updated_df,
                'total_score': recalc_result['total_score'],
                'total_benchmark': recalc_result['total_benchmark'],
                'validation': validation_result,
                'chart_data': chart_result.get('chart_data', {}),
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }