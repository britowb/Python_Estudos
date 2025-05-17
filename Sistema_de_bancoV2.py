from datetime import datetime, date

def registro_user(credencial): #DEF RESPONSAVEL POR CADASTRAR NOVOS USUARIOS.
    novo_user = {} #nossos usuarios são registrados em chave-valor. Essa var irá alimentar o nosso registro de usuarios em chave-valor.
    novo_user['nome'] = str(input('Digite seu nome').capitalize()) 
    while True:
        try:
            novo_user['Nascimento'] = int(input('Digite seu nascimento DD/MM/AAAA =>\n').replace('/','').replace(' ',''))
            break
        except ValueError:
            print('Apenas números, por favor.')
    novo_user['cpf'] = str(credencial)# Aqui eu resgato o CPF que já foi informado e verificado.
    print('Agora seu endereço =>\n')
    novo_user['endereco'] = registro_endereco() #Aqui alimentaremos a chave:valor endereço através da função registro_endereco. 
    conta = []
    novo_user['contas'] = conta
    return novo_user #Retornamos a variavel que só existe na def para que o registro possa absorver os dados tratados.

def registro_endereco(): #Com essa def vamos tratar os dados do endereço
    campos_endereco = ['rua', 'numero', 'bairro', 'cidade', 'estado']
    address = []
    for registro in campos_endereco: #Variável registro percorre variável campos_endereço
        if registro == 'estado': #Se no momento do loop registro for estado, então:
            while True: #aqui trataremos para que os dados atendam os critérios que queremos.
                estado = input('Digite a sigla do Estado =>\n').upper() 
                if len(estado) == 2:
                    address.append(estado)
                    break
                else:
                    print('Apenas a sigla, por favor.')
        elif registro == 'numero': #Se o registro, no momento do loop for numero
            while True: #LOOP em que tenta converter o input em integral. Só sai daqui quando o resultado for numeral.
                try:
                    address.append(int(input('Digite o numero da sua casa =>\n')))
                    break
                except ValueError:
                    print('Apenas números.')
        else: 
            address.append(input(f'Insira a(o) {registro} =>\n').capitalize()) #Se não houverem exceções a serem tratadas então só armazene o dado da vez.
    address = f'{address[0]}, {address[1]} - {address[2]} - {address[3]}/{address[4]}'
    print(address)
    return address

def abrir_conta(): 
    conta_nova =[]
    ag = '0001'
    print('Sua agência será 0001')
    conta_usuario = input('Digite uma identificacao para a conta')
    global contabilidade
    contabilidade += 1
    conta_id = str(contabilidade)  # Vou atualizar a variavel responsavel pelo id das contas, o novo numero é o identificador da nova conta. Converto para string pois assim posso criar lista
    print(f'Numero da conta: {conta_id}') 
    conta_nova.append(ag) #AGENCIA
    conta_nova.append(conta_id) #numero da conta
    conta_nova.append(conta_usuario) # USUARIO
    extrato = []
    conta_nova.append(extrato)
    return conta_nova    
         
        
