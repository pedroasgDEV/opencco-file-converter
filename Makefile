# Definindo as variáveis
VENV_NAME = .xml_convert
REQUIREMENTS = ./requirements.txt
SRC = ./__main__.py
DIST_DIR = ./dist
BUILD_DIR = ./build
SPEC_FILE = opencco-file-converter.spec
EXEC_NAME = opencco-file-converter

# Comando para criar o ambiente virtual
create-venv:
	@echo "Criando ambiente virtual em '$(VENV_NAME)'..."
	python3 -m venv $(VENV_NAME)
	@echo "Ambiente virtual criado com sucesso."

# Comando para instalar as dependências
install-deps: create-venv
	@echo "Instalando dependências do projeto..."
	$(VENV_NAME)/bin/pip install -r $(REQUIREMENTS)
	@echo "Dependências instaladas com sucesso."

# Comando para limpar arquivos temporários do PyInstaller
clean:
	@echo "Limpando arquivos temporários..."
	rm -rf $(DIST_DIR) $(BUILD_DIR) $(SPEC_FILE)
	@echo "Arquivos temporários limpos."

# Comando para empacotar o projeto com PyInstaller
build: install-deps
	@echo "Criando o executável com PyInstaller..."
	$(VENV_NAME)/bin/pyinstaller --onefile --name $(EXEC_NAME) --add-data "models:models" --add-data "utils:utils" $(SRC)
	@echo "Executável criado com sucesso."

# Comando principal: executar todas as etapas de uma vez (limpar, instalar, build)
all: clean build
	@echo "Tudo pronto! O executável está em '$(DIST_DIR)/$(EXEC_NAME)'"
	mv $(DIST_DIR)/$(EXEC_NAME) .
	rm -rf $(DIST_DIR) $(BUILD_DIR) $(SPEC_FILE)

# Redefine o comando padrão para 'make all'
.DEFAULT_GOAL := all
