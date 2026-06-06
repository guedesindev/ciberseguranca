# Como acontece o compartilhamento de chave simétrica sem prejudicar a segurança?
# O compartilhamento de chave simétrica pode ser realizado de maneira segura utilizando protocolos de troca de chaves, como o protocolo Diffie-Hellman. Este protocolo permite que duas partes estabeleçam uma chave secreta compartilhada sem a necessidade de transmitir a chave diretamente.

import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Chat_User:
    def __init__(self, nome: str):
        self.nome = nome
        self._chave_privada = secrets.choice(range(1, 1000))
        self.chave_publica = None
        self.chave_secreta_chat = None

        self.gerador = None
        self.primo = None

        self.chave_final_aes = None

    def configurar_novo_canal(self):
        def verificar_primo(n):
            if n <= 1:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        self.primo = secrets.choice(range(1000, 2000))
        while not verificar_primo(self.primo):
            self.primo = secrets.choice(range(1000, 2000))

        for g in range(2, self.primo):
            restos = set()
            for i in range(1, self.primo):
                restos.add((g**i) % self.primo)

            if len(restos) == self.primo - 1:
                self.gerador = g
                break

    def receber_parametros_do_canal(self, primo: int, gerador: int):
        self.primo = primo
        self.gerador = gerador

    def calcular_chave_publica(self):
        if self.gerador is None or self.primo is None:
            raise ValueError(
                "Gerador e primo devem ser definidos antes de calcular a chave pública."
            )

        self.chave_publica = (self.gerador**self._chave_privada) % self.primo
        return self.chave_publica

    def calcular_chave_secreta(self, chave_publica_receptor):
        if self.primo is None:
            raise ValueError(
                "Primo deve ser definido antes de calcular a chave secreta."
            )

        self.chave_secreta_chat = (
            chave_publica_receptor**self._chave_privada
        ) % self.primo

        segredo_em_bytes = str(self.chave_secreta_chat).encode()
        self.chave_final_aes = hashlib.sha256(segredo_em_bytes).digest()

    def enviar_mensagem(self, mensagem: str):
        if self.chave_final_aes is None:
            raise ValueError("Chave AES deve ser calculada antes de enviar mensagens.")

        motor_aes = AESGCM(self.chave_final_aes)
        nonce = secrets.token_bytes(12)
        pacote_cifrado = motor_aes.encrypt(nonce, mensagem.encode(), None)

        return nonce, pacote_cifrado

    def receber_mensagem(self, nonce: bytes, pacote_cifrado: bytes):
        if self.chave_final_aes is None:
            raise ValueError("Chave AES deve ser calculada antes de receber mensagens.")

        motor_aes = AESGCM(self.chave_final_aes)

        try:
            dados_decifrados = motor_aes.decrypt(nonce, pacote_cifrado, None)
            return dados_decifrados.decode()
        except Exception as e:
            raise ValueError(
                "Erro ao decifrar a mensagem. Verifique a chave e o nonce."
            )


# -----------------------------------------------------------------------------
# Simular a comunicação entre Alice e Bob utilizando o protocolo Diffie-Hellman

alice = Chat_User("Alice")
bob = Chat_User("Bob")

print("-" * 60)
print("Configurar um novo canal para iniicar o chat entre Alice e Bob")
alice.configurar_novo_canal()
print("-" * 60)

print("=" * 60)
print("Bob entra no chat e recebe os parâmetros de Alice")
bob.receber_parametros_do_canal(primo=alice.primo, gerador=alice.gerador)
print("-" * 60)

print("=" * 60)
print("Alice e Bob calculam suas chaves públicas")
alice_pub = alice.calcular_chave_publica()
bob_pub = bob.calcular_chave_publica()
print("-" * 60)

print("=" * 60)
print(f"Chave pública de Alice (viajou pela rede): {alice_pub}")
print(f"Chave pública de Bob (viajou pela rede): {bob_pub}")
print("-" * 60)

print("=" * 60)
print("Cada um calcula o segredo final localmente usando a chave pública do outro")
alice.calcular_chave_secreta(bob_pub)
bob.calcular_chave_secreta(alice_pub)
print("-" * 60 + "\n")


print("=" * 60 + "\n")
print(
    "Agora criar a criptografia ponta-a-ponta usando AES-GCM com a chave secreta compartilhada"
)

print("=" * 60 + "\n")
print("Alice e Bob calculam a chave final AES a partir do segredo compartilhado")
# print(f"Chave AES de Alice (Hex): {alice.chave_final_aes.hex()}")
# print(f"Chave AES do Bob (Hex): {bob.chave_final_aes.hex()}")
print("-" * 60 + "\n")


print(
    f"Testando a criptografia ponta-a-ponta na prática usando a chave AES compartilhada"
)
print("--- Alice enviando Mensagem ---")
mensagem_de_alice = "Olá, Bob!"

nonce_alice, pacote_cifrado_alice = alice.enviar_mensagem(mensagem_de_alice)


print(f"Pacote bruto enviado para a rede (HEX): {pacote_cifrado_alice.hex()}\n")


print(f"--- Bob recebendo a mensagem e decifrando ---")
mensagem_recebida = bob.receber_mensagem(nonce_alice, pacote_cifrado_alice)
print(f"Mensagem que apareceu na tela de Bob: {mensagem_recebida}")


print("\n" + "=" * 60)
print("--- Simular resposta do Bob para Alice ---")
mensagem_de_bob = "Olá Alice, e aí tudo bem? O que manda?"

nonce_bob, pacote_cifrado_bob = bob.enviar_mensagem(mensagem_de_bob)

print(f"\nPacote cifrado enviado por Bob (HEX): {pacote_cifrado_bob.hex()}\n")


print(f"--- Alice recebendo a mensagem e decifrando ---")
try:
    dados_decifrados_alice = alice.receber_mensagem(nonce_bob, pacote_cifrado_bob)
    print(f"Sucesso! Mensagem que apareceu na tela de Alice: {dados_decifrados_alice}")
except Exception as e:
    print("Erro! A tag de autenticação não bateu ou a chave está errada.")
print("=" * 60)
