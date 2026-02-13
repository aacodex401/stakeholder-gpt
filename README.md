# 🎯 StakeholderGPT

**Flight simulator for Product Managers.**

Practice your roadmap pitch with tough AI stakeholders before the real meeting. Get grilled by AI versions of your CEO, CTO, and Head of Design.

## Why?

Every PM knows the feeling: you walk into a roadmap review confident, then get blindsided by a question you didn't anticipate. StakeholderGPT lets you rehearse with demanding AI personas who ask the hard questions—so you're ready when it counts.

## Features

- **3 AI Stakeholder Personas:**
  - 👔 **CEO**: ROI, market timing, strategic focus, opportunity cost
  - 💻 **CTO**: Scalability, tech debt, integration risks, team capacity
  - 🎨 **Head of Design**: User problems, validation, UX complexity

- **Interactive Grilling**: Each stakeholder asks 2-3 tough questions
- **Readiness Score**: Get a 1-10 assessment with improvement suggestions
- **Local-First**: Uses Ollama (free) by default, OpenAI fallback available

## Installation

```bash
# Clone
git clone https://github.com/aacodex401/stakeholder-gpt.git
cd stakeholder-gpt

# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running with llama3.1
ollama pull llama3.1:8b
ollama serve
```

## Usage

```bash
# Inline pitch
python main.py grill --pitch "Your roadmap pitch here..."

# From file
python main.py grill --file my-pitch.txt

# Interactive (paste pitch, then Ctrl+D)
python main.py grill

# See example pitch
python main.py example
```

## Example Session

```
$ python main.py grill --pitch "Q2: AI Search. 50% faster search, 20% more conversions..."

🎯 StakeholderGPT
Flight simulator for Product Managers

👔 CEO Questions
- What's the $2M revenue calculation based on?
- Why AI search now vs. improving existing filters?
- What are we deprioritizing to staff this?

💻 CTO Questions  
- How does the vector DB scale with our catalog size?
- What's the ML model training pipeline look like?
- Integration risk with current search infrastructure?

🎨 Designer Questions
- Have we validated users want AI recommendations?
- What happens when AI gets it wrong—fallback UX?
- How does this affect mobile search experience?

📊 Readiness Assessment
Score: 6/10
Strengths: Clear metrics, reasonable timeline
Gaps: Missing competitive analysis, no user research cited
Suggestions: Add user interview quotes, clarify ML approach...
```

## Configuration

By default, uses Ollama with `llama3.1:8b`. To use a different model:

```bash
export STAKEHOLDER_MODEL="openai/gpt-4"  # OpenAI
export STAKEHOLDER_MODEL="ollama/mistral"  # Different Ollama model
```

## Built With

- [CrewAI](https://crewai.com) - Multi-agent orchestration
- [Typer](https://typer.tiangolo.com) - CLI framework
- [Rich](https://rich.readthedocs.io) - Terminal formatting
- [Ollama](https://ollama.ai) - Local LLM inference

## License

MIT

---

*Part of the [Fractional CPO Toolkit](https://github.com/aacodex401) — practical tools for product leaders.*
