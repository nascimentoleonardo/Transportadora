import csv  
import os
import time

#Abrir e ler e fechar o arquivo CSV
file = open('dist.csv', 'r')
distancias = list(csv.reader(file))
file.close()

#Variaveis globais
custoKm = 0
custosKm = []


#Função para limpar a tela
def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')


#Função de estrutura do menu para usuário.
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

# Função que valida se o custo por km é um valor numérico e maior que zero
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

#Função que valida se o custo por km foi inserido
def validaCustoPorKm():
    if custoKm == 0:
        print('\033[1;33mParece que o custo por km não foi informado, retorne ao menu e informe um valor válido!\033[0;0m\n')
        input('Pressione ENTER para continuar...')
    

#Função que valida a origem e destino inseridos e consulta a distância entre eles
def consultarTrecho(origem, destino):
    while origem not in distancias[0] or destino not in distancias[0] or origem == destino:
        if origem not in distancias[0] or destino not in distancias[0]:
            limparTela()
            print('\033[1;31mOrigem ou destino inválido!\033[0;0m\n')
            origem = input('Informe a origem: ').upper()
            destino = input('Informe o destino: ').upper()
        elif origem == destino:
            limparTela()
            print('\033[1;31mOrigem e destino não podem ser o mesmo!\033[0;0m\n')
            origem = input('Informe a origem: ').upper()
            destino = input('Informe o destino: ').upper()
    else:
        origem_index = 1 + distancias[0].index(origem)
        destino_index = distancias[0].index(destino)

        distancia = int(distancias[origem_index][destino_index])
        return distancia, origem, destino

#Função solicita três cidades separadas por vírgula, valida as entradadas e define a melhor rota entre cidades do Menu 3
def melhorRota():
    limparTela()
    print('\n..:: Melhor Rota ::..\n')
    cidades = ''
    while len(cidades) != 3 or cidades[0] == cidades[1] or cidades[0] == cidades[2] or cidades[1] == cidades[2] or cidades[0] not in distancias[0] or cidades[1] not in distancias[0] or cidades[2] not in distancias[0]:
        cidades = input('Informe três cidades separadas por vírgula: ').upper().strip().replace(', ',',').split(',')
        if len(cidades) != 3 and cidades[0] != '':
            limparTela()
            print('\033[1;31mInforme TRÊS cidades válidas e diferentes entre si!\033[0;0m\n')
        elif cidades[0] == cidades[1] or cidades[0] == cidades[2] or cidades[1] == cidades[2]:
            limparTela()
            print('\033[1;31mAs cidades não podem ser as mesmas!\033[0;0m\n')
        elif cidades[0] not in distancias[0] or cidades[1] not in distancias[0] or cidades[2] not in distancias[0]:
            limparTela()
            print('\033[1;31mInsira somente cidades válidas!\033[0;0m\n')
        
    else: #Calcula a disntância entre as três cidades
        a = cidades[0]
        b = cidades[1]
        distanciaAB = consultarTrecho(a, b)[0]
        b = cidades[1]
        c = cidades[2]
        distanciaBC = consultarTrecho(b, c)[0]
        c = cidades[2]
        a = cidades[0]
        distanciaCA = consultarTrecho(c, a)[0]
         #Verifica qual o melhor caminho e retorna o resultado na tela
        if distanciaAB < distanciaCA:
            with open('log.txt', 'a') as log:
                print('A melhor rota é {} -> {} com uma distância de {} km e {} -> {} com uma distância de {} km com uma distância total de {} km'.format(a, b, distanciaAB, b, c, distanciaBC, distanciaAB+distanciaBC), file=log)
            print('A melhor rota é \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m e \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m com uma distância total de \033[1;32m{} km\033[0;0m'.format(a, b, distanciaAB, b, c, distanciaBC, distanciaAB+distanciaBC))
        elif distanciaCA < distanciaAB:
            with open('log.txt', 'a', encoding = 'utf-8') as log:#Imprime o resultado no arquivo de log
                print('A melhor rota é {} -> {} com uma distância de {} km e {} -> {} com uma distância de {} km com uma distância total de {} km'.format(a, c, distanciaCA, c, b, distanciaBC, distanciaCA+distanciaBC), file=log)
            print('A melhor rota é \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m e \033[1;32m{} -> {}\033[0;0m com uma distância de \033[1;32m{} km\033[0;0m com uma distância total de \033[1;32m{} km\033[0;0m'.format(a, c, distanciaCA, c, b, distanciaBC, distanciaCA+distanciaBC))
        input('Pressione ENTER para continuar...')

