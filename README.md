# Meal Planner

A CLI tool that uses local AI to generate weekly meal plans and grocery lists for busy families.

## Why This Exists

Juggling family schedules, getting kids to sports practice, and still finding time to make healthy home-cooked meals is hard. This tool helps by:

- Generating realistic weekly meal plans tailored to your family
- Creating consolidated grocery lists to minimize shopping time
- Reusing ingredients across meals to reduce waste
- Remembering your preferences so you don't have to answer the same questions every week

## Features

- 🤖 **Local AI** - Uses Ollama with Qwen 2.5 (runs entirely on your laptop, no API costs)
- 🍳 **Smart meal planning** - Generates kid-friendly meals with overlapping ingredients
- 🛒 **Auto grocery lists** - Consolidates ingredients and categorizes them
- 💾 **Saves preferences** - Remembers your family size, dietary restrictions, etc.
- ⚡ **Fast** - Generates a full week's plan in ~30 seconds

## Prerequisites

- macOS (M-series chip recommended for best performance)
- [Homebrew](https://brew.sh/)
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager (handles Python installation automatically)

## Installation

### 1. Install uv and Ollama

```bash
brew install uv ollama
ollama pull qwen2.5:7b
```

### 2. Install the meal planner

```bash
git clone https://github.com/yourusername/meal-planner.git
cd meal-planner
make install
```

## Usage

### Generate a meal plan

```bash
meal-planner plan
```

You'll be prompted for:
- Family size
- Ages of kids
- Dietary restrictions
- Max cooking time
- Skill level
- Days to plan for

The tool saves your answers and uses them as defaults next time.

### View your current meal plan

```bash
meal-planner show
```

Shows the full meal plan with recipes and instructions.

### View your grocery list

```bash
meal-planner grocery
```

Shows the consolidated grocery list organized by category (produce, meat, dairy, etc.).

### Or use Make commands

```bash
make run       # Generate new meal plan
make show      # Show current plan
make grocery   # Show grocery list
```

## How It Works

1. **Collects preferences** - Asks about your family (or loads saved preferences)
2. **Generates meal plan** - Uses a local LLM to create recipes that:
   - Reuse ingredients across meals
   - Match your time constraints and skill level
   - Provide generous portions for your family size
3. **Creates grocery list** - Consolidates all ingredients and removes duplicates
4. **Saves everything** - Outputs `meal_plan.json` and `grocery_list.json`

## Development

### Run linter and formatter

```bash
make format    # Auto-format code
make lint      # Check for issues
make check     # Run both (used in CI)
```

### Run tests

```bash
make test
```

### Clean up generated files

```bash
make clean
```

## Project Structure

```
meal-planner/
├── src/
│   └── meal_planner/
│       ├── meal_planner.py   # Main CLI
│       ├── prompts.py        # LLM prompts
│       ├── grocery.py        # Grocery list logic
│       └── preferences.py    # Preference management
├── tests/
│   └── test_grocery.py       # Tests
├── Makefile                  # Dev commands
├── pyproject.toml            # Project config
└── README.md
```

## Output Files

- `meal_plan.json` - Full meal plan with recipes
- `grocery_list.json` - Consolidated grocery list
- `preferences.json` - Your saved preferences

These files are gitignored so they don't get committed.

## Tips

- **First run takes longer** - Ollama needs to load the model into memory (~5-10 seconds)
- **Subsequent runs are faster** - The model stays loaded for 5 minutes
- **Adjust the prompts** - Edit `src/meal_planner/prompts.py` to tweak recipe generation
- **Model management** - Check loaded models with `ollama ps`

## Troubleshooting

### "Connection refused" error

Make sure Ollama is running:
```bash
ollama serve
```

Or start it as a service:
```bash
brew services start ollama
```

### Meals have unrealistic portions

The LLM is still learning! You can:
1. Regenerate with `meal-planner plan`
2. Edit the prompt in `src/meal_planner/prompts.py` to be more specific
3. Manually adjust the output JSON files

### Want different recipes

Just run `meal-planner plan` again - it generates fresh recipes each time.

## Future Ideas

- [ ] Ingredient quantity consolidation (e.g., "3 onions" instead of listing separately)
- [ ] Leftover tracking across weeks
- [ ] Recipe rating/feedback to improve suggestions
- [ ] Export to shopping apps (Instacart, etc.)
- [ ] Nutrition information
- [ ] Recipe swapping (regenerate just one day)

## License

MIT

## Contributing

This is a personal project, but PRs welcome! Run `make check` and `make test` before submitting.

---

Built with ❤️ for busy families trying to juggle it all.