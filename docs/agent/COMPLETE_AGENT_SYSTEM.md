# 🚀 Complete Agent System for Startup Investment
## Built with Google ADK + A2A Protocol

Based on [Google ADK Python](https://github.com/google/adk-python) and [ADK Samples](https://github.com/google/adk-samples/tree/main/python)

---

## 🎯 Quick Overview

```
👤 INVESTOR 
   │
   ├─── 💬 Chat Interface
   ├─── 🎤 Voice Commands
   ├─── 📄 Upload Pitch Decks
   └─── 🔍 Investment Queries
   
   ▼
   
🧠 COORDINATOR AGENT (Main Orchestrator)
"Investment Decision Engine"
   │
   ├─── 💭 Analyzes: "What investment analysis needed?"
   ├─── 🤔 Routes: "Which specialist agent?"
   └─── ✅ HITL: "Confirm investment recommendation?"
   
   ▼
   
🤖 SPECIALIZED INVESTMENT AGENTS
   │
   ├─── 📄 Document Analyzer: "Extract pitch deck data"
   ├─── 🖼️ Vision Agent: "Analyze charts & screenshots" 
   ├─── 🔍 Market Research: "Find competitor data"
   ├─── 📊 Visualization: "Create investment dashboards"
   ├─── 🎤 Founder Interview: "Voice chat with founders"
   └─── 🔬 Investment Analyst: "Score & recommend"
   
   ▼
   
📁 MEMORY & KNOWLEDGE BASE
   │
   ├─── 💾 User Investment Preferences (ChromaDB)
   ├─── 📚 Past Investment History (Success/Fail tracking)
   ├─── 🔄 Portfolio Performance Analytics
   └─── 📊 Benchmark Database
   
   ▼
   
💬 INVESTMENT DECISION
   │
   ├─── 📝 Investment Memo
   ├─── 📊 Score Dashboard
   ├─── 🔊 Voice Summary
   └─── 📄 Red/Green Flags Report
```

---

## 🏗️ Architecture Layers

### Layer 1: User Interface
```
┌─────────────────────────────────┐
│         INVESTOR LAYER          │
│  • Chat Interface 💬            │
│  • Voice Commands 🎤            │  
│  • File Upload 📁               │
│  • Investment Dashboard 📊      │
└─────────────────────────────────┘
```

### Layer 2: Main Coordinator
```
┌─────────────────────────────────┐
│      COORDINATOR LAYER          │
│  • Understands request          │
│  • Routes to specialists        │
│  • HITL confirmation            │
│  • Aggregates results           │
└─────────────────────────────────┘
```

### Layer 3: Specialist Agents & Memory
```
┌─────────────────────────────────┐
│    SPECIALIST AGENTS LAYER      │
│  • 6 Investment Agents          │
│  • Memory System (ChromaDB)     │
│  • External APIs                │
└─────────────────────────────────┘
```

---

## 📦 The 6 Specialist Agents

| Agent | Purpose | Implementation |
|-------|---------|----------------|
| 📄 **Document Analyzer** | Extract pitch deck data | ADK Tools API + PDF libs |
| 🖼️ **Vision Agent** | Analyze charts/screenshots | Google Cloud Vision |
| 🔍 **Market Research** | Find competitor data | Web APIs (CrunchBase) |
| 📊 **Visualization** | Create investment charts | Plotly + Custom Tools |
| 🎤 **Founder Interview** | Voice chat with founders | A2A Protocol enabled |
| 🔬 **Investment Analyst** | Score & recommend | Multi-tool agent |

---

## 🎯 Core Platform Capabilities

### 📥 **1. Ingest Multiple Formats**
Our Document Analyzer agent processes diverse startup materials:
- **Pitch Decks** (PDF, PPTX) - Extract business models, team info, financials
- **Call Transcripts** - Analyze founder conversations and meeting notes  
- **Founder Updates** - Parse investor updates and progress reports
- **Email Communications** - Extract key metrics from email threads
- **Financial Documents** (XLSX, CSV) - Process cap tables, P&L statements

### 📊 **2. Sector Benchmarking** 
Market Research agent provides comprehensive comparative analysis:
- **Financial Multiples** - Revenue, EBITDA, and valuation multiples by sector
- **Hiring Data** - Team growth rates and talent acquisition patterns
- **Traction Signals** - Customer growth, MRR, churn rates vs industry
- **Competitive Positioning** - Market share and differentiation analysis
- **Geographic Benchmarks** - Regional performance comparisons

### 🚨 **3. Risk Detection**
Automated red flag identification across all data sources:
- **Inconsistent Metrics** - Discrepancies between pitch deck and financials
- **Inflated Market Size** - TAM/SAM/SOM validation against third-party data
- **Unusual Churn Patterns** - Abnormal customer retention metrics
- **Burn Rate Issues** - Unsustainable cash burn vs revenue growth
- **Team Red Flags** - Founder background checks and track record
- **Legal/Compliance Risks** - Regulatory issues in target markets

### 💡 **4. Investment Recommendations**
Investment Analyst agent generates actionable insights:
- **Growth Potential Summary** - Projected 3-5 year revenue trajectory
- **Customizable Weightages** - Adjust scoring based on fund strategy:
  - Early-stage focus: Team 40%, Market 30%, Product 30%
  - Growth-stage focus: Revenue 40%, Growth 30%, Market 30%
- **Investment Score** (0-100) with confidence intervals
- **Deal Terms Suggestions** - Recommended valuation and investment amount
- **Portfolio Fit Analysis** - Synergies with existing investments
- **Exit Strategy Assessment** - Potential acquirers and IPO readiness

### 🔄 **5. Deal Memo Generation**
Automated creation of comprehensive investment memos:
- **Executive Summary** - One-page investment thesis
- **Detailed Analysis** - 10-15 page deep dive with all metrics
- **Benchmarking Tables** - Side-by-side competitor comparisons
- **Risk Matrix** - Probability vs impact assessment
- **Recommendation** - Clear INVEST/PASS decision with rationale

---

## 🧠 Memory System & User Preferences

### 📊 **Investment History Tracking**
The system maintains comprehensive memory of all past investments:

#### **Past Investment Performance**
```python
investment_history = {
    "successful_exits": [
        {"company": "TechCo", "roi": 5.2, "exit_type": "acquisition"},
        {"company": "FinApp", "roi": 3.8, "exit_type": "ipo"}
    ],
    "failed_investments": [
        {"company": "StartupX", "loss": -0.8, "reason": "market_timing"}
    ],
    "active_portfolio": [
        {"company": "AIBot", "current_multiple": 2.1, "stage": "series_b"}
    ]
}
```

#### **Learning from Past Decisions**
- **Pattern Recognition** - Identifies what worked in successful investments
- **Mistake Avoidance** - Learns from failed investments to avoid similar issues
- **Success Replication** - Applies winning patterns to new opportunities

### 💾 **User Investment Preferences**
The system remembers and applies individual investor preferences:

```python
user_preferences = {
    "investment_thesis": {
        "sectors": ["fintech", "ai/ml", "saas"],
        "stages": ["seed", "series_a"],
        "check_size": {"min": 100000, "max": 1000000},
        "geography": ["us", "europe"]
    },
    "risk_appetite": {
        "risk_level": "moderate",  # conservative/moderate/aggressive
        "max_burn_multiple": 2.5,
        "min_runway_months": 12
    },
    "scoring_weights": {
        "team": 0.35,      # Prefers strong teams
        "market": 0.25,
        "product": 0.20,
        "financials": 0.20
    },
    "red_lines": [
        "no_revenue_model",
        "solo_founder",
        "highly_regulated_industries"
    ]
}
```

### 🔄 **Adaptive Learning Features**

#### **1. Performance-Based Adjustment**
```python
def adapt_scoring_based_on_history(current_weights, investment_history):
    """Adjust scoring weights based on what worked historically"""
    successful_patterns = analyze_successful_exits(investment_history)
    failed_patterns = analyze_failures(investment_history)
    
    # Increase weight for factors that correlated with success
    # Decrease weight for factors that led to failures
    return optimized_weights
```

#### **2. Preference Evolution**
```python
def update_preferences_from_feedback(user_feedback, current_prefs):
    """Learn from user's investment decisions and feedback"""
    if user_feedback == "invested_despite_low_score":
        # User saw value system missed - adjust criteria
        learn_new_pattern(user_feedback.reasons)
    elif user_feedback == "passed_despite_high_score":
        # User saw risks system missed - tighten criteria
        add_risk_factors(user_feedback.concerns)
```

#### **3. Portfolio Context Awareness**
```python
def consider_portfolio_context(new_opportunity, existing_portfolio):
    """Evaluate new investments in context of existing portfolio"""
    return {
        "diversification_score": calculate_sector_diversity(),
        "synergy_opportunities": find_portfolio_synergies(),
        "concentration_risk": check_overexposure(),
        "follow_on_reserves": calculate_reserve_requirements()
    }
```

### 📈 **Historical Analytics Dashboard**
The system provides insights from past investment patterns:

- **Success Rate by Sector** - Which sectors performed best
- **ROI by Stage** - Seed vs Series A vs Growth returns  
- **Red Flag Accuracy** - How often warnings proved correct
- **Score Correlation** - How scores correlated with outcomes
- **Exit Analysis** - Average time to exit, exit multiples

### 🎯 **Personalized Recommendations**
Based on history and preferences:

```python
def generate_personalized_recommendation(startup, user_profile):
    """Create recommendation based on user's history and preferences"""
    
    # Check against user's red lines
    if violates_red_lines(startup, user_profile.red_lines):
        return {"recommendation": "PASS", "reason": "Violates red lines"}
    
    # Apply personalized scoring weights
    score = calculate_score(startup, user_profile.scoring_weights)
    
    # Compare to historical successes
    similarity = compare_to_successful_investments(
        startup, 
        user_profile.investment_history
    )
    
    # Factor in portfolio context
    portfolio_fit = evaluate_portfolio_fit(
        startup,
        user_profile.active_portfolio
    )
    
    return {
        "score": score,
        "historical_similarity": similarity,
        "portfolio_fit": portfolio_fit,
        "personalized_recommendation": make_decision(score, similarity, portfolio_fit)
    }
```

---

## 🚀 Key System Features

### 1️⃣ **YAML Configuration (No-Code Option)**
```yaml
# agent_config.yaml
name: InvestmentCoordinator
model: gemini-2.0-flash
instruction: Analyze startups for investment
tool_confirmation: true  # HITL for safety
sub_agents:
  - DocumentAnalyzer
  - VisionAgent
  - FounderInterview
```

### 2️⃣ **HITL (Human in the Loop)**
```python
from google.adk.tools import ToolWithConfirmation

@ToolWithConfirmation(
    confirmation_message="Approve investment score: {score}?"
)
def calculate_investment_score(data):
    return score
```

### 3️⃣ **Built-in Development UI**
```bash
# Test agents visually
adk ui --agent investment_coordinator --port 8080
```

### 4️⃣ **Evaluation Framework**
```bash
# Measure performance
adk eval agents/investment evaluation/test_startups.json
```

### 5️⃣ **Easy Deployment**
```bash
# Deploy to production
adk deploy cloud-run --agent investment_coordinator
adk deploy vertex-ai --agent investment_coordinator
```

---

## 💻 Complete Implementation

### Main System Setup
```python
from google.adk.agents import LlmAgent
from google.adk.a2a import A2AProtocol
from google.adk.memory import MemoryService
from google.adk.tools import Tool

# Initialize Memory
memory = MemoryService(
    backend="chromadb",
    embedding_model="text-embedding-004"
)

# Document Analyzer Agent
document_analyzer = LlmAgent(
    name="DocumentAnalyzer",
    model="gemini-2.0-flash",
    tools=[pdf_extractor, data_parser],
    instruction="Extract and structure data from pitch decks"
)

# Vision Agent
vision_agent = LlmAgent(
    name="VisionAgent",
    model="gemini-2.0-flash",
    tools=[cloud_vision_api],
    instruction="Analyze charts, graphs, and screenshots"
)

# Founder Interview Agent (with A2A)
founder_interview = LlmAgent(
    name="FounderInterview",
    model="gemini-2.0-flash",
    a2a_config={
        "protocol": "a2a",
        "endpoint": "wss://founder-chat.api",
        "auth": "bearer_token"
    },
    instruction="Conduct voice interviews with founders"
)

# Investment Analyst Agent
investment_analyst = LlmAgent(
    name="InvestmentAnalyst",
    model="gemini-2.0-flash",
    tools=[score_calculator, benchmark_analyzer],
    tool_confirmation=True,  # Requires confirmation
    instruction="Calculate scores and generate recommendations"
)

# Main Coordinator
coordinator = LlmAgent(
    name="InvestmentCoordinator",
    model="gemini-2.0-flash",
    instruction="""
    You are an investment analysis coordinator.
    Analyze startups and provide investment recommendations.
    Route tasks to appropriate specialist agents.
    Always confirm critical investment decisions.
    """,
    sub_agents=[
        document_analyzer,
        vision_agent,
        founder_interview,
        investment_analyst
    ],
    memory=memory,
    tool_confirmation=True
)
```

### Critical Tools Implementation
```python
# 1. Multi-Format Ingestion
@Tool(description="Process multiple document formats")
def ingest_documents(files: list) -> dict:
    """Process pitch decks, transcripts, emails, financials"""
    extracted_data = {}
    for file in files:
        if file.endswith('.pdf'):
            extracted_data['pitch_deck'] = extract_pdf(file)
        elif file.endswith('.xlsx'):
            extracted_data['financials'] = parse_excel(file)
        elif file.endswith('.txt'):
            extracted_data['transcript'] = analyze_transcript(file)
    return extracted_data

# 2. Sector Benchmarking Tool
@Tool(description="Compare against sector benchmarks")
def sector_benchmark(company_metrics: dict, sector: str) -> dict:
    """Compare startup metrics against industry standards"""
    benchmarks = get_sector_data(sector)
    return {
        "revenue_multiple": company_metrics['valuation'] / company_metrics['revenue'],
        "sector_avg_multiple": benchmarks['avg_revenue_multiple'],
        "growth_percentile": calculate_percentile(
            company_metrics['growth_rate'], 
            benchmarks['growth_rates']
        ),
        "burn_efficiency": company_metrics['revenue'] / company_metrics['burn_rate']
    }

# 3. Risk Detection with HITL
@Tool(description="Detect red flags", confirmation_required=True)
def detect_red_flags(startup_data: dict) -> dict:
    """Comprehensive risk analysis with multiple checks"""
    red_flags = []
    yellow_flags = []
    
    # Financial risks
    if startup_data.get("burn_rate") > startup_data.get("revenue", 0) * 3:
        red_flags.append("🔴 Burn rate exceeds 3x revenue")
    
    # Market risks
    if startup_data.get("market_size_claim") > industry_data.get("verified_tam") * 2:
        red_flags.append("🔴 Inflated market size claims")
    
    # Metric consistency
    if abs(startup_data.get("reported_churn") - calculated_churn) > 0.1:
        yellow_flags.append("🟡 Inconsistent churn metrics")
        
    return {
        "red_flags": red_flags,
        "yellow_flags": yellow_flags,
        "risk_score": len(red_flags) * 20 + len(yellow_flags) * 10
    }

# 4. Investment Score with Customizable Weights
@Tool(description="Calculate investment score", confirmation_required=True)
def calculate_investment_score(
    startup_data: dict,
    weights: dict = None
) -> dict:
    """Calculate score with customizable weightages"""
    
    # Default weights (can be customized per fund strategy)
    if not weights:
        weights = {
            "team": 0.25,
            "market": 0.25,
            "product": 0.25,
            "financials": 0.25
        }
    
    # Calculate component scores
    team_score = evaluate_team(startup_data['founders'])
    market_score = evaluate_market(startup_data['market_size'], startup_data['growth'])
    product_score = evaluate_product(startup_data['traction'], startup_data['retention'])
    financial_score = evaluate_financials(startup_data['revenue'], startup_data['burn'])
    
    # Weighted final score
    final_score = (
        team_score * weights['team'] +
        market_score * weights['market'] +
        product_score * weights['product'] +
        financial_score * weights['financials']
    )
    
    return {
        "score": final_score,
        "components": {
            "team": team_score,
            "market": market_score,
            "product": product_score,
            "financials": financial_score
        },
        "recommendation": "INVEST" if final_score > 75 else "PASS",
        "confidence": calculate_confidence(startup_data)
    }

# 5. Deal Memo Generation
@Tool(description="Generate investment memo")
def generate_deal_memo(analysis_results: dict) -> str:
    """Create comprehensive investment memo"""
    memo_template = """
    # Investment Memo: {company_name}
    
    ## Executive Summary
    **Recommendation:** {recommendation}
    **Score:** {score}/100
    **Proposed Investment:** ${investment_amount} at ${valuation} valuation
    
    ## Key Metrics
    - ARR: ${arr}
    - Growth Rate: {growth}%
    - Burn Multiple: {burn_multiple}x
    - Market Size: ${market_size}
    
    ## Benchmarking
    {benchmark_table}
    
    ## Risk Assessment
    Red Flags: {red_flags}
    Yellow Flags: {yellow_flags}
    
    ## Investment Thesis
    {thesis}
    
    ## Next Steps
    {next_steps}
    """
    
    return memo_template.format(**analysis_results)
```

---

## 💬 User Interaction Examples

### Example 1: Complete Startup Analysis
```python
# Using ADK session management
from google.adk.sessions import Session

session = Session()
response = coordinator.run(
    session=session,
    prompt="Analyze TechCo startup for investment",
    attachments=["pitch_deck.pdf", "financials.xlsx"]
)

# Flow:
# 1. Coordinator receives request
# 2. Routes PDF to DocumentAnalyzer
# 3. Sends charts to VisionAgent
# 4. InvestmentAnalyst calculates score
# 5. HITL: "Approve score of 85/100?"
# 6. User confirms → Investment memo generated
```

### Example 2: Founder Interview
```python
response = coordinator.run(
    prompt="Schedule founder interview for TechCo",
    params={"company": "TechCo", "founder": "John Doe"}
)

# Flow:
# 1. FounderInterview agent activated
# 2. A2A protocol connects to founder
# 3. Conducts voice interview
# 4. Transcribes and analyzes responses
# 5. Updates investment score
```

---

## 🎯 Real Use Cases

### Use Case 1: Complete Startup Analysis
**Input:** Pitch deck (PDF) + Financials (XLSX)

#### Agent Flow:
1. **Main Coordinator** receives request
2. **Document Analyzer** extracts: Revenue $2M, 50% YoY growth
3. **Vision Agent** reads growth charts from slides
4. **Market Research** finds 3 competitors via CrunchBase
5. **Investment Analyst** calculates score: 82/100
6. **HITL Confirmation:** "Approve investment score 82/100?" ✅

#### Generated Investment Memo:
```markdown
# Deal Note: FinTechX Series A

## Executive Summary
FinTechX is a B2B lending platform showing strong traction with $2M ARR 
and 50% YoY growth. Recommend investment at $20M valuation (10x revenue multiple).

## Investment Score: 82/100 [INVEST]

## Sector Benchmarks:
- Revenue Multiple: 10x (vs 8-12x sector avg)
- Growth Rate: 50% (vs 40% sector avg)
- Burn Multiple: 2.5x (caution)

## Key Strengths:
✅ Strong product-market fit
✅ Experienced fintech team
✅ Enterprise client base

## Risk Factors:
⚠️ High burn rate vs revenue
⚠️ Competitive market landscape

## Next Steps: Schedule partner meeting
```

---

### Use Case 2: Automated Founder Interview
**Request:** "Interview FinTechX founder"

#### A2A Protocol in Action:
```
Agent: "Tell me about your product"
Founder: "We're building AI-powered lending platform..."

Agent: "What's your revenue model?"
Founder: "B2B SaaS, $500/month per client"

Agent: "Current traction?"
Founder: "20 enterprise clients, 150% growth QoQ"
```

#### Interview Analysis:
- **Key Insights:**
  - Clear monetization strategy
  - Strong early traction
  - Enterprise focus = higher LTV
- **Founder Score:** 17/20
- **Communication:** Clear & Confident
- **Auto-generated follow-ups:**
  - Request customer references
  - Deep dive on unit economics

---

### Use Case 3: Risk Assessment & Deal Memo
**Input:** TechStartup XYZ deck + financials

#### Red Flags Detected:
- **Financial:** Burn rate $500K/mo vs $100K revenue
- **Market:** 3 competitors with 10x funding, market leader owns 80% share
- **Runway:** Only 5 months remaining

#### Generated Investment Memo:
```markdown
# Deal Note: TechStartup XYZ - PASS

## Executive Summary
High-risk investment with unsustainable burn rate and dominant competition.
Recommend passing on this opportunity.

## Investment Score: 42/100 [PASS]

## Critical Issues:
❌ Burn multiple: 5x (critical)
❌ Market timing: Too late
❌ Competitive position: Weak

## HITL Override:
Partner can override if strategic value exists
```

---

## 🛠️ Quick Start Guide

### Step 1: Clone the Repository
```bash
# Clone the project
git clone https://github.com/Pooja-Vishnoi/GenAI_Hackathon
cd GenAI_Hackathon
```

### Step 2: Install ADK
```bash
pip install google-adk
pip install -r requirements_agentic.txt
```

### Step 2: Set Environment Variables
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
export GOOGLE_CLOUD_PROJECT="your-project"
```

### Step 3: Run Locally
```bash
# Start with built-in UI
adk ui --agent agents/investment_coordinator --port 8080

# Or run as API
adk serve --agent agents/investment_coordinator
```

### Step 4: Test the System
```bash
# Run evaluation
adk eval agents/ evaluation/test_startups.json
```

### Step 5: Deploy to Production
```bash
# Deploy to Cloud Run
adk deploy cloud-run \
    --agent investment_coordinator \
    --project your-gcp-project

# Or deploy to Vertex AI
adk deploy vertex-ai \
    --agent investment_coordinator \
    --region us-central1
```

---

## 📈 Benefits Summary

| Feature | Without ADK | With ADK | Improvement |
|---------|------------|----------|-------------|
| **Development Time** | 2-3 weeks | 3-5 days | 80% faster |
| **UI Development** | Custom build | Built-in UI | Zero effort |
| **Safety** | Manual checks | HITL confirmation | Automated |
| **Testing** | Manual | Evaluation framework | Automated |
| **Deployment** | Complex setup | One command | 99% faster |
| **Configuration** | Code only | YAML option | No-code capable |
| **Memory** | Custom implementation | MemoryService | Built-in |
| **A2A Communication** | Manual setup | Native protocol | Plug & play |

---

## ✨ What Makes This Special?

1. **Investment Focused** - Built specifically for startup analysis
2. **HITL Protection** - Confirms critical investment decisions
3. **Founder Interviews** - Direct voice communication via A2A
4. **Google ADK Native** - Official framework with support
5. **Code & No-Code** - YAML config or Python flexibility
6. **Built-in UI** - Test without building interface
7. **Production Ready** - Deploy instantly to cloud
8. **Evaluation Built-in** - Measure performance automatically
9. **Personalized Learning** - Remembers your investment history & preferences
10. **Adaptive Scoring** - Learns from your successful & failed investments
11. **Portfolio Aware** - Considers existing portfolio for diversification
12. **Fully Scalable** - From local to enterprise

---

## 🔑 Key Technologies

- **Google ADK** - Agent framework ([github.com/google/adk-python](https://github.com/google/adk-python))
- **Gemini 2.0 Flash** - LLM model
- **A2A Protocol** - Agent communication
- **ChromaDB** - Vector database
- **Google Cloud Vision** - Image analysis
- **Cloud Run / Vertex AI** - Deployment platforms

---

## 📊 System at a Glance

```
Total Components: 10
├── 1 Chat Interface (ADK UI)
├── 1 Coordinator Agent
├── 6 Specialist Agents  
├── 1 Memory System (ChromaDB)
└── 1 A2A Protocol Handler

Features:
├── HITL Confirmation ✅
├── No-Code Config ✅
├── Built-in UI ✅
├── Evaluation Framework ✅
└── One-Command Deploy ✅
```

---

**Built with [Google ADK](https://github.com/google/adk-python) - The Official Agent Development Kit** 🚀

**GitHub Repository**: [github.com/Pooja-Vishnoi/GenAI_Hackathon](https://github.com/Pooja-Vishnoi/GenAI_Hackathon)

**Ready for Gen AI Exchange Hackathon!** 🏆
