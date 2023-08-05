export PROJECTNAME=$(shell basename "$(PWD)")
export PYDIR=$(shell if [ -d "./venv" ]; then echo "./venv/bin/"; else echo ""; fi)


.SILENT: ;         # no need for @

setup: ## Setup virtual environment and install dependencies
	echo "Run the following commands to install required dependencies in a virtual environment"
	echo "> python3 -m venv venv"
	echo "> source venv/bin/activate"
	echo "> pip3 install -r requirements/dev.txt"
	echo "If the directory ./venv does not exist the system-wide python environment will be used\n"

b: ## Build package
	${PYDIR}python3 -m build

upload: ## Upload to pypi
	${PYDIR}python3 -m twine upload --repository pypi dist/*

deps: ## Reinstalls dependencies
	${PYDIR}python3 -m pip install -r requirements/dev.txt --upgrade

clean: ## Clean package and generated files (./build/*, ./dist/*, ./src/*.egg-info)
	rm -rf build/* dist/* src/*.egg-info

help: makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo
