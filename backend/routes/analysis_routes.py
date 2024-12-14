from fastapi import APIRouter, HTTPException
from utils.analysis import Analysis
import pandas as pd

# create router
router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)

# create analyzer object
analyzer = Analysis()

# define endpoints for analysis
@router.post("/analyze")
async def analyze_telemetry(data: dict):
    try:
        # convert data to dataframe
        df = pd.DataFrame(data['telemetry'])

        # analyze the data
        analysis = analyzer.analyze_telemetry(df)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
