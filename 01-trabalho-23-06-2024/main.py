from io import BufferedReader
import os
import sys
import argparse

print(sys.argv)
parser = argparse.ArgumentParser()

parser.add_argument('-e', type=str, required=True, help="The value associated with the -e flag.")

# Parse the arguments
args = parser.parse_args()

# Get the value associated with the -e flag
e_value = args.e

# Print the value
print(f"The value provided for -e is: {e_value}")

existeArquivoDeDados: bool = os.path.isfile('dados.dat')

if (existeArquivoDeDados is False):
    raise SystemExit('Erro, o arquivo "dados.dat" não existe na pasta atual!')

def lerArquivoDeOperacoes(arquivo) -> None:
    if os.path.isfile(arquivo) is False:
        raise SystemExit('Erro, o arquivo de operações não existe!')

    arquivo = open(arquivo, 'r')

    print(arquivo.read(1))

open('dados.dat', 'b+a')

def abrirArquivo() -> BufferedReader:
    arquivo: BufferedReader = open('dados.dat', 'rb')

    return arquivo

cabecalho = abrirArquivo()
print(cabecalho, int.from_bytes(cabecalho.read(4)))
lerArquivoDeOperacoes(args.e)
