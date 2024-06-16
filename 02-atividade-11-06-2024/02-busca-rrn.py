TAMANHO_REGISTRO: int = 64
CABECALHO_QUANTIDADE_DE_ITENS_NO_ARQUIVO: int = 4
SOBRA_DE_ESPACO: str = '\0'

def main():
    try:
        nomeDoArquivo = input('Digite o nome do arquivo a ser aberto: ')
        arquivo = open(nomeDoArquivo, 'rb')

        cabecalho = arquivo.read(CABECALHO_QUANTIDADE_DE_ITENS_NO_ARQUIVO)
        TOTAL_REGISTRO: int = int.from_bytes(cabecalho)

        numeroRelativoDoRegistro = int(input('Digite o RRN: '))

        if numeroRelativoDoRegistro >= TOTAL_REGISTRO:
            raise ValueError('RRN inválido! Cabou o programa')
        
        offsetDeLeitura: int = numeroRelativoDoRegistro * TAMANHO_REGISTRO + CABECALHO_QUANTIDADE_DE_ITENS_NO_ARQUIVO
        
        arquivo.seek(offsetDeLeitura)
        
        registro:str = arquivo.read(64).decode()

        camposDoRegistro = registro.split('|')
        
        contador: int = 0
        for campo in camposDoRegistro:
            if campo.startswith(SOBRA_DE_ESPACO):
                continue

            print(f'Campo {contador}: {campo}')
            contador += 1

        arquivo.close()

    except Exception as erro:
        print('Erro no arquivo')
        print(erro)

if __name__ == '__main__':
    main()
