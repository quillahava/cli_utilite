# Activate the virtual environment
shell:
	poetry install
	poetry shell

# Install cli_utilite into virtual environment
install: 
	python setup.py build
	python setup.py install

# Clean up build artifacts
clear:
	rm -rf build

# Uninstall the utility (remove it from the system)
uninstall:
	pip uninstall altbrains
