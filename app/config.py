import os

class Settings:
    MODEL_THRESHOLD: float = float(os.getenv("MODEL_THRESHOLD", 0.5))

settings = Settings()