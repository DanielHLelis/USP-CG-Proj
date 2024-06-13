---
title: "Lista de Exercícios 1 - Teoria"
author: "D. H. Lelis - 12543822"
date: 28/05/2024
---

## Exercício 1

> O que são e por qual motivo utilizar coordenadas homogêneas para especificar
> transformações geométricas em CG?

O uso de coordenadas homogêneas é importante para representar transformações
por simplificar a representação de operações e padronizar as operações de
maneira independente da dimensão do espaço, isso porque coordenadas homogêneas
permitem a representação das principais transformações geométricas (translação,
rotação, escala, projeção) de maneira unificada e simples através de matrizes,
permitindo a composição de transformações e a representação de transformações
afins e projetivas. Juntamente a isso, essa padronização permite o desenvolvimento
de hardware e software para computação gráfica de maneira mais eficiente e
otimizada, simplificando a implementação de algoritmos e a representação de
objetos e cenas.

## Exercício 2

> Apresente a matriz que representa uma transformação geométrica
> consistindo de uma translação seguida de uma rotação.

Dada a forma geral das matrizes de translação ($T$) e rotação ($R$), podemos
representar uma transformação geométrica composta por uma translação seguida
de uma rotação como a multiplicação dessas matrizes, ou seja, $M = R \cdot T$.

$$
T = \begin{bmatrix}
  1 & 0 & t_x \\
  0 & 1 & t_y \\
  0 & 0 & 1
\end{bmatrix}
$$

$$
R = \begin{bmatrix}
  \cos(\theta) & -\sin(\theta) & 0 \\
  \sin(\theta) & \cos(\theta) & 0 \\
  0 & 0 & 1
\end{bmatrix}
$$

$$
M = R \cdot T = \begin{bmatrix}
  \cos(\theta) & -\sin(\theta) & t_x \cos(\theta) - t_y \sin(\theta)\\
  \sin(\theta) & \cos(\theta) & t_x \sin(\theta) + t_y \cos(\theta) \\
  0 & 0 & 1
\end{bmatrix}
$$

## Exercício 3

> Apresente a matriz que representa uma transformação consistindo de
> uma translação tx=2 e ty=6 seguida de uma escala uniforme s=2.

Dada a forma geral da matriz de escala ($S$):

$$
S = \begin{bmatrix}
  s_x & 0 & 0 \\
  0 & s_y & 0 \\
  0 & 0 & 1
\end{bmatrix}
$$

Podemos representar a transformação proposta da seguinte forma:

$$
\left[\begin{matrix}2 & 0 & 0\\0 & 2 & 0\\0 & 0 & 1\end{matrix}\right] 
\cdot
\left[\begin{matrix}1 & 0 & 2\\0 & 1 & 6\\0 & 0 & 1\end{matrix}\right]
=
\left[\begin{matrix}2 & 0 & 4\\0 & 2 & 12\\0 & 0 & 1\end{matrix}\right]
$$

## Exercício 4

> Verifique se R(M+D) irá obter a mesma matriz de transformação do
> que R(M)*R(D).

Seja:

$$
R(M+D) = \begin{bmatrix}
  \cos(M+D) & -\sin(M+D) & 0 \\
  \sin(M+D) & \cos(M+D) & 0 \\
  0 & 0 & 1
\end{bmatrix}
$$

e

$$
\begin{aligned}
R(M) \cdot R(D) & = \begin{bmatrix}
  \cos(M) & -\sin(M) & 0 \\
  \sin(M) & \cos(M) & 0 \\
  0 & 0 & 1
\end{bmatrix}
\cdot
\begin{bmatrix}
  \cos(D) & -\sin(D) & 0 \\
  \sin(D) & \cos(D) & 0 \\
  0 & 0 & 1
\end{bmatrix}
\\
& =
\left[\begin{matrix}- \sin{\left(D \right)} \sin{\left(M \right)} + \cos{\left(D \right)} \cos{\left(M \right)} & - \sin{\left(D \right)} \cos{\left(M \right)} - \sin{\left(M \right)} \cos{\left(D \right)} & 0\\\sin{\left(D \right)} \cos{\left(M \right)} + \sin{\left(M \right)} \cos{\left(D \right)} & - \sin{\left(D \right)} \sin{\left(M \right)} + \cos{\left(D \right)} \cos{\left(M \right)} & 0\\0 & 0 & 1\end{matrix}\right]
\end{aligned}
$$

