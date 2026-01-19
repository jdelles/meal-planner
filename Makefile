.PHONY: help install lint format check test run clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync
	uv pip install -e .

lint: ## Run linter (ruff)
	uv run ruff check .

format: ## Format code with ruff
	uv run ruff format .

check: ## Run linter and formatter check
	uv run ruff check .
	uv run ruff format --check .

test: ## Run tests
	uv run pytest -v

run: ## Run the meal planner
	uv run meal-planner plan

show: ## Show current meal plan
	uv run meal-planner show

grocery: ## Show grocery list
	uv run meal-planner grocery

clean: ## Clean up generated files
	rm -f meal_plan.json grocery_list.json preferences.json
	rm -rf __pycache__ .pytest_cache .ruff_cache
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete