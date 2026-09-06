# Government Scheme Navigator

An **Agentic AI-powered Government Scheme Navigator** that helps citizens discover relevant government schemes based on their personal profile, understand eligibility requirements, and identify the benefits and documents required to apply.

The system combines **Large Language Models, tool-based reasoning, web data extraction, eligibility verification, and agent state management** to provide personalized scheme recommendations.

---

## Problem Statement

Government welfare and scholarship schemes are often difficult to discover because:

- Thousands of schemes are available across different departments.
- Eligibility conditions vary between schemes.
- Citizens may not know which schemes apply to them.
- Important information such as required documents and application procedures can be difficult to find.
- Manually searching multiple government portals is time-consuming.

### Our Solution

**Government Scheme Navigator** acts as an intelligent AI agent that understands a user's situation and navigates available government schemes to identify potentially relevant opportunities.

Instead of requiring users to search through schemes manually, the agent follows:

> **Understand → Reason → Search → Verify → Observe → Respond**

---

# 🤖 Key Features

### 1. Natural Language Understanding

Users can describe their situation naturally.

Example:

> "I am a female student from Tamil Nadu who studied in a government school. What schemes can I apply for?"

The AI extracts structured information such as:

- Age
- Gender
- State
- Occupation
- Income
- Category
- Education level
- Government school background

---

### 2. Agentic Reasoning

The system uses a ReAct-style architecture:

```text
User Query
     ↓
Understand User
     ↓
Extract Profile
     ↓
Reason About Next Action
     ↓
Select Tool
     ↓
Execute Tool
     ↓
Observe Result
     ↓
Verify Eligibility
     ↓
Generate Final Answer
