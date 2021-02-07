# Modelo computacional - ROSS

Nesta pasta estão os arquivos relacionados à modelagem computacional da bancada utilizando o software open source [ROSS Rotordynamics](https://github.com/ross-rotordynamics/ross).

Este programa foi escrito em *Python* e testado na versão **3.6**.

Segundo a documentação oficial, ROSS (*Rotordynamics Open Source Software*) é uma biblioteca criada para auxiliar em análises de sistemas dinâmicos rotativos, permitindo a construção de modelos de rotores e sua simulação numérica.

Os elementos do eixo, por padrão, são modelados observando a teoria de viga de Timoshenko, que considera os efeitos do cisalhamento e da inércia rotativa, sendo discretizados por meio do método de elementos finitos.

Os discos são considerados corpos rígidos, portanto sua energia de deformação é nula. Os rolamentos/vedações são incluídos como coeficientes de rigidez/amortecimento linear.

Após definir os elementos do modelo é possível plotar sua geometria e executar simulações que geram dados úteis para diversas análises como: diagrama de Campbell, modos de vibrar, resposta em frequência, e resposta temporal.

### Instalação

```bash
# UBUNTU 20.04 - Focal Fossa

# instalar pip3
$ sudo apt install python3-pip

# instala o pacote ross
$ pip3 install ross-rotordynamics

# executar o projeto
$ cd <pasta_com_codigo>
$ python3 index.py
```

---
Vinícius Gajo Marques Oliveira, 2021