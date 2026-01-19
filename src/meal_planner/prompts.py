def create_meal_plan_prompt(
    family_size: int,
    ages: str,
    dietary_restrictions: str,
    max_cook_time: int,
    skill_level: str,
    days: int
) -> str:
    """Create a prompt for generating a meal plan"""
    
    return f"""You are a practical meal planner for busy families.

Family Details:
- Family size: {family_size} people
- Ages of kids: {ages}
- Dietary restrictions: {dietary_restrictions}
- Maximum cooking time: {max_cook_time} minutes (total prep + cook)
- Cooking skill level: {skill_level}
- Days to plan for: {days}

Generate {days} dinner recipes that:
1. Use overlapping ingredients across meals to minimize waste and shopping
2. Are kid-friendly but not boring (real food, not just chicken nuggets)
3. Have simple, clear instructions appropriate for {skill_level} level
4. Include realistic portion sizes for {family_size} people
5. Can be prepared in {max_cook_time} minutes or less
6. Consider common pantry staples (assume basics like oil, salt, pepper, common spices)

Return ONLY valid JSON in this exact format (no markdown, no explanation):
{{
  "meals": [
    {{
      "recipe_name": "Name of dish",
      "cook_time": 30,
      "servings": {family_size},
      "ingredients": [
        "2 lbs chicken breast",
        "1 cup rice",
        "2 bell peppers, diced"
      ],
      "instructions": [
        "Step 1 description",
        "Step 2 description"
      ]
    }}
  ]
}}

Important: 
- Be specific with quantities (don't say "chicken", say "2 lbs chicken breast")
- Try to reuse ingredients across different meals
- Make instructions clear and concise
- Return ONLY the JSON, nothing else"""