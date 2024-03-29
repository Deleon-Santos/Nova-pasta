import PySimpleGUI as sg
import modulo_registrar as vendas
import json

lista_operadores=['Administrador','Operador1','Operador2']

try:
    with open('dados/usuarios.txt', 'r') as bd:
        dados_usuario = json.load(bd)
except FileNotFoundError:
    sg.popup("O arquivo 'badosdUsuario.txt' não foi encontrado. Verifique o caminho ou crie o arquivo.")

sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {
    'BACKGROUND': '#778899', 
    'TEXT': '#000000', 
    'INPUT': '#DCDCDC', 
    'TEXT_INPUT': '#000000', 
    'SCROLL': '#99CC99', 
    'BUTTON': ('#000000', '#C0C0C0'), 
    'PROGRESS': ('#D1826B', '#CC8019'), 
    'BORDER': 4, 
    'SLIDER_DEPTH': 4,  
    'PROGRESS_DEPTH': 1, } 
sg.theme('MyCreatedTheme') 

col1=[
    [sg.Image(filename="imagem/imagem_login.png",size=(392,267))],
]
col2=[
    [sg.T("Usuario",font=('any',12))],
    [sg.DD(default_value="Administrador",values=lista_operadores,size=(21,1),font=('any',18),key='-USUARIO-')],
    [sg.T("Senha  ",font=('any',12))],
    [sg.I('1234',key='-SENHA-',size=(21,1),font=('any',18),password_char='*')],
    [sg.T("",font=('Ani',1))],
    [sg.CalendarButton("Data",font=('Any',12),size=(4,1),close_when_date_chosen=True,target="-DATA-",location=(900,500),no_titlebar=False),
    sg.Input('2024-03-21 17:41:22',key="-DATA-",font=('any',16),size=(18,1))],
    [sg.T("",font=('Ani',1))],
    [sg.B("OK",font=('any',10,'bold'),size=(8,1)),sg.P(),sg.B('SAIR',font=('any',10,'bold'),size=(8,1),button_color='red'),
     sg.P(),sg.B('SUPORTE',font=('any',10,'bold'),size=(8,1))]   
]

layout=[
    [sg.Push(),sg.T('ENTRAR EM VENDAS',font=('Any',30,'bold')),sg.P()],
    [sg.HorizontalSeparator()],
    [sg.Col(col1),sg.VerticalSeparator(),sg.Col(col2)],   
]

window = sg.Window("NOVO PEDIDO", layout,size=(740,400),finalize=True)
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "SAIR"):
        break

    if event =='OK':
        usuario=values['-USUARIO-']
        senha=values['-SENHA-']
        data=str(values['-DATA-'])
        
        if not usuario or not senha or not data:
            sg.popup("Usuario, Senha ou Data\nnão devem ser nulos",font=('Any',18))
            continue
        else:
            for user in dados_usuario:
                if user['nome']==usuario  and user['senha']== senha:
                    vendas.sistema(usuario,data)
            sg.popup_error('Inserir Usuario e Senha para entrar',font=('Any',18))       
            continue
    
    elif event=='SUPORTE':
        try:
            with open('dados/usuarios.txt', 'r') as legenda:
                arquivo = legenda.read()
                sg.popup_scrolled(arquivo, title="Suporte")
        except FileNotFoundError:
            sg.popup("O arquivo 'comanda.txt' não foi encontrado.\n  Verifique o caminho ou crie o arquivo.",font=('Any',18))
        continue 
                    
window.close()