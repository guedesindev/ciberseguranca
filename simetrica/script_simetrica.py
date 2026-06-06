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
