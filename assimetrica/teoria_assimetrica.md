## Criptografia Assimétrica

Na outra sessão, expus que para um chat simples, ambos os usuários teriam de ter uma mesma chave para que a mensagem cifrada pudesse ser decifrada por ambos, usando a mesma mensagem da cifragem. Isso é um processo chamado criptografia simétrica, em que uma única chave é usada para cifrar e decifrar. Este tipo de criptografia tem suas desvantagens como o perigo de compartilhar a chave de criptografia, que pode ser minimizado utilizando o algoritmo Diffie-Hellman. Outro inconveninente é a complexidade da escalabilidade o gerenciamento de chaves pelo sistema massivo e impraticável para uma quantidade grande de usuários, quanto maior o número de usuários. Há uma outra dificuldade conhecida como `falta de não repúdio`. O que é isso? Uma vez que a chave é compartilhada, não há um método matemático de comprovar quem cifrou uma mensagem, tornando complicado o processo de atribuir uma mensagem a um usuário, este gerênciamento deve ser feito por outros métodos que não o reconhecimento da chave de cifragem.

Para amenizar tais situações, pensou-se em um processo mais seguro, e que a chave de decifragem não fosse compartilhado, que apenas um lado da comunicaçaõ a obtivesse. Este processo é um pouco mais lento que a criptografia simétrica, mas é mais seguro. É a `criptografia assimétrica`.

Agora cada usuário possui dois códigos um para cifragem e outro para decifragem. O código para cifragem pode ser público, qualquer um que tenha esta chave pode enviar uma mensagem, entretanto, a decifragem só é possível pelo destinatário.

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
