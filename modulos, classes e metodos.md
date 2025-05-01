# 🛠️ Módulos e Classes no Python

## 📂 Módulos
Módulos são arquivos que contêm código reutilizável. Digamos um novo arquivo Python chamado `meu_modulo.py`:

```python
def saudacao(nome):
    return f"Olá, {nome}!"
```

Esse módulo pode ser importado para outro arquivo através de:

```python
import meu_modulo
```

Podemos importar o **módulo inteiro** ou apenas **partes específicas** dele. Se quisermos apenas a função `saudacao`, podemos fazer:

```python
from meu_modulo import saudacao
```

Assim, compreendemos que o módulo é como qualquer outro arquivo Python contendo um algoritmo. A utilidade de se criar módulos é ter uma **caixa de ferramentas**, onde podemos reutilizar trechos de código e garantir melhor organização.

---

## 🏗️ Classes: Atributos e Métodos
As classes possuem **atributos** e **métodos**.

### ✨ Atributos
Os **atributos** são informações específicas dentro da classe, como cor, modelo e ano.

```python
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
```

Aqui, `meu_carro` tem atributos que definem suas características.

### ⚙️ Métodos
Os **métodos** são funções dentro da classe que definem **comportamentos**. Exemplo: um método `ligar()` que faz o carro "ligar".

```python
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
```

🔹 **Atributos** armazenam informações sobre um objeto.  
🔹 **Métodos** definem comportamentos que os objetos podem executar.

---

## 🏷️ Instâncias e Objetos
Um **objeto** (ou **instância**) de classe é tudo aquilo que é criado a partir dos **moldes** da classe.  

Uma instância **possui atributos** da classe e pode **executar os métodos** dela.

```python