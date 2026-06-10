## 📜 Um Pouco de História

Para entender o que é criptografia, vale a pena observar de onde surgiu a ideia e seus casos de uso que datam desde a antiguidade. Há milênios as pessoas possuem segredos que desejam proteger de terceiros, garantindo que tais mensagens alcancem apenas as partes de interesse.

A criptografia nada mais é do que o ato de embaralhar um conteúdo utilizando uma sequência lógica de ações que pode ser revertida. Se a criptografia não puder ser desfeita, ela perde o sentido, pois o conteúdo original seria perdido por completo — para isso, melhor seria apenas descartar o dado.

Vemos os primeiros sinais dessa prática no Egito Antigo com os hieróglifos, que consistiam na substituição de letras ou palavras por figuras para manter os segredos ocultos. Anterior à era dos computadores, métodos clássicos como a **Cifra de César** operavam por substituição simples: cada caractere era trocado pelo elemento que estava três posições à sua frente no alfabeto. Por ser um padrão fixo e linear, era uma cifra muito fácil de ser quebrada.

#### Exemplo da Cifra de César

A palavra `criptografia` viraria `fumsxrjudimd`.

### A evolução das chaves e a Cifra de Ottendorf

Com o tempo, introduziu-se o conceito de **chave criptográfica**. Uma forma de tornar mesmo os métodos de substituição mais complexos, garantindo que a decifragem só fosse possível se você estivesse em posse da chave correta.

Em livros e filmes de espionagem, é comum vermos mensagens cuja chave está oculta nas páginas de uma obra literária específica. Essa é a mecânica da **Cifra de Ottendorf**.

Para que funcione, o remetente e o destinatário precisam possuir exatamente o mesmo livro e a mesma edição. A cifra consiste em uma sequência numérica que aponta para: o número da página ($np$), o número da linha ($nl$) e a posição da palavra na linha ($pp$), contando da esquerda para a direita.

* **Formato do Código:** `121.7.5` $\rightarrow$ Página 121, linha 7, palavra 5.

#### Pontos Fortes

* **Resistência à força bruta:** Não há uma estrutura matemática óbvia para quebrar o código. O atacante precisaria descobrir o livro físico exato e a sua respectiva edição.
* **Segurança por obscuridade:** A mensagem parece apenas uma lista aleatória de números. Se o atacante sequer souber que se trata de uma Cifra de Ottendorf, os números jamais farão sentido.

#### Pontos Fracos

* **Padrões linguísticos:** Mensagens longas fatalmente repetem palavras comuns (como preposições e artigos), abrindo brechas para a análise de frequência.
* **Dependência total do meio:** Se o destinatário perder o seu exemplar do livro, a mensagem torna-se permanentemente inutilizável.

Com o advento das cifras eletromecânicas, como a famosa máquina **Enigma**, foi possível criar chaves rotativas muito mais robustas. Contudo, como qualquer corrente é tão forte quanto o seu elo mais fraco, a Enigma dependia de operadores humanos para configurar suas chaves diárias. Humanos tendem a repetir padrões, e analistas atentos (como a equipe de Alan Turing) conseguiram explorar essas falhas de comportamento para quebrar o sistema.

> 🎬 **Dica de filme:** Para entender os bastidores da quebra da Enigma, recomendo assistir a *O Jogo da Imitação (2014)* e *Enigma (2001)*.

Hoje, com o uso de computadores, as técnicas de criptografia moderna são tão poderosas que beiram o impossível de serem quebradas por força bruta. Dizemos "beirando o impossível" porque o cenário futuro com o advento da computação quântica ainda é uma incógnita.

---

## 🧠 Um Pouco de Matemática

Atualmente, uma das formas mais eficientes de proteger dados em repouso é a **criptografia simétrica**, onde uma única chave secreta é utilizada tanto para cifrar quanto para decifrar a mensagem.

Contudo, a comunicação online impõe um desafio: como fazer o destinatário saber qual chave foi usada pelo remetente sem transmitir a própria chave pela rede (onde ela poderia ser interceptada)?

O protocolo **Diffie-Hellman** é a solução ideal para este problema. Ele utiliza o conceito de **aritmética modular** (a matemática do relógio).

Imagine que queremos calcular $46 \pmod{12}$. Pense em uma corda com 46 unidades de comprimento sendo enrolada em volta de um relógio que possui apenas 12 horas. O ponto exato onde a ponta da corda parar será o nosso resultado.

![relógio modular](.\images\relogio_modular.png)

Neste caso, a corda dá 3 voltas completas ($12 \times 3 = 36$) e sobram 10 unidades. Portanto:

$$46 \equiv 10 \pmod{12}$$

Na criptografia, em vez do número 12, utilizamos um **módulo primo** ($p$), como o número 17. Para que o protocolo seja seguro, precisamos encontrar uma **raiz primitiva** (também chamada de **gerador** $g$) desse número primo.

Uma raiz primitiva não tem relação com a raiz quadrada. Ela é um número que, quando elevado a potências sucessivas de $1$ até $p-1$, gera como resto todos os números do relógio de forma embaralhada, **sem repetir nenhum**, até fechar o ciclo.

#### Testando se o número 3 é uma raiz primitiva de 17

