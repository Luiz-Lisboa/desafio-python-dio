import time


def main_menu():

    menu = """
    Selecione opção desejada:

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Cadastrar Usuário
    [5] Listar Usuários
    [6] Criar Conta Corrente
    [7] Listar Contas Correntes

    [Q] Sair
    
    => """

    return input(menu)


def deposit(saldo, valor_deposito, extrato, /): #v1.1 funcionando v1.3 corrige
    
    if valor_deposito > 0:
        saldo += float(valor_deposito)
        extrato += f"+ R$ {valor_deposito:.2f}\n"
        print(f"Insira o valor de R$ {valor_deposito:.2f} na gaveta")
        time.sleep(2)
        print(f"R$ {valor_deposito:.2f} depositado com sucesso")
    else:
        print("Valor inválido")
    return saldo, extrato


def withdraw(*, saldo, valor_saque, extrato, limite, cont_saque): #v1.2 funcionando v1.3 corrige
    if valor_saque > 0 and valor_saque <= 500 and valor_saque <= saldo:
        saldo -= valor_saque
        extrato += f"- R$ {valor_saque:.2f}\n"
        cont_saque += 1
        print(f"""valor sacado: R$ {valor_saque:.2f}\n Retire cédulas na gaveta automática.""")
    elif valor_saque <= 0:
        print("Valor inválido. Tente novamente.")
    elif valor_saque > saldo:
        print("Saldo insuficiente.")
    else:
        print(f"Valor de saque não permitido. Selecione valor até que R$ {limite:.2f}")
    
    return saldo, extrato, cont_saque
    

def historic(saldo, /, *, extrato): #v1.3 funcionando
    print("Extrato")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"saldo: R$ {saldo:.2f}")


def create_user_client(clientes):#v1.4 funcionando
    cpf = input("Informe o CPF: (Somente número): ")
    cliente = filter_user(cpf, clientes)

    if cliente:
        print("\nCPF vinculado a cliente já cadastrado!")
        return
    else:
        nome = input("Nome completo: ")
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        clientes.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
        print("Cliente cadastrado com sucesso!")


def filter_user(cpf, clientes):#v1.4 funcionando
    clientes_filtrados = [cliente for cliente in clientes if cliente["cpf"] == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def list_user_client(clientes):
        for clientes in clientes:
            listagem = f"""
                Nome:{clientes['nome']}
                CPF:{clientes['cpf']}
                Data de nascimento:{clientes['data_nascimento']}
                Endereço:{clientes['endereco']}
            """
            print(listagem)


def create_account(agencia, numero_conta, clientes, opcao_booleana): #v1.5 funcionando
    cpf = input("Informe o CPF do usuário: ")
    cliente = filter_user(cpf, clientes)

    if cliente:
        print("Conta corrente criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": cliente}
    else:
        print("Usuário não encontrado, deseja cadastrar novo usuário?")
        input(opcao_booleana)
        if opcao_booleana == "1": #Erro ñ identificado
            create_user_client(clientes)
        else:
            print("\033c", end="")


def list_account(contas): #v1.6 funcionando
    for contas in contas:
        listagem = f"""
            Agência:{contas['agencia']}
            C/C:{contas['numero_conta']}
            Titular:{contas['usuario']['nome']}
        """
        print(listagem)


def clear(): #Função limpar console
    input("Aperte enter para continuar...")
    print("\033c", end="")


def main():
    #Constantes
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    #Variáveis
    clientes = []
    contas = []
    cont_saque = 0 #alterado (numero_saques)
    extrato = "" #contador extraído ao transformar em string ({} >> "")
    limite = 500
    saldo = 0
    valor_deposito = 0 #alterado (deposito)
    valor_saque = 0
    opcao_booleana = """
    [1] Sim
    [2] Não
    => """

    while True:
        opcao = main_menu()

        if opcao == "1": #Depósito selecionado
            print("Depósito")
            valor_deposito = float(input("Informe valor a depositar: R$"))
            saldo, extrato = deposit(saldo, valor_deposito, extrato)

        elif opcao == "2": #Saque selecionado
            if LIMITE_SAQUES > cont_saque:
                print("Saque selecionado")
                valor_saque = float(input("Informe valor a sacar: R$ "))
                saldo, extrato, cont_saque = withdraw(
                    saldo=saldo,
                    valor_saque=valor_saque,
                    extrato=extrato,
                    limite=limite,
                    cont_saque=cont_saque)
            else:
                print("Limite de saques diário excedido! Operação cancelada")

        elif opcao == "3":#Extrato Selecionado
            historic(saldo, extrato=extrato)

        elif opcao == "4": #Cadastrar Usuário Selecionado
            create_user_client(clientes)
        
        elif opcao == "5": #Listar clientes usuários
            list_user_client(clientes)

        elif opcao == "6": #Criar Conta Corrente
            numero_conta = len(contas) + 1
            conta = create_account(AGENCIA, numero_conta, clientes, opcao_booleana)

            if conta:
                contas.append(conta)

        elif opcao == "7": #Listar Conta Corrente
            list_account(contas)

        elif opcao == "q" or "Q":#Encerra programa, Seletor executando como else
            print("Programa encerrado pelo usuário")
            clear()
            break

        else: #Seleção inválida, Seletor não chamado para executar
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            clear()
        
        clear()


main()


""" Requisitos do desafio:
        - Modularizar código do desafio anterior:
            - Função Saque:
                - Keyword only
                - Sugestão de argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques
                - Sugestão de retorno: saldo, extrato
            - Função depósito:
                - Positional only
                - Sugestão de argumentos: saldo, valor, extrato
                - Sugestão de retorno: saldo, extrato
            - Função extrato:
                - Positional e keyword
                - Argumentos posicionais: saldo
                - Argumentos nomeados: extrato
        - Criar 2 novas funções:
            - criar usuário(cliente)
                - Em lista
                - ñ permitir usuário duplicado
                - nome
                - data de nascimento
                - CPF: somente números
                - Endereço
                    - String no formato: logradouro - nro - cidade/sigla estado
            - criar conta corrente
                - Em lista
                - Filtar lista de usuários pelo CPF, criar conta automáticamente ao encontra-lo
                - Agência
                    - fixo "0001"
                - número da conta
                    - Sequêncial iniciada em 1
                - usuário único
                    - Possível mais de uma conta
        - Criar função ñ declarada"""