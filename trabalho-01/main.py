from dataclasses import dataclass
import os
import sys

existeArquivoDeDados: bool = os.path.isfile('dados.dat')

if (existeArquivoDeDados is False):
    raise SystemExit('Erro, o arquivo "dados.dat" não existe na pasta atual!')


open('dados.dat', 'b+a')

@dataclass
class Jogo:
    ID: int
    titulo: str
    ano: int
    genero: str
    produtora: str
    plataforma: str

fileDescriptor = open('dados.dat', 'rb')

# Ler o cabeçalho
header = fileDescriptor.read(4)

# Ler o registro passando o arquivo
def readEntireRecord(fileDescriptor):

    # chama uma função pra pegar o tamanho do registro
    sizeOfRegister = getRecordSize(fileDescriptor)
    if sizeOfRegister == 0:
        sys.exit()

    # print(f'size {sizeOfRegister}')

    # le de onde termina o tamanho do arquivo até o fim do registro
    record = fileDescriptor.read(sizeOfRegister)
    # print(record)
    return record[0:2], record

def getRecordSize(fileDescriptor) -> int:
    # le os primeiros 2 bytes do registro e retorna o tamanho
    return int.from_bytes(fileDescriptor.read(2))

while True:
    idDoRegister, record = readEntireRecord(fileDescriptor)

    print(idDoRegister[0], record)
    # if idDoRegister[0] == b'20':
        # print(idDoRegister)

    # if id == 20:
