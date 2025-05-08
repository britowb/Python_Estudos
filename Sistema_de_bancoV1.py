from datetime import datetime, date
import sys, os
# Variáveis de controle
limite_cliente= {
          'operacaoc': 10,# movimentacoes que o cliente ainda pode fazer 
          'saquec': 3,
          'dia': 0,
          'saldo': 0,}
limite_banco = {
             'saqueb': 3, # Apenas 3 saques por dia CONSTANTE
             'valor': 500,#Limite por operação CONSTANTE
             'movimentacao': 10, }#movimentações máximas por dia CONSTANTE
banco_extrato = {}
index = 0
linhas_mudanca = []
linhas = [10, 3, 7]
banco = {
    'limite_cliente': limite_cliente,
    'limite_banco': limite_banco,
    'extrato': banco_extrato,
    'linhas': linhas, }   

def arquivo_read(banco):
    if not os.path.exists('var.txt'): #Ele vai ler, mas se não existir ele cria.
        banco['linhas'][0] = f"{banco['limite_banco']['movimentacao']}\n" #Usei dessa forma em vez de append porque achava que aqui era um problema, mas no fim não era.
        banco['linhas'][1] = f"{banco['limite_banco']['saqueb']}\n"
        banco['linhas'][2] = f"{date.today().day}\n"
        #print(banco['linhas'])
        caminho = os.path.join(os.getcwd(), "var.txt") #Transformamos caminho em um objeto do módulo OS.
        with open(caminho, 'w') as arquivo:
            arquivo.writelines(banco['linhas'])
    else: #Mas se existir ele só lê.
       with open('var.txt', 'r') as leitura:
            linhas_mudanca = leitura.readlines()
            print(linhas_mudanca)
            print(f"Executando em: {os.getcwd()}")
            banco['limite_cliente']['operacaoc'] = int(linhas_mudanca[0])
            banco['limite_cliente']['saquec'] = int(linhas_mudanca[1].strip())
            banco['limite_cliente']['dia'] = int(linhas_mudanca[2].strip())
        
    return banco

def arquivo_write(banco): #Feito para sobrescrever com novos dados.
    with open('var.txt', 'r+') as arquivo:
        dia_atual = datetime.now().day
        print(dia_atual)
        linhas_mudanca = arquivo.readlines()
        arquivo.seek(0)
        print(f'{linhas_mudanca} linhas mudança')
        print(f'{banco['linhas']} banco linhas')
        data_registrada = int(linhas_mudanca[2]) #Para que eu consiga comparar as datas
        print(data_registrada)
        if data_registrada < dia_atual: # TEMOS QUE VERIFICAR SE LINHAS[2] É DIFERENTE DO DIA ATUAL PARA SALVAR NO TXT O NOVO DIA. SE NÃO, NÃO MODIFICAR O DIA.
            banco['linhas'] = [
                f'{banco['limite_cliente']['operacaoc']}\n',
                f'{banco['limite_cliente']['saquec']}\n',
                f'{banco['limite_cliente']['dia']}\n']
            print(banco['linhas'])
            linhas_mudanca = list(banco['linhas'])
                 #usamos o f'{}' para formatar para string adequadamente, preservando o linha a linha.
            arquivo.writelines(linhas_mudanca)
        else:
            banco['linhas'] = [
                f'{banco['limite_cliente']['operacaoc']}\n',
                f'{banco['limite_cliente']['saquec']}\n',
                f'{dia_atual}\n']
            print(banco['linhas'])
            linhas_mudanca = list(banco['linhas'])
            arquivo.writelines(linhas_mudanca)


# Funções do banco que serão chamadas no main
def deposito(banco):
    if banco['limite_cliente']['operacaoc'] <= 0: #Se não tem limite não tem nem pra que digitar valor. Daqui já retorna pro menu.
        print('Limite de operações zerado, aguarde o próximo dia!')
        return
    else: #Se tem limite bora depositar.
        while True:
            try:
                depositar = int(input('Insira o valor para depósito => '))
                if depositar <= 0:
                    print(f'O valor R${depositar} não é válido')
                else:
                    valor_depositado = depositar
                    break
            except ValueError:
                print('ERROR: Somente números inteiros. Voltando ao menu inicial...')
                return

    operacao = "Depósito de: +R$"
    data = datetime.now()
    data = data.strftime("às %H:%M, do dia %d/%m/%Y")
    valor = valor_depositado
    banco['limite_cliente']['saldo'] += valor_depositado
    banco['limite_cliente']['operacaoc'] -= 1
    print(banco['limite_cliente']['saldo'])
    print(banco['limite_cliente']['operacaoc'])
    index = len(banco['extrato'])
    adicionar_extrato(index, operacao, valor, data, banco)
    print(f'Foi depositado R${valor_depositado:.2f}')
    arquivo_write(banco)