* $3^1 \pmod{17} = 3$
* $3^2 \pmod{17} = 9$
* $3^3 \pmod{17} = 10 \quad \text{(pois } 27 - 17 = 10\text{)}$
* $3^4 \pmod{17} = 13 \quad \text{(pois } 81 - 68 = 13\text{)}$
* $3^5 \pmod{17} = 5$
* $3^6 \pmod{17} = 15$
* $3^7 \pmod{17} = 11$
* $3^8 \pmod{17} = 16$
* $3^9 \pmod{17} = 14$
* $3^{10} \pmod{17} = 8$
* $3^{11} \pmod{17} = 7$
* $3^{12} \pmod{17} = 4$
* $3^{13} \pmod{17} = 12$
* $3^{14} \pmod{17} = 2$
* $3^{15} \pmod{17} = 3$
* $3^{16} \pmod{17} = 1$

Note que o número 1 só aparece na última rodada, respeitando o Pequeno Teorema de Fermat:

$$g^{p-1} \equiv 1 \pmod p$$

O fato de não existir uma fórmula direta para encontrar essas raízes primitivas (obrigando o uso de testes sequenciais) é parte do que torna a matemática modular tão atraente para a segurança.

---

## 🤝 O Aperto de Mão (Handshake) na Prática

Imagine que **Eu ("E")** e **Você ("V")** queremos conversar em um aplicativo de chat sem que o bisbilhoteiro **"ELE"** consiga ler nossas mensagens. Para simplificar, vamos ilustrar o cenário usando números propositalmente pequenos.

Como "Eu" vou iniciar a conversa, meu aplicativo gera os parâmetros do canal e calcula a minha chave pública, enviando o seguinte pacote de dados em formato JSON:

```json
{
  "de": "eu",
  "para": "voce",
  "gerador": 5,
  "primo": 13,
  "chave_publica": 8,
  "mensagem": "cbf65b8d93bb2250940c3a37598d0b986c2b5b4c5e8565322c690b"
}
```

Como a minha chave pública foi calculada?O meu aplicativo sorteou um número secreto privado (que nunca sai do meu celular), por exemplo, 15. Utilizando o gerador 5 e o primo 13, a conta foi:$$5^{15} \pmod{13} = 8$$Você recebe esse pacote. Para responder e fechar o aperto de mão, seu aplicativo escolhe o seu próprio número secreto privado, por exemplo, 17, e calcula a sua chave pública:$$5^{17} \pmod{13} = 5$$O seu aplicativo me responde com o seguinte pacote JSON:

```json
{
  "de": "voce",
  "para": "eu",
  "chave_publica": 5,
  "mensagem": "4fa28646dea56beffe5c3567a18d7b4c8664ac44c98a5db6f5a91a71e48ad6aed092"
}
```

A Magia do Acordo de ChavesAgora eu tenho a sua chave pública (5) e você tem a minha chave pública (8). Veja o que acontece quando cada dispositivo calcula o segredo final localmente:No meu dispositivo (Eu): pego a sua chave pública (5) e elevo ao meu segredo (15):$$5^{15} \pmod{13} = 8$$No seu dispositivo (Você): pega a minha chave pública (8) e eleva ao seu segredo (17):$$8^{17} \pmod{13} = 8$$Ambos chegamos exatamente ao número 8! A nossa chave simétrica do chat está criada.Por que os resultados dão iguais?Isso acontece devido à propriedade de potência de potência.Eu calculei $(5^{17})^{15} \pmod{13}$, enquanto você calculou $(5^{15})^{17} \pmod{13}$. Em ambos os lados, a matemática subjacente executou a mesma operação: $5^{17 \times 15} \pmod{13}$. Como a ordem dos fatores não altera o produto dos expoentes, o resultado do resto é microscopicamente obrigado a ser idêntico nas duas pontas.O processo é fantástico: na tela de "Você" aparece Oi, e aí? e na minha aparece Beleza, e por aí?. Trafegamos os dados em texto claro nos nossos aparelhos, mas o "ELE", que estava monitorando a rede e interceptou os pacotes, só conseguiu ver os dados públicos transitando (g=5, p=13, público_eu=8, público_voce=5).Como "ELE" não possui os segredos privados (15 e 17), ele se depara apenas com blocos de lixo eletrônico ilegíveis: cbf65b8d93... e 4fa28646de....🎨 O Problema do Logaritmo DiscretoMas por que, tendo acesso aos números 5, 13, 8 e 5, o atacante não consegue reverter a conta para descobrir os nossos segredos práticos?Imagine que você misture tintas azul e amarela em uma paleta; você obterá a cor verde. Se alguém te entregar o pote de tinta verde, como você faria para separar fisicamente as porções exatas e originais do azul e do amarelo de volta? Não há como. É um processo de via única.Na matemática, essa mistura destrutiva é chamada de Problema do Logaritmo Discreto. No mundo real, os parâmetros utilizados possuem chaves que variam entre 300 e 600 dígitos. Descobrir os expoentes privados a partir dos resultados modulares exigiria tanto poder de processamento que mesmo combinando todos os supercomputadores do planeta, o cálculo levaria bilhões de anos para ser concluído. A nossa conversa está perfeitamente segura.