tomando as seguintes identidades trigonométricas:

$$
\begin{aligned}
  \cos(M+D) &= \cos(M) \cos(D) - \sin(M) \sin(D) \\
  \sin(M+D) &= \sin(M) \cos(D) + \cos(M) \sin(D)
\end{aligned}
$$

podemos verificar que $R(M+D) = R(M) \cdot R(D)$, já que podemos as
transformações trigonométricas em $R(M) \cdot R(D)$, obtendo:

$$
\begin{aligned}
  R(M) \cdot R(D) & =
  \left[\begin{matrix}
  \cos{\left(M \right)} \cos{\left(D \right)} - \sin{\left(M \right)} \sin{\left(D \right)}
    & - \left(\sin{\left(M \right)} \cos{\left(D \right)} + \cos{\left(M \right)} \sin{\left(D \right)} \right) & 0
  \\
    \sin{M} \cos{D} + \cos{M} \sin{D}
    & \cos(M) \cos(D) - \sin(M) \sin(D) & 0
  \\
    0 & 0 & 1
  \end{matrix}\right]
  \\
  & =
  \begin{bmatrix}
    \cos(M+D) & -\sin(M+D) & 0 \\
    \sin(M+D) & \cos(M+D) & 0 \\
    0 & 0 & 1
  \end{bmatrix}
\end{aligned}
$$

## Exercício 5

> Forneça a matriz de transformação que realiza a transformação
> abaixo (a seta indica o objeto inicial e o final após a transformação). Em
> seguida, apresente as coordenadas do objeto para uma escala uniforme
> s=2.
>
> (A imagem indica uma translação de (20,20) para (100, 80))

$$
T = \left[\begin{matrix}1 & 0 & 80\\0 & 1 & 60\\0 & 0 & 1\end{matrix}\right]
$$

$$
S = \left[\begin{matrix}2 & 0 & 0\\0 & 2 & 0\\0 & 0 & 1\end{matrix}\right]
$$

$$
M = S \cdot T = \left[\begin{matrix}2 & 0 & 160\\0 & 2 & 120\\0 & 0 & 1\end{matrix}\right]
$$

## Exercício 6

> Abaixo é apresentada a matriz resultante de quatro transformações.
> Aplique esta transformação em triângulo ABC (A=(0,0), B=(1,0),
> C=(0,1)) e mostre o resultado (novos vértices e o desenho). Em
> seguida, faça uma translação tx=M/10 e ty=M/10.

Translação pós transformação:

$$
T = \left[\begin{matrix}1 & 0 & 0.2\\0 & 1 & 0.2\\0 & 0 & 1\end{matrix}\right]
$$

Nova transformação:

$$
T \cdot M = \left[\begin{matrix}1.2 & -1 & 3.2\\1.6 & 2 & -1.8\\0 & 0 & 1\end{matrix}\right]
$$

Aplicando a transformação no triângulo ABC, teremos:

$$
\begin{aligned}
  A' & = T \cdot M \cdot A = \left[\begin{matrix}3.2\\-1.8\\1\end{matrix}\right] \rightarrow (3.2, -1.8) \\
  B' & =  T \cdot M \cdot B = \left[\begin{matrix}4.4\\-0.2\\1\end{matrix}\right] \rightarrow (4.4, -0.2) \\
  C' & =  T \cdot M \cdot C = \left[\begin{matrix}2.2\\0.2\\1\end{matrix}\right] \rightarrow (2.2, 0.2) \\
\end{aligned}
$$

## Exercício 7

> Mostre que a ordem das transformações pode modificar a matriz de
> transformação resultante (problema da comutatividade). OBS: É
> suficiente fornecer um exemplo.

A múltiplicação de matrizes não é comutativa, ou seja, $A \cdot B \neq B \cdot A$, a depender
dos valores de $A$ e $B$. Por exemplo, considere as matrizes:

$$
A = \left[\begin{matrix}1 & 0 & 10\\0 & 1 & 10\\0 & 0 & 1\end{matrix}\right]
$$

$$
B = \left[\begin{matrix}0 & -1 & 0\\1 & 0 & 0\\0 & 0 & 1\end{matrix}\right]
$$

Temos que $A \cdot B = \left[\begin{matrix}0 & -1 & 10\\1 & 0 & 10\\0 & 0 & 1\end{matrix}\right]$
e  $B \cdot A = \left[\begin{matrix}0 & -1 & -10\\1 & 0 & 10\\0 & 0 & 1\end{matrix}\right]$, ou
seja, a ordem das transformações altera o resultado final.

