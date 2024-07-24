from dataclasses import dataclass
from enum import Enum
import sys
import os
import io
from argparse import ArgumentParser, Namespace
from typing import List, Tuple

@dataclass
class Jogo:
    id: int
    titulo: str
    ano: int
    genero: str
    produtora: str
    plataforma: str

@dataclass
class OPERACOES(Enum):
    BUSCAR = 'b'
    INSERIR = 'i'
    REMOVER = 'r'

TAMANHO_HEADER = 4
TAMANHO_BYTES_REGISTRO = 2
TAMANHO_ID = 2

class LED:
    def __init__(self, arquivo):
        self._led: List[List[int, int]] = []

        self._arquivo = arquivo
        arquivo.seek(0)
        cabecalho = arquivo.read(TAMANHO_HEADER).decode('utf-8', 'ignore')
        self._ponteiroAtual: str = '-1' if cabecalho == '' else cabecalho

    def ponteiroAtual(self) -> int:
        return self._ponteiroAtual

    def estaVazia(self) -> bool:
        return self.ponteiroAtual() == '-1'

    def inserir(self, byteOffsetDoRegistro: int) -> None:
        self._arquivo.seek(0)
        self._arquivo.write(str(byteOffsetDoRegistro).encode('utf-8'))
        self._ponteiroAtual = byteOffsetDoRegistro

    def __str__(self):
        return 'LED'

def lerCabecalhoDoArquivo(arquivo) -> bytes:
    return arquivo.read(TAMANHO_HEADER)

def lerRegistro(arquivo) -> Tuple[int, str]:
    tamanho = tamanhoDoRegistro(arquivo)

    if tamanho == 0:
        return 0, ''

    registro = arquivo.read(tamanho)

    stringDoRegistro = registro.decode()
    idDoRegistro = int(stringDoRegistro.split('|')[0])

    return idDoRegistro, stringDoRegistro

def tamanhoDoRegistro(arquivo) -> int:
    return int.from_bytes(arquivo.read(TAMANHO_BYTES_REGISTRO))

def lerFlagsDeEntrada() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument('-e', type=str, required=False, help='Caminho do arquivo de operações')
    parser.add_argument('-p', type=str, required=False, help='Exibe a LED')

    argumentos = parser.parse_args()

    if argumentos.e is not None and argumentos.p is not None:
        sys.exit('Erro: Apenas uma flag pode ser passada por vez')

    if argumentos.e is None and argumentos.p is None:
        sys.exit('Erro: Nenhuma flag foi passada')

    return argumentos

def lerArquivoDeOperacoes(caminho: str) -> List[str]:
    arquivo = open(caminho, 'r')
    operacoes = arquivo.readlines()
    operacoes = [operacao.replace('\n', '') for operacao in operacoes]
    arquivo.close()

    return operacoes

def parsearOperacao(operacao: str):
    operacaoAExecutar = operacao[0:1]

    registro = operacao[2:]

    return operacaoAExecutar, registro

def buscaRegistro(id: int, arquivo) -> Tuple[str, int]:
    bytesLidos = 6
    arquivo.seek(0)
    arquivo.seek(4)

    while True:
        idDoRegistro, registro = lerRegistro(arquivo)
        # print(registro)

        if registro == '':
            return None, bytesLidos

        if idDoRegistro == id:
            return registro, bytesLidos

        bytesLidos += len(registro) + TAMANHO_BYTES_REGISTRO

def escreverRegistroNoFim(registro: str, arquivo) -> None:
    arquivo.seek(0, io.SEEK_END)
    arquivo.write(registro.encode('utf-8'))

def executarOperacoes(operacoes: List[str], led: LED, arquivo) -> None:
    for operacao in operacoes:
        operacao, registro = parsearOperacao(operacao)

        if operacao == OPERACOES.BUSCAR.value:
            continue
            id = int(registro)
            print(f'Busca pelo registro de chave "{id}"')

            jogo = buscaRegistro(id, arquivo)

            if jogo == '' or jogo is None:
                print('Erro: registro não encontrado', end='\n')
                continue

            print(f'{jogo} ({len(jogo)} bytes)', end='\n')

        if operacao == OPERACOES.INSERIR.value:
            tamanhoDoRegistro = len(registro)
            idRegistro = int(registro.split('|')[0])
            print(f'Inserção do registro de chave "{idRegistro}" ({tamanhoDoRegistro} bytes)')
            print(registro)
            if led.estaVazia():
                # escreverRegistroNoFim(registro, arquivo)
                print('Local: fim do arquivo', end='\n')
            else:
                byteOffsetDisponivel = int(led.ponteiroAtual())
                arquivo.seek(byteOffsetDisponivel)

                tamanhoDoRegistroAtual = arquivo.read(2)
                tamanhoDoRegistroAtual = int.from_bytes(tamanhoDoRegistroAtual)

                if tamanhoDoRegistroAtual < tamanhoDoRegistro:
                    continue

                sobra = tamanhoDoRegistroAtual - tamanhoDoRegistro

                arquivo.write(registro.encode('utf-8'))

                # Se tiver, escreve o registro lá
                # Se não tiver, escreve no fim do arquivo

                print('')

        if operacao == OPERACOES.REMOVER.value:
            id: int = int(registro)
            jogo, byteOffsetDoRegistro = buscaRegistro(id, arquivo)

            print(f'Remoção do registro de chave "{id}"')

            if jogo == '' or jogo is None:
                print('Erro: registro não encontrado', end='\n')
                continue

            tamanhoDoRegistro: int = len(jogo)

            print(jogo)

            print(f'Registro removido! ({tamanhoDoRegistro} bytes)')
            print(f'Local: offset = {byteOffsetDoRegistro} bytes ({hex(byteOffsetDoRegistro)})', end='\n')

            ponteiroAtualDaLED: int = led.ponteiroAtual()
            removeRegistroLogicamente(arquivo, byteOffsetDoRegistro, ponteiroAtualDaLED)
            led.inserir(byteOffsetDoRegistro)

def removeRegistroLogicamente(arquivo, byteOffsetDoRegistro: int, ponteiroAtualDaLED: str) -> None:
    arquivo.seek(0)
    arquivo.seek(byteOffsetDoRegistro + TAMANHO_BYTES_REGISTRO + TAMANHO_ID)

    registro = arquivo.read(1)

    arquivo.write(f'*{ponteiroAtualDaLED}'.encode('utf-8'))

def main() -> None:
    existeArquivoDeDados: bool = os.path.isfile('dados.dat')

    if (existeArquivoDeDados is False):
        raise SystemExit('Erro, o arquivo "dados.dat" não existe na pasta atual!')

    flag = lerFlagsDeEntrada()

    arquivo = open('dados.dat', 'r+b')

    led = LED(arquivo)

    if flag.e:
        operacoes = lerArquivoDeOperacoes(flag.e)

        executarOperacoes(operacoes, led, arquivo)

    arquivo.close()

if __name__ == '__main__':
    main()
