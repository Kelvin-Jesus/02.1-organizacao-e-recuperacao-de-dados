import os

TAMANHO_REGISTRO: int = 64
CABECALHO_QUANTIDADE_DE_ITENS_NO_ARQUIVO: int = 4
SOBRA_DE_ESPACO: str = '\0'


def centralizaTexto(texto: str) -> str:
    larguraDoTerminal: int = os.get_terminal_size().columns

    return texto.center(larguraDoTerminal)

def printaOpcoes():
    print(centralizaTexto('PROGRAMA PARA INSERÇÃO E ATUALIZAÇÃO DE REGISTROS\n'))
    print('Suas opcoes sao:')
    print((' '*5)+'1. Inserir um novo Registro')
    print((' '*5)+'2. Buscar um registro por RRN para alteracoes')
    print((' '*5)+'3. Terminar o Programa\n')


def main():
    # nomeDoArquivo: str = input('Digite o nome do arquivo a ser aberto:')
    nomeDoArquivo: str = 'fixo1.bin'

    if os.path.isfile(nomeDoArquivo) is False:
        arquivo = open(nomeDoArquivo, 'w+b')
        TOTAL_REGISTROS: int = 0
        arquivo.write(TOTAL_REGISTROS.to_bytes(4))

    try:
        arquivo = open(nomeDoArquivo, 'r+b')
        arquivo.read(1)
    except:
        print(erro)

    printaOpcoes()

    escolha: int = int(input('Digite o número de sua escolha: '))
    
    

if __name__ == '__main__':
    main()
