# 12 - Anti-Hallucination Framework

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Anti-Hallucination Framework  
**Target Audience:** AI Safety Team, Developers  
**Approx Tokens:** ~2,500

---

## 12.1 Why Anti-Hallucination Matters

AI hallucinations can lead to:
- **Incorrect diagnoses** - misidentifying root causes
- **Unsafe remediations** - executing harmful actions
- **Compliance violations** - generating false audit data
- **Operational risks** - creating confusion during incidents

## 12.2 Anti-Hallucination Techniques

### 12.2.1 Strict Truth Constraints

These instructions are added to the system prompt:
- "Base answers ONLY on provided context"
- "State 'I don't know' if information is not available"
- "Never create fake data or citations"
- "Verify claims against provided evidence"

### 12.2.2 "According To" Prompting

Force the AI to cite sources:
- "For every claim, cite the source"
- "List full bibliographic details at the end"

### 12.2.3 Step-by-Step Reasoning

Make the AI show its work:
- "Analyze step-by-step before answering"
- "State confidence level for each step"

### 12.2.4 Self-Verification

Make the AI check its own work:
- "Review answers for unsupported claims"
- "Generate verification questions"

## 12.3 Implementation

### 12.3.1 System Prompt

The system prompt includes strict constraints:
```python
system_prompt = """
You are an expert SRE assistant. Answer ONLY based on the provided context.
If the answer is not contained within the provided text, state 'Data not available'.
Never create fake data or citations.
"""
```

### 12.3.2 Tool Output Validation

Every tool output is validated against expected schemas:
```python
def validate_tool_output(tool_name, output_data):
    schema = TOOL_SCHEMAS[tool_name]
    try:
        schema.validate(output_data)
        return True
    except ValidationError as e:
        log_error(f"Tool {tool_name} output validation failed: {e}")
        return False
```

## 12.4 Monitoring Hallucinations

### 12.4.1 Hallucination Detection Metrics

| Metric | Description | Threshold |
|--------|-------------|-----------|
| **Confidence Score** | AI's confidence in its answer | < 0.7 = warning |
| **Source Citation Rate** | Percentage of claims with valid sources | < 90% = warning |
| **Unsupported Claim Rate** | Percentage of claims without evidence | > 5% = critical |

### 12.4.2 Response to Hallucinations

| Severity | Action |
|----------|--------|
| **Warning** | Log event, notify admin via UI banner |
| **Critical** | Block tool execution, require human approval |

## 12.5 Best Practices for Prompt Engineering

### 12.5.1 Prompt Structure

1. Clear task definition
2. Relevant context provided
3. Strict output format required
4. Examples given (few-shot learning)
5. Verification steps included

### 12.5.2 Prompt Versioning

Use tools like Langfuse or Opik to:
- Version system prompts
- Track changes
- Prevent "prompt bloat"

*Anti-hallucination measures are critical for production AI systems. This framework ensures reliable and safe AI operation.*