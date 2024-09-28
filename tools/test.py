from crewai import Crew
from log_search import log_analysis_task,log_analyst
from metric_search import metric_analysis_task,metric_analyst
from trace_search import trace_analysis_task,trace_analyst
from sre_assistant import combined_analysis_task,sre_engineer

# Create the SRE Assistant crew
sre_crew = Crew(
    agents=[ metric_analyst, trace_analyst, sre_engineer],
    tasks=[ metric_analysis_task, trace_analysis_task, combined_analysis_task],
    verbose=True
)

# Run the crew
result = sre_crew.kickoff()
