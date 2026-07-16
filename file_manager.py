import os

PASTA_SCRIPTS = "scripts"

def inicializar_pasta():
    """Garante que a pasta de scripts exista"""
    if not os.path.exists(PASTA_SCRIPTS):
        os.makedirs(PASTA_SCRIPTS)

def listar_scripts():
    """Retorna uma lista com os nomes dos arquivos .txt salvos"""
    inicializar_pasta()
    return [f for f in os.listdir(PASTA_SCRIPTS) if f.endswith('.txt')]

def salvar_script(nome_arquivo, conteudo):
    """Salva o texto dentro de um arquivo .txt na pasta de scripts"""
    inicializar_pasta()
    if not nome_arquivo.endswith(".txt"):
        nome_arquivo += ".txt"
    
    caminho = os.path.join(PASTA_SCRIPTS, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

def ler_script(nome_arquivo):
    """Lê o conteúdo de um script específico"""
    caminho = os.path.join(PASTA_SCRIPTS, nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()