def saque(banco):
    print(f'Olá, está disponível um limite de {limite_cliente['saquec']} saque(s) hoje') #O limite de saque é menor que o de operações, por isso não entrará em valores negativos, burlando o limite de 3.
    if banco['limite_cliente']['saquec'] == 0:
        print('Aguarde o próximo dia para repor seu limite de saque.')
    while banco['limite_cliente']['saquec'] <= banco['limite_banco']['saqueb'] and banco['limite_cliente']['saquec'] > 0:
        try:
            saque = float(input('Qual valor deseja sacar?'))
            if saque <= 0:
                print(f'Não há como sacar R${saque:.2f}')
                break
        except ValueError:
            print('Você precisa digitar apenas números')
        if saque > banco['limite_cliente']['saldo'] or banco['limite_cliente']['saldo'] == 0:
           print('saldo insuficiente ou inexistente.')
           break
        elif saque > limite_banco['valor']:
            print(f'Apenas R${banco['limite_banco']['valor']:.2f} por operação!')
        else:
            operacao = "Saque de: -R$"
            data = datetime.now()
            data = data.strftime("às %H:%M, do dia %d/%m/%Y")
            banco['limite_cliente']['saldo'] -= saque
            valor = saque
            banco['limite_cliente']["operacaoc"] -= 1
            banco['limite_cliente']["saquec"] -= 1
            print(f'Saque de R${saque:.2f} realizado com sucesso')
            index = len(banco['extrato']) #verificamos o tamanho do extrato para termos um indice atualizado.
            adicionar_extrato(index, operacao, valor, data, banco)
            return arquivo_write(banco)
        
def adicionar_extrato(index, operacao, valor, data, banco):
    banco['extrato'][index] = (operacao, valor, banco['limite_cliente']['saldo'], data)
    index += 1
    return banco

def extrato(banco):
    try:
        print('---------- EXTRATO -------------')
        for _, registro in banco['extrato'].items(): # O primeiro valor de um dic a ser relatado é a chave. extrato = {0: ("Depósito", 100, 1000, "28/04/2025"). Portanto iremos ignorar ele e fazer registro obter os valores da tupla.
            operacao, valor, banco['limite_cliente']['saldo'], data = registro
            print(f'\n{operacao}{valor:.2f},{data}')
        banco['limite_cliente']['saldo'] = list(banco['extrato'].values())[-1][2] #Dicionários não podem ser fatiados como Strings ou Listas. Aqui convertemos a VAR dic para lista dentro da var limite_cliente['saldo']. Agora conseguimos definir o último item da lista e mostrar qual o conteúdo do terceiro valor da tupla. [-1][2]
        print(f'Seu saldo é de: R${banco['limite_cliente']['saldo']:.2f}')
        print(f'\n Restam {banco['limite_cliente']['operacaoc']} operações sendo {banco['limite_cliente']["saquec"]} saques. ')
    except (KeyError, IndexError): #Não podemos usar Or nessas exceções. Precisa ser em forma de tupla.
        print('Histórico vazio! Faça um depósito na conta para movimentá-la.')
        deposito(banco)

def sair(*args, **kwargs): #Eu queria ignorar os argumentos e descobri que assim dá certo
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
arquivo_read(banco) 
data_verificador = date.today().day
print(data_verificador)
print(limite_cliente['dia'])
if limite_cliente['dia'] < data_verificador: #limite_cliente['dia'] é 0 por padrão. Sempre será inferior a qualquer data. Portanto aqui atualizamos a data e devolvemos os limites ao mesmo tempo.
    limite_cliente['operacaoc'] = limite_banco['movimentacao']
    limite_cliente['saquec'] = limite_banco['saqueb']
    limite_cliente['dia'] = date.today().day
if banco['limite_cliente']['operacaoc'] <= banco['limite_banco']['movimentacao']: # Aqui decidimos que enquanto termos limite poderemos executar algo. Eu não defini o que acontece no = 0 pois quero que seja possivel tentar a toa. E tirar extrato :D
    while True:
        opcao = input('Digite a função desejada => ').upper() 
        if opcao in menu: 
            _, funcao = menu[opcao] # podemos usar um _ para ignorar valores que não te interessam da tupla
            print(f"Executando em: {os.getcwd()}") 
            funcao(banco)
        else:
            print(f'{opcao} Não é uma opção válida')
            continue