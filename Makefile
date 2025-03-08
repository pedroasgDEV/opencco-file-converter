VENV_NAME = .xml_convert
REQUIREMENTS = ./requirements.txt
SRC = ./__main__.py
DIST_DIR = ./dist
BUILD_DIR = ./build
SPEC_FILE = opencco-file-converter.spec
EXEC_NAME = opencco-file-converter

create-venv:
	@echo "Creating virtual environment in '$(VENV_NAME)'..."
	python3 -m venv $(VENV_NAME)
	@echo "Virtual environment created successfully."

install-deps: create-venv
	@echo "Installing project dependencies..."
	$(VENV_NAME)/bin/pip install -r $(REQUIREMENTS)
	@echo "Dependencies installed successfully."

clean:
	@echo "Cleaning up temporary files..."
	mv $(DIST_DIR)/$(EXEC_NAME) .
	rm -rf $(DIST_DIR) $(BUILD_DIR) $(SPEC_FILE) $(VENV_NAME)
	@echo "Cleaned temporary files."

build: install-deps
	@echo "Creating the executable with PyInstaller..."
	$(VENV_NAME)/bin/pyinstaller --onefile --name $(EXEC_NAME) --add-data "models:models" --add-data "utils:utils" $(SRC)
	@echo "Executable '$(EXEC_NAME)' created successfully."

all: build clean
	@echo "'./$(EXEC_NAME) --help' to help"

.DEFAULT_GOAL := all
