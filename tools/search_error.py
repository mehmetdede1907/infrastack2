from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool , RagTool, ScrapeWebsiteTool, FirecrawlCrawlWebsiteTool
import os
from data_aggregator import aggregate_data_task

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
    tools=[scrape_tool, search_tool]
)

web_search_task = Task(
    description="""
    Analyze the provided system overview and performance data. Your task is to:

    1. Identify and research the root causes of the reported issues.
    2. Propose detailed solutions for each identified problem.
    3. Suggest improvements to prevent similar issues in the future.
    4. Provide an in-depth analysis of the errors, particularly focusing on TimeoutError and DatabaseError.

    Use the search and scrape tools to gather information from relevant websites, including but not limited to 
    https://sre.google/sre-book/introduction/. Pay special attention to best practices in SRE, 
    microservices architecture, and performance optimization.

    Your analysis should cover:
    - Detailed explanations of potential root causes
    - Step-by-step solutions for each issue
    - Best practices for preventing similar problems
    - Recommendations for performance improvements
    - Insights into error handling and mitigation strategies

    Format your response as a structured report with clear sections for each aspect of your analysis.
    """,
    agent=web_searcher,
    expected_output="""
    A comprehensive report containing:

    1. Root Cause Analysis:
       - Detailed breakdown of each identified issue
       - Research-backed explanations of potential causes

    2. Proposed Solutions:
       - Step-by-step solutions for each problem
       - Justification for each solution based on research

    3. Improvement Suggestions:
       - Long-term strategies to prevent similar issues
       - Best practices for system reliability and performance

    4. Detailed Error Analysis:
       - In-depth look at TimeoutError and DatabaseError
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
    context=[aggregate_data_task]
)




