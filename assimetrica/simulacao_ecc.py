# Primeiro Passo: Criação do algoritmo passo a passo do zero

import secrets


# Nesta implementação vou simular uma curva para não ter de escrever muitas linhas de algebra abstrata.
class CurvaElipticaMinima:
    """Curva: y^2 = x^3 + ax + b (mod p)"""
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
    
    def inverso_modular(self, n):
        return pow(n, self.p - 2, self.p)
    
    def somar_pontos(self, P, Q):
        if P is None: return Q
        if Q is None: return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None
        
        if x1 != x2:
            num = (y2 - y1) % self.p
            den = self.inverso_modular((x2 - x1) % self.p)
            m = (num* den) % self.p
        else:
            num = (3 * pow(x1, 2) + self.a) % self.p
            den = self.inverso_modular((2 * y1) % self.p)
            m = (num * den) % self.p

        # ponto resultante R
        x3 = (pow(m, 2) - x1 - x2) % self.p
        y3 = (m *(x1 - x3)-y1) % self.p

        r = (x3, y3)

        return r
    
    def multiplicar_ponto(self, k, P):
        resultado = None
        ponto_atual = P

        while k > 0:
            if k % 2 == 1:
                resultado = self.somar_pontos(resultado, ponto_atual)
            ponto_atual = self.somar_pontos(ponto_atual, ponto_atual)
            k //= 2

        return resultado



class UsuarioECC:
    def __init__(self, nome:str, curva: CurvaElipticaMinima, G: tuple, chave_privada: int):
        self.nome = nome
        self.curva = curva
        self.G = G
        self.chave_privada = chave_privada
        self.chave_publica = self.curva.multiplicar_ponto(self.chave_privada, self.G)

        self.segredo_compartilhado = None

    def calcular_segredo_diffie_hellman(self, chave_publica_outro_usuario: tuple):
        self.segredo_compartilhado = self.curva.multiplicar_ponto(self.chave_privada, chave_publica_outro_usuario)

    def cifrar_mensagem(self, mensagem: str, chave_publica_receptor: tuple, chave_efemera_k: int):
        """Simulação do ECIES"""
        ponto_R = self.curva.multiplicar_ponto(chave_efemera_k, self.G)

        ponto_S = self.curva.multiplicar_ponto(chave_efemera_k, chave_publica_receptor)

        semente_secreta = ponto_S[0]

        mensagem_bytes = mensagem.encode('utf-8')
        bytes_cifrados = bytearray()

        for i, b in enumerate(mensagem_bytes):
            chave_byte = (semente_secreta + i) % 256
            bytes_cifrados.append(b ^ chave_byte)
        
        return ponto_R, bytes(bytes_cifrados)
    
    def decifrar_mensagem(self, ponto_R: tuple, bytes_cifrados: bytes):
        ponto_S = self.curva.multiplicar_ponto(self.chave_privada, ponto_R)

        semente_secreta = ponto_S[0]

        bytes_decifrados = bytearray()
        for i, b in enumerate(bytes_cifrados):
            chave_byte = (semente_secreta + i) % 256
            bytes_decifrados.append(b ^ chave_byte)

        return bytes_decifrados.decode('utf-8')



# ------------------------------
# --- Laboratório Didático 1 ---

curva_didatica = CurvaElipticaMinima(a=2, b=2, p=17)
PONTO_G = (5, 1)

print(f"=== Parâmetros Públicos Do Sistema ===")
print(f"Equação: y^2 = x^3 + 2x + 2 (mod 17)")
print(f"Ponto Gerador G: {PONTO_G}\n")

fernando = UsuarioECC('Fernando', curva=curva_didatica, G=PONTO_G, chave_privada=3)

outro_usuario = UsuarioECC("Amigo", curva=curva_didatica, G=PONTO_G, chave_privada=7)

print("=== GERAÇÃO DE CHAVES ===")
print(f"[{fernando.nome}] Chave Privada: {fernando.chave_privada} | chave_publica (ponto na curva): {outro_usuario.chave_publica}\n")


print("=== APERTO DE MÃO (DIFFIE-HELLMAN) ===")
fernando.calcular_segredo_diffie_hellman(outro_usuario.chave_publica)
outro_usuario.calcular_segredo_diffie_hellman(fernando.chave_publica)

print(f"[{fernando.nome}] Coordenada do Segredo Calculado: {fernando.segredo_compartilhado}")
print(f"[{outro_usuario.nome}] Coordenada do Segredo Calculado: {outro_usuario.segredo_compartilhado}")

if fernando.segredo_compartilhado == outro_usuario.segredo_compartilhado:
    print("🌟 SUCESSO ABSOLUTO! Ambos chegaram ao mesmo ponto secreto sem revelar suas chaves privadas.\n\n")

### Cifrar uma mensagem é demasiado trabalhoso pois é necessário calcular um ponto a partir do texto, ponto este que deve estar definido na curvaEliptica, Há um metodo temporário possível, que é gerar uma chave AES e uma chave k_temporária, enviar o ponto da mensagem cifrada e o k_temporário para que possa ser realizada a decifragem da mensagem.

# --------------------------------
# ---- Laboratório Didático 2 ----
# --------------------------------

# Utilizarei a mesma curva criada antes

# Enviando uma mensagem cifrada
print("=== ENVIO DE MENSAGEM ===")
mensagem_original = "Olá Mundo!"
print(f"Mensagem original: {mensagem_original}")

# Chave elíptica temporária
k_temporario = 3

