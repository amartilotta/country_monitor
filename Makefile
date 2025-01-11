# Build configuration
# -------------------

APP_NAME := `sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
APP_VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
GIT_REVISION = `git rev-parse HEAD`
VENV = .venv

# Introspection targets
# ---------------------

.PHONY: help
help: header targets

.PHONY: header
header:
	@echo "\033[34mEnvironment\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@printf "\033[33m%-23s\033[0m" "APP_NAME"
	@printf "\033[35m%s\033[0m" $(APP_NAME)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "APP_VERSION"
	@printf "\033[35m%s\033[0m" $(APP_VERSION)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "GIT_REVISION"
	@printf "\033[35m%s\033[0m" $(GIT_REVISION)
	@echo "\n"

.PHONY: targets
targets:
	@echo "\033[34mDevelopment Targets\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'


# Project targets
# -------------

.PHONY: fresh-install
fresh-install: ## ENV - Fresh install of the environment
	@echo "⚠️  Este comando eliminará el entorno actual y lo reinstalará."
	@echo "⚠️  Antes de continuar asegurate de salir de tu entorno actual con 'deactivate'"
	@read -p "Do you want to continue? [y/N] " REPLY; \
	case $$REPLY in \
	[Yy]*) ;; \
	*) echo "Aborting"; exit 1 ;; \
	esac
	sudo rm -rf $(VENV)
	make clean-cache
	sh scripts/environment.sh
	poetry env use 3.11
	make reinstall-package

.PHONY: clean-cache
clean-cache: ## Cleanup - Remove __pycache__, *_cache and *.pyc files
	sudo find . -type d -name "__pycache__" -exec sudo rm -rf {} + 
	sudo find . -type d -name "*_cache" -exec sudo rm -rf {} + 
	sudo find . -type f -name "*.pyc" -exec sudo rm -f {} + 
	@echo "✅ Cache cleanup completed!"

.PHONY: reinstall-package
reinstall-package: ## ENV - Update the package
	poetry install
	make build
	make restart


# Docker targets
# -------------

.PHONY: build
build: ## Docker - build the server
	docker compose build $(APP_NAME)

.PHONY: start
start: ## Docker - Starts the server
	docker compose up -d
	docker logs --tail 1000 -f $(APP_NAME)

.PHONY: restart
restart: ## Docker - Stops the server
	docker compose down $(APP_NAME) --remove-orphans
	docker compose up -d $(APP_NAME)
	docker logs --tail 1000 -f $(APP_NAME)

.PHONY: shell-docker
shell-docker: health-container ## Docker - container shell
	docker exec -it $(APP_NAME) sh

.PHONY: logs
logs: health-container ## Docker - logs container 
	docker logs --tail 1000 -f $(APP_NAME)

.PHONY: attach
attach: health-container ## Docker - attach container 
	docker logs --tail 50 $(APP_NAME) && docker attach --detach-keys="ctrl-c" $(APP_NAME)

.PHONY: health-container
health-container: ## Docker - check health of the container
	@if [ "$(shell docker inspect -f '{{.State.Running}}' $(APP_NAME))" != "true" ]; then \
		echo "\n ❌  Container  $(APP_NAME) is not running \n"; exit 1; \
	fi

# Quality targets
# ------------------------------

.PHONY: format
format: ## Quality - Format the code
	poetry run black src

.PHONY: linter
linter: ## Quality - Run the linter
	poetry run ruff check --fix src

.PHONY: shell
shell: health-container ## Run python shell in the container
	docker exec -it $(APP_NAME) python manage.py shell