#Função que define a rota completa entre as cidades informadas pelo usuário
def rotaCompleta():
    limparTela()
    print('Informe o nome de pelo menos três cidades e digite "fim" para finalizar') #Solicita as cidades ao usuário, as valida e as coloca em uma lista
    distanciasPercorridas = []
    cidades = []
    cidadeIn = ''
    while True:
        try:
            cidadeIn = str(input('Informe uma cidade: ').upper())
            if cidadeIn == 'FIM' and len(cidades) >= 3:
                break
            elif cidadeIn == 'FIM' and len(cidades) < 3:
                limparTela()
                print('\033[1;31mInforme pelo menos três cidades\033[0;0m')
            elif cidadeIn not in distancias[0]:
                limparTela()
                print('\033[1;31mCidade inválida!\033[0;0m')
            elif cidadeIn in cidades:
                limparTela()
                print('\033[1;31mCidade já informada\033[0;0m')
            else:
                limparTela()
                cidades.append(cidadeIn)
                print(cidades)
        except ValueError:
            print('\033[1;31mEsse tipo de caractér é invalido\033[0;0m')

    limparTela()
    for i in range(len(cidades)-1): #Calcula a distância entre as cidades informadas pelo usuário
        origem_index = 1 + distancias[0].index(cidades[i])
        destino_index = distancias[0].index(cidades[i+1])
        distancia = int(distancias[origem_index][destino_index])
        distanciasPercorridas.append(distancia)
        with open('log.txt', 'a', encoding = 'utf-8') as log:
            print('A distância entre {} e {} é {} km'.format(cidades[i], cidades[i+1], distancia), file=log)
        print('A distância entre \033[1;32m{} e {}\033[0;0m é \033[1;32m{} km\033[0;0m'.format(cidades[i], cidades[i+1], distancia))
    distanciaTotal = sum(distanciasPercorridas) #Calcula a distância total percorrida
    #Imprime o resultado na tela
    print('\nA distância total da viagem é de \033[1;32m{} km\033[0;0m'.format(distanciaTotal))
    print('O custo total da viagem é de \033[1;32mR${:.2f}\033[0;0m'.format(distanciaTotal * custoKm))
    print('A quantidade total de litros de combustível consumidos ao final da viagem é de \033[1;32m{:.2f} litros\033[0;0m'.format(distanciaTotal * 2.57))
    print('O número de dias para finalizar a viagem é de \033[1;32m{:.2f} dias\033[0;0m'.format(distanciaTotal / 583))
    with open('log.txt', 'a', encoding = 'utf-8') as log:#Imprime o resultado no arquivo de log
        print('A distância total da viagem é de {} km'.format(distanciaTotal), file=log)
        print('O custo total da viagem é de R${:.2f}'.format(distanciaTotal * custoKm), file=log)
        print('A quantidade total de litros de combustível consumidos ao final da viagem é de {:.2f} litros'.format(distanciaTotal * 2.57), file=log)
        print('O número de dias para finalizar a viagem é de {:.2f} dias'.format(distanciaTotal / 583), file=log)
    cidades = []
    input('Pressione ENTER para continuar...')
        
#Loop de execução do programa e finalização da execução.
if __name__ == '__main__':
    escolha = 0
    while(escolha != 5):
        escolha = menu()

        if escolha == 1:  
            limparTela()
            custoKm = input('Informe o custo por km rodado:R$')
            custoPorKm()
            limparTela()
            with open('log.txt', 'a', encoding = 'utf-8') as log:#Imprime o resultado no arquivo de log
                print('O custo por km rodado foi definido como R${:.2f}\n'.format(custoKm), file=log)
            print('O valor do custo por km inserido foi de \033[1;32mR${:.2f}\033[0;0m\n'.format(custoPorKm()))
            input('Pressione ENTER para continuar...')
        elif escolha == 2:
            limparTela()
            validaCustoPorKm()
            if custoKm > 0:
                print('\033[1;32mInforme a cidade de origem e destino: \033[0;0m\n')
                origem = input('Informe a origem: ').upper()
                destino = input('Informe o destino: ').upper()
                distancia, origem_out, destino_out = consultarTrecho(origem, destino)
                with open('log.txt', 'a', encoding = 'utf-8') as log:#Imprime o resultado no arquivo de log
                    print('\nA distância da cidade de {} até {} é de {} km e o custo total do trecho é de R${:.2f}\n'.format(origem_out, destino_out, distancia, distancia * custoPorKm()), file=log)
                print('\nA distância da cidade de {} até {} é de \033[1;32m{} km\033[0;0m e o custo total do trecho é de \033[1;32mR${:.2f}\033[0;0m\n'.format(origem_out, destino_out, distancia, distancia * custoPorKm()))
                input('Pressione ENTER para continuar...')        
        elif escolha == 3:
            limparTela()
            validaCustoPorKm()
            if custoKm > 0:
                melhorRota()
        elif escolha == 4:
            limparTela()
            validaCustoPorKm()
            if custoKm > 0:
                rotaCompleta()
        elif escolha == 5:
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
        else:
            limparTela()
            print('\033[1;31mOpção inválida!\033[0;0m')
            input('Pressione ENTER para continuar...')