ponto_R, texto_cifrado = fernando.cifrar_mensagem(
    mensagem=mensagem_original,
    chave_publica_receptor=outro_usuario.chave_publica,
    chave_efemera_k=k_temporario
    )

print(f"Ponto R(Chave efêmera enviada publicamente): {ponto_R}")
print(f"Texto cifrado em HEX transitando pela rede: {texto_cifrado.hex()}\n")

print("=== RECEBER MENSAGEM ===")
mensagem_revelada = outro_usuario.decifrar_mensagem(ponto_R, texto_cifrado)

print(f"Texto decifrado: {mensagem_revelada}")

print("🌟 SUCESSO ABSOLUTO! A mensagem foi cifrada e decifrada.\n\n")

# =====================================================================
title = "=== IMPLEMENTAÇÃO DO ALGORITMO ECC COM BIBLIOTECA CRYPTOGRAPHY ==="
print("\n" +"="*len(title))
print(title)
print("="*len(title) + "\n")

# PASSOS FUNDAMENTAIS
# 1. Geração do Par de Chaves: Cada usuário gera sua chave privada elíptica e extrai sua respectiva chave pública

# 2. Aperto de Mão (ECDH): Igual ao algoritmo rsa é necessário compartilhar de um segredo Bruto.

# 3. Derivação de Chave (HKDF): A chave simétrica não pode ser usada diretamente, é nessário que o segredo seja trabalhado por uma função de derivação de alto nível para gerar uma chave simétrica perfeitamente aleatória de 32 bytes (256 bits)

# 4. Cifragem Simétrica Estilo Autenticada (AES-GCM): Com a chave eliptica derivada o AES-GCM é usado para cifrar e decifrar qualquer tamanho de mensagem com garantia de integridade.

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class ChatECC:
    def __init__(self, nome: str):
        self.nome = nome

        # Passo 1
        self._chave_privada = x25519.X25519PrivateKey.generate()
        self.chave_publica = self._chave_privada.public_key()

    def exportar_chave_publica_bytes(self) -> bytes:
        from cryptography.hazmat.privitives import serialization

        return self.chave_publica.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    
    def calcular_chave_simetrica_hkdf(self, chave_publica_outro_usuario) -> bytes:
        """ Passo 2 e 3"""

        # Passo 2 troca de chaves elípticas pura (ECDH)
        segredo_bruto = self._chave_privada.exchange(chave_publica_outro_usuario)

        # Passo 3: HKDF
        chave_derivada = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"sessao-chat-criptografado"
        ).derive(segredo_bruto)

        return chave_derivada
    
    def cifrar_mensagem(self, mensagem:str, chave_simetrica: bytes) -> tuple[bytes, bytes]:
        # Passo 4A: cifra o texto plano usando AES-GCM
        texto_plano_bytes = mensagem.encode('utf-8')

        nonce = os.urandom(12)

        aesgcm = AESGCM(chave_simetrica)

        texto_cifrado = aesgcm.encrypt(nonce, texto_plano_bytes, associated_data=None)

        return nonce, texto_cifrado


    def decifrar_mensagem(self, nonce: bytes, texto_cifrado: bytes, chave_simetrica: bytes) -> str:
        # Passo 4B: Decifrar mensagem
        aesgcm = AESGCM(chave_simetrica)

        texto_plano_bytes = aesgcm.decrypt(nonce, texto_cifrado, associated_data=None)

        return texto_plano_bytes.decode('utf-8')
    


# --------------------------------
# ---- Laboratório Didático 3 ----
# --------------------------------
text = "=== INICIALIZANDO USUÁRIOS COMPONENTES ECC ==="
print("\n"+"="*len(text))
print(text)
print("="*len(text)+"\n")

# de volta a Alice e Bob
alice = ChatECC("Alice")
bob = ChatECC("Bob")

print(f"Chave Privada Alice (Objeto em memória): {alice._chave_privada}")
print(f"Chave Privada Bob (Objeto em memória): {bob._chave_privada}\n")

print("=== APERTO DE MÃO (CONTRATAÇÃO DE CHAVE SIMÉTRICA) ===")
chave_sessao_alice = alice.calcular_chave_simetrica_hkdf(bob.chave_publica)
chave_sessao_bob = bob.calcular_chave_simetrica_hkdf(alice.chave_publica)

print(f"Chave AES derivada pela Alice: {chave_sessao_alice.hex()}")
print(f"Chave AES derivada pela Bob: {chave_sessao_bob.hex()}")
assert chave_sessao_alice == chave_sessao_bob, "Erro: as chaves derivadas não coincidem!"

print("✨ Chave simétrica idêntica estabelecida com sucesso nos dois lados!\n")

print("\n=== FLUXO DE MENSAGEM CRIPTOGRAFADA")
mensagem_original = input("Agora não há limites de tamanho de mensagem:\nDigite a mensagem que quer cifrar:\n").strip()
print(f"\nAlice escreve: '{mensagem_original}'")

# Crifragem da mensagem original
nonce, pacote_cifrado = alice.cifrar_mensagem(mensagem_original, chave_sessao_alice)

print(f"\n-> Nonce enviado: {nonce.hex()}")
print(f"-> Texto cifrado em trânsito (Hex): {pacote_cifrado.hex()}\n")

# Recepção do nonce e pacote cifrado para decifrá-la
mensagem_recebida = bob.decifrar_mensagem(nonce, pacote_cifrado, chave_sessao_bob)
print(f"\nBob recebeu e decifrou: {mensagem_recebida}")