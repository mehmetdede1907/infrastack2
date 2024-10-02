from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from crewai import Crew
from log_search import log_analysis_task, log_analyst
from metric_search import metric_analysis_task, metric_analyst
from trace_search import trace_analysis_task, trace_analyst
from sre_assistant import combined_analysis_task, sre_engineer
from data_aggregator import data_aggregator, aggregate_data_task
from search_error import web_search_task, web_searcher

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(
    metric_file: UploadFile = File(...),
    trace_file: UploadFile = File(...)
):
    # Ensure the data directory exists
    os.makedirs("datas", exist_ok=True)

    # Save metric file
    with open("datas/metric.json", "wb") as buffer:
        shutil.copyfileobj(metric_file.file, buffer)

    # Save trace file
    with open("datas/trace.json", "wb") as buffer:
        shutil.copyfileobj(trace_file.file, buffer)

    # Run the analysis
    result = run_analysis()

    return {"message": "Analysis completed", "result": result}

def run_analysis():
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
        f.write(str(result))

    # Save task outputs
    task_outputs = {}
    for task_output in result.tasks_output:
        filename = f"{task_output.task.name}.md"
        with open(filename, "w") as f:
            f.write(task_output.raw)
        task_outputs[filename] = task_output.raw

    return task_outputs

@app.get("/results")
async def get_results():
    results = {}
    for filename in ["aggregate_data.md", "metric_analysis.md", "trace_analysis.md", "web_searcher.md", "verbose_output.txt"]:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                results[filename] = f.read()
        else:
            results[filename] = "File not found"
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)