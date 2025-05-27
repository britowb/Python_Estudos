from abc import ABC, abstractmethod
from datetime import datetime, date
class Cliente:
    def __init__(self, endereco):
        self.endereco : str = endereco
        self.contas : list = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf : str = cpf
        self._nome : str = nome
        self._data_nascimento : date = data_nascimento

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def data_nascimento(self):
        return self._data_nascimento        
              
class Conta:
    contador_contas = 0
    def __init__(self, numero, cliente):
        self._saldo : float = 0
        self._numero : int = numero
        self._agencia : str = "0001"
        self._cliente  = cliente
        self._historico = Historico()

    def mostrar_saldo(self):
        return print(f'Seu saldo é de R${self.saldo:.2f}')
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        conta = Conta(numero=int(numero), cliente=cliente )
        return conta
 
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico


    def sacar(self, valor):
        if self._saldo >= valor:
            self._saldo -= valor
            print('\nSaque realizado com sucesso!')
        elif valor > self._saldo:
            print('\nVocê não tem saldo suficiente')
            return False
        else:
            print('\nValor inválido')
            return False
        return True 

    def depositar(self, valor):
        if valor <= 0:
            print('\nValor inválido')
            return False
        else:
            self._saldo += valor
            print('\nDepósito realizado com sucesso.')
            return True
        
class ContaCorrente(Conta): #Aqui sobrescrevemos Conta. 
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite : float = limite
        self.limite_saques : int = limite_saques
    
    def __str__(self):
        return f'Conta Corrente - Agência: {self.agencia}, Número: {self.numero}, Saldo: R${self.saldo:.2f}'

    def sacar(self, valor):
        numero_saques = len([ transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        if self.historico.transacoes and numero_saques == 0:
            numero_saques+=1
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        if excedeu_limite:
            print('\nOperação falhou. Valor de saque excede o limite.')
        elif excedeu_saques:
            print('\nOperação falhou! Numero máximo de saques excedido')
        else:
            return super().sacar(valor)
        return False #Se opção 1 ou 2, então False.
    
class Historico: #Acessado pelo registrar que joga o depósito/saque (se declarados True pelo método depositar/sacar da conta) no histórico.
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def mostrar_transacao(self):
        if self._transacoes:
            for extratos in self._transacoes:
                print(f"{extratos['data']}: {extratos['tipo']} de R$ {extratos['valor']}")
        else:
            print('Não existem transações.')
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y às %H:%M"),
            }
        )

class Transacao(ABC): #Será através dessa classe abstrata que eu acessarei os fluxos de tratamento de dados referentes a Saque e Depósito 
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor : float = valor
 
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor) #Se o valor retornado for True, adicione ao histórico. Aqui está chamando diretamente da Classe Conta uma vez que ContaCorrente não sobrescreve depósito.
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)     

class Saque(Transacao):
    def __init__(self, valor):
        self._valor : float = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor) #Aqui ela chama o módulo SACAR da classe ContaCorrente.
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def registro_user(credencial): #DEF RESPONSAVEL POR CADASTRAR NOVOS USUARIOS.
     #nossos usuarios são registrados em chave-valor. Essa var irá alimentar o nosso registro de usuarios em chave-valor.
    nome = str(input('Digite seu nome').capitalize()) 
    while True:
        try:
            data_nascimento = int(input('Digite seu nascimento DD/MM/AAAA =>\n').replace('/','').replace(' ',''))
            break
        except ValueError:
            print('Apenas números, por favor.')
    cpf = str(credencial)# Aqui eu resgato o CPF que já foi informado e verificado.
    print('Agora seu endereço =>\n')
    endereco = registro_endereco() #Aqui alimentaremos a chave:valor endereço através da função registro_endereco.
    novo_user = PessoaFisica(cpf, nome, data_nascimento, endereco)
    return novo_user

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

def abrir_conta(user_unico, contabilidade): 
    print('Sua agência será 0001')
    print(f'\nSeu usuário é: {user_unico}')
    contabilidade +=1  # Vou atualizar a variavel responsavel pelo id das contas, o novo numero é o identificador da nova conta. Converto para string pois assim posso criar lista
    print(f'Numero da conta: {contabilidade}') 
    conta_nova = ContaCorrente(contabilidade, user_unico)
    Conta.contador_contas = contabilidade
    return conta_nova
         
        
