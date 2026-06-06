from script_simetrica import Chat_User

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
