import joblib
import os
import tldextract
import pandas as pd
import difflib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.feature_extraction import extract_features_from_url

app = FastAPI(title="Fischer Detector API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_PATH = "models/best_model.joblib"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

class URLRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    url: str
    prediction: str
    risk_score: float
    features: dict

# Comprehensive Whitelist of Trusted Brands
TRUSTED_BRANDS = {
    "google", "chatgpt", "openai", "facebook", "apple", "microsoft", "amazon", 
    "youtube", "instagram", "twitter", "linkedin", "netflix", "github", 
    "stackoverflow", "wikipedia", "yahoo", "bing", "reddit", "paypal", "chase", 
    "wellsfargo", "bankofamerica", "icloud", "ycombinator", "vercel", "netlify",
    "medium", "nytimes", "cnn", "bbc", "forbes", "bloomberg", "reuters", 
    "techcrunch", "wired", "theverge", "quora", "twitch", "discord", "spotify", 
    "adobe", "dropbox", "googleusercontent", "gstatic", "microsoftonline",
    "visualstudio", "azure", "aws", "cloudfront", "fastly", "cloudflare"
}

@app.get("/")
async def root():
    return {
        "message": "Fischer Detector Malicious URL Detection API is running.",
        "version": "1.1.0",
        "status": "active"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: URLRequest):
    try:
        url = request.url.lower().strip()
        print(f"Incoming request for URL: {url}")
        
        # 1. Normalize URL for extraction
        if not url.startswith(('http://', 'https://')):
            url_for_ext = 'http://' + url
        else:
            url_for_ext = url
            
        ext = tldextract.extract(url_for_ext)
        domain = ext.domain
        
        # 2. Whitelist Check
        if domain in TRUSTED_BRANDS:
            print(f"Whitelist match: {domain}")
            return PredictionResponse(
                url=request.url,
                prediction="Benign",
                risk_score=0.001,
                features={}
            )
            
        # 3. Typosquatting detection
        for brand in TRUSTED_BRANDS:
            similarity = difflib.SequenceMatcher(None, domain, brand).ratio()
            if 0.85 < similarity < 1.0:
                print(f"Potential typosquatting detected: {domain} similar to {brand}")
                features = extract_features_from_url(url_for_ext)
                return PredictionResponse(
                    url=request.url,
                    prediction="Malicious",
                    risk_score=0.99,
                    features={**features, "typosquatting_indicator": 1, "target_brand": brand}
                )

        # 4. AI Prediction
        features = extract_features_from_url(url_for_ext)
        features_df = pd.DataFrame([features])
        
        # Ensure column order matches training
        expected_columns = model.feature_names_in_
        features_df = features_df[expected_columns]
        
        prob = model.predict_proba(features_df)[0][1]
        
        # 5. Heuristic Adjustments
        # If very low complexity domain with no path and no digits, reduce risk
        if features['path_len'] == 0 and features['count_digits'] == 0 and features['count_suspicious'] == 0:
            prob = prob * 0.2
            
        prediction = "Malicious" if prob > 0.5 else "Benign"
        
        print(f"Result for {url}: {prediction} ({prob:.4f})")
        
        return PredictionResponse(
            url=request.url,
            prediction=prediction,
            risk_score=float(prob),
            features=features
        )
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
