import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

# Load .env for API keys
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY not found. Make sure .env file exists in the same folder as this script.")
os.environ["SERPER_API_KEY"] = SERPER_API_KEY
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "fake")

# ── LLM config ────────────────────────────────────────────────────────────────
# Default: local Ollama. To use a cloud model, see README.md
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "ollama/qwen2.5:7b")

llm = LLM(
    model=OLLAMA_BASE_URL and OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.1,
)

# ── Embedder config (uses Ollama, no OpenAI needed) ───────────────────────────
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

embedder = {
    "provider": "ollama",
    "config": {
        "model": EMBED_MODEL,
        "base_url": OLLAMA_BASE_URL
    }
}

# ── Initialize tools ──────────────────────────────────────────────────────────
search_tool = SerperDevTool(api_key=SERPER_API_KEY)
scrape_tool = ScrapeWebsiteTool()

# ── Load skill files as knowledge sources ─────────────────────────────────────
# Files must be inside the knowledge/ folder (CrewAI requirement)
d_skill  = TextFileKnowledgeSource(file_paths=["skill_d.md"],         embedder=embedder)
ev_skill = TextFileKnowledgeSource(file_paths=["skill_evaluator.md"], embedder=embedder)
f_skill  = TextFileKnowledgeSource(file_paths=["skill_f.md"],         embedder=embedder)
v_skill  = TextFileKnowledgeSource(file_paths=["skill_v.md"],         embedder=embedder)

# ── Agents ────────────────────────────────────────────────────────────────────

desirability_agent = Agent(
    role="Desirability Evaluation Agent",
    goal="Determine whether the proposed solution addresses a genuine user need and whether sufficient market demand exists.",
    backstory="You are an expert market research analyst and user experience strategist.",
    llm=llm,
    tools=[search_tool, scrape_tool],
    knowledge_sources=[d_skill],
    verbose=True,
    max_iter=4
)

feasibility_agent = Agent(
    role="Feasibility Evaluation Agent",
    goal="Evaluate the technical buildability of a startup idea strictly from the Feasibility dimension of the DFV framework.",
    backstory="You are an expert technical architect, systems analyst, and execution strategist.",
    llm=llm,
    tools=[search_tool, scrape_tool],
    knowledge_sources=[f_skill],
    verbose=True,
    max_iter=4
)

viability_agent = Agent(
    role="Viability Evaluation Agent",
    goal="Determine whether the proposed solution can generate sustainable business value and long-term growth.",
    backstory="You are an expert startup strategist, business consultant, and commercialisation analyst.",
    llm=llm,
    tools=[search_tool, scrape_tool],
    knowledge_sources=[v_skill],
    verbose=True,
    max_iter=4
)

dfv_risk_decision_agent = Agent(
    role="Internal DFV Decision and Risk Assessment Engine",
    goal="Identify hidden risks across project dimensions and produce a final GO/NO-GO decision.",
    backstory="You are an expert venture risk analyst and product strategist.",
    knowledge_sources=[ev_skill],
    verbose=True,
    llm=llm
)

# ── Tasks — skills handle all structure and format ────────────────────────────

desirability_task = Task(
    description="Run a full desirability evaluation on this project: {project_json}",
    expected_output="A Desirability Analysis Report following your knowledge source guidelines.",
    agent=desirability_agent
)

feasibility_task = Task(
    description="Run a full feasibility evaluation on this project: {project_json}",
    expected_output="A Feasibility Analysis Report following your knowledge source guidelines.",
    agent=feasibility_agent
)

viability_task = Task(
    description="Run a full viability evaluation on this project: {project_json}",
    expected_output="A Viability Analysis Report following your knowledge source guidelines.",
    agent=viability_agent
)

dfv_decision_task = Task(
    description=(
        "Review the Desirability, Feasibility, and Viability reports from your context "
        "and produce a final DFV decision for this project: {project_json}"
    ),
    expected_output="A final GO/NO-GO decision report following your knowledge source guidelines.",
    context=[desirability_task, feasibility_task, viability_task],
    agent=dfv_risk_decision_agent
)

# ── Sample Input Datasets ─────────────────────────────────────────────────────

whatsapp_bot = {
    "project_profile": {
        "target_customer": "Undergraduate students at PES University who are at risk of low internal marks.",
        "proposed_solution_idea": "A WhatsApp-based automated bot that scrapes and sends morning deadline alerts from the university LMS."
    },
    "dfv_hypotheses": {
        "desirability_statement": "We believe target students care enough about losing internal marks that they will actively setup and configure a third-party WhatsApp bot rather than relying on peer chats.",
        "feasibility_statement": "We believe our engineering team can build a Python script to scrape the PES LMS and connect it to a WhatsApp wrapper within 2 weeks using open APIs.",
        "viability_statement": "We believe we can sustain this project by charging anxious parents a small monthly fee for academic risk alerts."
    },
    "identified_risk_signals": {
        "current_behavior_alternative": "Students currently rely on chaotic peer-to-peer WhatsApp groups and checking the LMS manually right before exams.",
        "biggest_user_friction_point": "Students suffer from massive notification fatigue. The biggest risk is that they will mute or ignore the bot out of habit within 3 days.",
        "user_anxiety_or_fear": "Students might fear that the bot will glitch, miss an assignment change, or get them into trouble for using an unofficial script."
    }
}

