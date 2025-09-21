"""
Company Data Loader Utilities for AI Analyst Platform
GenAI Exchange Hackathon - AI Analyst for Startup Evaluation

This module handles loading and organizing startup company data from
the CompanyData folder for analysis by the AI-powered analyst platform.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# ============================================================================
# CONSTANTS
# ============================================================================
COMPANY_DATA_PATH = Path("/home/neosoft/test/GenAI_Hackathon/data/CompanyData")

# Company industry/sector mapping for benchmarking
COMPANY_SECTORS = {
    "Data stride": {"sector": "Analytics & Data Solutions", "stage": "Growth", "tags": ["B2B", "SaaS", "Analytics"]},
    "Naario": {"sector": "Women-focused Platform", "stage": "Early", "tags": ["B2C", "Social Impact", "Platform"]},
    "Inlustro": {"sector": "Design & Innovation", "stage": "Early", "tags": ["Creative", "Design", "Services"]},
    "Ctruh": {"sector": "XR Commerce Studio", "stage": "Seed", "tags": ["XR", "AR/VR", "E-commerce", "DeepTech"]},
    "Cashvisory": {"sector": "Financial Advisory", "stage": "Growth", "tags": ["FinTech", "B2B", "Advisory"]},
    "Dr.Doodley": {"sector": "Healthcare Solutions", "stage": "Early", "tags": ["HealthTech", "B2C", "Digital Health"]},
    "Kredily": {"sector": "HR & Payroll Platform", "stage": "Growth", "tags": ["HRTech", "SaaS", "B2B", "Payroll"]},
    "Indishreshtha": {"sector": "Excellence Platform", "stage": "Early", "tags": ["EdTech", "Platform", "B2C"]},
    "We360 AI": {"sector": "AI-Powered Solutions", "stage": "Growth", "tags": ["AI/ML", "B2B", "Enterprise", "Productivity"]},
    "Sensesemi": {"sector": "Semiconductor Tech", "stage": "Series A", "tags": ["Hardware", "DeepTech", "B2B", "Semiconductors"]},
    "Hexafun": {"sector": "Gaming & Entertainment", "stage": "Seed", "tags": ["Gaming", "Entertainment", "B2C", "Mobile"]},
    "Timbuckdo": {"sector": "Travel & Tourism", "stage": "Early", "tags": ["TravelTech", "B2C", "Marketplace"]},
    "Multipl": {"sector": "Multiple Ventures", "stage": "Growth", "tags": ["FinTech", "Investment", "B2C"]},
    "Ziniosa": {"sector": "Innovation Platform", "stage": "Early", "tags": ["Platform", "B2B", "Innovation"]}
}

# Document type classification patterns
DOCUMENT_PATTERNS = {
    'pitch_deck': ['pitch', 'deck', 'presentation'],
    'founders_checklist': ['checklist', 'founders', 'lv'],
    'investment_memo': ['investment', 'memorandum', 'memo'],
    'financials': ['financial', 'audited', 'accounts', 'finance'],
    'call_transcript': ['call', 'transcript', 'meeting'],
    'email': ['email', 'correspondence'],
}

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def get_available_companies() -> Dict[str, Path]:
    """
    Get list of available companies from the CompanyData folder
    
    Returns:
        dict: Dictionary with company names as keys and their folder paths as values
    """
    companies = {}
    
    if COMPANY_DATA_PATH.exists():
        for folder in sorted(COMPANY_DATA_PATH.iterdir()):
            if folder.is_dir():
                # Extract company name (remove number prefix)
                company_name = folder.name.split('. ', 1)[-1] if '. ' in folder.name else folder.name
                companies[company_name] = folder
    
    return companies


def classify_document(file_path: Path) -> str:
    """
    Classify a document based on its filename
    
    Args:
        file_path: Path to the document
    
    Returns:
        str: Document type classification
    """
    file_name_lower = file_path.name.lower()
    
    for doc_type, patterns in DOCUMENT_PATTERNS.items():
        if any(pattern in file_name_lower for pattern in patterns):
            return doc_type
    
    return 'other'


def get_company_files(company_folder: Path) -> Dict[str, Any]:
    """
    Get all files for a selected company with intelligent classification
    
    Args:
        company_folder: Path to the company folder
    
    Returns:
        dict: Dictionary with file types as keys and file paths as values
    """
    files = {
        'pitch_deck': None,
        'founders_checklist': None,
        'investment_memo': None,
        'financials': None,
        'call_transcript': None,
        'email': None,
        'other_docs': []
    }
    
    if company_folder.exists():
        for file_path in company_folder.iterdir():
            if file_path.is_file():
                doc_type = classify_document(file_path)
                
                # Special handling for PDF pitch decks
                if doc_type == 'pitch_deck' and file_path.suffix.lower() == '.pdf':
                    files['pitch_deck'] = file_path
                elif doc_type in files and files[doc_type] is None:
                    files[doc_type] = file_path
                elif doc_type == 'other':
                    files['other_docs'].append(file_path)
    
    return files


def load_company_documents(company_name: str) -> Tuple[Optional[bytes], List[Dict[str, Any]]]:
    """
    Load documents for a selected company for AI analysis
    
    Args:
        company_name: Name of the selected company
    
    Returns:
        tuple: (pitch_deck_bytes, other_files_list)
            - pitch_deck_bytes: Binary data of the pitch deck PDF
            - other_files_list: List of dictionaries with document metadata
    """
    companies = get_available_companies()
    
    if company_name not in companies:
        return None, []
    
    company_folder = companies[company_name]
    files = get_company_files(company_folder)
    
    loaded_files = []
    pitch_deck_data = None
    
    # Load pitch deck if available (required for analysis)
    if files['pitch_deck']:
        with open(files['pitch_deck'], 'rb') as f:
            pitch_deck_data = f.read()
    
    # Load other relevant documents for comprehensive analysis
    priority_docs = ['founders_checklist', 'investment_memo', 'financials', 'call_transcript', 'email']
    
    for doc_type in priority_docs:
        if files[doc_type]:
            with open(files[doc_type], 'rb') as f:
                loaded_files.append({
                    'name': files[doc_type].name,
                    'data': f.read(),
                    'type': doc_type,
                    'path': str(files[doc_type])
                })
    
    # Load any additional documents
    for doc in files['other_docs']:
        with open(doc, 'rb') as f:
            loaded_files.append({
                'name': doc.name,
                'data': f.read(),
                'type': 'other',
                'path': str(doc)
            })
    
    return pitch_deck_data, loaded_files


def get_company_metadata(company_name: str) -> Dict[str, Any]:
    """
    Get metadata and sector information for a company
    
    Args:
        company_name: Name of the company
    
    Returns:
        dict: Company metadata including sector, stage, and tags
    """
    return COMPANY_SECTORS.get(company_name, {
        "sector": "Unknown",
        "stage": "Unknown",
        "tags": []
    })


def get_benchmark_companies(company_name: str) -> List[str]:
    """
    Get list of companies suitable for benchmarking against the selected company
    
    Args:
        company_name: Name of the company to benchmark
    
    Returns:
        list: List of comparable company names
    """
    if company_name not in COMPANY_SECTORS:
        return []
    
    target_metadata = COMPANY_SECTORS[company_name]
    target_tags = set(target_metadata.get('tags', []))
    target_stage = target_metadata.get('stage', '')
    
    benchmark_companies = []
    
    for comp_name, comp_metadata in COMPANY_SECTORS.items():
        if comp_name == company_name:
            continue
        
        # Check for tag overlap
        comp_tags = set(comp_metadata.get('tags', []))
        tag_overlap = len(target_tags.intersection(comp_tags))
        
        # Check for stage similarity
        stage_similar = comp_metadata.get('stage', '') == target_stage
        
        # Include if significant overlap or same stage
        if tag_overlap >= 2 or (stage_similar and tag_overlap >= 1):
            benchmark_companies.append(comp_name)
    
    return benchmark_companies[:5]  # Return top 5 comparable companies


def get_sector_statistics() -> Dict[str, int]:
    """
    Get statistics about available companies by sector
    
    Returns:
        dict: Count of companies per sector/tag
    """
    stats = {}
    
    for company_data in COMPANY_SECTORS.values():
        # Count by sector
        sector = company_data.get('sector', 'Unknown')
        stats[sector] = stats.get(sector, 0) + 1
        
        # Count by tags
        for tag in company_data.get('tags', []):
            stats[f"Tag: {tag}"] = stats.get(f"Tag: {tag}", 0) + 1
    
    return stats


def generate_analysis_context(company_name: str) -> Dict[str, Any]:
    """
    Generate comprehensive context for AI analysis based on company selection
    
    Args:
        company_name: Name of the selected company
    
    Returns:
        dict: Analysis context including metadata, benchmarks, and flags
    """
    metadata = get_company_metadata(company_name)
    benchmark_companies = get_benchmark_companies(company_name)
    
    context = {
        'company_name': company_name,
        'metadata': metadata,
        'benchmark_companies': benchmark_companies,
        'analysis_focus': [],
        'risk_flags': []
    }
    
    # Set analysis focus based on sector/tags
    tags = metadata.get('tags', [])
    
    if 'FinTech' in tags:
        context['analysis_focus'].extend(['regulatory_compliance', 'financial_metrics', 'unit_economics'])
        context['risk_flags'].extend(['regulatory_changes', 'compliance_issues'])
    
    if 'HealthTech' in tags or 'Healthcare' in metadata.get('sector', ''):
        context['analysis_focus'].extend(['clinical_validation', 'regulatory_approval', 'patient_impact'])
        context['risk_flags'].extend(['FDA_approval', 'clinical_trials'])
    
    if 'DeepTech' in tags or 'Hardware' in tags:
        context['analysis_focus'].extend(['technology_readiness', 'IP_portfolio', 'manufacturing_scalability'])
        context['risk_flags'].extend(['technology_risk', 'supply_chain'])
    
    if 'B2B' in tags:
        context['analysis_focus'].extend(['enterprise_sales_cycle', 'customer_concentration', 'retention_metrics'])
    
    if 'B2C' in tags:
        context['analysis_focus'].extend(['user_acquisition_cost', 'lifetime_value', 'churn_rate'])
    
    return context


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_pitch_deck(file_path: Path) -> bool:
    """
    Validate if a file is a valid pitch deck
    
    Args:
        file_path: Path to the file
    
    Returns:
        bool: True if valid pitch deck, False otherwise
    """
    if not file_path.exists():
        return False
    
    # Check file extension
    if file_path.suffix.lower() not in ['.pdf', '.pptx', '.ppt']:
        return False
    
    # Check file size (should be between 100KB and 50MB)
    file_size = file_path.stat().st_size
    if file_size < 100 * 1024 or file_size > 50 * 1024 * 1024:
        return False
    
    return True


def get_document_summary(company_name: str) -> Dict[str, Any]:
    """
    Get a summary of available documents for a company
    
    Args:
        company_name: Name of the company
    
    Returns:
        dict: Summary of available documents with counts and types
    """
    companies = get_available_companies()
    
    if company_name not in companies:
        return {'error': 'Company not found'}
    
    files = get_company_files(companies[company_name])
    
    summary = {
        'total_documents': 0,
        'document_types': [],
        'has_required_docs': False,
        'missing_docs': []
    }
    
    # Count documents
    for doc_type, file_path in files.items():
        if doc_type != 'other_docs':
            if file_path:
                summary['total_documents'] += 1
                summary['document_types'].append(doc_type)
            else:
                if doc_type in ['pitch_deck', 'founders_checklist']:
                    summary['missing_docs'].append(doc_type)
        else:
            summary['total_documents'] += len(file_path)
            if file_path:
                summary['document_types'].append(f"{len(file_path)} additional docs")
    
    # Check for required documents
    summary['has_required_docs'] = files['pitch_deck'] is not None
    
    return summary
