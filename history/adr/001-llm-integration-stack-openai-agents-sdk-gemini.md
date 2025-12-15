# ADR-001: LLM Integration Stack - OpenAI-Agents-SDK with Gemini

> **Scope**: This ADR documents the decision cluster for LLM integration including SDK choice, model selection, and agent architecture pattern.

- **Status:** Accepted
- **Date:** 2025-12-12
- **Feature:** 001-sub-agent-skills (AI-native Textbook Multi-Agent System)
- **Context:** The project requires AI-powered generation for educational content (glossary definitions, diagrams, translations, exercises). A decision was needed on how to integrate LLM capabilities into the multi-agent system, including SDK choice, model provider, and agent architecture pattern.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - defines how all agents communicate with LLM
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - 3 alternatives evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - affects all skill agents and orchestrator
-->

## Decision

We will use **OpenAI-Agents-SDK with Google Gemini model** in OpenAI-compatible mode for all LLM interactions:

- **SDK**: `openai-agents-sdk` (provides Agent, Runner, OpenAIChatCompletionsModel classes)
- **Model Provider**: Google Gemini via OpenAI-compatible endpoint
- **Model**: `gemini-2.5-flash` (fast, cost-effective for educational content)
- **Base URL**: `https://generativelanguage.googleapis.com/v1beta/openai/`
- **Agent Architecture**: BaseSkillAgent (abstract base) + 4 specialized sub-agents + MainOrchestratorAgent
- **Execution Pattern**: Synchronous via `Runner.run_sync()` for simplicity

**Implementation Pattern:**
```python
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("GEMINI_BASE_URL")
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)

agent = Agent(name="skill_name", instructions="...", model=model)
result = Runner.run_sync(agent, input=query)
```

## Consequences

### Positive

1. **Unified SDK**: Single SDK for agent creation, execution, and model management
2. **Model Flexibility**: OpenAI-compatible mode allows switching models (Gemini, Claude, GPT) with minimal code changes
3. **Existing Pattern**: Consistent with existing `my_agent.py` RAG implementation
4. **Cost Effective**: Gemini 2.5 Flash offers competitive pricing for high-volume educational queries
5. **Clean Architecture**: BaseSkillAgent inheritance promotes code reuse and single model configuration
6. **Extensibility**: Easy to add new skill agents by extending BaseSkillAgent

### Negative

1. **API Dependency**: Requires active Gemini API key and internet connectivity
2. **Latency**: LLM calls add 2-5 seconds latency per request (mitigated by "Thinking..." UI indicator)
3. **Rate Limits**: Subject to Gemini API rate limits and quotas
4. **Cost Accumulation**: Per-request pricing can accumulate with heavy usage
5. **Vendor Coupling**: Tied to Google's Gemini service availability and pricing changes

## Alternatives Considered

### Alternative A: Template-Based Generation (Previous Approach)
- **Components**: Python dictionaries, string templates, keyword matching
- **Pros**: Zero latency, offline capable, no API costs, deterministic output
- **Cons**: Limited vocabulary, no understanding of context, poor quality for complex queries
- **Rejected Because**: User explicitly requires AI-powered generation; template approach cannot match quality expectations

### Alternative B: Direct Google Generative AI Library
- **Components**: `google-generativeai` Python package, direct Gemini API calls
- **Pros**: Native Google SDK, potentially better Gemini-specific features
- **Cons**: Different API interface, no agent abstraction, would require custom orchestration
- **Rejected Because**: User specified OpenAI-compatible mode via OpenAI-Agents-SDK; would break consistency with existing codebase

### Alternative C: OpenAI API Directly
- **Components**: `openai` Python package, GPT-4 or GPT-3.5-turbo models
- **Pros**: Well-documented, stable API, strong model performance
- **Cons**: Higher cost than Gemini Flash, different provider than requested
- **Rejected Because**: User specified Gemini model; OpenAI pricing may be prohibitive for educational use case

## References

- Feature Spec: [specs/sub-agent-skills/spec.md](../../specs/sub-agent-skills/spec.md)
- Implementation Plan: [specs/sub-agent-skills/plan.md](../../specs/sub-agent-skills/plan.md)
- Research Document: [specs/sub-agent-skills/research.md](../../specs/sub-agent-skills/research.md)
- Related ADRs: None (first ADR for this project)
- Existing Pattern: [backend/my_agent.py](../../backend/my_agent.py) - demonstrates OpenAI-Agents-SDK + Gemini integration