blnkt = {
    "project_profile": {
        "target_customer": "Millennials, Gen Z, busy professionals, and students in metro cities aged 18-40.",
        "proposed_solution_idea": "A 10-minute grocery and essentials delivery app using dark stores."
    },
    "dfv_hypotheses": {
        "desirability_statement": "Urban consumers need immediate access to groceries without traveling to stores and will pay a delivery fee for 10-minute fulfillment.",
        "feasibility_statement": "The platform can be built using React Native, cloud infrastructure, and route optimization with a dark store network within 6 months.",
        "viability_statement": "Revenue from delivery fees, seller commissions, brand advertising, and a Prime membership can make the business contribution-margin positive."
    },
    "identified_risk_signals": {
        "current_behavior_alternative": "Consumers currently visit nearby kirana stores or use standard 30-45 min delivery apps.",
        "biggest_user_friction_point": "High delivery cost sensitivity — users may switch back to kiranas for small orders.",
        "user_anxiety_or_fear": "Fear of wrong items delivered, out-of-stock situations, or delayed delivery breaking the 10-min promise."
    }
}

sncc = {
    "project_profile": {
        "target_customer": "Students, office workers, and urban consumers who want quick snacks and beverages.",
        "proposed_solution_idea": "SNACCED — a quick-service food delivery platform delivering snacks and light meals within 10-15 minutes."
    },
    "dfv_hypotheses": {
        "desirability_statement": "Consumers want faster snack delivery that existing full-meal platforms don't prioritize.",
        "feasibility_statement": "SNACCED can be built using existing delivery tech and dark stores stocked with snack-specific SKUs.",
        "viability_statement": "Revenue through delivery fees, markups, subscriptions, and brand partnerships can sustain the business."
    },
    "identified_risk_signals": {
        "current_behavior_alternative": "Users currently snack from office vending machines, canteens, or order from Swiggy/Zomato.",
        "biggest_user_friction_point": "Low average order value makes unit economics very tight per delivery.",
        "user_anxiety_or_fear": "Users fear stale products or the app not being worth it for a small snack order."
    }
}

qubi = {
    "project_profile": {
        "target_customer": "Busy mobile-first consumers wanting premium short-form video during commutes and breaks.",
        "proposed_solution_idea": "Quibi — a mobile streaming platform offering premium episodes under 10 minutes."
    },
    "dfv_hypotheses": {
        "desirability_statement": "Consumers will pay for premium short-form content they can watch during daily micro-moments.",
        "feasibility_statement": "A mobile streaming platform with Turnstyle (portrait/landscape switching) can be built with sufficient investment.",
        "viability_statement": "Subscription revenue combined with premium content exclusivity will drive retention and profitability."
    },
    "identified_risk_signals": {
        "current_behavior_alternative": "Users already consume free short-form content on YouTube, TikTok, and Instagram.",
        "biggest_user_friction_point": "No social sharing features limited organic growth and virality.",
        "user_anxiety_or_fear": "Users didn't see enough value over free alternatives to justify a paid subscription."
    }
}

ggls = {
    "project_profile": {
        "target_customer": "General consumers seeking hands-free augmented reality and instant information access.",
        "proposed_solution_idea": "Google Glass — a wearable AR heads-up display for navigation, photos, and notifications."
    },
    "dfv_hypotheses": {
        "desirability_statement": "Consumers will adopt hands-free AR wearables for everyday convenience and productivity.",
        "feasibility_statement": "The hardware can deliver a seamless AR experience despite battery, heat, and display constraints.",
        "viability_statement": "Premium pricing at $1,500 with an app ecosystem will drive sustainable revenue."
    },
    "identified_risk_signals": {
        "current_behavior_alternative": "Users rely on smartphones for navigation, photos, and notifications.",
        "biggest_user_friction_point": "Social discomfort and privacy concerns led to bans in public spaces.",
        "user_anxiety_or_fear": "Consumers feared being recorded without consent and saw the device as socially intrusive."
    }
}

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Switch between: whatsapp_bot | blnkt | sncc | qubi | ggls
    # Or pass your own dict in the same format
    selected_input = whatsapp_bot

    crew = Crew(
        agents=[desirability_agent, feasibility_agent, viability_agent, dfv_risk_decision_agent],
        tasks=[desirability_task, feasibility_task, viability_task, dfv_decision_task],
        process=Process.sequential,
        verbose=True,
        embedder=embedder
    )

    result = crew.kickoff(inputs={"project_json": json.dumps(selected_input, indent=2)})

    print("\n--- FINAL DFV ANALYSIS REPORT ---\n")
    print(result)
