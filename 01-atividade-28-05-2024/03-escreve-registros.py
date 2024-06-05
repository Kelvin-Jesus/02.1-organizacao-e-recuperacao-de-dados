arquivo = None

try:
    arquivo = open('pessoas-bin.txt', 'wb')
except:
    print('Erro ao abrir arquivo')


while True:
    sobrenome: str = input('Digite o sobrenome: ')

    if len(sobrenome) == 0:
        print('cabo')
        break

    nome: str = input('Digite o nome: ')
    endereco: str = input('Digite o endereço: ')
    cidade: str = input('Digite a cidade: ')
    estado: str = input('Digite o estado: ')
    cep: str = input('Digite o cep: ')

    pessoa: str = f'{sobrenome}|{nome}|{endereco}|{cidade}|{estado}|{cep}|'
    pessoaEmBinario: bytes = pessoa.encode()
    tamanhoEmBytes: int = len(pessoaEmBinario)
    tamanhoEmBinario: bytes = tamanhoEmBytes.to_bytes(2)
    
    arquivo.write(tamanhoEmBinario)
    arquivo.write(pessoaEmBinario)
    print('')