## Exercício 8

> As transformações de rotação e escala são comutativas entre si?
> OBS: a ordem da multiplicação dessas transformações altera a matriz
> de transformação resultante?

Sim, as transformações de rotação e escala são comutativas entre si, como
pode ser demonstrado pela aplicação da forma geral das matrizes de rotação
e escala:

$$ 
R \cdot S = \left[\begin{matrix}s_{x} \cos{\left(\theta \right)} & - s_{y} \sin{\left(\theta \right)} & 0\\s_{x} \sin{\left(\theta \right)} & s_{y} \cos{\left(\theta \right)} & 0\\0 & 0 & 1\end{matrix}\right]
$$

$$
S \cdot R = \left[\begin{matrix}s_{x} \cos{\left(\theta \right)} & - s_{x} \sin{\left(\theta \right)} & 0\\s_{y} \sin{\left(\theta \right)} & s_{y} \cos{\left(\theta \right)} & 0\\0 & 0 & 1\end{matrix}\right]
$$

Como podemos ver, a ordem das transformações não altera o resultado final.

## Exercício 9

> As transformações de translação e escala são comutativas entre si?
> E entre translação e rotação?

As transformações de translação e escala não são comutativas entre si,
como pode ser visto na aplicação das matrizes de translação e escala:

$$
T \cdot S = \left[\begin{matrix}s_{x} & 0 & t_{x}\\0 & s_{y} & t_{y}\\0 & 0 & 1\end{matrix}\right]
$$

$$
S \cdot T = \left[\begin{matrix}s_{x} & 0 & s_{x} t_{x}\\0 & s_{y} & s_{y} t_{y}\\0 & 0 & 1\end{matrix}\right]
$$

Como pode ser visto, a ordem das transformações altera o resultado final,
com a aplicação da escala após a translação resultando em um deslocamento
maior.


As transformações de translação e rotação também não são comutativas entre si,
como pode ser visto na aplicação das matrizes de translação e rotação:

$$
T \cdot R = \left[\begin{matrix}\cos{\left(\theta \right)} & - \sin{\left(\theta \right)} & t_{x}\\\sin{\left(\theta \right)} & \cos{\left(\theta \right)} & t_{y}\\0 & 0 & 1\end{matrix}\right]
$$

$$
R \cdot T = \left[\begin{matrix}\cos{\left(\theta \right)} & - \sin{\left(\theta \right)} & t_{x} \cos{\left(\theta \right)} - t_{y} \sin{\left(\theta \right)}\\\sin{\left(\theta \right)} & \cos{\left(\theta \right)} & t_{x} \sin{\left(\theta \right)} + t_{y} \cos{\left(\theta \right)}\\0 & 0 & 1\end{matrix}\right]
$$

Como pode ser visto, a ordem das transformações altera o resultado final,
fazendo com que a rotação após a translação altere o referencial de rotação.


## Exercício 10

> Forneça a sequência de transformações que leva o triângulo T1 ao
> triângulo T2 e dê a matriz resultante.

Primeiramente, vamos levar o triângulo T1 para a origem, facilitando a rotação,
para isso, podemos fazer uma translação de $-P1 = (-5, -2)$, na sequência, 
aplicamos a rotação de $90\deg$ em sentido anti-horário, que levará T1 para a 
mesma orientação de T2, porém fora de posição, agora basta corrigir a posição do 
referencial P1, fazendo a translação de $P1' = (4, 1)$. A forma matricial dessas 
transformações é dada por:

$$
M =
\left[\begin{matrix}1 & 0 & -5\\0 & 1 & -2\\0 & 0 & 1\end{matrix}\right]
\cdot
\left[\begin{matrix}0 & -1 & 0\\1 & 0 & 0\\0 & 0 & 1\end{matrix}\right]
\cdot
\left[\begin{matrix}1 & 0 & 4\\0 & 1 & 1\\0 & 0 & 1\end{matrix}\right]
=
\left[\begin{matrix}0 & -1 & 6\\1 & 0 & -4\\0 & 0 & 1\end{matrix}\right]
$$

Verificando para os pontos propostos, conseguimos ver que a transformação é correta:

