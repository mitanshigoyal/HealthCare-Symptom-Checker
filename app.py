from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI(title="Healthcare Symptom Checker (Educational Only)")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Models ----------
class SymptomRequest(BaseModel):
    symptoms: str

class SymptomResponse(BaseModel):
    symptoms: str
    probable_conditions: str
    recommendations: str
    disclaimer: str

# ---------- Route ----------
@app.post("/api/symptom-check", response_model=SymptomResponse)
def symptom_check(req: SymptomRequest):
    text = req.symptoms.strip()

    if not text or len(text) < 3:
        raise HTTPException(status_code=400, detail="Please enter valid symptoms.")

    prompt = f"""
You are a healthcare assistant for educational purposes only.

Given the following symptoms: "{text}"

1. Suggest the most probable conditions (common to rare).
2. Give short, clear recommendations or next steps.
3. Always include an educational disclaimer saying this is not a substitute for professional medical advice.
4. Keep it concise, readable, and safe.
"""

    try:
        # Try real LLM call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        result = response.choices[0].message.content.strip()

    except Exception as e:
        # ✅ Fallback for quota or network errors
        print("⚠️ LLM call failed, using fallback response instead.")
        result = (
            "Possible conditions:\n"
            "- Common Cold or Flu\n"
            "- COVID-19 infection\n"
            "- Seasonal allergies\n\n"
            "Recommendations:\n"
            "- Stay hydrated and get enough rest\n"
            "- Take paracetamol for fever (if not allergic)\n"
            "- Consult a doctor if symptoms worsen or last >3 days\n\n"
            "Disclaimer: This output is AI-generated for educational purposes only, "
            "not a substitute for professional medical advice."
        )

    disclaimer = (
        "⚠️ This tool is for educational purposes only and not a substitute for professional medical advice. "
        "If you experience severe or worsening symptoms, seek immediate medical care."
    )

    return SymptomResponse(
        symptoms=text,
        probable_conditions=result,
        recommendations="Refer to the above response for suggested steps.",
        disclaimer=disclaimer
    )

@app.get("/")
def home():
    return {"message": "Healthcare Symptom Checker API running successfully."}
