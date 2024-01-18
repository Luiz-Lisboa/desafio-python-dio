import time
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>"""


#variaveis globais
saldo = 0
deposito = 0
limite = 500
saque = 0
extrato = {}
i = int(0) #contador para extrato
numero_saques = 0
LIMITE_SAQUES = 3

#Função limpar console
def limpar():
    input("Aperte enter para continuar...")
    print("\033c", end="")

while True:
    opcao = input(menu)


    #Depósito selecionado
    if opcao == "d":
        print("Depósito")
        deposito = float(input("Informe valor a depositar: R$"))
        if deposito > 0:
            saldo += float(deposito)
            i += 1
            extrato[i] = f"+ R$ {deposito:.2f}"
            print(f"Insira o valor de R$ {deposito:.2f} na gaveta")
            time.sleep(2)
            print(f"R$ {deposito:.2f} depositado com sucesso")
        else:
            print("Valor inválido")
    

    #Saque selecionado
    elif opcao == "s" and LIMITE_SAQUES > numero_saques:
        print("Sacar")
        saque = float(input("Informe valor a sacar: R$ "))
        if saque > 0 and saque <= 500 and saque <= saldo:
            saldo -= saque
            i += 1
            extrato[i] = f"- R$ {saque:.2f}"
            numero_saques += 1
            print(f"""valor sacado: R$ {saque:.2f}\n Retire cédulas na gaveta automática.""")
        elif saque <= 0:
            print("Valor inválido. Tente novamente.")
        elif saque > saldo:
            print("Saldo insuficiente.")
        else:
            print(f"Valor de saque não permitido. Selecione valor até que R$ {limite:.2f}")
    elif opcao == "s" and LIMITE_SAQUES <= numero_saques:
        print("Limite de saques diário excedido")


    #Extrato Selecionado
    elif opcao == "e":
        print("Extrato")
        if i == 0:
            print("Não foram realizadas movimentações.")
        else:
            for i in range(1, i+1, 1):
                print(extrato[i])
        print(f"saldo: R$ {saldo:.2f}")
    
    #Encerra programa
    elif opcao == "q":
        limpar()
        break


    #Seleção inválida  
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    limpar()
