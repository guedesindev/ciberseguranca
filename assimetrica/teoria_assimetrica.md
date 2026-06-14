## Criptografia Assimétrica

Na outra sessão, expus que para um chat simples, ambos os usuários teriam de ter uma mesma chave para que a mensagem cifrada pudesse ser decifrada por ambos, usando a mesma mensagem da cifragem. Isso é um processo chamado criptografia simétrica, em que uma única chave é usada para cifrar e decifrar. Este tipo de criptografia tem suas desvantagens como o perigo de compartilhar a chave de criptografia, que pode ser minimizado utilizando o algoritmo Diffie-Hellman. Outro inconveninente é a complexidade da escalabilidade o gerenciamento de chaves pelo sistema massivo e impraticável para uma quantidade grande de usuários, quanto maior o número de usuários. Há uma outra dificuldade conhecida como `falta de não repúdio`. O que é isso? Uma vez que a chave é compartilhada, não há um método matemático de comprovar quem cifrou uma mensagem, tornando complicado o processo de atribuir uma mensagem a um usuário, este gerênciamento deve ser feito por outros métodos que não o reconhecimento da chave de cifragem.

Para amenizar tais situações, pensou-se em um processo mais seguro, e que a chave de decifragem não fosse compartilhado, que apenas um lado da comunicaçaõ a obtivesse. Este processo é um pouco mais lento que a criptografia simétrica, mas é mais seguro. É a `criptografia assimétrica`.

Agora cada usuário possui dois códigos um para cifragem e outro para decifragem. O código para cifragem pode ser público, qualquer um que tenha esta chave pode enviar uma mensagem, entretanto, a decifragem só é possível pelo destinatário.

**Por que é seguro**

Para a criação das duas chaves, utiliza-se da dificuldade matemática de fatorar números muito grandes compostos por dois primos.

**Como Funciona?**

Imagine que uma pessoa quer enviar um pacote para outra, mas quer ter certeza que apenas o destinatário possa abrí-lo. Vamos supor que este pacote seja uma caixa. Aí o remetente diz para o destinatário: "Manda pra mim um cadeado que só você tenha a chave". O remetente recebe o cadeado e trava a caixa com este cadeado, cadeado este feito de titânio que nenhum alicate possa quebrar, nenhum pé-de-cabra possa forçá-lo e que fosse à prova da utilização de artefatos que forcem o segredo, ou que a quantidade de pinos do segredo fosse tão grande que ninguém conseguisse usar um grampo de aço para cabelo.

Então o destinatário recebe a caixa e abre com a chave que apenas ele possui. Tá a análogia do cadeado é legal, mas e se mais de uma pessoa quiser enviar pacotes ao mesmo tempo? Aí é que está a coisa, o destinatário tem vários cadeados e possui uma chave mestra que abre todos eles, então, pode enviar o cadeado para trancar vários pacotes ao mesmo tempo e poderá abrir todos eles com a mesma chave gran-mestra.

![Chave Gran-Mestra](.\images\chave_gran_mestra.jpeg)

Os cadeados podem ser compartilhados com qualquer um, desde que a chave seja de posse apenas do destinatário.

Esta é a diferença entre criptografia simétrica e assimétrica. Se o usuário "A" tiver chats com 1000 usuários diferentes, será necessário compartilhar 1000 segredos diferentes. Agora imagine os 1000 usuários podendo se comunicar entre si, quantas chaves serão necessárias?
$$ \frac{1000 * (100-1)}{2} $$

E isso cresce a cada usuário, para ficar genérico pense que são "N" usuários então a quantidade de chaves que precisam ser gerenciados pelo sistema é:
$$ \frac{N * (N-1)}{2} $$

Já na criptografia assimétrica cada usuário possui 2 chaves, uma para cifragem e outra para decifragem, a chave para cifragem não é segredo é pública então é a mesma chave enviada para todos os $"N-1"$ usuários do sistema, já a chave secreta é a mesma para qualquer mensagem recebida. Quanta economia de processamento e espaço em banco de dados, não é verdade?

## Mas como os pares de chaves são gerados?

Inicialmente 3 números são gerados aleatoriamente, vamos chamar esses números de *e*, *p* e *q*. O *e* é o número que fará parte da chave pública e *p* e *q* farão parte da chave privada.

Como fazer com que exista uma relação entre *e*, *p* e *q*?

Um número *n* é gerado e com ele é obtida a chave pública ao relacioná-lo com expoente *e*. Mas de onde surge esse *n* e de onde surge *e*?

Ao fazer $ p \times q = n$, deste modo, *n* é um número composto, que podemos chamá-lo de número semiprimo, pois é  dependente de *p* e *q* dois números primos. Logo a chave pública e a chave privada estão relacionadas entre si.

A geração do expoente *e* segue um:

1 - Deve ser maior que 1 e menor que Totiente. `Totiente`? Sim, a função Totiente também é conhecida como função de Euler.

Esta função é definida como a quantidade de números inteiros co-primos com um número $n$ entre $1$ e esse $n-1$

Vou fugir aqui de uma explicação matemática mais profunda e vou direto a um exemplo que torne o conceito fácil de entender.

Por exemplo,

```Matemática
Suponha que queira encontrar a quantidade de coprimos de 8.
Então pegamos os números entre 1 e 8 e vejamos possuem como divisor comum apenas o 1.
```

Entenda o que são números coprimos com o exemplo abaixo:

8 e 9, apesar de serem números compostos, são copirmos entre si?
Chamaremos o conjunto dos divisores de 8 de $D_8$ e os divisores de 9 de $D_9$

