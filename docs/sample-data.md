# 📊 Sample Data Documentation

## 📋 Overview
This document describes the sample data formats, structures, and examples used in the GenAI Hackathon startup analysis platform.

## 📤 Input Document Formats

### 📄 Pitch Deck Structure (PDF)
Expected content sections:
```json
{
  "company_overview": {
    "name": "Company Name",
    "founded": "Year",
    "sector": "Industry vertical",
    "location": "Headquarters"
  },
  "team": {
    "founders": "Number and backgrounds",
    "key_members": "Experience and education",
    "advisors": "Industry experts"
  },
  "market": {
    "tam": "Total addressable market size",
    "sam": "Serviceable addressable market",
    "som": "Serviceable obtainable market"
  },
  "product": {
    "description": "Product/service overview",
    "unique_value": "Differentiation factors",
    "technology": "Tech stack and innovation"
  },
  "traction": {
    "users": "User count and growth rate",
    "revenue": "Current revenue metrics",
    "partnerships": "Key partnerships"
  },
  "financials": {
    "revenue_model": "How money is made",
    "unit_economics": "Per unit profitability",
    "funding_history": "Previous rounds"
  },
  "competition": {
    "competitors": "Main competitors",
    "advantages": "Competitive advantages",
    "market_position": "Current position"
  },
  "ask": {
    "funding_amount": "Investment sought",
    "use_of_funds": "Allocation plan",
    "milestones": "Key objectives"
  }
}
```

### 📝 Call Transcript Format (TXT)
```text
Date: [Date of call]
Participants: [Names and roles]

[Speaker 1]: Opening remarks about company vision...
[Speaker 2]: Questions about market size...
[Speaker 1]: Our TAM is approximately $50B...

Key Points Discussed:
- Market opportunity
- Product differentiation
- Team capabilities
- Growth metrics
- Funding requirements
```

### 📧 Founder Material Format (DOCX)
```
FOUNDER PROFILE

Name: [Founder Name]
Role: [CEO/CTO/etc.]

Education:
- [Degree, University, Year]
- [Additional qualifications]

Experience:
- [Company, Role, Duration]
- [Key achievements]

Expertise:
- [Domain knowledge]
- [Technical skills]

Previous Ventures:
- [Company name, outcome]
```

## 🔄 Processing Pipeline Data

### 📊 Extracted Parameters JSON
```json
{
  "company_name": "FinTechX",
  "sector": "Finance",
  "founded": "2022",
  "team": "3 founders from IIT Delhi, 2 from IIM Ahmedabad, 10 engineers",
  "market": "Indian SME lending market worth $50B",
  "traction": "10,000 active users, 20% MoM growth",
  "revenue": "INR 2 Cr ARR",
  "unique_selling_point": "AI-driven credit underwriting with 30% lower default rate",
  "competition": "KreditBee, LendingKart, Capital Float",
  "business_model": "Interest on loans + processing fees",
  "risks": "Regulatory changes, funding dependency, market saturation"
}
```

### 🎯 Scored Data Structure
```json
{
  "Parameter": "Team_Quality",
  "Raw_Value": "3 IIT founders + 10 engineers",
  "Score": 8,
  "Weight": 0.15,
  "Weighted_Score": 1.2,
  "Benchmark": 7,
  "vs_Benchmark": "+1",
  "Notes": "Strong technical team with IIT background"
}
```

### 📈 Final Analysis Output
```json
{
  "summary": {
    "company_name": "FinTechX",
    "sector": "Finance",
    "final_score": 7.8,
    "recommendation": "CONSIDER",
    "analysis_date": "2024-01-15"
  },
  "scores": {
    "Team_Quality": 8,
    "Market_Size": 9,
    "Traction": 7,
    "Financials": 7,
    "Product_Uniqueness": 8,
    "Competitive_Landscape": 7,
    "Business_Model_Clarity": 7,
    "Risk_Factors": 6
  },
  "weighted_scores": {
    "Team_Quality": 1.2,
    "Market_Size": 1.35,
    "Traction": 1.05,
    "Financials": 0.7,
    "Product_Uniqueness": 1.2,
    "Competitive_Landscape": 0.7,
    "Business_Model_Clarity": 0.7,
    "Risk_Factors": 0.6
  },
  "red_flags": [
    "Risk_Factors score (6) is below threshold (7). Refer page No 8",
    "Financials need improvement - burn rate high"
  ],
  "green_flags": [
    "Market_Size score (9) is excellent",
    "Team_Quality (8) shows strong founding team"
  ],
  "recommendations": [
    "Focus on reducing customer acquisition cost",
    "Strengthen risk mitigation strategies",
    "Consider strategic partnerships for market expansion",
    "Improve unit economics before next funding round"
  ]
}
```

