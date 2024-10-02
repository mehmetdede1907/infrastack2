from crewai import Task, Agent,Crew
from crewai_tools import JSONSearchTool

import os

from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create the JSON search tool for metrics
metric_search_tool = JSONSearchTool(json_path="kaan_data/metrics.json")

# Define the Metric Analyst agent
metric_analyst = Agent(
    role="Metric Analyst",
    goal="Analyze system metrics to identify performance issues related to timeouts and errors",
    backstory="Expert in system performance metrics with a focus on identifying anomalies and trends",
    verbose=True,
    allow_delegation=False
)

# Define the Metric Analysis task
metric_analysis_task = Task(
    description="""
    Analyze the system metrics using metric_search tool identify errors focusing on:
    1. CPU and memory usage patterns
    2. Request duration metrics
    3. Error count metrics
    4. Any other relevant performance indicators

    Use the metric_search_tool to query and analyze the metric data. Provide me detailed anlaysis report.
    """,
    expected_output="""
    A report containing:
    1. Key performance metrics around the time of reported errors
    2. Any significant spikes or anomalies in system performance
    3. Correlation between metrics and known error events
    4. Potential performance bottlenecks identified from the metrics
    """,
    output_file= "metric_analysis.md",
    agent=metric_analyst,
    async_execution=True, #for running same time with other anaysis
    tools=[metric_search_tool]
)

log_test_crew = Crew(
    agents=[metric_analyst],
    tasks=[metric_analysis_task],
    verbose=True,
    memory=True

)