def user_loggin(credencial_encontrada): #(Aqui verificamos dados com o cpf escolhido. Os dados verificados são da var user.)
    if credencial_encontrada == None:
        return
    print(credencial_encontrada['cpf']) #Testar o retorno da variavel na def
    print(f'''
{user} Var user.
{credencial_encontrada} Var credencial_encontrada
{credencial_encontrada['cpf']}''' ) #Testar o retorno da var na def
    while True: # RODA UM LOOP PARA QUE POSSA ALTERNAR ENTRE OPÇÕES
        opcoes = int(input(''' 
    1 - Listar contas    
    2 - Abrir conta
    3 - Operações bancárias
    4 - Sair
    => '''))     # Ação que tomaremos uma vez que conseguimos autenticar os dados
        if opcoes == 1: #LISTAR CONTAS
            if credencial_encontrada['contas']:
                for i, items in enumerate(credencial_encontrada['contas']): #iterar valor de índice e valores da chave:valor 'conta'.
                    #if items: #Se houver alguma coisa
                    if items[3]:
                        print(f'\n{i+1} - Agência: {items[0]} Conta: {items[1]}. Usuário: {items[2]}')
                        saldo_conta = float(items[3][-1][3]) #ITEMS 3 SÃO AS TUPLAS. [-1] E A ÚLTIMA TUPLA. 
                        print(f'Saldo total de: R$ {saldo_conta:.2f}')
                    else:
                        print(f'\n{i+1} - Agência: {items[0]} Conta: {items[1]}. Usuário: {items[2]}')
                        print('Conta zerada.')           
            else:
                print('Não existem contas')
        elif opcoes == 2: # CRIAR CONTA
                credencial_encontrada['contas'].append(abrir_conta())
                print(credencial_encontrada['contas'][-1])
                print('Conta criada com sucesso')
        elif opcoes == 3:#Operações bancárias
            menu(credencial_encontrada)
    
        elif opcoes == 4: #SAIR
            break
        else:
            print('opção não encontrada. Digite o numero referente a opção desejada.')

def autentica(credencial): #Parte do código que trata o loggin.
    credencial_encontrada = next((usuario for usuario in user if usuario['cpf'] == credencial), None) 
    if credencial_encontrada is not None: 
        print(credencial_encontrada)
        return credencial_encontrada
    else:
        return print('CPF não encontrado.')

def menu(credencial_encontrada): 
    while True:
        selecionar_conta = input('Digite o usuário')
        indice, conta_logada = next(((indice, select_conta) for indice, select_conta in enumerate(credencial_encontrada['contas']) if selecionar_conta == select_conta[2]),(None, None)) #Aqui vamos iterar sobre a lista contas e trabalhar com o valor específico de cada conta.
        if conta_logada:
            break
        else:
            print('Conta inexistente!')
    print('''
      MENU:
      1 - Saque
      2 - Depósito
      E - Extrato
      M - Ver Saldo
      S - Sair
      ''')
    while True:            
        entrada = input('=>') 
        if entrada.isdigit():
            op_menu = int(entrada)
            break
        else:
            op_menu = str(entrada.upper())
            break
    if op_menu ==2:
        try:
            entrada = int(input('Digite o valor para depósito'))
            valor_deposito = entrada
            valor_atualizado, _  = deposito(valor_deposito, conta_logada[3]) #Já atualizamos dentro da def depósito
            print(f'''
                  +R${entrada} depositado com sucesso na conta ag {conta_logada[0]}, conta {conta_logada[1]}''')
        except ValueError:
             print('Somente números, por favor!')
    elif op_menu =='E':
        if conta_logada[3]:
            valor_atualizado = conta_logada[3][-1][3] #Aqui pegamos o último valor do extrato, que é o saldo atualizado.
            mensagem = demonstrativo(valor_atualizado, extrato=conta_logada[3])
            print("\n".join(mensagem))
            return 
        else:
            print('Não há extrato')
            return
    elif op_menu =='M':
        if conta_logada[3]:
            valor_atualizado = conta_logada[3][-1][3]
            print(f'Você possui: R$ {valor_atualizado:.2f}')
        else:
            valor_atualizado = 0
            print(f'Não há dinheiro na conta.')
    elif op_menu == 'S':
        return
    else:
        print('Opção inexistente')
    return menu(credencial_encontrada)


def demonstrativo(saldo, /, extrato):
    i = 0
    msg = []
    for op, valor, data, _ in extrato: #iterando sob as tuplas dentro de extrato
        #"Operação de +R$:{VALOR}. Dia {Data e hora}"
        msg.append(f'{op}{valor:.2f}. Dia {data}')   #CORRIGIR RETORNO APARECENDO LISTA TODA.
        i += 1
    msg.append(f'Saldo final: {saldo}\nUm total de {i} operações')    
    return msg

