# uma classe de usuário de chat utilizando a criptografia assimétrica RSA
import math
import secrets

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class UserBasico:
    def __init__(self, nome:str):
        self.nome = nome
        self._privada = secrets.choice(range(1, 1000000))
        self.publica = None
        self.expoent = None
        self.g = None
        self.q = None
        self.n = None
        self.totiente_n = None

    def configurar_canal(self):
        print('Configurando Canal')
        def verificar_primo(n):
            if n <= 1:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        self.p = secrets.choice(range(10000, 20000))
        self.q = secrets.choice(range(10000, 20000))

        while not verificar_primo(self.p):
            self.p = secrets.choice(range(10000, 20000))

        while not verificar_primo(self.q) or self.p == self.q:
            self.q = secrets.choice(range(10000, 20000))

        self.n = self.q * self.p
        self.totiente_n = (self.q - 1)*(self.p - 1)

        self.expoent = secrets.choice(range(1, self.totiente_n))

        while math.gcd(self.expoent, self.totiente_n) != 1:
            self.expoent = secrets.choice(range(1, self.totiente_n))

        self._privada = pow(self.expoent, -1, self.totiente_n)
        self.publica = (self.n, self.expoent)
    
    def receber_chave_publica(self, chave_publica:tuple):
        if chave_publica[0] > chave_publica[1]:
            self.n = chave_publica[0]
            self.expoent = chave_publica[1]
        else:
            self.n = chave_publica[1]
            self.expoent = chave_publica[0]


    def cifrar_mensagem(self, mensagem: str, e:int, n:int):
        # Observação: Este método de cifragem é o mais grosseiro, crifragem de caractere por caracter.
        mensagem_cifrada = []

        for c in mensagem:
            m = ord(c)
            c = pow(m, e, n)
            mensagem_cifrada.append(c)

        return mensagem_cifrada


    def decifrar_mensagem(self, lista_cifrada: list, n: int):
        # Uma observação, este método é o mais grosseiro possível para mostrar a decifragem caractere por caracter.
        mensagem_original = ""
        d = self._privada
        for c in lista_cifrada:
            m = pow(c, d, n)

            caractere = chr(m)
            mensagem_original += caractere

        return mensagem_original
    
# implementação chave de 1024 bits
class SuperRSAUser:
    def __init__(self, nome:str):
        self.nome = nome
        self._privada = None
        self.publica = None
        self.p = None
        self.q = None
        self.n = None
        self.expoent = None
        self.totiente_n = None

    # este aqui é um motor para primos gigantes - (MILLER-RABIN)
    def _teste_miller_rabin(self, n: int, k:int = 40) -> bool:
        if n <= 1: return False
        if n <= 3: return True
        if n % 2 == 0: return False

        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(k):
            a = secrets.randbelow(n-3) + 2
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False                

        return True
    
    def _gerar_primo_grande(self, bits:int = 512) -> int:
        while True:
            candidato = secrets.randbits(bits) | (1 << (bits - 1)) | 1
            if self._teste_miller_rabin(candidato):
                return candidato
    
    def configurar_canal(self):
        self.p = self._gerar_primo_grande(bits=512)
        self.q = self._gerar_primo_grande(bits=512)

        while self.p == self.q:
            self.q = self._gerar_primo_grande(bits=512)

        # módulo n
        self.n = self.p * self.q
        
        # Totiente
        totiente_n = (self.p - 1)*(self.q - 1)

        self.e = 65537
        if math.gcd(self.e, totiente_n) != 1:
            self.e = secrets.choice(range(3, totiente_n, 2))
            while math.gcd(self.e, totiente_n) != 1:
                self.e = secrets.choice(range(3, totiente_n, 2))

        # chave privada
        self.d = pow(self.e, -1, totiente_n)
        print(f"[{self.nome}] Canal configurado com sucesso!")

    def cifrar(self, mensagem_text: str, e_destinatario: int, n_destinatario: int) -> int:
        # Conversão texto em bytes utf-8
        mensagem_bytes = mensagem_text.encode('utf-8')

        # mensage para um único número inteiro (Base 64)
        m_inteiro = int.from_bytes(mensagem_bytes, byteorder='big')

        if m_inteiro >= n_destinatario:
            raise ValueError(f"Mensagem grande demais para o tamanho da chave!")
        
        c_cifrado = pow(m_inteiro, e_destinatario, n_destinatario)
        return c_cifrado
    
    def decifrar(self, numero_cifrado: int) -> str:
        m_inteiro = pow(numero_cifrado, self.d, self.n)

        num_bytes = (m_inteiro.bit_length() + 7) // 8

        mensagem_bytes = m_inteiro.to_bytes(num_bytes, byteorder='big')

        return mensagem_bytes.decode('utf-8')


