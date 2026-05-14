## Project Overview

Retail AI Assistant is a simulation-based agentic AI system designed to handle two major retail workflows:

1. Personal Shopper (Revenue Agent)
2. Customer Support Assistant (Operations Agent)

The system uses:

* LLM-based reasoning (Groq + Llama 3.3)
* Dynamic tool calling
* Structured business logic
* Deterministic policy evaluation
* Grounded retrieval from CSV data

The assistant dynamically selects tools based on user queries instead of relying on hardcoded routing.


# Features

## Personal Shopper Agent

The assistant can:

* Recommend products
* Filter by price
* Filter by tags/preferences
* Check stock availability
* Filter by requested sizes
* Prioritize sale items
* Consider bestseller score
* Explain recommendation reasoning

Example:

```text
Need a modest evening gown under $300 in size 8 on sale
```

---

## Customer Support Agent

The assistant can:

* Fetch order details
* Evaluate return eligibility
* Apply return policies
* Handle vendor-specific exceptions
* Reject invalid orders
* Prevent hallucinated responses

Example:

```text
Can I return order O0005?
```

---

# Tech Stack

* Python
* FastAPI
* Groq API
* Llama 3.3 70B
* Pandas
* Tool Calling / Function Calling

---

# Project Structure

```text
retail-ai-assistant/
│
├── agent/
│   └── retail_agent.py
│
├── tools/
│   ├── product_tools.py
│   ├── order_tools.py
│   └── return_tools.py
│
├── utils/
│   └── data_loader.py
│
├── data/
│   ├── product_inventory.csv
│   ├── orders.csv
│   └── policy.txt
│
├── main.py
├── requirements.txt
├── README.md
├── architecture.md
└── .env
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your_repo_link>
cd retail-ai-assistant
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

venv\Scripts\activate

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
.env
```

Add:

```text
GROQ_API_KEY=your_api_key_here
```

---

# Running The Application

## CLI Mode

```bash
python -m agent.retail_agent
```

---

## FastAPI Server

```bash
uvicorn main:app --reload
```

---

# API Endpoint

## POST

```text
/chat
```

Example Request:

```json
{
  "query": "Show me sale items under $250"
}
```

---

# Example Queries

## Shopping Queries

```text
Need a modest evening gown under $300 in size 8 on sale
```

```text
Show me cocktail dresses under $200
```

```text
I need a sleeve dress in size 16
```

---

## Support Queries

```text
Can I return order O0005?
```

```text
Show me details for order O0005
```

```text
Tell me about product P0001
```

---

# Hallucination Prevention

The system avoids hallucination by:

* Using structured tools for retrieval
* Separating reasoning from business logic
* Rejecting invalid order IDs
* Rejecting invalid product IDs
* Using deterministic policy evaluation
* Avoiding direct LLM-generated inventory data

---

# Key Architectural Design

* LLM handles reasoning and orchestration
* Tools handle factual retrieval
* Policies are evaluated deterministically
* Tool outputs are grounded in CSV data
* Business logic is separated from AI reasoning
