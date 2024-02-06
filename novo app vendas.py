#SISTEMA DE COBRAÇA EM CAIXA DE SUPERMERCADOS E AFINS
#Este sistema esta em desenvolvimento em carater academico e conta com colaboração de profissionais e estudantes 
#da area de Tecnololgia e desenvolvimento de sistemas

import PySimpleGUI as sg
import json

lista_cupom = [[""]]
carrinho = []
pesquisa_cupom = []
item_cancelado = []

valor_a_pagar = 0
num_item = int(0)
n_cupom = int(0)
try:
    with open('comanda.txt', 'r') as adic:
        dic = json.load(adic)

    # Seu código para ler o arquivo
except FileNotFoundError:
    sg.popup("O arquivo 'comanda.txt' não foi encontrado. Verifique o caminho ou crie o arquivo.")

#with open('comanda.txt', 'r') as adic:  # comando para ler o Aquivo.txt com os dados dos produtos
   

# =============================================================================================================

def remover(valor_a_pagar ):
    try:  # leia a lista1 e encontre o item informado
        remove_item = int(sg.popup_get_text('Remover o Item', font=("Any", 18)))
        print(f"item removido{remove_item}")

        for indice, material in enumerate(carrinho):
            if indice == remove_item:
                valor_a_pagar -= material[6]
                material[4]*=-1
                material[5]*=-1
                material[6]*=-1
                window["-TABELA-"].update(values=carrinho)
                
                return valor_a_pagar
        #sg.popup("Item não encontrado", font=("Any", 18))
                
        return valor_a_pagar
    except:
        sg.popup("Rejeitar Item", font=("Any", 18))
        return valor_a_pagar




# =====================================================================================================================
def pagar(soma2):
    frame6=[[sg.Text("Valor Total da Compra ", size=(28, 1), font=("Any", 12)),
        sg.Text(f"R$ {soma2:.2f}", size=(18, 1), justification='right', key="valor", font=("Any", 18))],
        [sg.Text("Valor Recolhido ", size=(28, 1), font=("Any", 12)),
        sg.Text(f'R$ 0.00', size=(18, 1), key="recebido", justification='right', font=("Any", 18))],
        [sg.Text("Troco Devolvido ", size=(28, 1), font=("Any", 12)),
        sg.Text(f'R$ 0.00', size=(18, 1), key="R$", justification='right', font=("Any", 18))],
        [sg.Text("", size=(10, 1))],
        [sg.Button('CARTAO', size=(20, 1)), sg.Button('PIX', size=(20, 1)), sg.Button('DINHEIRO', size=(20, 1))],

    ]
    layout = [
        [sg.Text("CONDIÇÃO DE PAGAMENTO", size=(35, 1), justification='center', font=("Any", 18))],
        [sg.Text("",size=(8,1)),sg.Image(filename="111.png",size=(400,100))],
        [sg.Text("", size=(10, 1))],
        [sg.Frame("",frame6)]

    ]

    window = sg.Window("PAGAMENTO", layout, finalize=True)

    while True:
        
        event, values = window.read()
        pago = soma2
        troco = 0
        window["valor"].update(f"R$ {soma2:.2f}")

        if event == (sg.WIN_CLOSED):
            sg.popup("Cancelar forma de Pagamento", font=("Any", 12))
            #return soma2


        elif event in ("CARTAO", "PIX"):  # para cartão e pix o valor e descontado itegralmente
            if soma2 > 0:  # somente se o subtotal existir e for maior que "0"
                soma2 = 0
                window["valor"].update(f"R$ {soma2:.2f}")
                window["recebido"].update(f"R$ {pago:.2f}")
                sg.popup("Pagamento Autorizado", font=("Any", 12))
                return soma2
                #break

        elif event == "DINHEIRO":
            try:
                dinheiro = sg.popup_get_text("Valor Recebido", font=("Any", 12))
                if dinheiro is not None:  # verifica se tem valores
                    dinheiro = float(dinheiro)
                    if dinheiro >= soma2:
                        troco = dinheiro - soma2
                        soma2 = 0
                        window["valor"].update(f"R$ {soma2:.2f}")
                        window["recebido"].update(f"R$ {dinheiro:.2f}")
                        window["R$"].update(f"R$ {troco:.2f}")

                        sg.popup("Pagamento efetuado com sucesso", font=("Any", 18))
                        return soma2  # desconta o subtotal e retorna o troco
                        #break
                    else:
                        sg.popup("Valor Insuficiente", font=("Any", 18))
                        continue
                else:
                    continue
            except ValueError:
                sg.popup("Insira um valor válido", font=("Any", 18))
                continue
        break
    window.close()


