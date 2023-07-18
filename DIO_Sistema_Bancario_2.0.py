import textwrap


def menu():
    opcoes = """>>>>  Banco DIO  <<<<

        [1] Sacar
        [2] Depositar
        [3] Extrato
        [4] Cadastro usuário
        [5] Cadastro de conta
        [6] Listar contas
        [0] Sair

    >>> """

    return int(input(opcoes))


def sacar(*, saldo, saque, extrato, limite, num_saque, lim_saque):
    if num_saque == lim_saque:
        print('Limite diário de saques excedido')
    elif saque > saldo:
        print('Saldo insuficiente')
    elif saque <= saldo:
        if saque > limite:
            print('Limite de R$ 500.00 por saque excedido')
        elif saque <= limite:
            print('Sacando...\n')
            saldo -= saque
            num_saque += 1
            extrato += f"\033[31m-\tR$ {saque:.2f}\n\033[m"

    return saldo, extrato


def depositar(saldo, deposito, extrato, /):
    if deposito > 0:
        saldo += deposito
        extrato += f"\033[32m+\tR$ {deposito:.2f}\n\033[m"
        print(f'Depósito de R${deposito:.2f} realizado com sucesso')

    return saldo, extrato


def mostrar_extrato(saldo, /, *, extrato):
    print("\n============== EXTRATO ==============")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("======================================")


def cadastro(usuarios):
    cpf = input('Insira o CPF [apenas números]: ')
    usuario = filt_usuario(cpf, usuarios)

    if usuario:
        print('CPF já cadastrado')
        return
    nome = input('Insira o seu nome completo: ')
    nasc = input('Insira sua data de nascimento [dd-mm-aaaa]: ')
    end = input('Insira seu endereço [rua, nº - bairro - cidade/sigla]: ')
    usuarios.append({'nome': nome, 'data_nascimento': nasc, 'cpf': cpf, 'endereco': end})

    print('\033[32mNovo usuário cadastrado com sucesso\033[m')


def filt_usuario(cpf, usuarios):
    filtro_usuarios = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return filtro_usuarios[0] if filtro_usuarios else None


def criar_conta(ag, numero_conta, usuarios):
    cpf = input('Insira seu CPF: ')
    usuario = filt_usuario(cpf, usuarios)

    if usuario:
        print('\033[32mConta criada com sucesso\033[m')
        return {'agencia': ag, 'numero_conta': numero_conta, 'usuario': usuario}

    print('\033[31mUsuário não cadastrado\033[m')


def list_contas(contas):
    for conta in contas:
        cc = f"Agência: {conta['agencia']} \nC/C: {conta['numero_conta']}\nTitular: {conta['usuario']['nome']}"
        print('=-' * 30)
        print(cc)


def principal():

    saldo = 0
    limite = 500
    extrato = ""
    num_saque = 0
    lim_saque = 3
    usuarios = []
    contas = []
    ag = '0001'

    while True:
        opcao = menu()

        if opcao == 1:
            print()
            print('>>> Saque <<<')
            saque = int(input('\nQual valor deseja sacar: '))

            saldo, extrato = sacar(saldo=saldo, saque=saque, extrato=extrato, limite=limite, num_saque=num_saque, lim_saque=lim_saque)

        elif opcao == 2:
            print()
            print('>>> Depósito <<<')
            deposito = int(input('Qual valor deseja depositar: '))

            saldo, extrato = depositar(saldo, deposito, extrato)

        elif opcao == 3:
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == 4:
            cadastro(usuarios)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            conta = criar_conta(ag, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 6:
            list_contas(contas)

        elif opcao == 0:
            print()
            print('=-' * 15)
            print('Obrigada pela preferência.')
            break


principal()
