from crewai import Agent, Task
from crewai_tools import SerperDevTool , RagTool, ScrapeWebsiteTool, FirecrawlCrawlWebsiteTool
import os
from data_aggregator import aggregate_data_task
from metric_search import metric_analysis_task
from trace_search import trace_analysis_task


from dotenv import load_dotenv

load_dotenv()

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

web_searcher = Agent(
    role="Web Research and Analysis Specialist",
    goal="Analyze system issues, propose solutions, and suggest improvements based on web research",
    backstory="""You are an experienced SRE with a knack for problem-solving and a vast knowledge of web resources. 
    Your expertise lies in quickly finding relevant information online, analyzing it in the context of the given problem, 
    and proposing actionable solutions. You have a deep understanding of microservices architectures, 
    cloud technologies, and performance optimization techniques.""",
    verbose=True,
    allow_delegation=False,
    tools=[scrape_tool, search_tool],
    
)

web_search_task = Task(
    description="""
    Analyze the aggregate_data and analysis of the errors from metric and trace analysis. Please give importance on interprocess communication while answering. For every part of the output you should always refer and explain and relate to the error anlaysis or aggregate data. Provide good reasons. Your task is to:

    1. Identify and research the root causes of the reported issues.
    2. Propose detailed solutions for each identified problem. You should be spesific to the project.
    3. Suggest improvements to prevent similar issues in the future.
    4. Provide an in-depth analysis of the errors, particularly focusing on TimeoutErrors and DataBaseErrors.

    Use the search and scrape tools to gather information from relevant websites, including but not limited to 
    https://sre.google/sre-book/introduction/ and https://opentelemetry.io/docs/. 

    Your analysis should cover:
    - Detailed explanations of potential root causes
    - Step-by-step solutions for each issue
    - Recommendations for performance improvements
    - Insights into error handling and mitigation strategies

    Format your response as a structured report with clear sections for each aspect of your analysis.
    """,
    agent=web_searcher,
    expected_output="""
    A comprehensive report containing:
    1. Executive Summary
       - Overview of key issues identified, with emphasis on interprocess communication problems. Include timing details of the errors

    2. Root Cause Analysis:
       - Detailed breakdown of each identified issue
       - Research-backed explanations of potential causes

    3. Proposed Solutions:
       - Step-by-step solutions for each problem
       - Justification for each solution based on research

    4. Detailed Error Analysis:
       - In-depth look at TimeoutError
       - Strategies for error handling and prevention

    5. Performance Optimization Recommendations:
       - Specific suggestions for improving system performance
       - Tools or techniques discovered through research

    6. References:
       - List of sources used in the analysis
       - Any relevant code snippets or configuration examples found

    The report should be thorough, well-structured, and provide actionable insights based on the latest 
    industry standards and best practices.
    """,
    context=[aggregate_data_task, metric_analysis_task,trace_analysis_task],
    
)