# ===========================================================================================================
def achar(material):
    for lanche in dic:
        if lanche["cod"] == material:
            return lanche["cod"]  # busca o produto dentro do cadastro
    sg.popup("Erro em Produto", title="Erro", font=("Any", 18))
    return False


def limpar_saida():
    carrinho.clear()
    window["com"].update("")
    window["preco"].update("")
    window["unitario"].update("")
    window["subtotal"].update("")
    window["descricao"].update("")
    

# limpa os campos sempre que uma nova função e chamada
def venda_cupom(cupom):
                                                            
    while True:
        try:
            
                
            for indice in enumerate(lista_cupom):
                if indice == cupom:
                    pesquisa_cupom.append(indice)
                    print(pesquisa_cupom)
                                       
                    return True
        except:
            sg.Text("Não Encontrado!", font=("Any", 18))           




# ===================================== Inicio do programa principal======================================================================
sg.theme("darkBlue3")
#sg.theme("darkBlue2")
titulos = ["Item","Cod","    EAN    "," Descrição do Produto","QTD","PUni R$","Preço R$"]

menu_layout = [["Novo", ["Nova Compra", "Novo Produto", "Pesquisar Produto"]],          
               ["Totais", ["Venda Cupom", "Venda Total"]], ["Suporte", ["Ajuda", "Data"]]]

bloco_1=[   [sg.Text("Numero do Cupom", size=(35, 1),font=("Any",17)), sg.Input(size=(17, 1), key="com", font=("Any", 25),justification="right")],
            [sg.Table(values=carrinho, headings=titulos, max_col_width=10, auto_size_columns=True,
            display_row_numbers=False, justification="right",text_color="black",font=("Any",11),background_color="lightyellow", num_rows=25, key="-TABELA-", row_height=20)],
            [sg.Text(" Preço Unitário R$",size=(67,1),font=("Any",12)),sg.Text("SubTotal Item R$",size=(13,1),font=("Any",12))],
            [sg.Input(key="unitario",size=(10,1),font=("Any",18),justification="right"),sg.Text(" ",size=(57,1)),sg.Input(key="preco",size=(10,1),font=("Any",18),justification="right")],
            [sg.Text("TOTAL R$", size=(12, 1), font=("Any", 40)),
            sg.Input(size=(13, 1), key="subtotal", font=("Any", 41), justification='right')],]
             
bloco_2=[   [sg.Text(" CAIXA FECHADO", size=(15, 1), key='caixa', font=("Any", 56, "bold"))],
            
            [sg.Text('Código do Produto', size=(25, 1), font=("Any", 12)),sg.Text("", size=(35, 1)),
             sg.Text('  Quantidade', size=(10, 1), font=("Any", 12))],
            [sg.InputText(background_color='White', size=(3,2 ), key='lanche1', font=("Any", 25)),
             sg.InputText(background_color='White', size=(14,2 ), key='ean', font=("Any", 25)),
             sg.Text("", size=(24, 1)),sg.InputText("1", size=(8, 2), key='qtd', font=("Any", 25),justification="right")],
            [sg.Text('Descrição do Produto', size=(25, 1), font=("Any", 12))],
            [sg.InputText(size=(38, 2), key='descricao', font=("Any", 25))],]