$$
\begin{aligned}
  P1' & = M \cdot P1 = \left[\begin{matrix}4\\1\\1\end{matrix}\right] \rightarrow (4, 1) \\
  P2' & = M \cdot P2 = \left[\begin{matrix}4\\7\\1\end{matrix}\right] \rightarrow (4, 7) \\
  P3' & = M \cdot P3 = \left[\begin{matrix}0\\4\\1\end{matrix}\right] \rightarrow (0, 4) \\
\end{aligned}
$$

## Exercício 11

> Seja um quadrado de lado L=5, inicialmente posicionado em x=M e
> y=D. Calcule e apresente a matriz de transformação que faça o
> quadrado rotacionar 45 graus em relação ao seu próprio centro.
> Apresente os vértices iniciais e finais do quadrado.

Para rotacionar um objeto em torno de seu próprio centro,
primeiro transladamos seu centro para a origem, rotacionamos
e transladamos de volta. Para um quadrado de lado $L=5$, 
$M = 2$ e $D = 6$. Assumiremos que o posicionamento inicial
é relativo ao ponto inferior esquerdo do quadrado, o que implica
que teremos que transladar o quadrado em:
$\left(-(2 + 2.5), -(6 + 2.5)\right) = (-4.5, -8.5)$, além disso,
assumiremos que a rotação será no sentido anti-horário. Sendo assim, 
teremos as seguintes transformações:

$$
\begin{aligned}
  T_1 & = \left[\begin{matrix}1 & 0 & -4.5\\0 & 1 & -8.5\\0 & 0 & 1\end{matrix}\right] \\
  R & = \left[\begin{matrix}\frac{\sqrt{2}}{2} & - \frac{\sqrt{2}}{2} & 0\\\frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2} & 0\\0 & 0 & 1\end{matrix}\right] \\
  T_2 & = \left[\begin{matrix}1 & 0 & 4.5\\0 & 1 & 8.5\\0 & 0 & 1\end{matrix}\right] \\
\end{aligned}
$$

A matriz de transformação final será dada por:

$$
\begin{aligned}
  M & = T_2 \cdot R \cdot T_1 = \left[\begin{matrix}\frac{\sqrt{2}}{2} & - \frac{\sqrt{2}}{2} & 2.0 \sqrt{2} + 4.5\\\frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2} & 8.5 - 6.5 \sqrt{2}\\0 & 0 & 1\end{matrix}\right] \\
  & \approxeq \left[\begin{matrix}0.707 & -0.707 & 7.33\\0.707 & 0.707 & -0.692\\0 & 0 & 1\end{matrix}\right]
\end{aligned}
$$

## Exercício 12

> Dado um vértice/ponto posicionado em x=D e y=M, apresente as
> matrizes de transformação para (1) espelhar esse vértice em relação ao
> eixo X e (2) espelhar esse vértice em relação ao eixo Y.

O proceso de espelhar um vértice em relação ao eixo X é simplesmente
inverter o sinal de sua coordenada y, enquanto que para o eixo Y, invertemos
o sinal da coordenada x. Sendo assim, as matrizes de transformação para
espelhar um vértice em relação ao eixo X e Y são dadas por:

$$
\begin{aligned}
  M_X & = \left[\begin{matrix}1 & 0 & 0\\0 & -1 & 0\\0 & 0 & 1\end{matrix}\right] \\
  M_Y & = \left[\begin{matrix}-1 & 0 & 0\\0 & 1 & 0\\0 & 0 & 1\end{matrix}\right] \\
\end{aligned}
$$

## Exercício 13

> Pesquisa e descreva sobre as matrizes de transformação 3D para
> fazer espelhamento de um objeto.

Para realizar o espelhamento de um objeto em 3D, podemos utilizar
as matrizes de transformação homogêneas para realizar a operação
de espelhamento em relação a um dos planos de projeção.  A versão
generalizada para o espelhamento de um objeto em relação a um plano
$ax + by + cz + d = 0$  em um espaço 3D é dada por:

$$
\begin{bmatrix}
  1 - 2a^2 & -2ab & -2ac & -2ad \\
  -2ab & 1 - 2b^2 & -2bc & -2bd \\
  -2ac & -2bc & 1 - 2c^2 & -2cd \\
  0 & 0 & 0 & 1
\end{bmatrix}
$$

onde $a$, $b$ e $c$ são os coeficientes do plano de projeção e $d$ é a
distância do plano à origem. Tomemos como exemplo o espelhamento em relação
ao plano $z = 0$ (XY), a matriz de transformação será dada por:

