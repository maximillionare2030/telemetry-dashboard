from fastapi import APIRouter, HTTPException
from utils.analysis import Analysis
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Create router with prefix
router = APIRouter(
    prefix="/api/analysis",
    tags=["analysis"],
    responses={404: {"description": "Not found"}},
)

analyzer = Analysis()

@router.post("/analyze")  # Now just the endpoint part
async def analyze_telemetry(data: dict):
    logger.info("Accessing endpoint: /analyze")
    try:
        # convert data to dataframe
        df = pd.DataFrame(data['telemetry'])
        user_message = data.get('message', '')

        # analyze the data
        analysis = analyzer.analyze_telemetry(df)

        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
