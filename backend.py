from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import re
from fastapi.middleware.cors import CORSMiddleware
# Configure the Generative AI model
genai.configure(api_key="AIzaSyDrs22GsHU78vtwMdyfrxkrhnaODcB_eXg")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize the FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Pydantic model for input validation
class IngredientsRequest(BaseModel):
    ingredients: str
    cuisine:str
    meal_type:str

# Helper function to clean the AI-generated response
def clean_response(response: str) -> str:
    response = re.sub(r"\*\*|\*|_", "", response)  # Remove '**', '*', and '_'
    response = re.sub(r"\s{2,}", " ", response)    # Collapse multiple spaces
    response = response.strip()                   # Remove leading/trailing spaces
    return response

@app.post("/generate-recipe")
async def generate_recipe(request: IngredientsRequest):
    try:
        # Generate the recipe based on the provided ingredients
        prompt = f"Give me a good {request.cuisine} {request.meal_type} recipe based on these ingredients: {request.ingredients}"
        data = model.generate_content(prompt)
        raw_response = data.text

        # Clean the response
        cleaned_response = clean_response(raw_response)

        return {"recipe": cleaned_response}
    except Exception as e:
        # Handle any errors during the process
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")
