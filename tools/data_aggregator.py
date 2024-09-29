
from crewai import Task, Agent, Crew
from log_search import log_analysis_task
from metric_search import metric_analysis_task
from trace_search import trace_analysis_task
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class AggregateData(BaseModel):
    SystemOverview: str
    KeyPerformanceMetrics: str
    CriticalErrors: str
    PerformanceAnomalies:str
    ServiceAnalysis: str
    TraceHighlights:str
    CorrelatedEvents: str
    PotentialRootCauses: str
    RecommendedActions: str
    QueryTerms:str


data_aggregator = Agent(
    role='Data Aggregator and Synthesis Specialist',
    goal='Compile, structure, and synthesize data from log, metric, and trace analyses into a comprehensive and actionable report',
    backstory="""You are an expert data scientist with a specialization in system performance analysis and a deep understanding of microservices architectures. With years of experience in SRE practices, you have a knack for identifying patterns and correlations across diverse data sets. Your ability to distill complex technical information into clear, actionable insights has made you a go-to resource for troubleshooting critical system issues.""",
    verbose=True,
)

# Define the Data Aggregation Task
aggregate_data_task = Task(
    description="""
    Analyze and synthesize the provided metric analysis and trace analysis reports into a consolidated, structured report. Your task involves:

    1. Extracting key performance indicators, error events, and anomalies from both reports.
    2. Correlating data points across metrics and traces to identify potential causal relationships.
    3. Correlating the interprocess comminication between services and errors. This is important
    4. Summarizing the most critical issues affecting system performance and reliability.
    5. Structuring the information in a format that facilitates easy querying and analysis by other agents.
    6. Highlighting potential areas for further investigation or immediate action.

    Use your expertise to interpret the data and provide context where necessary. The output should be comprehensive yet concise, enabling efficient use by the Web Search Agent and Retrieval Agent.
    """,
    agent=data_aggregator,
    expected_output="""
    A structured JSON report containing:

    1. "SystemOverview": A high-level summary of the system's current state.
    2. "KeyPerformanceMetrics": Aggregated metrics with timestamps, services, and values.
    3. "CriticalErrors": List of major errors with details (type, service, timestamp, message).
    4. "PerformanceAnomalies": Identified spikes or unusual patterns in system behavior.
    5. "ServiceAnalysis": Per-service breakdown of issues and performance metrics.
    6. "TraceHighlights": Key findings from trace analysis, including slow spans and bottlenecks.
    7. "CorrelatedEvents": Identified relationships between metrics, traces, and errors.
    8. "PotentialRootCauses": Initial hypotheses about the causes of observed issues.
    9. "RecommendedActions": Prioritized list of suggested next steps for investigation or mitigation.
    10. "QueryTerms": A list of key terms, error messages, and concepts for use in web searches and document retrieval.

    Each section should be detailed enough to provide clear context but concise enough to facilitate quick analysis by subsequent agents. Include relevant timestamps, service names, and quantitative data where applicable.
    """,
    context= [metric_analysis_task,trace_analysis_task],
    #    context= [log_analysis_task, metric_analysis_task, trace_analysis_task]
    output_json=AggregateData,
    output_file= "aggregatedata.json"

)