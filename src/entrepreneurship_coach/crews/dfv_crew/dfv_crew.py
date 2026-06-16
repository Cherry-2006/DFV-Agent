from crewai import Agent, Crew, Process, Task, LLM
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.project import CrewBase, agent, crew, task
from crewai.skills import discover_skills, activate_skill
from datetime import datetime
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel, Field
from pathlib import Path

now = datetime.now()
TodayDate = now.strftime("%d - %B - %Y")


load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
os.environ["SERPER_API_KEY"] = SERPER_API_KEY or ""

# Initialize tools required for Phase 1 Desirability market analysis
search_tool = SerperDevTool(api_key=SERPER_API_KEY)
scrape_tool = ScrapeWebsiteTool()


# llm = LLM(
#     model="bonsai-8b", 
#     base_url="http://127.0.0.1:1234/v1", 
#     api_key="lm-studio",
#     temperature=0.1,
# )

llm = LLM(
    model="ollama/qwen3.5:9b", 
    base_url="http://100.118.97.103:11434", 
    temperature=0.1,
)


class RefinedIdea(BaseModel):
    customer_segment: str = Field(description="A precise description of the target customer segment for this proposal, identifying who specifically experiences the problem (e.g. demographics, role, location, or behavioral traits), based strictly on the information given.")
    qualified_problem: str = Field(description="The specific, qualified problem or pain point this proposal addresses, stated clearly enough to show why it is a real and recurring issue for the identified customer segment.")
    consequence: str = Field(description="The direct negative consequence the customer segment faces if this problem remains unsolved, expressed in concrete terms (e.g. financial, time, opportunity, or experiential cost).")
    proposed_solution: str = Field(description="A concise description of the product, service, or solution being proposed to address the qualified problem, capturing its core mechanism and how it delivers value to the customer.")

class Hypotheses(BaseModel):
    desirability_statement: str = Field(description="A 'We believe [target customer] will [specific action/behavior]...' hypothesis statement that tests whether the target customer cares enough about the identified problem to adopt the proposed solution.")
    feasibility_statement: str = Field(description="A 'We believe [team/resource] can [build/deliver action] within [timeframe] using [tools/methods]...' hypothesis statement that tests whether the proposed solution can realistically be built or delivered with the resources and constraints described.")
    viability_statement: str = Field(description="A 'We believe we can sustain/grow this by [revenue model or business approach]...' hypothesis statement that tests whether the proposed business model can generate enough value to remain financially sustainable.")

class TipsValidatedMetrics(BaseModel):
    timely_factor: str = Field(description="The urgency/timeliness factor explaining why this problem matters to solve right now, based on any relevant trends, changes, deadlines, or shifting conditions mentioned in the proposal.")
    importance_metric: str = Field(description="The importance/severity metric explaining how significant the consequence is for the target customer, and why it matters enough to justify a solution.")
    profitability_pivot: str = Field(description="The core revenue or business model approach for this proposal, identifying who pays, how, and why that payer is willing to do so.")
    solvability_constraint: str = Field(description="The technical or operational feasibility constraint showing the proposed solution can realistically be implemented given the resources, tools, or infrastructure described in the proposal.")

class DecisionGate(BaseModel):
    status: str = Field(description="The definitive operational verdict for this proposal. Must be strictly either 'GO' (all three DFV dimensions - Desirability, Feasibility, Viability - pass without a fatal flaw) or 'NO-GO' (at least one dimension reveals a fatal flaw requiring a major structural pivot).")
    justification: str = Field(description="A concise, evidence-based explanation of the single most critical factor (positive or negative) across the Desirability, Feasibility, and Viability reports that determined the GO or NO-GO status.")

class DFAOutput(BaseModel):
    refined_idea: RefinedIdea
    hypotheses: Hypotheses 
    tips_validated_metrics: TipsValidatedMetrics
    final_decision: DecisionGate

skill = discover_skills(Path(__file__).resolve().parent / "skills")
activated = [activate_skill(s) for s in skill]

@CrewBase
class dfv_crew:
    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    @agent
    def desirability_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["desirability_agent"],  # type: ignore[index]
            llm=llm,
            tools=[search_tool, scrape_tool],
            verbose=True,
            skills=[activated[0]],
            max_iter=7
        )

    @agent
    def feasibility_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["feasibility_agent"],  # type: ignore[index]
            llm=llm,
            tools=[search_tool, scrape_tool],
            verbose=True,
            skills=[activated[2]],
            max_iter=7
        )

    @agent
    def viability_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["viability_agent"],  # type: ignore[index]
            llm=llm,
            tools=[search_tool, scrape_tool],
            verbose=True,
            skills=[activated[3]],
            max_iter=7
        )
    
    @agent
    def dfv_risk_decision_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["dfv_risk_decision_agent"],  # type: ignore[index]
            verbose=True,
            skills=[activated[1]],
            llm=llm
        )

    @task
    def desirability_task(self) -> Task:
        return Task(
            config=self.tasks_config["desirability_task"],  # type: ignore[index]

        )

    @task
    def feasibility_task(self) -> Task:
        return Task(
            config=self.tasks_config["feasibility_task"],  # type: ignore[index]
        )

    @task
    def viability_task(self) -> Task:
        return Task(
            config=self.tasks_config["viability_task"],  # type: ignore[index]
        )    
    @task
    def dfv_decision_task(self) -> Task:
        return Task(
            config=self.tasks_config["dfv_decision_task"],  # type: ignore[index]
            context=[
            self.desirability_task(),
            self.feasibility_task(),
            self.viability_task(),
            ],
            output_json=DFAOutput
        )

    @crew
    def crew(self) -> Crew:
        """Creates the dfv Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

