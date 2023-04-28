import PySimpleGUI as sg
import json
import bcrypt

sg.theme('Reddit')

layout = [    [sg.Text('Usuário'), sg.Input(key='usuario')],
    [sg.Text('Senha'), sg.Input(key='senha', password_char='*')],
    [sg.Button('Login')],
    [sg.Button('Novo Usuário')]
]

def fazer_cadastro(nome, senha, limite=8):
    if not validar_entrada(nome, senha, limite):
        return

    try:
        with open('bd.json', 'r', encoding='utf8') as banco:
            usuarios = json.load(banco)
    except FileNotFoundError:
        usuarios = []

    for usuario in usuarios:
        if usuario['Usuário'] == nome:
            sg.popup('O usuário já existe!')
            return

    senha_com_hash = bcrypt.hashpw(senha.encode('utf8'), bcrypt.gensalt())
    novo_usuario = {"Usuário": nome, "Senha": senha_com_hash.decode('utf8')}

    usuarios.append(novo_usuario)
    sg.popup('Usuário cadastrado!')

    with open('bd.json', 'w', encoding='utf8') as banco:
        json.dump(usuarios, banco)

def fazer_login(nome, senha):

    with open('bd.json', 'r', encoding='utf8') as banco:
        usuarios = json.load(banco)

    for usuario in usuarios:
        if nome == usuario['Usuário']:
            senha_com_hash = usuario['Senha'].encode('utf8')
            if bcrypt.checkpw(senha.encode('utf8'), senha_com_hash):
                sg.popup('Login realizado com sucesso!')
                return
            else:
                sg.popup('Senha inválida!')
                return
    sg.popup('Usuário inválido!')

def validar_entrada(usuario, senha, limite=8):
    if len(usuario) > limite:
        sg.popup('O nome de usuário deve ter no máximo 8 caracteres.')
        return False
    if len(senha) > limite:
        sg.popup('A senha deve ter no máximo 8 caracteres.')
        return False
    return True

janela = sg.Window('Sistema', layout)

while True:

    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED:
        break
    if evento == 'Login':
        fazer_login(valores['usuario'], valores['senha'])

    if evento == 'Novo Usuário':
        janela.hide()
        cadastro_layout = [
            [sg.Text('Usuário'), sg.Input(key='usuario_cadastro')],
            [sg.Text('Senha'), sg.Input(key='senha_cadastro', password_char='*')],
            [sg.Button('Cadastrar')]
        ]
        
        cadastro_janela = sg.Window('Cadastro', cadastro_layout)

        while True:
            evento_cadastro, valores_cadastro = cadastro_janela.read()
            if evento_cadastro == sg.WIN_CLOSED:
                break
            if evento_cadastro == 'Cadastrar':
                fazer_cadastro(valores_cadastro['usuario_cadastro'], valores_cadastro['senha_cadastro'])
                cadastro_janela.close()
                janela.un_hide()

janela.close()
