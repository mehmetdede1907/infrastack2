from crewai import Task, Agent
from log_search import log_analysis_task,log_analyst
from metric_search import metric_analysis_task,metric_analyst
from trace_search import trace_analysis_task,trace_analyst

# Define the SRE Engineer agent
sre_engineer = Agent(
    role="SRE Engineer",
    goal="Synthesize findings from log, metric, and trace analysis to identify root causes and propose solutions",
    backstory="Senior SRE with expertise in complex system analysis and problem-solving",
    verbose=True,
    allow_delegation=False
)

# Define the Combined Analysis task
combined_analysis_task = Task(
    description="""
    Synthesize the findings from the log, metric, and trace analyses to:
    1. Identify correlations between log events, metric anomalies, and trace bottlenecks
    2. Determine the root causes of the observed errors and performance issues
    3. Propose solutions to address the identified problems
    4. Suggest improvements to prevent similar issues in the future

    Use the outputs from the log_analysis_task, metric_analysis_task, and trace_analysis_task as input for this analysis.
    """,
    expected_output="""
    A comprehensive report containing:
    1. Summary of key findings from log, metric, and trace analyses
    2. Identified correlations between different data sources
    3. Root cause analysis for the observed errors and performance issues
    4. Proposed solutions to address the identified problems
    5. Recommendations for system improvements and monitoring enhancements
    """,
    context=[metric_analysis_task,trace_analysis_task],

    agent=sre_engineer
)