import csv  # Biblioteca para manipulação de arquivos CSV
import os
import time

file = open('dist.csv', 'r')
distancias = list(csv.reader(file))
file.close()

custoKm = 0
distancia = 0

def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    limparTela()
    print('\n..:: Sistema para Gerenciamento de Logística ::..\n')
    print('1 - Custo por KM rodado')
    print('2 - Consultar trecho')
    print('3 - Melhor rota')
    print('4 - Rota Completa')
    print('5 - Sair')
    opcao = int(input('Escolha uma opção: '))
    return opcao

# Valida se o custo por km é um valor numérico e maior que zero
def custoPorKm():
    global custoKm
    while True:
        try:
            if float(custoKm) > 0:
                break
            else:
                limparTela()
                print('\033[1;31mO custo por KM não poder ser menor ou igual a zero!\033[0;0m\n')
                custoKm = input('Informe o custo por km rodado: R$')
        except ValueError:
            limparTela()
            print('\033[1;31mInforme apenas valores numéricos!\033[0;0m\n')
            custoKm = input('Informe o custo por km rodado: R$')
    custoKm = float(custoKm)
    return custoKm

#Valida se o custo por km foi inserido
def validaCustoPorKm():
    if custoKm == 0:
        print('\033[1;33mParece que o custo por km não foi informado, retorne ao menu e informe um valor válido!\033[0;0m\n')
        input('Pressione ENTER para continuar...')

# Valida a origem e destino inseridos e consulta a distância entre eles
def consultarTrecho(origem, destino):
    while origem not in distancias[0] or destino not in distancias[0] or origem == destino:
        limparTela()
        print('\033[1;31mOrigem ou destino inválido!\033[0;0m\n')
        origem = input('Informe a origem: ').upper()
        destino = input('Informe o destino: ').upper()
    else:
        origem_index = 1 + distancias[0].index(origem)
        destino_index = distancias[0].index(destino)

        distancia = int(distancias[origem_index][destino_index])
        with open('log.txt', 'a') as log:
            print('\nA distância da cidade de {} até {} é de {} km e o custo total do trecho é de R${:.2f}\n'.format(origem, destino, distancia, distancia * custoPorKm()), file=log)
        print('\nA distância da cidade de {} até {} é de \033[1;32m{} km\033[0;0m e o custo total do trecho é de \033[1;32mR${:.2f}\033[0;0m\n'.format(origem, destino, distancia, distancia * custoPorKm()))
        print()
        input('Pressione ENTER para continuar...')
        return distancia

#Loop de execução do programa
if __name__ == '__main__':
    escolha = 0

    while(escolha != 5):
        escolha = menu()

        if escolha == 1:  
            limparTela()
            custoKm = input('Informe o custo por km rodado:R$')
            custoPorKm()
            limparTela()
            print('O valor do custo por km inserido foi de \033[1;32mR${:.2f}\033[0;0m\n'.format(custoPorKm()))
            input('Pressione ENTER para continuar...')

        if escolha == 2:
            limparTela()
            validaCustoPorKm()
            if custoKm > 0:
                print('Informe a cidade de origem e destino: ')
                origem = input('Origem: ').upper()
                destino = input('Destino: ').upper()
                consultarTrecho(origem, destino) 
                
                
                
                

        if escolha == 5:
            limparTela()
            print('\033[1;33mSAINDO EM 3...\033[0;0m')
            time.sleep(0.75)
            limparTela()
            print('\033[1;33mSAINDO EM 2...\033[0;0m')
            time.sleep(0.75)
            limparTela()
            print('\033[1;33mSAINDO EM 1...\033[0;0m')
            time.sleep(0.75)
            limparTela()    
