# Activate the virtual environment
shell:
	poetry install
	poetry shell

# Install cli_utilite into virtual environment
install: 
	python3 setup.py install


# Uninstall the utility (remove it from the system)
uninstall:
	pip uninstall altbrains
