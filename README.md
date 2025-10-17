🩺 Healthcare Symptom Checker

An AI-powered symptom checker that suggests possible conditions + next steps based on user input.
Built with FastAPI + OpenAI GPT 💡

⚠️ Educational use only — not medical advice.

🚀 Features

✅ Enter your symptoms
✅ Get AI-generated probable conditions
✅ Simple web UI (HTML + JS)
✅ Auto-fallback if API quota runs out

⚙️ Run it locally
pip install fastapi uvicorn openai
$env:OPENAI_API_KEY="sk-your-key"
uvicorn app:app --reload


Open index.html in browser or via Live Server 🔥

🧠 Example
Input: Fever and cough for 3 days
→ Common Cold / Flu
→ Rest, fluids, consult doctor if it worsens

💬 Disclaimer

This project is for educational purposes only and should not replace professional medical consultation 🩹