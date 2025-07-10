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

# Input model for recipe recommendation
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

# Input model for calorie analysis
class NutritionInput(BaseModel):
    ingredients: List[str]  # Example: ["1 cup rice", "2 eggs"]

@app.post("/calorie")
async def calorie_analysis(data: NutritionInput):
    url = "https://api.edamam.com/api/nutrition-details"
    headers = {"Content-Type": "application/json"}
    params = {
        "app_id": os.getenv("EDAMAM_APP_ID"),
        "app_key": os.getenv("EDAMAM_APP_KEY")
    }

    # Clean input
    cleaned_ingredients = [item.strip() for item in data.ingredients if item.strip()]
    if not cleaned_ingredients:
        return {"error": "Ingredient list is empty or improperly formatted."}

    payload = {
        "title": "Recipe Analysis",
        "ingr": cleaned_ingredients
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        result = response.json()

        if response.status_code != 200:
            return {
                "error": result.get("error", "API request failed."),
                "message": result.get("message", "Unknown issue from Edamam."),
                "status_code": response.status_code
            }

        # Safely extract nutritional info
        calories = result.get("calories", 0)
        protein = result.get("totalNutrients", {}).get("PROCNT", {}).get("quantity", 0)
        fat = result.get("totalNutrients", {}).get("FAT", {}).get("quantity", 0)
        carbs = result.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity", 0)

        return {
            "calories": round(calories, 2),
            "protein": round(protein, 2),
            "fat": round(fat, 2),
            "carbs": round(carbs, 2)
        }

    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}
