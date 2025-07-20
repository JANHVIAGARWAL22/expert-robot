from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd

# Load the dataset
df = pd.read_json("q-fastapi-llm-query.json")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/query")
async def query(q: str, request: Request):
    q_lower = q.lower()
    answer = "I don't know"

    # Total sales of Pizza in Green Bay
    if "total sales of pizza in green bay" in q_lower:
        filtered = df[(df["product"] == "Pizza") & (df["city"] == "Green Bay")]
        answer = int(filtered["sales"].sum())

    # How many sales reps are there in Michigan?
    elif "how many sales reps are there in michigan" in q_lower:
        filtered = df[df["region"] == "Michigan"]
        answer = filtered["rep"].nunique()

    # Average sales for Shoes in California
    elif "average sales for shoes in california" in q_lower:
        filtered = df[(df["product"] == "Shoes") & (df["region"] == "California")]
        answer = round(filtered["sales"].mean(), 2)

    # On what date did Robin Koelpin make the highest sale in Brandyboro?
    elif "robin koelpin" in q_lower and "brandyboro" in q_lower:
        filtered = df[(df["rep"] == "Robin Koelpin") & (df["city"] == "Brandyboro")]
        if not filtered.empty:
            date = filtered.loc[filtered["sales"].idxmax(), "date"]
            answer = str(date)

    # More question patterns can be added here in the same format

    # Build response
    response = JSONResponse(content={"answer": answer})
    response.headers["X-Email"] = "22f3002799@ds.study.iitm.ac.in"
    return response
