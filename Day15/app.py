# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Recipe Recommender", page_icon="🥘")
st.title("🥘 Recipe Recommendation ChatBot")

# Input section
ingredients = st.text_input("Enter your available ingredients (comma-separated):")
meal_type = st.selectbox("Select Meal Type (Optional)", ["Any", "Breakfast", "Lunch", "Dinner", "Snack"])

# Helper to format steps nicely
def format_steps(instruction_text):
    steps = instruction_text.split('. ')
    return [step.strip() for step in steps if step.strip()]

# Recipe Recommendation Section
if st.button("Recommend"):
    with st.spinner("Finding delicious recipes for you..."):
        try:
            res = requests.post(
                "http://127.0.0.1:8000/recommend",
                json={"ingredients": ingredients}
            )
            data = res.json()

            if data:
                for recipe in data:
                    st.subheader(f"🍽 {recipe['recipe']}")
                    st.markdown(f"**🧂 Ingredients:** {recipe['ingredients']}")

                    st.markdown("**📖 Instructions:**")
                    steps = format_steps(recipe["instructions"])
                    for i, step in enumerate(steps, 1):
                        st.markdown(f"**Step {i}:** {step}")
            else:
                st.warning("❗ No matching recipes found.")
        except Exception as e:
            st.error(f"⚠️ Error fetching recipes: {e}")

# Divider for feature 6
st.divider()
st.subheader("🧮 Calorie & Nutrition Analysis")

# Input for calorie analysis
calorie_ingredients = st.text_area("Enter ingredients (one per line):", height=150)

if st.button("Analyze Calories"):
    lines = [line.strip() for line in calorie_ingredients.split('\n') if line.strip()]
    if lines:
        with st.spinner("Analyzing nutrition..."):
            try:
                res = requests.post("http://127.0.0.1:8000/calorie", json={"ingredients": lines})
                if res.status_code == 200:
                    result = res.json()
                    st.success("✅ Calorie Analysis")
                    st.write(f"**Total Calories**: {result['calories']:.2f} kcal")
                    st.write(f"**Protein**: {result['protein']:.2f} g")
                    st.write(f"**Fat**: {result['fat']:.2f} g")
                    st.write(f"**Carbohydrates**: {result['carbs']:.2f} g")
                else:
                    st.warning("❗ Could not analyze the given ingredients.")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter at least one ingredient.")
