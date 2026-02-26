# -------- Variables --------
PYTHON = python3
PIP = pip3
PYTEST = pytest
PROJECT_NAME = swag-labs-automation
ARGS ?= 
MARKERS ?= 

# -------- Default --------
.PHONY: help
help:
	@echo "Available commands:"
	@echo " make install        Install dependencies"
	@echo " make test           Run all tests"
	@echo " make smoke          Run smoke tests"
	@echo " make regression     Run regression suite"
	@echo " make inventory      Run inventory tests"
	@echo " make cart           Run cart tests"
	@echo " make checkout       Run checkout tests"
	@echo " make order          Run order tests"
	@echo " make filters        Run filter tests"
	@echo " make cookies        Run cookie tests"
	@echo " make negative       Run negative tests"
	@echo " make slow           Run slow tests"
	@echo " make clean          Remove cache files"
	@echo " make lint           Run flake8"
	@echo " make format         Format with black"
	@echo " make run" MARKERS="<marker>" ARGS="extra arguments                   For running Generalized"

# -------- Setup --------
.PHONY: install
install:
	$(PIP) install -r requirements.txt
	playwright install

# -------- Run Tests --------
.PHONY: test
test:
	$(PYTEST) -v $(ARGS)

.PHONY: smoke
smoke:
	$(PYTEST) -m smoke -v $(ARGS)

.PHONY: regression
regression:
	$(PYTEST) -m regression -v $(ARGS)

.PHONY: inventory
inventory:
	$(PYTEST) -m inventory -v $(ARGS)

.PHONY: cart
cart:
	$(PYTEST) -m cart -v $(ARGS)

.PHONY: checkout
checkout:
	$(PYTEST) -m checkout -v $(ARGS)

.PHONY: order
order:
	$(PYTEST) -m order -v $(ARGS)

.PHONY: filters
filters:
	$(PYTEST) -m filters -v $(ARGS)

.PHONY: cookies
cookies:
	$(PYTEST) -m cookies -v $(ARGS)

.PHONY: negative
negative:
	$(PYTEST) -m negative -v $(ARGS)

.PHONY: slow
slow:
	$(PYTEST) -m slow -v $(ARGS)


#-----------General------------
.PHONY: run
run: 
	$(PYTEST) -m "$(MARKERS)" -v $(ARGS)

# -------- Clean --------
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "test-results" -exec rm -r {} +