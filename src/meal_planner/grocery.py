from collections import defaultdict
import re

def consolidate_grocery_list(meals: list) -> dict:
    """
    Consolidate ingredients from multiple meals into a categorized grocery list.
    
    This is a simple version - just groups by basic categories.
    Could be enhanced with quantity consolidation later.
    """
    
    # Basic categorization (can be improved)
    categories = {
        "produce": ["onion", "garlic", "tomato", "pepper", "lettuce", "carrot", 
                   "celery", "potato", "broccoli", "spinach", "bell pepper",
                   "mushroom", "zucchini", "lemon", "lime", "apple", "banana"],
        "meat": ["chicken", "beef", "pork", "turkey", "fish", "salmon", "shrimp",
                "ground beef", "steak", "sausage"],
        "dairy": ["milk", "cheese", "butter", "yogurt", "cream", "sour cream",
                 "eggs"],
        "pantry": ["rice", "pasta", "flour", "sugar", "bread", "tortilla",
                  "beans", "stock", "broth", "sauce", "oil"],
        "frozen": ["frozen"],
        "other": []
    }
    
    grocery_list = defaultdict(list)
    
    # Collect all ingredients
    for meal in meals:
        for ingredient in meal.get("ingredients", []):
            # Categorize ingredient
            category = categorize_ingredient(ingredient, categories)
            grocery_list[category].append(ingredient)
    
    # Remove duplicates while preserving order
    for category in grocery_list:
        grocery_list[category] = list(dict.fromkeys(grocery_list[category]))
    
    return dict(grocery_list)

def categorize_ingredient(ingredient: str, categories: dict) -> str:
    """Categorize an ingredient based on keywords"""
    ingredient_lower = ingredient.lower()
    
    for category, keywords in categories.items():
        if category == "other":
            continue
        for keyword in keywords:
            if keyword in ingredient_lower:
                return category
    
    return "other"