import os
from enum import Enum

TAMANHO_REGISTRO: int = 64
TAMANHO_CABECALHO: int = 4
SOBRA_DE_ESPACO = b'\0'

class OPCAO(Enum):
    INSERIR: int = 1
    BUSCAR: int = 2
    SAIR: int = 3

    @classmethod
    def temOValor(cls, valor: int):
        return valor in cls._value2member_map_

def centralizaTexto(texto: str) -> str:
    larguraDoTerminal: int = os.get_terminal_size().columns

    return texto.center(larguraDoTerminal)

def printaOpcoes():
    ESPACO_VAZIO = (' '*5)
    print(centralizaTexto('PROGRAMA PARA INSERÇÃO E ATUALIZAÇÃO DE REGISTROS\n'))
    print('Suas opções são:')
    print(ESPACO_VAZIO + '1. Inserir um novo Registro')
    print(ESPACO_VAZIO + '2. Buscar um registro por RRN para alterações')
    print(ESPACO_VAZIO + '3. Terminar o Programa\n')

def escolhaOpcao() -> int:
    escolha: int = int(input('Digite o número de sua escolha: '))
    if OPCAO.temOValor(escolha) is False:
        print('Escolha inválida!')
        escolhaOpcao()

    return escolha

def calculaOffset(totalRegistrosOuRRN: int) -> int:
    return totalRegistrosOuRRN * TAMANHO_REGISTRO + TAMANHO_CABECALHO 

def leiaRegistro(arquivo) -> str:
    registro = arquivo.read(TAMANHO_REGISTRO)
    return registro.encode()

def mostraRegistro(registro: str):
    campos = registro.split('|')

    for campo in campos:
        if campo.startswith(SOBRA_DE_ESPACO.decode()):
            continue

        print((' '*5)+campo)

def novoRegistro():
    print('\nDigite os dados para o registro')

    registro = ''
    registro += input('Sobrenome: ') + '|'
    registro += input('Nome: ') + '|'
    registro += input('Endereço: ') + '|'
    registro += input('Cidade: ') + '|'
    registro += input('Estado: ') + '|'
    registro += input('CEP: ') + '|'

    registro = registro.encode().ljust(TAMANHO_REGISTRO, SOBRA_DE_ESPACO)

    return registro

def querAlterarRegistro() -> bool:
    print('Você quer alterar este registro?')
    querAlterar = input('Responda S ou N, seguido de <ENTER> => ')

    querAlterarRegistro = True if querAlterar.upper() == 'S' else False

    return querAlterarRegistro


def main():
    nomeDoArquivo = input('Digite o nome do arquivo a ser aberto: ')
    TOTAL_REGISTROS: int = 0

    if os.path.isfile(nomeDoArquivo) is False:
        arquivo = open(nomeDoArquivo, 'w+b')
        arquivo.write(TOTAL_REGISTROS.to_bytes(TAMANHO_CABECALHO))

    try:
        arquivo = open(nomeDoArquivo, 'r+b')
        registrosEmBytes = arquivo.read(TAMANHO_CABECALHO)
        TOTAL_REGISTROS = int.from_bytes(registrosEmBytes) 

        printaOpcoes()

        escolha: int = escolhaOpcao()    
        while escolha != OPCAO.SAIR.value:
     
            if escolha == OPCAO.INSERIR.value:
                registro = novoRegistro()
                offsetDeGravacao: int = calculaOffset(TOTAL_REGISTROS)

                arquivo.seek(offsetDeGravacao) 
                arquivo.write(registro)

                TOTAL_REGISTROS += 1

            if escolha == OPCAO.BUSCAR.value:
                numeroRelativoDoRegistro: int = int(input('Digite o RRN: '))
                if numeroRelativoDoRegistro >= TOTAL_REGISTROS:
                    raise ValueError('RRN inválido!')

                offsetDeLeitura: int = calculaOffset(numeroRelativoDoRegistro)
                arquivo.seek(offsetDeLeitura)
                registro = leiaRegistro(arquivo)

                mostraRegistro(registro)
                alterar: bool = querAlterarRegistro()

                if alterar is False:
                    continue

                registro = novoRegistro()

                arquivo.seek(offsetDeLeitura)
                arquivo.write(registro)

            printaOpcoes()
            escolha = escolhaOpcao()

        arquivo.seek(0)
        arquivo.write(TOTAL_REGISTROS.to_bytes(TAMANHO_CABECALHO))
        arquivo.close()

    except Exception as erro:
        print(f'\n{erro}')


if __name__ == '__main__':
    main()
