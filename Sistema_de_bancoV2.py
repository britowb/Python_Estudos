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
    saldo = 0
    extrato = ['operação', 'valor', 'data', saldo]
    conta_nova.append(extrato)
    conta_nova.append(saldo)
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
            for i, items in enumerate(credencial_encontrada['contas']): #iterar valor de índice e valores da chave:valor 'conta'.
                i += 1
                if items: #Se houver alguma coisa 
                    print(f'\n{i} - Agência: {items[0]} Conta: {items[1]}. Usuário: {items[2]}') #Mostra
                else:
                    print('Não existem contas')
        elif opcoes == 2: # CRIAR CONTA
                #PRECISO DEFINIR A SELEÇÃO DE CONTA PARA EFETUAR DEPÓSITO.
                credencial_encontrada['contas'].append(abrir_conta())
                print('Conta criada com sucesso')
        elif opcoes == 3:#Operações bancárias
            credencial_encontrada['contas'].append(menu(credencial_encontrada))
        elif opcoes == 4: #SAIR
            break
        else:
            print('opção não encontrada. Digite o numero referente a opção desejada.')

def autentica(credencial): #Decidi separar em uma função a parte do código que trata o loggin, para futuras reutilizações.
    credencial_encontrada = next((usuario for usuario in user if usuario['cpf'] == credencial), None) #next busca o primeiro resultado, o for percorre toda a variável. 
    if credencial_encontrada is not None: 
        print(credencial_encontrada)
        return credencial_encontrada
    else:
        return print('CPF não encontrado.')


extrato = ['operação', 'valor', 'data', 'saldo']
def menu(credencial_encontrada): #Aqui iremos trabalhar apenas com os valores da lista de cada conta.
    while True:
        selecionar_conta = input('Digite o usuário')
        conta_logada = next((select_conta for select_conta in credencial_encontrada['contas'] if selecionar_conta == select_conta[2]), None) #Aqui vamos iterar sobre a lista contas e trabalhar com o valor específico de cada conta.
        if conta_logada:
            break
        else:
            print('Conta inexistente!')
            continue
    print('''
      MENU:
      1 - Saque
      2 - Depósito
      3 - Extrato''')
    while True:            
        entrada = input('=>') 
        if entrada.isdigit():
            op_menu = int(entrada)
            break
        else:
            print('Opção inválida')
            continue
    if op_menu ==1:
        saque()
    elif op_menu ==2:
        try:
            entrada = int(input('Digite o valor para depósito').strip())
            valor_deposito = entrada
            depositar = deposito(valor_deposito, credencial_encontrada)
            conta_logada.append(depositar)
            conta_logada[4] += entrada
            print(f'''
                  +R${entrada} depositado com sucesso na conta ag {conta_logada[0]}, conta {conta_logada[1]}''')
        except ValueError:
             print(valor_deposito)
             print(type(valor_deposito))
             print('Somente números, por favor!')
    elif op_menu ==3:
        saldo = conta_logada[4]
        conta_logada[3].append(demonstrativo(saldo, extrato=conta_logada))
    else:
        print('Opção inexistente')

    return conta_logada


def demonstrativo(saldo, /, extrato):
    for i, demonstrativo in extrato:
        #"Operação de +R$:{VALOR}. Dia {Data e hora}"
        print(f'\n{demonstrativo[0]}{demonstrativo[1]:.2f}. Dia {demonstrativo[2]}')
    print(f'Saldo final: {saldo}')    
    print(f'Um total de {i} operações')

def deposito(deposito, extrato):
    if deposito <= 0:
        return print('Operação impossível')
    else:
        agora = datetime.now()
        att_extrato =[]
        att_extrato.append('Depósito de +R$:')
        att_extrato.append(int(deposito))
        att_extrato.append(agora.strftime("%d/%m/%Y às %H:%M"))
        return  extrato


#def deposito(saldo, valor, extrato):


#def extrato(saldo,/,extrato):


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
        #print(user[0]) Como usamos .append não sobrescrevemos o primeiro valor. 
        #print(user[1]) A partir daqui será incrementado os novos registros.
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