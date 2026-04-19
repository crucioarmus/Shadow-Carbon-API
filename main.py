from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Shadow Carbon API")

app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

# -----------------------------
# 📊 Data Models (Input Schema)
# -----------------------------
class Transaction(BaseModel):
    amount: float
    category: str
    country: str = "PK"   # optional default


# -----------------------------
# 📈 Emission Factors Dataset
# -----------------------------
factors = {
    "fuel": 0.009,
    "groceries": 0.002,
    "transport": 0.007,
    "utilities": 0.005
}

# -----------------------------
# 🌍 GHG Scope Mapping
# -----------------------------
scope_map = {
    "fuel": "Scope 3",
    "groceries": "Scope 3",
    "transport": "Scope 3",
    "utilities": "Scope 2"
}

# -----------------------------
# 📜 ESG (CSRD) Mapping
# -----------------------------
framework_map = {
    "Scope 1": "CSRD - Direct Emissions",
    "Scope 2": "CSRD - Energy Emissions",
    "Scope 3": "CSRD - Financed / Indirect Emissions"
}

# -----------------------------
# 🏠 Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "Shadow Carbon API is running"}

# -----------------------------
# ⚡ Core Endpoint
# -----------------------------
@app.post("/estimate-carbon")
def estimate(transaction: Transaction):
    
    # Extract input
    amount = transaction.amount
    category = transaction.category.lower()

    # Step 1: Get emission factor
    factor = factors.get(category, 0.005)

    # Step 2: Calculate carbon
    carbon = amount * factor

    # Step 3: Map scope
    scope = scope_map.get(category, "Scope 3")

    # Step 4: Map ESG framework
    reporting_category = framework_map.get(scope)

    # Step 5: Return response
    return {
        "estimated_carbon_kg": round(carbon, 2),
        "category": category,
        "scope": scope,
        "framework": "CSRD",
        "reporting_category": reporting_category,
        "confidence": "low (proxy-based estimate)",
        "esg_ready": True
    }