# implementação lib cryptography
class UserRSACryptography:
    def __init__(self, nome:str):
        self.nome = nome
        self._privada = None
        self.publica = None
        
    def set_keys(self):
        self._privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        self.publica = self._privada.public_key()
        
        print(f"[{self.nome}] Chave pública e privada geradas com sucesso!")

    def transmitir_chave_publica(self):
        pem_publico = self.publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print(f"[{self.nome}] chave pública compartilhada!")
        return pem_publico

    def get_public_key(self, pem_publico: str):
        self.publica = serialization.load_pem_public_key(pem_publico)


    def cifrar_mensagem(self, mensagem: str, chave_publica):
        mensagem_bytes = mensagem.encode('utf-8')
        mensagem_cifrada = chave_publica.encrypt(
            mensagem_bytes, 
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))

        return mensagem_cifrada
    

    def decifrar_mensagem(self, mensagem_cifrada: bytes):
        if self._privada:
            mensagem_decifrada = self._privada.decrypt(
                mensagem_cifrada,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return mensagem_decifrada.decode('utf-8')

##############
# ------------        
# ------------
# Teste UsuárioBasico RSA
print("="*35)
print("|== Implementação manual de RSA ==|")
print("="*35)

fernando = UserBasico('Fernando')
fernando.configurar_canal()
e = fernando.expoent
n = fernando.n

print('-'*35)
print("Parâmetros do canal")
print("-"*35)

print(f"Primos: p: {fernando.p}, q: {fernando.q}")
print(f"Totiente de N: {fernando.totiente_n}")
print(f"Chave Pública: (n, e): ({n},{e})")
print(f"Chave Privada: d: {"*"*len(str(fernando._privada))}")


mensagem = input("Digite uma mensagem a cifrar: \nobs:Caso dê erro tente uma mensagem menor,\neste script gera uma chave pequena.\n").strip()

mensagem_cifrada = fernando.cifrar_mensagem(mensagem, e, n)
print(f"\n***Aqui está sua mensagem cifrada: {mensagem_cifrada}\n")

mensagem_decifrada = fernando.decifrar_mensagem(mensagem_cifrada, n)
print(f"\n***Agora Decifrada: {mensagem_decifrada}\n")

print("-"*35)

# ---------------
# Teste SuperRSAUser

print("="*35)
print("--- SuperUsuário RSA ---")
print("="*35)

fernando = SuperRSAUser('Fernando')
fernando.configurar_canal()

print(f"\nO tamanho do 'n' do Fernando é de {fernando.n.bit_length()} bits")
print(f"\nExemplo do 'n' gerado (gigante): {fernando.n}\n")

mensagem_teste = 'Olá, Esta é uma mensagem de teste trasmitida como um único número totalmente seguro pelo canal do chat.'

print(f"--- Enviando mensagem ---")
mensagem = input("Digite uma mensagem para cifrar: \nobs:Perceba que agora o limite de quantidade de caracteres da mensagem aumento 😉\n").strip()
numero_cifrado = fernando.cifrar(mensagem, fernando.e, fernando.n)
print(f"\nMensagem enviada via pacotes do chat (Numero Cifrado): {numero_cifrado}\n")

print(f"\n--- Recebendo mensagem ---")
mensagem_revelada = fernando.decifrar(numero_cifrado)
print(f"Mensagem que apareceu no ecrã do receptor: '{mensagem_revelada}'\n")


# -----------------------
# implementação RSA com biblioteca cryptographer
print("="*35)
print("--- Teste com biblioteca cryptography ---")
print("="*35)

fernando = UserRSACryptography('Fernando')
fernando.set_keys()

fernando.transmitir_chave_publica()

mensagem = input("Digite uma mensagem a cifrar:\nAqui a coisa está mais profissional, pode mandar ver na menasgem 🚀\n").strip()

mensagem_cifrada = fernando.cifrar_mensagem(mensagem, fernando.publica)
print("="*35)
print(f"\n***Aqui está sua mensagem cifrada: {mensagem_cifrada}\n")

fernando.get_public_key(fernando.transmitir_chave_publica())

mensagem_decifrada = fernando.decifrar_mensagem(mensagem_cifrada)
print("="*35)
print(f"\n***Agora Decifrada: {mensagem_decifrada}\n")

print("-"*35)
print("--- Fim dos Testes ---")
print("-"*35)