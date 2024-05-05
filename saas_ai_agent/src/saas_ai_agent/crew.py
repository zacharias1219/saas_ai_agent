from saas_ai_agent.tools.custom_tool import SaasDataTool, TechnologyTool, FinancialTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from agentops.agent import track_agent
import agentops
import os

agentops.init()

@CrewBase
class SaaSCrew:
    """SaaSCrew crew for analyzing and developing a SaaS product from market research to launch strategy."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        # Groq
        self.groq_llm = ChatGroq(
            temperature=0,
            groq_api_key=os.environ.get("GROQ_API_KEY"),
            model_name="llama3-70b-8192",
        )

        # OpenAI
        self.ollama_llm = ChatOpenAI(
            model="mistral",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            temperature=0,
        )

    @track_agent(name="market_analyst")
    @agent
    def market_analyst(self) -> Agent:
        """Agent responsible for analyzing market trends and customer needs."""
        return Agent(
            config=self.agents_config["market_analyst"],
            #tools=[SaasDataTool()],
            allow_delegation=False,
            llm=self.groq_llm,
            verbose=True,
        )

    @track_agent(name="technology_architect")
    @agent
    def technology_architect(self) -> Agent:
        """Agent responsible for selecting the appropriate technology stack."""
        return Agent(
            config=self.agents_config["technology_architect"],
            #tools=[TechnologyTool()],
            allow_delegation=False,
            llm=self.groq_llm,
            verbose=True,
        )

    @track_agent(name="ux_designer")
    @agent
    def ux_designer(self) -> Agent:
        """Agent responsible for designing the user interface."""
        return Agent(
            config=self.agents_config["ux_designer"],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @track_agent(name="compliance_officer")
    @agent
    def compliance_officer(self) -> Agent:
        """Agent responsible for ensuring product compliance."""
        return Agent(
            config=self.agents_config["compliance_officer"],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @track_agent(name="financial_analyst")
    @agent
    def financial_analyst(self) -> Agent:
        """Agent responsible for financial planning and analysis."""
        return Agent(
            config=self.agents_config["financial_analyst"],
            #tools=[FinancialTool()],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @track_agent(name="agile_coach")
    @agent
    def agile_coach(self) -> Agent:
        """Agent responsible for implementing agile methodologies."""
        return Agent(
            config=self.agents_config["agile_coach"],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @track_agent(name="customer_support_manager")
    @agent
    def customer_support_manager(self) -> Agent:
        """Agent responsible for setting up and managing customer support."""
        return Agent(
            config=self.agents_config["customer_support_manager"],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @track_agent(name="marketing_strategist")
    @agent
    def marketing_strategist(self) -> Agent:
        """Agent responsible for developing and executing marketing strategies."""
        return Agent(
            config=self.agents_config["marketing_strategist"],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @task
    def perform_market_analysis_task(self) -> Task:
        """Task to perform market analysis."""
        return Task(
            config=self.tasks_config["market_research_task"],
            agent=self.market_analyst(),
            output_file="market_analysis.md",
        )

    @task
    def select_technology_task(self) -> Task:
        """Task to select the appropriate technology stack."""
        return Task(
            config=self.tasks_config["technology_selection_task"],
            agent=self.technology_architect(),
            output_file="technology_selection.md",
        )

    @task
    def design_ui_task(self) -> Task:
        """Task to design the user interface."""
        return Task(
            config=self.tasks_config["ux_design_task"],
            agent=self.ux_designer(),
            output_file="ui_design.md",
        )

    @task
    def ensure_compliance_task(self) -> Task:
        """Task to ensure compliance with regulations."""
        return Task(
            config=self.tasks_config["compliance_audit_task"],
            agent=self.compliance_officer(),
            output_file="compliance_report.md",
        )

    @task
    def conduct_financial_analysis_task(self) -> Task:
        """Task to conduct financial analysis."""
        return Task(
            config=self.tasks_config["financial_modeling_task"],
            agent=self.financial_analyst(),
            output_file="financial_analysis.md",
        )

    @task
    def implement_agile_task(self) -> Task:
        """Task to implement agile methodologies."""
        return Task(
            config=self.tasks_config["agile_implementation_task"],
            agent=self.agile_coach(),
            output_file="agile_implementation.md",
        )

    @task
    def setup_customer_support_task(self) -> Task:
        """Task to set up customer support systems."""
        return Task(
            config=self.tasks_config["customer_support_setup_task"],
            agent=self.customer_support_manager(),
            output_file="customer_support_setup.md",
        )

    @task
    def develop_marketing_strategy_task(self) -> Task:
        """Task to develop and execute marketing strategies."""
        return Task(
            config=self.tasks_config["marketing_campaign_task"],
            agent=self.marketing_strategist(),
            output_file="marketing_strategy.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SaaSCrew crew"""
        return Crew(
            agents=[
                self.market_analyst(),
                self.technology_architect(),
                self.ux_designer(),
                self.compliance_officer(),
                self.financial_analyst(),
                self.agile_coach(),
                self.customer_support_manager(),
                self.marketing_strategist(),
            ],
            tasks=[
                self.perform_market_analysis_task(),
                self.select_technology_task(),
                self.design_ui_task(),
                self.ensure_compliance_task(),
                self.conduct_financial_analysis_task(),
                self.implement_agile_task(),
                self.setup_customer_support_task(),
                self.develop_marketing_strategy_task(),
            ],
            process=Process.sequential,
            memory=False,
            max_rpm=2,
            verbose=2,
        )
