import PySimpleGUI as sg
def remover(valor_pagar,carrinho,window):
    try:  # leia a lista1 e encontre o item informado
        remove_item = int(sg.popup_get_text('Remover o Item',size=(10,1), font=("Any", 10),button_color="red"))
        print(f"item removido{remove_item}")
        for indice, material in enumerate(carrinho):
            if indice == remove_item:
                valor_pagar -= material[6]
                material[4]*=-1
                material[5]*=-1
                material[6]*=-1
                window["-TABELA-"].update(values=carrinho)
                return valor_pagar
    except:
        sg.popup("Rejeitar Item", font=("Any", 10),button_color="red")
        return valor_pagar