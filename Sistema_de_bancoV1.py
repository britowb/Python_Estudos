from datetime import datetime
import sys
# Variáveis de controle
limite_saque = 500 #Limite por operação CONSTANTE
limite_diario = 3 # Apenas 3 saques por dia CONSTANTE
saldo = 0
saque_diario = 3
banco_extrato = {}
index = 0

# Funções do banco que serão chamadas no main
def deposito():
    global saldo
    try:
        deposito = int(input('Insira o valor para depósito => '))
        if deposito <= 0:
            print(f'O valor R${deposito} não é válido')
            return
        else:
            valor_depositado = deposito
    except ValueError:
       print('Por favor: somente números inteiros.')
    operacao = "Depósito de: +R$"
    data = datetime.now()
    data = data.strftime("às %H:%M, do dia %d/%m/%Y")
    valor = valor_depositado
    saldo += valor_depositado
    adicionar_extrato(operacao, valor, saldo, data)
    print(f'Foi depositado R${valor_depositado:.2f}')

def saque():
    global saldo, limite_diario, saque_diario, limite_saque
    print(f'Olá, está disponível um limite de {saque_diario} saque(s) hoje')
    if saque_diario == 0:
        print('Aguarde o próximo dia para repor seu limite de saque.')
    while saque_diario <= limite_diario and saque_diario > 0:
        try:
            saque = float(input('Qual valor deseja sacar?'))
            if saque <= 0:
                print(f'Não há como sacar R${saque:.2f}')
                break
        except ValueError:
            print('Você precisa digitar apenas números')
        if saque > saldo or saldo == 0:
           print('Saldo insuficiente ou inexistente.')
           break
        elif saque > limite_saque:
            print(f'Apenas R${limite_saque:.2f} por operação!')
        else:
            operacao = "Saque de: -R$"
            data = datetime.now()
            data = data.strftime("às %H:%M, do dia %d/%m/%Y")
            saldo -= saque
            valor = saque
            saque_diario -= 1
            limite_diario -= 1
            print(f'Saque de R${saque:.2f} realizado com sucesso')
            adicionar_extrato(operacao, valor, saldo, data)
            break
        
def adicionar_extrato(operacao, valor, saldo, data):
    global index
    banco_extrato[index] = (operacao, valor, saldo, data)
    index += 1

def extrato():
    try:
        print('---------- EXTRATO -------------')
        for _, registro in banco_extrato.items(): # O primeiro valor de um dic a ser relatado é a chave. extrato = {0: ("Depósito", 100, 1000, "28/04/2025"). Portanto iremos ignorar ele e fazer registro obter os valores da tupla.
            operacao, valor, saldo, data = registro
            print(f'\n{operacao}{valor:.2f},{data}')
        saldo = list(banco_extrato.values())[-1][2] #Dicionários não podem ser fatiados como Strings ou Listas. Aqui convertemos a VAR dic para lista dentro da var Saldo. Agora conseguimos definir o último item da lista e mostrar qual o conteúdo do terceiro valor da tupla. [-1][2]
        print(f' Seu saldo é de: R${saldo:.2f}')
    except (KeyError, IndexError): #Não podemos usar Or nessas exceções. Precisa ser em forma de tupla.
        print('Histórico vazio! Faça um depósito na conta para movimentá-la.')
        deposito()

def sair():
    print('Obrigado pela preferência\nAté logo!')
    sys.exit()

#Variavel de navegação do menu
menu ={
"D": ("Depósito", deposito),
"S": ("Saque", saque),
"E": ("Extrato", extrato),
"Q": ("Sair", sair)} 

# Sistema principal: NOSSO MENU.
for keyword, (descricao, funcao) in menu.items(): 
    print(f'[{keyword}] {descricao}') 
while True:
    opcao = input('Digite a função desejada => ').upper() 
    if opcao in menu: 
        
        _, funcao = menu[opcao] # Ou podemos usar um _ para ignorar valores que não te interessam da tupla
        funcao() 
    else:
        print(f'{opcao} Não é uma opção válida')