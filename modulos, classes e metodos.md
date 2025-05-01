Módulos são arquivos que contêm código. Digamos um novo arquivo python:
meu_modulo.py

Que contém:

def saudacao(nome):
    return f"Olá, {nome}!"

Ele pode ser importado para outro arquivo através do Import meu_modulo
Módulos inteiros ou apenas classes/funções/objetos e por fim variáveis.
Assim se não quiser um módulo inteiro e só quiser uma função:

From meu_modulo Import saudacao

Assim que se compreende que o módulo é como qualquer arquivo nosso contendo um algoritmo
Fica fácil de entender a diferença entre o módulo e nosso arquivo contendo o projeto normal.
Pois a utilidade de se criar módulos é de se ter uma caixa de ferramentas.
Através de um módulo podemos reutilizar trechos de código.
Garantindo organização.

As classes possuem atributos e métodos.

Os atributos são as informações específicas dentro da classe. Como cor, modelo e ano.

class Carro:
    def __init__(self, cor, modelo, ano):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano

# Criando um objeto da classe Carro
meu_carro = Carro("Vermelho", "Fusca", 1970)

print(meu_carro.cor)  # Saída: Vermelho
print(meu_carro.modelo)  # Saída: Fusca
print(meu_carro.ano)  # Saída: 1970

Meu_carro tem seus atributos que definem as suas características.

Já sobre métodos, são funções dentro da classe que definem comportamento. Como por exemplo Ligar.

class Carro:
    def __init__(self, cor, modelo, ano):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano

    def ligar(self):
        print(f"O {self.modelo} está ligado!")

# Criando uma instância
meu_carro = Carro("Vermelho", "Fusca", 1970)
meu_carro.ligar()  # Saída: O Fusca está ligado!

Atributos armazenam informações sobre um objeto.

Métodos definem comportamentos que os objetos podem executar.

Agora objetos ou instância de classe é tudo aquilo que é criado a partir dos moldes da Classe.
Uma instância possui os atributos da Classe e poderá realizar os métodos da mesma.
Então qualquer variável que você tenha que receba valores tratados por uma classe são um objeto.
E isso se aplica a classes internas do python também:
Se você cria uma Var que recebe integrais, strings, listas ou dicionários você está criando um objeto da classe deles.
int, str, dict, list são todos Classes do python.

Módulo → Arquivo que contém código reutilizável. Pode conter várias classes, funções e variáveis.

Classe → Define um tipo de objeto, com atributos e métodos.

Função → Bloco de código dentro de um módulo ou classe que realiza uma ação específica.

Objeto → Instância de uma classe, criada para armazenar dados e funcionalidades.

Variável → Nome que armazena um valor, que pode ser um objeto de uma classe.
