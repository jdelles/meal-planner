import click
import json
from pathlib import Path
from langchain_ollama import ChatOllama
from meal_planner.prompts import create_meal_plan_prompt
from meal_planner.grocery import consolidate_grocery_list
from meal_planner.preferences import load_preferences, save_preferences

PREFERENCES_FILE = Path("preferences.json")

@click.group()
def cli():
    """Meal Planner - Generate weekly meal plans and grocery lists"""
    pass

@cli.command()
def plan():
    """Generate a new meal plan"""
    
    # Load saved preferences or get new ones
    prefs = load_preferences(PREFERENCES_FILE)
    
    click.echo("\n🍳 Let's plan your meals for the week!\n")
    
    # Collect preferences (use saved as defaults)
    family_size = click.prompt(
        "Family size", 
        default=prefs.get("family_size", 4),
        type=int
    )
    
    ages = click.prompt(
        "Ages of kids (comma-separated, or 'none')",
        default=prefs.get("ages", "5,8")
    )
    
    dietary_restrictions = click.prompt(
        "Dietary restrictions (or 'none')",
        default=prefs.get("dietary_restrictions", "none")
    )
    
    max_cook_time = click.prompt(
        "Max cooking time (minutes)",
        default=prefs.get("max_cook_time", 45),
        type=int
    )
    
    skill_level = click.prompt(
        "Cooking skill level",
        type=click.Choice(["beginner", "intermediate", "advanced"]),
        default=prefs.get("skill_level", "intermediate")
    )
    
    days = click.prompt(
        "Days to plan for",
        default=prefs.get("days", 7),
        type=int
    )
    
    # Save preferences for next time
    new_prefs = {
        "family_size": family_size,
        "ages": ages,
        "dietary_restrictions": dietary_restrictions,
        "max_cook_time": max_cook_time,
        "skill_level": skill_level,
        "days": days
    }
    save_preferences(PREFERENCES_FILE, new_prefs)
    
    click.echo("\n🤖 Generating your meal plan...\n")
    
    # Initialize LLM
    llm = ChatOllama(model="qwen2.5:7b", temperature=0.7)
    
    # Create prompt
    prompt = create_meal_plan_prompt(
        family_size=family_size,
        ages=ages,
        dietary_restrictions=dietary_restrictions,
        max_cook_time=max_cook_time,
        skill_level=skill_level,
        days=days
    )
    
    # Generate meal plan
    response = llm.invoke(prompt)
    
    try:
        # Parse the JSON response
        content = response.content if isinstance(response.content, str) else str(response.content)
        meal_plan = json.loads(content)
        
        # Display meal plan
        click.echo("📅 Your Weekly Meal Plan:\n")
        for i, meal in enumerate(meal_plan["meals"], 1):
            click.echo(f"Day {i}: {meal['recipe_name']} ({meal['cook_time']} min)")
        
        # Generate grocery list
        click.echo("\n🛒 Generating grocery list...\n")
        grocery_list = consolidate_grocery_list(meal_plan["meals"])
        
        # Display grocery list
        click.echo("Grocery List:")
        for category, items in grocery_list.items():
            click.echo(f"\n{category.upper()}:")
            for item in items:
                click.echo(f"  - {item}")
        
        # Save to files
        with open("meal_plan.json", "w") as f:
            json.dump(meal_plan, f, indent=2)
        
        with open("grocery_list.json", "w") as f:
            json.dump(grocery_list, f, indent=2)
        
        click.echo("\n✅ Saved meal_plan.json and grocery_list.json")
        
    except json.JSONDecodeError:
        click.echo("❌ Error parsing meal plan. Raw response:")
        content = response.content if isinstance(response.content, str) else str(response.content)
        click.echo(content)

@cli.command()
def show():
    """Show the current meal plan"""
    try:
        with open("meal_plan.json", "r") as f:
            meal_plan = json.load(f)
        
        click.echo("\n📅 Current Meal Plan:\n")
        for i, meal in enumerate(meal_plan["meals"], 1):
            click.echo(f"\nDay {i}: {meal['recipe_name']}")
            click.echo(f"Cook time: {meal['cook_time']} min")
            click.echo(f"\nIngredients:")
            for ing in meal['ingredients']:
                click.echo(f"  - {ing}")
            click.echo(f"\nInstructions:")
            for j, step in enumerate(meal['instructions'], 1):
                click.echo(f"  {j}. {step}")
    except FileNotFoundError:
        click.echo("❌ No meal plan found. Run 'meal-planner plan' first.")

@cli.command()
def grocery():
    """Show the grocery list"""
    try:
        with open("grocery_list.json", "r") as f:
            grocery_list = json.load(f)
        
        click.echo("\n🛒 Grocery List:\n")
        for category, items in grocery_list.items():
            click.echo(f"\n{category.upper()}:")
            for item in items:
                click.echo(f"  - {item}")
    except FileNotFoundError:
        click.echo("❌ No grocery list found. Run 'meal-planner plan' first.")

if __name__ == "__main__":
    cli()