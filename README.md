# Product Review Summarizer - Learn LangGraph Step by Step

A beginner-friendly LangGraph project that analyzes customer product reviews and determines whether a product should be recommended based on sentiment, rating, pros, and cons.

The project demonstrates a clear LangGraph pattern:

```text
                    [Product Reviews]
                             |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
   extract_pros       extract_cons     gauge_overall_sentiment
        \                  |                  /
         \                 |                 /
          +----------------+----------------+
                           |
                           v
             execute_commended_or_not
                           |
                      conditional
                     /           \
                    v             v
      recommended_summary   not_recommended_summary
                    |             |
                   END           END
```

---

## What This Project Does

A user enters one or more product reviews such as:

- `Battery life is excellent.`
- `The camera quality is amazing.`
- `The phone gets hot during gaming.`

The graph then:

1. Extracts positive feedback (Pros).
2. Extracts negative feedback (Cons).
3. Determines overall sentiment.
4. Estimates an overall rating.
5. Decides whether the product should be recommended.
6. Generates a final recommendation summary.
7. Prints execution logs from each node.

---

## LangGraph Concepts Covered

| Concept | Where It Appears |
|---|---|
| State | `ProductReviewState` Pydantic model |
| Nodes | `extract_pros`, `extract_cons`, `gauge_overall_sentiment`, `execute_commended_or_not`, `recommended_summary`, `not_recommended_summary` |
| Parallel execution | Three specialist nodes start from `START` |
| Fan-in | Three specialist outputs merge into `execute_commended_or_not` |
| Conditional edges | `route_after_decision` decides the final path |
| Final output | Recommendation summary |
| Message accumulation | `messages: Annotated[list, operator.add]` |

---

## Project Files

```text
product_review_summrizer.py   Main LangGraph project
README.md                     Project documentation
requirements.txt              Python dependencies
.env                          OpenAI API key
```

---

## Setup

### 1. Create and activate a virtual environment

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

Create a `.env` file:

```text
OPENAI_API_KEY=sk-...
```

Never commit your real `.env` file.

### 4. Run the project

```powershell
python product_review_summrizer.py
```

---

## Expected Flow

Example input:

```text
Battery life is excellent.
Camera quality is great.
The phone heats up during gaming.
```

The graph will:

1. Extract pros.
2. Extract cons.
3. Calculate sentiment and rating.
4. Decide whether the product is recommended.
5. Generate a final recommendation summary.
6. Print execution messages showing which nodes ran.

---

## Code Walkthrough

| Step | What Happens | File |
|---|---|---|
| 1 | Define `ProductReviewState` | `product_review_summrizer.py` |
| 2 | Initialize `ChatOpenAI` | `product_review_summrizer.py` |
| 3 | Define graph node functions | `product_review_summrizer.py` |
| 4 | Define `route_after_decision` | `product_review_summrizer.py` |
| 5 | Add nodes and edges to `StateGraph` | `product_review_summrizer.py` |
| 6 | Compile graph as `app` | `product_review_summrizer.py` |
| 7 | Execute using `run_product_review_checker()` | `product_review_summrizer.py` |

---

## Graph Architecture

```text
START
 ├── extract_pros
 ├── extract_cons
 └── gauge_overall_sentiment

extract_pros ───────────────┐
extract_cons ───────────────┼──► execute_commended_or_not
gauge_overall_sentiment ────┘

execute_commended_or_not
      │
      ▼
route_after_decision
      │
 ┌────┴─────┐
 ▼          ▼
recommended not_recommended
     │            │
     ▼            ▼
    END          END
```

---

## Important Note

This project is intended for educational purposes to learn:

- LangGraph
- Agent workflows
- State management
- Conditional routing
- OpenAI integration

The generated recommendations are AI-generated opinions and should not be considered professional product advice.

---

## Key Takeaways

1. State carries data across all nodes.
2. Nodes are Python functions that update the shared state.
3. Fan-out allows parallel execution of specialist agents.
4. Fan-in merges multiple results into a decision node.
5. Conditional routing dynamically determines the final workflow path.
6. LangGraph makes complex AI workflows easier to build and maintain.
