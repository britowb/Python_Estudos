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

def abrir_conta(user_unico): 
    conta_nova =[]
    ag = '0001'
    print('Sua agência será 0001')
    conta_usuario = user_unico
    print(f'\nSeu usuário é: {conta_usuario}')
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
                        print(f'Saldo total de: R${saldo_conta:.2f}')
                    else:
                        print(f'\n{i+1} - Agência: {items[0]} Conta: {items[1]}. Usuário: {items[2]}')
                        print('Conta zerada.')           
            else:
                print('Não existem contas')
        elif opcoes == 2: # CRIAR CONTA
                verificar_usuario = input('Defina uma identificação para sua conta.\n=> ')
                if verificar_usuario in credencial_encontrada['contas']:
                    print('Identificação já existe')
                    continue
                else:
                    credencial_encontrada['contas'].append(abrir_conta(verificar_usuario))
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
        if credencial_encontrada['contas']:
            selecionar_conta = input('Digite o usuário')
            conta_logada = next(( select_conta for select_conta in credencial_encontrada['contas'] if selecionar_conta == select_conta[2]), None) #Aqui vamos iterar sobre a lista contas e trabalhar com o valor específico de cada conta.
            if conta_logada:
                break
            else:
                print('Conta inexistente!')
        else:
            print('O usuário não possui contas em aberto.')
            return 
    print('''
      MENU:
      1 - Saque
      2 - Depósito
      3 - Extrato
      4 - Ver Saldo
      5 - Sair
      ''')
    while True:
        while True:
            entrada = 0            
            entrada = input('Opção menu => ')
            menu = ['1', '2', '3', '4', '5'] 
            if entrada.isdigit():
                if entrada in menu:
                    op_menu = int(entrada)
                else:
                    print('opção inexistente')
                    print('Digite novamente!')
                break
            else:
                print('Somente números, por favor.')
                continue
        if conta_logada[3]:
                saldo_bancario = float(conta_logada[3][-1][3])
        else:
                saldo_bancario = 0
        if op_menu ==1:
                if saldo_bancario > 0:
                    valor_sacar = float(input('Digite o valor que deseja sacar'))
                    saque(saldo = saldo_bancario, saque = valor_sacar, conta = conta_logada[3])
                    print(
                        f'''-R${valor_sacar:.2f} sacado com sucesso da conta ag {conta_logada[0]}, conta {conta_logada[1]}''')
                else:
                    print('Você não possui saldo para realizar saques!')
                    continue
        elif op_menu ==2:
                try:
                    valor_depositar = float(input('Digite o valor para depósito'))
                    deposito(saldo_bancario, valor_depositar, conta_logada[3]) #Já atualizamos dentro da def depósito
                    print(
                        f'''+R${valor_depositar:.2f} depositado com sucesso na conta ag {conta_logada[0]}, conta {conta_logada[1]}''')
                except ValueError:
                     print('Somente números, por favor!')
                     continue
        elif op_menu ==3:
                if saldo_bancario:
                    mensagem = demonstrativo(saldo_bancario, extrato=conta_logada[3])
                    print("\n".join(mensagem)) 
                else:
                    print('Não há extrato')
                    continue
        elif op_menu ==4:
                if conta_logada[3]:
                    print(f'Você possui: R$ {saldo_bancario:.2f}')
                else:
                    print(f'Não há dinheiro na conta.')
                continue
        else:
            break

    


def demonstrativo(saldo, /, extrato):
    i = 0
    msg = []
    for op, valor, data, _ in extrato: #iterando sob as tuplas dentro de extrato
        #"Operação de +R$:{VALOR}. Dia {Data e hora}"
        msg.append(f'{op}{valor:.2f}. Dia {data}')   #CORRIGIR RETORNO APARECENDO LISTA TODA.
        i += 1
    msg.append(f'Saldo final: R${saldo:.2f}\nUm total de {i} operações')    
    return msg

def saque(*, saldo, saque, conta):
    agora = datetime.now()
    agora = agora.strftime("%d/%m/%Y às %H:%M")
    while True:
        if saque > saldo:
            print('Saldo insuficiente.')
            continue
        else:
            valor = saldo-saque
            operacao = 'Saque de: -R$'
            att_extrato = (operacao, valor, agora, saldo) #enviaremos extrato como tupla para a lista de contas
            conta.append(att_extrato)
            break
        


def deposito(saldo, deposito, conta):
    agora = datetime.now()
    agora = agora.strftime("%d/%m/%Y às %H:%M")
    if deposito <= 0:
        print('Operação impossível')
        return None 
    else:
        saldo = saldo+deposito
        operacao = 'Depósito de: +R$'
        att_extrato = (operacao, deposito, agora, saldo) #enviaremos extrato como tupla para a lista de contas
        conta.append(att_extrato)

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