while True:
    sobrenome: str = input("Digite o sobrenome: ")

    if len(sobrenome) == 0:
        print('cabo')
        break

    nome: str = input('Digite o nome: ')
    endereco: str = input('Digite o endereço: ')
    cidade: str = input('Digite a cidade: ')
    estado: str = input('Digite o estado: ')
    cep: str = input('Digite o cep: ')

    with open('pessoas.txt', 'a') as arquivo:
        arquivo.writelines(sobrenome+'|'+nome+'|'+endereco+'|'+cidade+'|'+estado+'|'+cep+'|\n')
