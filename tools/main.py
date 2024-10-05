from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from crewai import Crew
from tools.metric_search import metric_analysis_task, metric_analyst
from tools.trace_search import trace_analysis_task, trace_analyst
from tools.data_aggregator import data_aggregator, aggregate_data_task
from tools.search_error import web_search_task, web_searcher

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL
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

    # Create the SRE Assistant crew
    sre_crew = Crew(
        agents=[trace_analyst, metric_analyst, data_aggregator, web_searcher],
        tasks=[trace_analysis_task, metric_analysis_task, aggregate_data_task, web_search_task],
        verbose=True,
        memory=True
    )

    # Run the crew
    sre_crew.kickoff()

    return {"message": "Analysis completed"}

@app.get("/results")
async def get_results():
    results = {}
    for filename in ["aggregatedata.json", "metric_analysis.md", "trace_analysis.md", "web_search.md"]:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                results[filename] = f.read()
        else:
            results[filename] = "File not found"
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)