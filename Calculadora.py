from flet import (
    app, Page,Text, ThemeMode, TextField, ElevatedButton, Row, Column, Container, AlertDialog, TextButton,
    padding, Alignment, MainAxisAlignment, ButtonStyle, RoundedRectangleBorder, colors
)
import mysql.connector

def main(page: Page):

    page.title = "Calculadora de Juros Compostos"
    page.theme_mode = ThemeMode.LIGHT
    page.window.resizable = False
    page.window.maximizable = False
    page.window.center()
    page.window.width = 500
    page.window.height = 400
    
    def limpar_campos(e):
        for campo in [txt1, txt2, txt3, txt4]:
            campo.value = ""
            campo.error_text = None
        page.window.height = 400
        page.update()

    def voltar(e):
        container.visible = True
        container2.visible = False
        page.window.height = 400
        page.update()

    def close_dialog(e):
        if dialog1.open is True:
            dialog1.open = False 
        if dialog2.open is True: 
            dialog2.open = False
        page.update()

    def calcular_juros_compostos(e):
        
        # Resetar as mensagens de erro ao iniciar o cálculo
        txt1.error_text = None
        txt2.error_text = None
        txt3.error_text = None
        txt4.error_text = None
        
        try:
            taxa_juros = float(txt1.value.replace(",", "."))
            if taxa_juros < 0:
                raise ValueError
        except ValueError:
            txt1.error_text = "Informe Uma Taxa de Juros Válida"
            taxa_juros = None

        try:
            periodo = int(txt2.value)
            if periodo < 0:
                raise ValueError
        except ValueError:
            txt2.error_text = "Informe Um Período Válido"
            periodo = None

        try:
            valor_inicial = float(txt3.value.replace(",", "."))
            if valor_inicial < 0:
                raise ValueError
        except ValueError:
            txt3.error_text = "Informe Um valor Inicial Válido"
            valor_inicial = None

        try:
            deposito_mensal = float(txt4.value.replace(",", "."))
            if deposito_mensal < 0:
                raise ValueError
        except ValueError:
            txt4.error_text = "Informe um Depósito Mensal Válido"
            deposito_mensal = None

        if None not in [taxa_juros, periodo, valor_inicial, deposito_mensal]:
            # Calcular montante usando a fórmula dos juros compostos
            taxa_juros_mensal = taxa_juros / 12 / 100
            
            patrimonio_bruto = valor_inicial * (1 + taxa_juros_mensal)**periodo + deposito_mensal * (((1 + taxa_juros_mensal)**periodo - 1) / taxa_juros_mensal)
            
            rendimento_bruto = patrimonio_bruto - (valor_inicial + deposito_mensal * periodo)
            
            valor_investido = valor_inicial + deposito_mensal * periodo           

            rendimento_liquido = 0.0

            if periodo <= 6:
                rendimento_liquido = rendimento_bruto * 0.775
            elif 6 < periodo <= 12:
                rendimento_liquido = rendimento_bruto * 0.80
            elif 12 < periodo <= 24:
                rendimento_liquido = rendimento_bruto * 0.825
            else:
                rendimento_liquido = rendimento_bruto * 0.85

            patrimonio_liquido = valor_investido + rendimento_liquido
            
            txt5.value = f"{valor_investido:.2f}"
            txt6.value = f"{patrimonio_bruto:.2f}"
            txt7.value = f"{rendimento_bruto:.2f}"
            txt8.value = f"{patrimonio_liquido:.2f}"
            txt9.value = f"{rendimento_liquido:.2f}"

            
            container.visible = False
            page.window.height = 465
            container2.visible = True
        page.update()
    
    def enviar_para_banco(e):
        try:
            conexao = mysql.connector.connect(host="localhost",user="root",password="root",database="database")

            juros = txt1.value.replace(",", ".")
            periodo = txt2.value
            valor_inicial = txt3.value.replace(",", ".")
            deposito_mensal = txt4.value.replace(",", ".")
            investimento_total = txt5.value
            patrimonio_bruto = txt6.value
            rendimento_bruto = txt7.value
            patrimonio_liquido = txt8.value
            rendimento_liquido = txt9.value

            if conexao.is_connected():
                cursor = conexao.cursor()
                comando = f'INSERT INTO tb_investimentos (Porcentagem_ao_Ano, Período_em_Meses, Valor_Inicial, Aporte_Mensal, Investimento_Total, Patrimônio_Bruto, Rendimento_Bruto, Patrimônio_Líquido, Rendimento_Líquido) VALUES ({juros}, {periodo}, {valor_inicial}, {deposito_mensal}, {investimento_total}, {patrimonio_bruto}, {rendimento_bruto}, {patrimonio_liquido}, {rendimento_liquido})'
                cursor.execute(comando)
                conexao.commit()
                page.open(dialog1)
                
        except:
            page.open(dialog2)

    txt1 = TextField(label="Taxa de Juros Anual (%)", bgcolor=colors.WHITE)
    txt2 = TextField(label="Período (em meses)", bgcolor=colors.WHITE)
    txt3 = TextField(label="Valor Inicial", prefix_text="R$ ", bgcolor=colors.WHITE)
    txt4 = TextField(label="Aporte Mensal", prefix_text="R$ ", bgcolor=colors.WHITE) 
    btn = ElevatedButton(text="Calcular", height=45, bgcolor=colors.BLACK87, color=colors.WHITE, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)), expand=True, on_click=calcular_juros_compostos)
    btn2 = ElevatedButton(text="Limpar", height=45, bgcolor=colors.WHITE, color=colors.BLACK87, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)), expand=True, on_click=limpar_campos)
    
    txt5 = TextField(label="Investimento Total", prefix_text="R$ ", read_only=True, bgcolor=colors.BLUE_100)
    txt6 = TextField(label="Patrimônio Bruto", prefix_text="R$ ", read_only=True, bgcolor=colors.YELLOW_100)
    txt7 = TextField(label="Rendimento Bruto", prefix_text="R$ ", read_only=True, bgcolor=colors.YELLOW_100) 
    txt8 = TextField(label="Patrimônio Liquido", prefix_text="R$ ", read_only=True, bgcolor=colors.GREEN_100)
    txt9 = TextField(label="Rendimento Líquido", prefix_text="R$ ", read_only=True, bgcolor=colors.GREEN_100)    
    btn3 = ElevatedButton(text="Salvar", height=45, bgcolor=colors.BLACK87, color=colors.WHITE, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)), expand=True, on_click=enviar_para_banco)
    btn4 = ElevatedButton(text="Voltar", height=45, bgcolor=colors.WHITE, color=colors.BLACK87, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)), expand=True, on_click=voltar)
    
    dialog1 = AlertDialog(modal=True,title=Text("Sucesso!"),content=Text("Dados Salvos no Banco de Dados!"),actions=[ElevatedButton("Ok", on_click=close_dialog, color=colors.BLACK87),],actions_alignment=MainAxisAlignment.END)
    dialog2 = AlertDialog(modal=True,title=Text("Erro!"),content=Text("Conexão com o Banco de Dados Mal-Sucedida"),actions=[ElevatedButton("Ok", on_click=close_dialog, color=colors.BLACK87),],actions_alignment=MainAxisAlignment.END)

    linha = Row(controls=[btn, btn2], alignment=MainAxisAlignment.CENTER)
    coluna = Column(
        controls=[txt1,txt2,txt3,txt4,linha],
        alignment=MainAxisAlignment.CENTER,
        spacing=15
    )
    container = Container(
        content=coluna,
        padding=padding.all(20),
        alignment=Alignment(-1,0),
        expand=True,
        visible=True
    )

    linha2 = Row(controls=[btn3, btn4], alignment=MainAxisAlignment.CENTER)
    coluna2 = Column(
        controls=[txt5,txt6,txt7,txt8,txt9,linha2],
        alignment=MainAxisAlignment.CENTER,
        spacing=15
    )
    container2 = Container(
        content=coluna2,
        padding=padding.all(20),
        alignment=Alignment(-1,0),
        expand=True,
        visible=False
    )

    page.add(container, container2)

app(target=main)
