def leiaRegistro(arquivo) -> str:
    tamanhoDoRegistro = int.from_bytes(arquivo.read(2))

    if tamanhoDoRegistro > 0:
        s = arquivo.read(tamanhoDoRegistro)
        return s.decode()

    return ''

def main() -> None:
    try:
        nomeDoArquivo = input('Digite o nome do arquivo a ser aberto: ')
        arquivo = open(nomeDoArquivo, 'rb')

        sobrenomeBuscado = input('Digite o SOBRENOME a ser buscado: ')

        achou = False
        registro = leiaRegistro(arquivo)

        while registro != '' and not achou:
            sobrenome = registro.split(sep='|')[0]

            if sobrenome == sobrenomeBuscado:
                achou = True
            else:
                registro = leiaRegistro(arquivo)
        
        if achou:
            contador = 1
            campos = registro.split('|')
            for campo in campos:
                if campo != '':
                    print(f'Campo {contador}: {campo}')
                    contador += 1
        else:
            print('Sobrenome não encontrado')

        arquivo.close()
    except Exception as erro:
        print('cabo')
        print(erro)

if __name__ == '__main__':
    main()
