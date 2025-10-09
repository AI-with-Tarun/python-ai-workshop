from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb

from dotenv import load_dotenv
load_dotenv()

customer_agent = Agent(
    name="Customer Agent",
    role="You are an expert Customer Service AI Assistant specialized in resolving customer queries with empathy and accuracy.",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Always use web search to find the most accurate and up-to-date answers before responding.",
        "Never redirect the user to external platforms; summarize and provide the relevant information directly.",
        "Keep your responses concise, polite, and solution-oriented."
    ],
)

marketer_agent = Agent(
    name="Marketer Agent",
    role="You are an expert Marketing & SEO AI Assistant skilled in crafting marketing strategies, content ideas, and social media optimization plans.",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[TavilyTools()],
    instructions=[
        "Whenever a strategy, marketing, or SEO-related question is asked, perform an in-depth web search to support your analysis with data or trends.",
        "Focus on providing a detailed, insight-driven response backed by real examples or social proof.",
        "Keep your tone professional, persuasive, and focused on business growth outcomes."
    ],
)

worker = Team(
    name="Main orchestrator",
    members=[marketer_agent,customer_agent],
    model=Gemini(id="gemini-2.5-flash"),
    instructions=[
        "You are a service based router that directs questions to the appropriate team i.e., Customer or Marketer",
        "If a query involves marketing, product promotion, or social media strategy, route it to the 'Marketer Agent'.",
        "If a query involves customer support, product troubleshooting, or service assistance, route it to the 'Customer Agent'.",
    ],
    show_members_responses=True,
    db=SqliteDb(db_file="tmp/test.db"), 
    add_history_to_context=True, 
    markdown=True,
)

from agno.os import AgentOS # needs fastapi,uvicorn

agent_os = AgentOS(
    id = "Router-Agent",
    description="route queries to the appropriate team",
    agents=[marketer_agent,customer_agent],
    teams=[worker],
)

app = agent_os.get_app() # fastapi
if __name__ == "__main__":
    agent_os.serve(app="multiagentcode:app", reload=True)