nomeDoArquivo: str = input('Digite o nome do arquivo: ')

try:
    with open(nomeDoArquivo, 'r') as arquivo:
        linhas: list[str] = arquivo.readlines()

        print('')
        for pessoa in linhas:
            dadosDaPessoa = pessoa.split('|')
            
            print(f'campo#0: {dadosDaPessoa[0]}')
            print(f'campo#1: {dadosDaPessoa[1]}')
            print(f'campo#2: {dadosDaPessoa[2]}')
            print(f'campo#3: {dadosDaPessoa[3]}')
            print(f'campo#4: {dadosDaPessoa[4]}')
            print(f'campo#5: {dadosDaPessoa[5]}')
            print('')
    
except FileNotFoundError:
    print(f'Arquivo "{nomeDoArquivo}" não encontrado')

