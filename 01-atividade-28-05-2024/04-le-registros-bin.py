nomeDoArquivo: str = input('Digite o nome do arquivo a ser aberto: ')

def leiaRegistro(arquivo) -> str:
    tamanhoDoRegistroEmBytes = arquivo.read(2)
    tamanhoDoRegistroComoInteiro: int = int.from_bytes(tamanhoDoRegistroEmBytes)

    if tamanhoDoRegistroComoInteiro < 0:
        return ''

    buffer = arquivo.read(tamanhoDoRegistroComoInteiro)

    return buffer.decode()

try:
    with open(nomeDoArquivo, 'rb') as arquivo:
        bufferDeRegistro = leiaRegistro(arquivo)

        contadorDeRegistros = 1
        while bufferDeRegistro != '':
            dadosDaPessoa = bufferDeRegistro.split('|')

            contadorDeDados = 1
            print(f'Registro #{contadorDeRegistros} (tamanho = {len(bufferDeRegistro)})')
            for dado in dadosDaPessoa:
                if dado == '':
                    continue

                print(f'Campo #{contadorDeDados}: {dado}')
                contadorDeDados += 1

            print('')
            contadorDeRegistros += 1
            bufferDeRegistro = leiaRegistro(arquivo)
        

except:
    print(f'Erro ao abrir arquivo "{nomeDoArquivo}"')
