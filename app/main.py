from fastapi import FastAPI, HTTPException
from app.schema import Transaction
from app.inference import fraud_model
from app.logger import logger
from app.utils import generate_request_id

app = FastAPI(title="Fraud Detection API")

@app.on_event("startup")
def load_model():
    logger.info("Loading model...")
    fraud_model.load_model()

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict")
def predict(transaction: Transaction):
    request_id = generate_request_id()

    try:
        logger.info(f"[{request_id}] Incoming request")

        result = fraud_model.predict(transaction.features)

        logger.info(f"[{request_id}] Prediction: {result}")

        return {
            "request_id": request_id,
            "result": result
        }

    except ValueError as ve:
        logger.warning(f"[{request_id}] Validation Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.error(f"[{request_id}] Internal Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/explain")
def explain():
    return {
        "message": "SHAP explainability endpoint coming in next step"
    }