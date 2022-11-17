import csv  
import os
import time

file = open('dist.csv', 'r')
distancias = list(csv.reader(file))
file.close()

custoKm = 0
custosKm = []
# distancia = 0

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
    custosKm.append(custoKm)
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
        # print('\nA distância da cidade de {} até {} é de \033[1;32m{} km\033[0;0m e o custo total do trecho é de \033[1;32mR${:.2f}\033[0;0m\n'.format(origem, destino, distancia, distancia * custoPorKm()))
        # print()
        # input('Pressione ENTER para continuar...')
        return distancia, origem, destino

def melhorRota():
    limparTela()
    print('\n..:: Melhor Rota ::..\n')
    cidades = input('Informe três cidades separadas por vírgula: ').upper().split(',')
    cidades_lista = [cidade.strip() for cidade in cidades]
    while len(cidades) != 3 or cidades[0] == cidades[1] or cidades[0] == cidades[2] or cidades[1] == cidades[2] or cidades[0] not in distancias[0] or cidades[1] not in distancias[0] or cidades[2] not in distancias[0]:
        limparTela()
        print('\033[1;31mInforme três cidades válidas e diferentes entre si!\033[0;0m\n')
        cidades = input('Informe três cidades separadas por vírgula: ').upper().split(',')
        cidades_lista = [cidade.strip() for cidade in cidades]
    else:
        a = cidades_lista[0]
        b = cidades_lista[1]
        distanciaAB = consultarTrecho(a, b)[0]
        b = cidades_lista[1]
        c = cidades_lista[2]
        distanciaBC = consultarTrecho(b, c)[0]
        c = cidades_lista[2]
        a = cidades_lista[0]
        distanciaCA = consultarTrecho(c, a)[0]
        distanciaTotal = distanciaAB + distanciaBC + distanciaCA
        
        if distanciaAB < distanciaBC and distanciaAB < distanciaCA:
            with open('log.txt', 'a') as log:
                print('A melhor rota é{} -> {} com uma distância de {} km e {} -> {} com uma distância de {} km com uma distância total de {} km'.format(a, b, distanciaAB, b, c, distanciaBC, distanciaAB+distanciaBC), file=log)
            print('A melhor rota é \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m e \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m com uma distância total de \033[1;32m{} km\033[0;0m'.format(a, b, distanciaAB, b, c, distanciaBC, distanciaAB+distanciaBC))
        elif distanciaBC < distanciaAB and distanciaBC < distanciaCA:
            with open('log.txt', 'a') as log:
                print('A melhor rota é{} -> {} com uma distância de {} km e {} -> {} com uma distância de {} km com uma distância total de {} km'.format(b, c, distanciaBC, c, a, distanciaCA, distanciaBC+distanciaCA), file=log)
            print('A melhor rota é \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m e \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m com uma distância total de \033[1;32m{} km\033[0;0m'.format(b, c, distanciaBC, c, a, distanciaCA, distanciaBC+distanciaCA))
        elif distanciaCA < distanciaAB and distanciaCA < distanciaBC:
            with open('log.txt', 'a') as log:
                print('A melhor rota é{} -> {} com uma distância de {} km e {} -> {} com uma distância de {} km com uma distância total de {} km'.format(c, a, distanciaCA, a, b, distanciaAB, distanciaCA+distanciaAB), file=log)
            print('A melhor rota é \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m e \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m com uma distância total de \033[1;32m{} km\033[0;0m'.format(c, a, distanciaCA, a, b, distanciaAB, distanciaCA+distanciaAB))
        input('Pressione ENTER para continuar...')

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
                distancia, origem_out, destino_out = consultarTrecho(origem, destino)
                print('\nA distância da cidade de {} até {} é de \033[1;32m{} km\033[0;0m e o custo total do trecho é de \033[1;32mR${:.2f}\033[0;0m\n'.format(origem_out, destino_out, distancia, distancia * custoPorKm()))
                input('Pressione ENTER para continuar...')
        
        if escolha == 3:
            limparTela()
            validaCustoPorKm()
            if custoKm > 0:
                melhorRota()

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
