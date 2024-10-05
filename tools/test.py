# from crewai import Crew
# from tools.log_search import log_analysis_task,log_analyst
# from tools.metric_search import metric_analysis_task,metric_analyst
# from tools.trace_search import trace_analysis_task,trace_analyst
# from tools.sre_assistant import combined_analysis_task,sre_engineer
# from tools.data_aggregator import data_aggregator,aggregate_data_task
# from tools.search_error import web_search_task,web_searcher

# # Create the SRE Assistant crew
# sre_crew = Crew(
#     agents=[ trace_analyst,metric_analyst, data_aggregator,web_searcher],
#     tasks=[  trace_analysis_task,metric_analysis_task, aggregate_data_task,web_search_task],
#     verbose=True,
#     memory= True
# )

# # Run the crew
# result = sre_crew.kickoff()
