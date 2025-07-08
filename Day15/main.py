# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from typing import List
import requests
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Load embeddings and vector DB
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local("recipes_index", embedding, allow_dangerous_deserialization=True)
retriever = db.as_retriever()

# Request body for recommendation
class Query(BaseModel):
    ingredients: str

@app.post("/recommend")
async def recommend(query: Query):
    results = retriever.get_relevant_documents(query.ingredients, k=10)
    user_ingredients = set(map(str.strip, query.ingredients.lower().split(',')))
    filtered = []
    for r in results:
        recipe_ingredients = set(map(str.strip, r.metadata["ingredients"].lower().split(',')))
        if user_ingredients.issubset(recipe_ingredients):
            filtered.append({
                "recipe": r.metadata["name"],
                "ingredients": r.metadata["ingredients"],
                "instructions": r.metadata["instructions"]
            })
    return filtered[:3]  # Return top 3 valid matches

# Request body for calorie analysis
class NutritionInput(BaseModel):
    ingredients: List[str]  # List like ["1 cup rice", "2 eggs"]

@app.post("/calorie")
async def calorie_analysis(data: NutritionInput):
    url = "https://api.edamam.com/api/nutrition-details"
    headers = {"Content-Type": "application/json"}
    payload = {
        "title": "Recipe",
        "ingr": data.ingredients
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        params={
            "app_id": os.getenv("EDAMAM_APP_ID"),
            "app_key": os.getenv("EDAMAM_APP_KEY")
        }
    )

    # Check for non-200 response
    if response.status_code != 200:
        return {
            "error": response.json().get("message", "API Error"),
            "details": response.json()
        }

    result = response.json()
    
    
    return {
        "calories": result.get("calories"),
        "protein": result["totalNutrients"]["PROCNT"]["quantity"],
        "fat": result["totalNutrients"]["FAT"]["quantity"],
        "carbs": result["totalNutrients"]["CHOCDF"]["quantity"]
    }
    
