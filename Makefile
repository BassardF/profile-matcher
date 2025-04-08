# Profile Matcher Makefile
# Variables
VENV_NAME := venv
PYTHON := python3
FLASK_APP := app.app
PORT := 5000
PLAYER_ID := 97983be2-98b7-11e7-90cf-082e5f28d836

# Check if we're in the virtual environment
ifeq ($(shell which python | grep -c $(VENV_NAME)), 0)
    IN_VENV = false
else
    IN_VENV = true
endif

# Create virtual environment
venv:
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Virtual environment created. Activate it with 'make activate'"

# Activate virtual environment (this will print instructions since make runs in a separate shell)
activate:
	@echo "To activate the virtual environment, run:"
	@echo "source $(VENV_NAME)/bin/activate"

# Install dependencies
install: 
	@if [ "$(IN_VENV)" = "false" ]; then \
		echo "Please activate the virtual environment first with 'source $(VENV_NAME)/bin/activate'"; \
		exit 1; \
	fi
	pip install -r requirements.txt
	@echo "Dependencies installed successfully"

# Initialize the database
init-db:
	@if [ "$(IN_VENV)" = "false" ]; then \
		echo "Please activate the virtual environment first with 'source $(VENV_NAME)/bin/activate'"; \
		exit 1; \
	fi
	$(PYTHON) init_db.py
	@echo "Database initialized successfully"

# Run the Flask server
run:
	@if [ "$(IN_VENV)" = "false" ]; then \
		echo "Please activate the virtual environment first with 'source $(VENV_NAME)/bin/activate'"; \
		exit 1; \
	fi
	FLASK_APP=$(FLASK_APP) FLASK_DEBUG=1 flask run --port=$(PORT)

# Test the healthcheck endpoint
test-health:
	curl -X GET http://127.0.0.1:$(PORT)/

# Test the get_client_config endpoint with the sample player ID
test-config:
	curl -X GET http://127.0.0.1:$(PORT)/get_client_config/$(PLAYER_ID)

# Setup everything (create venv, install deps, init db)
setup: venv
	@echo "Run the following commands to complete setup:"
	@echo "source $(VENV_NAME)/bin/activate"
	@echo "make install"
	@echo "make init-db"

# Help command
help:
	@echo "Available commands:"
	@echo "  make venv         - Create a virtual environment"
	@echo "  make activate     - Show instructions to activate the virtual environment"
	@echo "  make install      - Install dependencies (run after activating venv)"
	@echo "  make init-db      - Initialize the database with sample data"
	@echo "  make run-server   - Start the Flask server"
	@echo "  make test-health  - Test the healthcheck endpoint"
	@echo "  make test-config  - Test the get_client_config endpoint with sample player ID"
	@echo "  make setup        - Setup everything (will provide instructions for next steps)"
	@echo "  make help         - Show this help message"

.PHONY: venv activate install init-db run-server test-health test-config setup help