bloco_3=[   [sg.Button('OK', size=(15,1),font=("Any",25)), sg.Text("", size=(10, 1)),sg.Button('DELETE', size=(15, 1),font=("Any",25))],
            [sg.Button('PAGAR', size=(15, 1),font=("Any",25)),sg.Text("", size=(10, 1)), sg.Button('VOLTAR', size=(15, 1),font=("Any",25))],]

bloco_4=[   [sg.Image(filename="images.png",size=(695,210))],]
bloco_5=[   [sg.Text("Operador de Caixa:",size=(17,1),font=("Any",18)),sg.Input("ADMINISTRADOR DO SISTEMA",key='LOG',size=(40, 1),font=("Any", 15))],
            [sg.CalendarButton("Data",size=(5,1),close_when_date_chosen=True,target="data",location=(0,0),no_titlebar=False),
            sg.Input(key="data",size=(17,1)),sg.Text("               Em Desenvolvimento", size=(28, 1), font=("Any", 10)),
            sg.Text("      linkedin.com/in/deleon-santos-1b835a290")],]
                  
frame1= [   
            [sg.Frame("",bloco_2)],
            [sg.Frame("",bloco_3)],
            [sg.Frame("",bloco_4)],
            [sg.Frame("",bloco_5)]]

frame2= [    [sg.Frame("",bloco_1)] , ]

layout= [  
            [sg.Menu(menu_layout)],           
            [sg.Col(frame1),sg.Col(frame2)],]

#====================================================================================================================================

