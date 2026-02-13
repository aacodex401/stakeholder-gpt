#!/usr/bin/env python3
"""
StakeholderGPT - Flight simulator for Product Managers
Practice your roadmap pitch with tough AI stakeholders before the real meeting.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from crewai import Agent, Task, Crew
import os

app = typer.Typer()
console = Console()

# Configure LLM - Ollama local by default, OpenAI fallback
LLM_CONFIG = {
    "model": os.getenv("STAKEHOLDER_MODEL", "ollama/llama3.1:8b"),
}

def create_stakeholders():
    """Create the 3 AI stakeholder personas."""
    
    ceo = Agent(
        role="CEO",
        goal="Evaluate roadmap proposals from a business and strategic perspective",
        backstory="""You are a seasoned CEO who has built multiple successful companies. 
        You care deeply about ROI, market timing, resource allocation, and strategic focus. 
        You ask tough questions about business value and opportunity cost. 
        You're supportive but demanding - you want to see clear thinking.""",
        verbose=False,
        llm=LLM_CONFIG["model"],
    )
    
    cto = Agent(
        role="CTO",
        goal="Evaluate roadmap proposals from a technical feasibility and architecture perspective",
        backstory="""You are an experienced CTO who has scaled systems from startup to enterprise.
        You care about technical debt, scalability, integration complexity, and team capacity.
        You ask probing questions about implementation risks and technical trade-offs.
        You're collaborative but rigorous - you want realistic plans.""",
        verbose=False,
        llm=LLM_CONFIG["model"],
    )
    
    designer = Agent(
        role="Head of Design",
        goal="Evaluate roadmap proposals from a user experience and validation perspective",
        backstory="""You are a user-obsessed design leader who has shipped products used by millions.
        You care about user problems, validation, usability, and design coherence.
        You ask challenging questions about user research and experience trade-offs.
        You're empathetic but principled - you advocate for users.""",
        verbose=False,
        llm=LLM_CONFIG["model"],
    )
    
    return ceo, cto, designer


def create_grilling_tasks(pitch: str, ceo, cto, designer):
    """Create tasks for each stakeholder to grill the pitch."""
    
    ceo_task = Task(
        description=f"""Review this roadmap pitch and ask 2-3 tough business questions:

PITCH:
{pitch}

Ask questions a CEO would ask:
- What's the ROI and how did you calculate it?
- Why now? What's the market timing?
- What are we choosing NOT to do by pursuing this?
- How does this align with our strategic priorities?
- What's the competitive risk if we don't do this?

Be direct but constructive. Challenge assumptions.""",
        expected_output="2-3 tough business-focused questions about the roadmap pitch",
        agent=ceo,
    )
    
    cto_task = Task(
        description=f"""Review this roadmap pitch and ask 2-3 tough technical questions:

PITCH:
{pitch}

Ask questions a CTO would ask:
- How does this scale? What's the architecture?
- What technical debt are we taking on?
- What are the integration risks with existing systems?
- Do we have the team capacity and skills?
- What's the rollback plan if it fails?

Be thorough but fair. Identify real technical risks.""",
        expected_output="2-3 tough technical questions about the roadmap pitch",
        agent=cto,
    )
    
    designer_task = Task(
        description=f"""Review this roadmap pitch and ask 2-3 tough user experience questions:

PITCH:
{pitch}

Ask questions a Head of Design would ask:
- What specific user problem does this solve?
- How have we validated this with users?
- What's the UX complexity for end users?
- How does this fit with our existing product experience?
- What are users asking for that we're ignoring?

Be user-focused but practical. Advocate for the customer.""",
        expected_output="2-3 tough user experience questions about the roadmap pitch",
        agent=designer,
    )
    
    return [ceo_task, cto_task, designer_task]


