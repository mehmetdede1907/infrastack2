from crewai import Task, Agent
from crewai_tools import JSONSearchTool
import os

from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create the JSON search tool for traces
trace_search_tool = JSONSearchTool(json_path="kaan_data/traces.json")

# Define the Trace Analyst agent
trace_analyst = Agent(
    role="Trace Analyst",
    goal="Analyze distributed traces to identify bottlenecks and errors in request flows",
    backstory="Expert in distributed systems and request tracing, specializing in performance optimization",
    verbose=True,
    allow_delegation=False
)

# Define the Trace Analysis task
trace_analysis_task = Task(
    description="""
    Analyze the distributed traces to identify bottlenecks and errors in request flows, focusing on:
    1. Give more importance on traces related to the error events.
    2. Service dependencies and their impact on request flow
    3. Timing of different spans within traces
    4. Any anomalies or unexpected behavior in the request flow

    Use the trace_search_tool to query and analyze the trace data.
    Provide me report anyway.
    """,
    expected_output="""
    A report containing:
    1. Analysis of traces related to known error events
    2. Identification of slow spans or services in the request flow
    3. Any anomalies or unexpected behavior observed in the traces
    4. Potential bottlenecks or points of failure in the system based on trace analysis
    """,
    output_file="trace_analysis.md",
    agent=trace_analyst,
    async_execution=True, #for running same time with other anaysis
    tools=[trace_search_tool]
)