## 📁 Sample Files in `/input` Directory

### 1. `startup_ptch_deck.pdf`
- **Type**: Complete pitch deck
- **Pages**: 15
- **Content**: Full startup presentation
- **Use Case**: Primary testing file

### 2. `FinTechX_ AI-Powered SME Lending Revolution.pdf`
- **Type**: FinTech pitch deck
- **Pages**: 12
- **Content**: Finance sector example
- **Use Case**: Sector-specific testing

### 3. `transcript.txt`
- **Type**: Call transcript
- **Size**: ~2000 words
- **Content**: Investor-founder discussion
- **Use Case**: Supplementary information

### 4. `pitch_deck_draft.txt`
- **Type**: Text-based pitch
- **Size**: ~1500 words
- **Content**: Pitch outline in text
- **Use Case**: Non-PDF testing

### 5. `email.docx`
- **Type**: Email communication
- **Size**: 2 pages
- **Content**: Follow-up correspondence
- **Use Case**: Additional context

### 6. `founder_material.docx`
- **Type**: Founder profiles
- **Size**: 4 pages
- **Content**: Team backgrounds
- **Use Case**: Team evaluation

## 🎯 Scoring Examples

### High Score Example (8-10)
```json
{
  "parameter": "Market_Size",
  "raw_value": "$100B global market, 25% CAGR",
  "score": 9,
  "reasoning": "Large TAM with high growth rate"
}
```

### Medium Score Example (5-7)
```json
{
  "parameter": "Traction",
  "raw_value": "5,000 users, 10% MoM growth",
  "score": 6,
  "reasoning": "Moderate user base with decent growth"
}
```

### Low Score Example (1-4)
```json
{
  "parameter": "Risk_Factors",
  "raw_value": "Heavy regulation, high burn, competitor threats",
  "score": 3,
  "reasoning": "Multiple significant risk factors"
}
```

## 📊 Benchmark Data Structure

### `sector_benchmarks.csv`
```csv
Sector,Team_Quality,Market_Size,Traction,Financials,Product_Uniqueness
Technology,7,8,6,5,8
Finance,8,7,7,6,7
Healthcare,8,9,5,4,9
E-commerce,6,8,8,7,6
Education,7,7,6,5,7
```

## 🔄 Data Transformation Examples

### Text to Parameter Extraction
**Input**: "Our team consists of 3 IIT graduates with 10+ years experience"
**Output**: 
```json
{
  "team": "3 IIT graduates, 10+ years experience",
  "team_score": 8
}
```

### Market Size Parsing
**Input**: "TAM is approximately $50 billion"
**Output**:
```json
{
  "market_size_value": 50000000000,
  "market_size_unit": "USD",
  "market_score": 9
}
```

### Traction Metrics Extraction
**Input**: "10K MAU with 20% MoM growth"
**Output**:
```json
{
  "users": 10000,
  "growth_rate": 0.20,
  "growth_period": "monthly",
  "traction_score": 7
}
```

## 🧪 Test Data Sets

### Successful Startup Profile
```json
{
  "expected_score": "8.5+",
  "characteristics": {
    "team": "Serial entrepreneurs from top schools",
    "market": ">$10B TAM",
    "traction": ">15% MoM growth",
    "product": "Clear differentiation",
    "risks": "Well-mitigated"
  }
}
```

### Average Startup Profile
```json
{
  "expected_score": "5.5-7.5",
  "characteristics": {
    "team": "First-time founders with domain expertise",
    "market": "$1-10B TAM",
    "traction": "5-15% MoM growth",
    "product": "Some differentiation",
    "risks": "Manageable risks"
  }
}
```

### High-Risk Startup Profile
```json
{
  "expected_score": "<5.5",
  "characteristics": {
    "team": "Limited experience",
    "market": "<$1B TAM",
    "traction": "<5% MoM growth",
    "product": "Me-too product",
    "risks": "Multiple red flags"
  }
}
```

## 📝 Usage Guidelines

### For Testing
1. Use files from `/input` directory
2. Start with `startup_ptch_deck.pdf`
3. Add optional files for comprehensive testing

### For Development
1. Refer to JSON structures for data format
2. Use benchmark data for calibration
3. Test with various score ranges

### For Validation
1. Compare output against expected scores
2. Verify red flag detection
3. Check recommendation relevance