def deposito(deposito, extrato):
    if deposito <= 0:
        print('Operação impossível')
        return None 
    else:
        agora = datetime.now()
        agora = agora.strftime("%d/%m/%Y às %H:%M")
        if extrato: #Lembrar que aqui extrato é extrato=conta_logada[3] ou seja, a lista de tuplas que contém as operações.
            valor = extrato[-1][3]
        else:
            valor = 0       
        saldo = valor+deposito
        operacao = 'Depósito de: +R$ '
        att_extrato = (operacao, deposito, agora, saldo) #enviaremos extrato como tupla para a lista de contas
        extrato.append(att_extrato)
        return saldo, extrato

conta = []
user = [{'nome': 'nome', 'Nascimento': 'data', 'cpf': 'cpf', 'endereco': 'endereço', 'contas':conta,}] #Nosso registro de usuários alimentado pela def registro_user
contabilidade = len(conta) #Atualizador das contas
while True:
    escolha = int(input('''
                        1 - Logar
                        2 - Registrar-se
                        '''))
    if escolha == 1:
        try:
            credencial = input('Insira seu cpf').replace('-', '').replace('.','')#strip só remove do inicio ou fim. Replace é a melhor opção.
            credencial_encontrada = autentica(credencial)
            user_loggin(credencial_encontrada)
        except ValueError:
            print('Somente números, por favor.')
    elif escolha == 2: #REGISTRAR. Primeiro verifico o CPF e se não existir eu permito o registro.
        print(user)
        credencial = input('Insira seu cpf').replace('-', '').replace('.','')#Replace para evitar a fadiga de quem vai digitar o cpf
        if credencial.isdigit(): #Aqui verifico se é só número mesmo para evitar erro.
            credencial_encontrada = next((usuario for usuario in user if usuario['cpf'] == credencial), None) #next busca o primeiro resultado, o for percorre toda a variável. 
            if credencial_encontrada is not None: #Então eu verifiquei se o cpf já não existe para impedir sobreposições. 
                print('Cliente já cadastrado.')
                continue
            else: #Como não tem, eu deixo registrar. Mas já envio credencial que tem o cpf armazenado
                user.append(registro_user(credencial))  #A var retornada por registro_user é utilizada para preencher o responsável por manter o registro dos usuários.
        else:
            print('Apenas números, por favor.')
        print(user)
    else:
        print('Opção inválida')
        continue


    
#Dividir todas as funções do sistema em defs. O retorno e o nome das variáveis é de meu critério FEITO

#SAQUE DEVERÁ SER KEYWORD ONLY . saldo(valor = valor, saldo = saldo)
#Sugestão de argumento é checar saldo e ver valor.
# IDEIA MINHA: Vamos usar o módulo do extrato para retornar tanto para saque como para depósito.
#SUGESTÃO DE RETORNO DO SAQUE: SALDO ATUAL E EXTRATO.

#Função depósito deve receber argumentos positional only.
#Sugestão de argumentos: saldo, valor, extrato.
#Sugestão de retorno: saldo e extrato.

#EXTRATO DEVE RECEBER ARGUMENTOS POR POSIÇÃO E NOME.
# Argumentos posicionais: saldo
# Argumntos nomeados: extrato

#Criar usuário e conta corrente. E pode fazer mais funções, se quiser. Como listar ou inativar conta.

#Criar usuário (cliente)
#Armazenar usuários em uma lista. Um usuário é composto por: nome, data de nascimento, cpf e endereço.
# O endereço é uma string com o formato: logradouro, numero - bairro - cidade/sigla estado.
# Deve ser armazenado somente os números do cpf. (SEM CARACTERES ESPECIAIS)

# Criar conta corrente

#O programa deve armazenar contas em uma lista
#Conta é composta por ag, numero da conta e usuário
#ag padrão 0001. Numero da conta é sequencial a partir de 1
#O usuário pode ter diversas contas (vamos criar um limitador modulado )
#Uma conta só pode pertencer a um usuário
#Se não houver um usuário deve ser impossível criar a conta.
#Se houver um usuário com o cpf informado, vincule.