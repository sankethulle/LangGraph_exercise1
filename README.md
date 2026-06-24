# Product Review Summarizer Agent - Learn LangGraph Step by Step

A multi-agent Product Review Analysis system built using LangGraph, LangChain, and OpenAI GPT-4.1 Mini that extracts pros, cons, sentiment, ratings, and recommendation decisions from customer reviews.

Overview

This project demonstrates how to build a workflow-driven AI agent using LangGraph.

Instead of asking a single LLM prompt to perform all tasks, the application divides the work among specialized agents:

Pros Extraction Agent
Cons Extraction Agent
Sentiment Analysis Agent
Recommendation Decision Agent
Summary Agent

Each agent contributes information to a shared state object, creating a modular and maintainable AI workflow.

Key Features

✅ Extract positive product feedback

✅ Extract negative product feedback

✅ Calculate overall sentiment

✅ Estimate product rating

✅ Generate recommendation decision

✅ Create final recommendation summary

✅ Stateful workflow using LangGraph

✅ OpenAI GPT-powered analysis

System Architecture
                    ┌────────────────────┐
                    │ Product Reviews    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Extract Pros Agent │
                    └───────┬────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
      ┌─────────────────┐   ┌─────────────────────┐
      │ Extract Cons    │   │ Sentiment Analyzer  │
      │ Agent           │   │ Agent               │
      └─────────────────┘   └─────────┬───────────┘
                                      │
                                      ▼
                        ┌────────────────────────┐
                        │ Recommendation Agent   │
                        └──────────┬─────────────┘
                                   │
                  ┌────────────────┴─────────────┐
                  │                              │
                  ▼                              ▼
      ┌─────────────────────┐      ┌─────────────────────┐
      │ Recommended Summary │      │ Not Recommended     │
      │ Agent               │      │ Summary Agent       │
      └──────────┬──────────┘      └──────────┬──────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               ▼
                             END
Sequence Diagram
User
 │
 │ Reviews
 ▼
Pros Agent
 │
 ├────────────► Extract positive feedback
 │
 ▼
Cons Agent
 │
 ├────────────► Extract negative feedback
 │
 ▼
Sentiment Agent
 │
 ├────────────► Determine sentiment
 ├────────────► Estimate rating
 │
 ▼
Recommendation Agent
 │
 ├────────────► Recommended?
 │
 ├── YES ──► Recommended Summary
 │
 └── NO ───► Not Recommended Summary
                │
                ▼
          Final Result
LangGraph Workflow

The workflow is represented as a directed graph.

START
  ↓
extract_pros
  ↓
extract_cons

extract_pros
  ↓
gauge_overall_sentiment
  ↓
execute_commended_or_not

execute_commended_or_not
  ├── recommended
  └── not_recommended

END

State transitions are managed using a shared ProductReviewState object.
## Setup
### 1. Create and activate a virtual environment

```Installation
Clone Repository
git clone https://github.com/yourusername/product-review-summarizer.git
```

```powershell
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure your OpenAI API key

```powershell
copy .env.example .env
```

Edit `.env` and add your API key:

```text
OPENAI_API_KEY=sk-...
```

Never commit your real `.env` file.

### 4. Run the project

```powershell
product-review-summarizer.py
```

---

Example Input:

Battery backup is amazing.
Camera quality is excellent.
Device becomes hot while gaming.
Example Output
Pros:
- Excellent battery backup
- Great camera quality

Cons:
- Heating issue during gaming

Overall Sentiment:
Positive

Estimated Rating:
4.2/5

Recommended:
True

Summary:
This product receives mostly positive feedback with strong battery performance and camera quality. Minor heating issues were reported but do not significantly impact overall satisfaction.
Project Structure
product-review-summarizer/
│
├── product_review_summrizer.py
├── .env
├── README.md
└── requirements.txt

## Key Takeaways

Agentic AI workflows
LangGraph state management
Conditional routing
Multi-agent orchestration
Prompt engineering
Structured JSON outputs
OpenAI integration