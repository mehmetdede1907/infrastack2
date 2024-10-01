from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from crewai import Crew
from log_search import log_analysis_task, log_analyst
from metric_search import metric_analysis_task, metric_analyst
from trace_search import trace_analysis_task, trace_analyst
from sre_assistant import combined_analysis_task, sre_engineer
from data_aggregator import data_aggregator, aggregate_data_task
from search_error import web_search_task, web_searcher
import asyncio
import os

app = FastAPI()

class AnalysisRequest(BaseModel):
    log_data: str
    metric_data: str
    trace_data: str

@app.post("/analyze")
async def analyze(request: AnalysisRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_analysis, request)
    return {"message": "Analysis started"}

async def run_analysis(request: AnalysisRequest):
    # Create the SRE Assistant crew
    sre_crew = Crew(
        agents=[trace_analyst, metric_analyst, data_aggregator, web_searcher],
        tasks=[trace_analysis_task, metric_analysis_task, aggregate_data_task, web_search_task],
        verbose=True,
        memory=True
    )

    # Run the crew
    result = sre_crew.kickoff()

    # Save verbose output
    with open("verbose_output.txt", "w") as f:
        f.write(result)

@app.get("/results")
async def get_results():
    results = {}
    for filename in ["aggregate_data.json", "metric_analysis.md", "trace_analysis.md", "web_searcher.md", "verbose_output.txt"]:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                results[filename] = f.read()
        else:
            results[filename] = "File not found"
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)