def user_loggin(credencial_encontrada, contabilidade): #(Aqui verificamos dados com o cpf escolhido. Os dados verificados são da var user.)
    if credencial_encontrada == None:
        return
    print(credencial_encontrada) #Testar o retorno da variavel na def
    print(f'''
{user} Var user.
{credencial_encontrada} Var credencial_encontrada
{credencial_encontrada.cpf}''' ) #Testar o retorno da var na def
    while True: # RODA UM LOOP PARA QUE POSSA ALTERNAR ENTRE OPÇÕES
        opcoes = int(input(''' 
    1 - Listar contas    
    2 - Abrir conta
    3 - Operações bancárias
    4 - Sair
    => '''))
        if opcoes == 1: #LISTAR CONTAS
            if len(credencial_encontrada.contas):
                for conta in credencial_encontrada.contas:
                    if conta.historico:
                        print(ContaCorrente(conta.numero, conta.cliente))
                        print(conta.mostrar_saldo())
                    else:
                        print(ContaCorrente(conta.numero, conta.cliente))
                        print('Conta zerada.')           
            else:
                print('Não existem contas')
        elif opcoes == 2: # CRIAR CONTA
                verificar_usuario = input('Defina uma identificação para sua conta.\n=> ')
                if verificar_usuario in credencial_encontrada.contas:
                    print('Identificação já existe')
                    continue
                else:
                    contabilidade = Conta.contador_contas
                    credencial_encontrada.contas.append(abrir_conta(verificar_usuario, contabilidade))
                    print('Conta criada com sucesso')
        elif opcoes == 3:#Operações bancárias
            menu(credencial_encontrada)
    
        elif opcoes == 4: #SAIR
            break
        else:
            print('opção não encontrada. Digite o numero referente a opção desejada.')

def autentica(credencial): #Autenticador de login
    credencial_encontrada = next((usuario for usuario in user if usuario.cpf == credencial), None) 
    if credencial_encontrada is not None: 
        return credencial_encontrada
    else:
        return print('CPF não encontrado.')

def menu(credencial_encontrada):
    while True:
        if credencial_encontrada.contas:
            selecionar_conta = input('Digite o usuário')
            conta_logada = next(( select_conta for select_conta in credencial_encontrada.contas if selecionar_conta == select_conta.cliente), None) #Aqui vamos iterar sobre a lista contas e trabalhar com o valor específico de cada conta.
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
            entrada = input('Opção menu => ')
            menu = ['1', '2', '3', '4', '5'] 
            if entrada.isdigit():
                if entrada in menu:
                    op_menu = int(entrada)
                    break
                else:
                    print('opção inexistente')
                    print('Digite novamente!')
            else:
                print('Somente números, por favor.')
                continue
        if op_menu ==1:
                valor = float(input('\nDigite o valor que deseja sacar\t\n=> '))
                transacao1 = Saque(valor)
                transacao1.registrar(conta_logada)
                continue
        elif op_menu ==2:
                try:
                    valor = float(input('\nDigite o valor para depósito\t\n=> '))
                    transacao1 = Deposito(valor)
                    transacao1.registrar(conta_logada)
                except ValueError:
                     print('Somente números, por favor!')
                     continue
        elif op_menu ==3:
                conta_logada.historico.mostrar_transacao()
                continue
        elif op_menu ==4:
                conta_logada.mostrar_saldo()
                continue
        else:
            break

conta = []
user = [] #alimentado pela def registro_user
contabilidade = len(conta)
while True:
    escolha = int(input('''
                        1 - Logar
                        2 - Registrar-se
                        '''))
    if escolha == 1: #LOGAR
        try:
            credencial = input('Insira seu cpf').replace('-', '').replace('.','')
            credencial_encontrada = autentica(credencial)
            user_loggin(credencial_encontrada, contabilidade)
        except ValueError:
            print('Somente números, por favor.')
    elif escolha == 2: #REGISTRAR.
        credencial = input('Insira seu cpf').replace('-', '').replace('.','')
        if credencial.isdigit(): 
            credencial_encontrada = next((usuario for usuario in user if usuario.cpf == credencial), None)  
            if credencial_encontrada is not None:
                print('Cliente já cadastrado.')
                continue
            else:
                user.append(registro_user(credencial)) 
        else:
            print('Apenas números, por favor.')
    else:
        print('Opção inválida')
        continue
