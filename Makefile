# ==== ISP Billing (Sendi) — Makefile ====
# Host: bit78 · Port 793 (web) · DB: MariaDB :: FreeRADIUS :: MicroTik API

APP_NAME := jawara-billing
PYTHON := python3
VENV := .venv
PY := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip3

.PHONY: help setup venv install dev test migrate migrate-upgrade run clean

help: ## Show this help
	@echo "Available targets:"
	@grep -E '^[a-z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup: venv install-db ## Install venv + requirements

venv: ## Create virtualenv
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@echo "venv ready: $(PY)"

install: $(PIP) ## Install Python deps
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "deps installed"

install-db: ## Install MariaDB + FreeRADIUS (root)
	@if [ "$$(id -u)" -ne 0 ]; then echo "run: sudo make install-db"; exit 1; fi
	apt-get update
	apt-get install -y mariadb-server freeradius freeradius-mysql
	systemctl enable --now mariadb freeradius

dev: venv install ## Dev mode: watch reload
	$(PY) -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 793

run: venv install migrate ## Start production
	$(PY) -m gunicorn -w 2 -b 0.0.0.0:793 backend.app.main:app

migrate: ## Generate DB migration
	$(PY) -m alembic revision --autogenerate -m "auto migration"

migrate-upgrade: ## Run DB migration
	$(PY) -m alembic upgrade head

initdb: ## Create initial DB schema
	$(PY) scripts/init_db.py

wait-db: ## Wait for MariaDB
	$(PY) scripts/wait_db.py

clean: ## Remove venv, pycache, redis
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

license-check: ## Verify LICENSE header in each file
	@echo "check license headers (optional)"
