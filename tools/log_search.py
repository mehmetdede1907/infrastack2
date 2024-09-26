from crewai_tools import JSONSearchTool
from crewai_tools import BaseTool
from crewai import Task, Agent, Crew



log_search_tool = JSONSearchTool(json_path="data/log.json")
log_analyst = Agent(
    role="Log Analyst",
    goal="Collect, organize, and provide initial analysis of relevant logs for error investigation",
    backstory="Experienced in identifying patterns and crucial information in log data for effective troubleshooting",
    verbose=True,
    allow_delegation=False
)

log_analysis_task = Task(
    description="""
    1. Collect and Organize Relevant OpenTelemetry Log Data:
       a. Gather Error Logs:
          - Collect all log entries with severity: "ERROR" related to the affected services.
          - Include logs from a time window before and after the error occurred to provide context.
       b. Include Relevant Info Logs:
          - Gather informational logs (severity: "INFO") that may be related to the error. 
            For example, logs showing system status changes, user actions, or service interactions.
    
    2. Perform Initial Analysis:
       a. Identify the most frequent error types or messages.
       b. Note any patterns in the timing or sequence of errors.
       c. Highlight any correlation between INFO logs and subsequent ERRORs.
    
    Use the log_search_tool to query and analyze this data from the logs.
    """,
    expected_output="""
    A report containing:
    1. A chronological list of ERROR logs with their timestamps, error messages, and related service information.
    2. A list of relevant INFO logs that provide context around the errors.
    3. A summary of findings, including:
       - The time range of the analyzed logs
       - The main services involved in the errors
       - The most common error types or messages
       - Any notable patterns or correlations observed in the log data
    4. At least two specific log entry examples that illustrate key findings.
    
    This report should be concise but informative enough to guide further investigation by other agents.
    """,
    agent=log_analyst,
    tools=[log_search_tool]
)