$$
\begin{bmatrix}
  1 & 0 & 0 & 0 \\
  0 & 1 & 0 & 0 \\
  0 & 0 & -1 & 0 \\
  0 & 0 & 0 & 1
\end{bmatrix}
$$

Referência: <https://en.wikipedia.org/wiki/Transformation_matrix#Reflection_2>

## Exercício 14

> Explique, com suas palavras, o mapeamento 2D de uma imagem de
> textura para um objeto 3D (apresente pelo menos 3 tipos de
> mapeamento).

O mapeamento de texturas em objetos 3D consiste de uma técnica onde
colore-se um objeto 3D com uma imagem 2D, de forma a adicionar detalhes
e realismo ao objeto. Para isso, tratamos a imagem 2D como uma textura
onde cada pixel é chamado de texel e mapeamos esses texels nos vértices
durante a renderização do objeto 3D. Fazendo o mapeamento das coordenadas
uv dos vértices do objeto para as coordenadas ts da textura. Existem diversos 
tipos de mapeamento de texturas, dentre os quais podemos citar:

1. **Mapeamento planar**: no mapeamento planar, mapeia-se de maneira ortogonal
  a textura em um dos planos do objeto, como XY, XZ ou YZ. Esse mapeamento
  é bastante simples e eficiente, porém resulta em distorções em objetos
  com muita curvatura ou que não são paralelos ao plano de projeção.
2. **Mapeamento cúbico**: o mapeamento cúbico é análogo ao mapeamento planar,
  porém mapeia-se a textura nos seis lados de um cubo que envolve o objeto. Esse
  mapeamento é mais complexo, porém permite uma melhor distribuição da textura
  em objetos mais complexos.
3. **Mapeamento esférico**: o mapeamento esférico mapeia as coordenadas uv de
  acordo com as coordenadas polares esféricas do objeto, permitindo uma melhor
  distribuição da textura em objetos esféricos ou que possuam uma curvatura
  esférica. Em contrapartida, esse mapeamento é mais complexo e menos eficiente
  que os anteriores.

## Exercício 15

> Em texturas, explique a relação entre Pixels e Texels.

Os texels são os pixels originais da textura, ou seja, cada texel
corresponde a um pixel da imagem de textura. Durante o processo de
renderização os texels são mapeados nos vértices do objeto 3D, porém,
dependendo da resolução da textura e do objeto, um pixel pode corresponder
a vários texels ou vice-versa. Sendo assim, quanto mais pixels na textura,
mais texels teremos para mapear no objeto, resultando em uma textura mais
detalhada e realista. Quanto mais texels e os parâmetros de mapeamento,
maior será a qualidade da textura no objeto 3D no processo de renderização
onde são computados os valores dos pixels da tela.

## Exercício 16

> Na parametrização de texturas, explique a diferença entre os
> parâmetros REPEAT e CLAMP.

Os parâmetros REPEAT e CLAMP são utilizados para definir o comportamento
da textura quando as coordenadas uv dos vértices do objeto ultrapassam
os limites da textura. O parâmetro REPEAT faz com que a textura seja
repetida ao ultrapassar os limites, ou seja, a textura é repetida várias
vezes ao longo do objeto. Já o parâmetro CLAMP faz com que a textura
seja "esticada" ao ultrapassar os limites, ou seja, a última linha ou
coluna da textura é repetida ao longo do objeto. O parâmetro REPEAT é
útil para texturas que não possuem bordas ou que são simétricas, enquanto
que o parâmetro CLAMP é útil para texturas que possuem bordas ou que
não podem ser repetidas.

## Exercício 17

> Durante o mapeamento de pixels e texels, qual a diferença entre as
> técnicas LINEAR e NEAREST?

As técnicas LINEAR e NEAREST são utilizadas para interpolar os valores
dos texels ao mapeá-los nos pixels da tela. A técnica NEAREST simplesmente
seleciona o texel mais próximo do pixel, resultando em uma interpolação
mais brusca e com artefatos visuais, porém é mais eficiente computacionalmente.
Já a técnica LINEAR interpola linearmente os valores dos texels mais próximos
do pixel para obter um valor intermediário por meio de uma média, resultando
em uma interpolação mais suave e realista, porém é mais custosa computacionalmente.
A técnica LINEAR é recomendada para texturas de alta resolução e objetos próximos
à câmera, enquanto que a técnica NEAREST é recomendada para texturas de baixa
resolução e objetos distantes.
