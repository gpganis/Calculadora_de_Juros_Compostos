from flet import (
    app, Page, ThemeMode, TextField, ElevatedButton, Row, Column, Container, 
    padding, Alignment, MainAxisAlignment, ButtonStyle, RoundedRectangleBorder, colors
)

def main(page: Page):

    page.title = "Calculadora de Juros Compostos"
    page.theme_mode = ThemeMode.LIGHT
    page.window.resizable = False
    page.window.maximizable = False
    page.window.center()
    page.window.width = 500
    page.window.height = 500
    
    def limpar_campos(e):
        for campo in [txt1, txt2, txt3, txt4]:
            campo.value = ""
            campo.error_text = None
        page.update()

    def calcular_juros_compostos(e):
        
        # Resetar as mensagens de erro ao iniciar o cálculo
        txt1.error_text = None
        txt2.error_text = None
        txt3.error_text = None
        txt4.error_text = None
        
        try:
            valor_inicial = float(txt1.value.replace(",","."))
            if valor_inicial < 0:
                raise ValueError("Valor inicial deve ser positivo")
        except ValueError:
            txt1.error_text = "Informe um valor inicial válido"
            valor_inicial = None

        try:
            taxa_juros = float(txt2.value.replace(",","."))
            if taxa_juros < 0:
                raise ValueError("Taxa de juros deve ser positiva")
        except ValueError:
            txt2.error_text = "Informe uma taxa de juros válida"
            taxa_juros = None

        try:
            deposito_mensal = float(txt3.value.replace(",","."))
            if deposito_mensal < 0:
                raise ValueError("Depósito mensal deve ser positivo")
        except ValueError:
            txt3.error_text = "Informe um depósito mensal válido"
            deposito_mensal = None

        try:
            periodo = int(txt4.value)
            if periodo < 0:
                raise ValueError("Período deve ser positivo")
        except ValueError:
            txt4.error_text = "Informe um período válido"
            periodo = None

        if None not in [valor_inicial, taxa_juros, deposito_mensal, periodo]:
            # Calcular montante usando a fórmula dos juros compostos
            taxa_juros_mensal = taxa_juros / 12 / 100
            montante = valor_inicial * (1 + taxa_juros_mensal)**periodo + deposito_mensal * (((1 + taxa_juros_mensal)**periodo - 1) / taxa_juros_mensal)
            
            txt5.value = f"{montante:.2f}"
            txt6.value = f"{(montante - (valor_inicial + deposito_mensal * periodo)):.2f}"
            txt7.value = f"{(valor_inicial + deposito_mensal * periodo):.2f}"
            
            container.visible = False
            container2.visible = True
        page.update()

    def voltar(e):
        container.visible = True
        container2.visible = False
        page.window.height = 500
        page.update()

    txt1 = TextField(label="Valor Inicial", prefix_text="R$ ", bgcolor=colors.GREEN_50)
    txt2 = TextField(label="Taxa de Juros Anual (%)", bgcolor=colors.GREEN_50)
    txt3 = TextField(label="Depósito Mensal", prefix_text="R$ ", bgcolor=colors.GREEN_50)
    txt4 = TextField(label="Período (em meses)", bgcolor=colors.GREEN_50)
    txt5 = TextField(label="Valor Final", prefix_text="R$ ", read_only=True, bgcolor=colors.GREEN_50)
    txt6 = TextField(label="Rendimentos", prefix_text="R$ ", read_only=True, bgcolor=colors.GREEN_50)
    txt7 = TextField(label="Total Investido", prefix_text="R$ ", read_only=True, bgcolor=colors.GREEN_50)
    
    btn = ElevatedButton(text="Calcular", height=45, bgcolor=colors.GREEN_700, color=colors.WHITE, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)), expand=True, on_click=calcular_juros_compostos)
    btn2 = ElevatedButton(text="Limpar", height=45, bgcolor=colors.WHITE, color=colors.GREEN_700, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)), expand=True, on_click=limpar_campos)
    btn3 = ElevatedButton(text="Voltar", height=45, bgcolor=colors.GREEN_700, color=colors.WHITE, style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)), expand=True, on_click=voltar)
    
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

    linha2 = Row(controls=[btn3], alignment=MainAxisAlignment.CENTER)
    coluna2 = Column(
        controls=[txt7,txt6,txt5,linha2],
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
