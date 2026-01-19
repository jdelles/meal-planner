from meal_planner.grocery import categorize_ingredient, consolidate_grocery_list


def test_categorize_ingredient():
    """Test ingredient categorization"""
    categories = {
        "produce": ["onion", "garlic", "tomato"],
        "meat": ["chicken", "beef"],
        "dairy": ["milk", "cheese"],
        "other": []
    }
    
    assert categorize_ingredient("2 onions, diced", categories) == "produce"
    assert categorize_ingredient("1 lb chicken breast", categories) == "meat"
    assert categorize_ingredient("1 cup milk", categories) == "dairy"
    assert categorize_ingredient("random ingredient", categories) == "other"


def test_consolidate_grocery_list():
    """Test grocery list consolidation"""
    meals = [
        {
            "recipe_name": "Chicken Stir Fry",
            "ingredients": ["2 lbs chicken breast", "1 onion", "2 bell peppers"]
        },
        {
            "recipe_name": "Beef Tacos",
            "ingredients": ["1 lb ground beef", "1 onion", "1 cup cheese"]
        }
    ]
    
    grocery_list = consolidate_grocery_list(meals)
    
    # Should have categorized items
    assert "meat" in grocery_list
    assert "produce" in grocery_list
    assert "dairy" in grocery_list
    
    # Should consolidate duplicates (onion appears twice)
    produce_items = grocery_list["produce"]
    onion_count = sum(1 for item in produce_items if "onion" in item.lower())
    assert onion_count == 1  # Only one onion entry despite appearing in 2 meals


def test_consolidate_empty_meals():
    """Test with empty meal list"""
    grocery_list = consolidate_grocery_list([])
    assert grocery_list == {}