window = sg.Window("NOVO PEDIDO", layout,size=(800,800), resizable=True)
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Fechar"):
        # sg.popup("ENCERRAR",font=("Any", 18))
        break
    elif event == "Nova Compra":
        
        n_cupom += 1
        carrinho.append(n_cupom)
        window['com'].update(f'N°{n_cupom}')
        window['caixa'].update('      CAIXA ABERTO')
        window['subtotal'].update(f'R$ {valor_a_pagar:.2f}')
        window["-TABELA-"].update("")
        # dentro deste bloco de eventos serão registrados apenas os botoes (OK,DELETE,PAGAR,VOLTAR)
        while True:
            try:
                event, values = window.read()
                if event =='OK': 
                    # verifica se ha valores nos campos de produto e quantidade
                    material = values['lanche1']
                    qtd_item = int(values["qtd"])
                    if not material:
                        sg.popup("Erro em Produto!", title="Erro", font=("Any", 18))
                        continue
                    elif qtd_item > 0 and qtd_item < 100:
                        cod_item = achar(material)
                        # recebe o codigo e integra o produto ao dicionario e lista local
                        if cod_item == False:
                            #sg.popup("Erro em Produto", title="Erro", font=("Any", 18))
                            continue
                        else:
                            #qtd_item = int(qtd_item)
                            for item in dic:
                                if item["cod"] == cod_item:
                                    num_item += 1
                                    ean_item = item["ean"]
                                    desc_item = item["lanche"]
                                    v_item_uni = item["preco"]
                                    v_item_x_qtd = item['preco'] * qtd_item
                                    valor_a_pagar += v_item_x_qtd
                            dicionario=[ num_item ,cod_item,  ean_item,  desc_item, qtd_item ,v_item_uni, v_item_x_qtd]
                                           
                            carrinho.append(dicionario)
                            window["descricao"].update(desc_item)
                            window['-TABELA-'].update(values=carrinho)
                            window["unitario"].update(f"{v_item_uni:.2f}")
                            window["preco"].update(f"{v_item_x_qtd:.2f}")
                            window['subtotal'].update(f" {valor_a_pagar:.2f}")
                            
                            
                          
              
                elif event == 'DELETE':
                    valor_a_pagar = remover(valor_a_pagar)
                    window['subtotal'].update(f"R$ {valor_a_pagar:.2f}")
                    window["-TABELA-"].update(values=carrinho)

                    cancelados = len(item_cancelado)
                     # condição para mostra o valor estornado
                    if cancelados == 1:
                        
                        
                        item_cancelado.clear()
                    continue

                elif event == 'PAGAR':
                    # condição para conciderar o cupom com "pago"
                    valor_a_pagar = pagar(valor_a_pagar)
                    if valor_a_pagar == float(0):
                        lista_cupom.extend(carrinho)
                        limpar_saida()
                        num_item = 0
                        print(f"lista_produto{lista_cupom}")
                        break
                    else:
                        continue
                elif event == "VOLTAR":  # limpa todos os valores e lista local
                    carrinho.clear()
                    limpar_saida()

                    valor_a_pagar = 0
                    n_cupom -= 1
                    
                    break
                elif event == (sg.WIN_CLOSED):
                    sg.popup("ENCERRAR", font=("Any", 18))
                    break
            except ValueError:  # trata erro de valor não numerico
                sg.popup('Erro na quantidade', title="Erro em Quantidade", font=("Any", 18))
                continue
    elif event == "Venda Total":
        limpar_saida()
        
    
    elif event == "VOLTAR":
        window['caixa'].update('CAIXA FECHADO')
        limpar_saida()
        continue
    elif event == "Novo Produto":
        limpar_saida()
        
    elif event == "Venda Cupom":
        cupom=sg.popup_get_text("Informe o item da Pesquisa")
        limpar_saida()
        cupom=venda_cupom(cupom)
        if cupom==True:
            window["-TABELA-"].update(values=pesquisa_cupom)
        else:
            sg.popup("Seu cupom não foi encontrado")
    elif event == "Data":
        limpar_saida()
        data = sg.popup_get_text("Data", font=("Any", 18))
        if data:  # permite inserir uma data atual ao sistema
            window["data"].update(f'{data}')

    elif event == "Ajuda":
        sg.popup_scrolled(" Sistema em desenvolvimento, algumas funcionalidades  podem  apresentar erros\n" +
                          "e falhas inesperadas, caso ocorram problemas reportem ao desenvolvedor  atraves\n" +
                          "do contato disponivel pra que as correções seja incorporadas ao codigo.Em brevo\n" +
                          "apresentaremos uma bibliotca. Aguardem!\n" +
                          "delps.santos1987@gmail.com , linkedin.com/in/deleon-santos-1b835a290\n" +
                          "\n" +
                          "PRIMEIROS PASSOS EM APP_VENDAS\n" +
                          "\n" +
                          "-Novo>\n" +
                          "  -Pesqisar Produto: Pesquisa todos os produtos cadastrados ate o ultimo login.\n" +
                          "  -Novo Produto:Cadastra um novo produto no banco de dados(OBS:o novo item sera\n" +
                          "   exibido no proximo login).\n" +
                          "  -Nova Compra: Habilita o numero de cupom e inicia a tela de registro.\n" +
                          "       -Botão OK: Confirma a escolha do item selacionado na entrada de produto.\n" +
                          "       -Botão DELETE: Permite excluir um item da seu carrinho de compra. \n" +
                          "       -Botão PAGAR: Permite pagar o sub total do carrinho de compra. \n" +
                          "       -Botão VOLTAR: Permite cancelar o cupon ou sair de qualquer menu do APP.\n" +
                          "\n" +
                          "-Totais>\n" +
                          "   -Venda Cupon: Permite consultar por numero de cupon ou todos os cupons\n" +
                          "   -Venda Total: Permite ver a venda total por item, valores  e total de  venda\n" +
                          "\n" +
                          "-Suporte>\n" +
                          "   -Ajuda: Retorna um menu minimalista com as principais funcionalidades de app\n" +
                          "   -Data: permite alterar a data no sistema", title='Ajuda')
        continue
window.close()

