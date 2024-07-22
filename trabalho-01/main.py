import os

existeArquivoDeDados: bool = os.path.isfile('dados.dat')

if (existeArquivoDeDados is False):
    raise SystemExit('Erro, o arquivo "dados.dat" não existe na pasta atual!')


open('dados.dat', 'b+a')
    