def create_evaluation_task(pitch: str, questions: str, ceo):
    """Create final evaluation task."""
    
    return Task(
        description=f"""Based on the stakeholder questions raised about this pitch, provide a readiness assessment:

ORIGINAL PITCH:
{pitch}

STAKEHOLDER QUESTIONS:
{questions}

Provide:
1. **Readiness Score**: 1-10 (10 = ready to present to real stakeholders)
2. **Strengths**: What's strong about this pitch?
3. **Gaps**: What needs more work before the real meeting?
4. **Suggested Improvements**: 3 specific things to add or clarify

Be honest and helpful. The goal is to make them better prepared.""",
        expected_output="A readiness assessment with score, strengths, gaps, and improvement suggestions",
        agent=ceo,
    )


@app.command()
def grill(
    pitch: str = typer.Option(None, "--pitch", "-p", help="Your roadmap pitch text"),
    pitch_file: str = typer.Option(None, "--file", "-f", help="File containing your pitch"),
):
    """Get grilled by AI stakeholders on your roadmap pitch."""
    
    # Get pitch content
    if pitch_file:
        with open(pitch_file, 'r') as f:
            pitch_text = f.read()
    elif pitch:
        pitch_text = pitch
    else:
        console.print("[yellow]Enter your pitch (Ctrl+D or Ctrl+Z when done):[/yellow]")
        import sys
        pitch_text = sys.stdin.read()
    
    if not pitch_text.strip():
        console.print("[red]No pitch provided. Use --pitch or --file.[/red]")
        raise typer.Exit(1)
    
    console.print(Panel(
        "[bold blue]🎯 StakeholderGPT[/bold blue]\n"
        "[dim]Flight simulator for Product Managers[/dim]",
        subtitle="Preparing your stakeholder grilling session..."
    ))
    
    # Create stakeholders
    console.print("\n[dim]Assembling your stakeholder panel...[/dim]")
    ceo, cto, designer = create_stakeholders()
    
    # Create grilling tasks
    tasks = create_grilling_tasks(pitch_text, ceo, cto, designer)
    
    # Run the grilling
    console.print("[dim]Starting the grilling session...[/dim]\n")
    
    crew = Crew(
        agents=[ceo, cto, designer],
        tasks=tasks,
        verbose=False,
    )
    
    results = crew.kickoff()
    
    # Display questions from each stakeholder
    console.print(Panel("[bold red]👔 CEO Questions[/bold red]", expand=False))
    console.print(Markdown(str(tasks[0].output)))
    
    console.print(Panel("[bold blue]💻 CTO Questions[/bold blue]", expand=False))
    console.print(Markdown(str(tasks[1].output)))
    
    console.print(Panel("[bold green]🎨 Designer Questions[/bold green]", expand=False))
    console.print(Markdown(str(tasks[2].output)))
    
    # Combine all questions for evaluation
    all_questions = f"""
CEO: {tasks[0].output}

CTO: {tasks[1].output}

Designer: {tasks[2].output}
"""
    
    # Run evaluation
    console.print("\n[dim]Calculating your readiness score...[/dim]\n")
    
    eval_task = create_evaluation_task(pitch_text, all_questions, ceo)
    eval_crew = Crew(agents=[ceo], tasks=[eval_task], verbose=False)
    eval_crew.kickoff()
    
    console.print(Panel(
        Markdown(str(eval_task.output)),
        title="[bold yellow]📊 Readiness Assessment[/bold yellow]",
        border_style="yellow"
    ))
    
    console.print("\n[green]✅ Grilling session complete! Use this feedback to strengthen your pitch.[/green]")


@app.command()
def example():
    """Show an example pitch for testing."""
    
    example_pitch = """
# Q2 Roadmap: AI-Powered Search

## Problem
Users spend 3+ minutes finding products. Search abandonment is 40%.

## Solution
Implement semantic search with AI recommendations.

## Timeline
- Month 1: Vector database integration
- Month 2: ML model training on user behavior  
- Month 3: A/B test and rollout

## Resources
- 2 backend engineers
- 1 ML engineer
- $15k/month infra costs

## Expected Impact
- 50% reduction in search time
- 20% increase in conversion
- $2M additional revenue (projected)
"""
    
    console.print(Panel(
        Markdown(example_pitch),
        title="[bold]Example Pitch[/bold]",
        subtitle="Copy this or use: stakeholder-gpt grill --file example.txt"
    ))


if __name__ == "__main__":
    app()