Temos:
$$ D_8 = { 1, 2, 4, 8}$$
$$ D_9 = { 1, 3, 9 } $$

Para os conjuntos acima vemos que a interseção
$$ D_8 \cap D_9 = {1}$$

A função $\phi$ ou Função de Eule (pronuncia-se Óiler) retorna a quantidade de números coprimos de n entre 1 e n.

Veja agora o cálculo da função phi para o número 8

| Par | É coprimo de 8? |
|:---:|:---:|
| 8 e 1 | Sim |
| 8 e 2 | Não, pois 2 é divisor de 8|
| 8 e 3 | Sim |
| 8 e 4 | Não, pois 4 é divisor de 8 |
| 8 e 5 | Sim |
| 8 e 6 | Não, pois 2 é divisor de 6 e 8|
| 8 e 7 | Sim |

Assim $ \phi(8) = 4 $

Um atalho, para n composto, $ \phi(n) = \phi(p^k) = p^k - p^{k-1} $
O que esta notação significa?

$ \phi(8) = \phi(2^3) = 2^3 - 2^{3-1} = 8 - 4 = 4 $

Agora quando n for primo é o que importa para a criptografia RSA.

$ \phi(n) = n - 1$

Agora finalmente sabemos como calcula-se *e* da chave pública.

Primeira regra, estar entre 1 e Totiente de n (que é o produto entre p e q)
Segunda regra, ser coprimo do Totiente.

Então para um exemplo válido, n deve ser o produto entre 2 números primos. Então supomos: p = 3 e q = 5. Desta forma n = 15;

$ \phi(15) = (p - 1)(q - 1) = (3-1)(5-1) = 2 * 4 = 8 $

Então a escolha para o expoente *e* precisa ser um número entre 1 e 8 que sejam coprimos, assim os possíveis números podem ser: {1, 3, 5, 7}, assim sendo o nº 3 pode ser a escolha para o expoente.

## Mas como uma mensagem é cifrada?

Para nossa mensagem de estudos vamos pensar em p e q números primos 233 e 347 respectivamente.

| chave pública | mensagem | chave privada
| :---:|:---:|:---:|
| e = 3, n = 80851 | O (original) | p = 233
| | C (cifrada)|  q = 347 |

Para esses valores encontramos um $\phi(n) = \phi(80851) = 80272$

**A escolha do expoente *e***:

O número 3 funciona, pois o Máximo Divisor Comum entre 3 e 80272 é 1.

**Cálculo da mensagem cifrada**
$$ O^e mod (n) \equiv C $$

**Cálculo da mensagem decifrada**
$$ C^d mod (n) \equiv O $$

Agora vamos conhecer aqui a tabela ASCII, pois a mensagem original e a mensagem decifrada utilizarão a mesma tabela, para os cálculos.

![Tabela ASCII](.\images\tabela_ascii_completa.jpeg)

A tabela acima traz uma conversão dos bytes utilizados para representar cada caractere do idioma em números inteiros.
Vamos supor que a `Alice` quer enviar a mensagem "Oi" para o `Bob`, como essa mensagem será cifrada?

**O aperto de mão entre Alice e Bob**

Nós já sabemos que *e* e *n* compõem a chave pública e isso quer dizer que não é segredo para ninguém. Então Bob gera o *e* e o *n* e compartilha com Alice.

Do lado de Alice a mensagem oi é codificada da seguinte forma

| Mesagem original (O) | Mensagem original ASCII |
| :---: | :---: |
| O = 79 <br> i = 105 | Oi = 79105 |

Para cifrar Alice faz:
$$ C = O^e (mod) 80851 $$

$$ C = 79105^3 (mod) 80851 \therefore C = 3790$$

Então Bob recebe a mensagem cifrada 3790.

Quando Bob recebe a mensagem cifrada de Alice faz o seguinte cálculo:

$$ C^d (mod n) $$

Ué mas quem é *d*? Até agora não falamos dele. Mas matematicamente sabemos que:

$$ ed \equiv 1(mod(p-1)(q-1))$$

sabemos também que $ e = 3, p = 3, q = 5 $
Então,
$$ ed \equiv 1(mod(p-1)(q-1)) $$
$$ 3d \equiv 1(mod(233-1)(347-1)) $$
$$ 3d \equiv 1(mod(232)(346)) $$
$$ 3d \equiv 1(mod(80272)) \implies 3d (mod(80272)) = 1$$

Qual número que multiplicado por 3 e dividido por 80272 deixa resto 1?

Ao proceder com este cálculo encontramos o valor de d.

Então se $$ 3d (mod(80272)) = 1 \therefore d = 53515 $$

Assim sendo, $$ C^d (mod(80851)) $$ resulta na mensagem original.
$$ 3790^{53515} (mod(80851)) \equiv  79105$$

Veja que agora Bob lê 79105.

Mas aí fica a perqunta:

Como que 79105 vira Oi e não outra coisa?

Como sabe que deve agrupar os bytes?

A transformação em binário impede a confusão.

Por exemplo:

Oi Em bytes vira:

| Letra | Decimal | Binário |
| :---: | :---: | :---: |
| O | 79 | 0100 1111 |
| i | 105 | 0110 1001 |

Este agrupamento, quando trasnmitido informa ao receptor como ler 79105. Só a título de curiosidade 😉.

Agora entendemos como funciona o algoritmo RSA de criptografia assimétrica que é o padrão ouro atualmente de segurança de menagens atualmente.
