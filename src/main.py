import flet as ft
import pyBCV as pbv
import threading

tasa_valor = "Cargando tasa..."

def fetch_data(page: ft.Page, tasa_control: ft.Text):
    
    tasa_control.value = "Cargando tasas..."
    page.update()
    
    try:
        bcv = pbv.Currency()
        tasa_usd = bcv.get_rate(currency_code='USD')
        tasa_eur = bcv.get_rate(currency_code='EUR')
        
        tasa_control.value = f"USD($): {tasa_usd}\nEUR(€): {tasa_eur}"
        tasa_control.size = 20
        
    except Exception as e:
        tasa_control.value = f"Error al cargar datos: {e}"
        tasa_control.color = ft.colors.RED_600

    page.update()

def main(page: ft.Page):
    page.title = "RateFlash VZ"
    page.theme_mode = "DARK"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def openPopup(e):
        page.dialog = resultPopup
        resultPopup.open = True
        page.update()
        
    def closePopup(e):
        resultPopup.open=False
        page.update()
    
    resultPopup = ft.AlertDialog(
        title=ft.Text(
            "Conversion", 
            text_align=ft.TextAlign.CENTER
        ),
        content=ft.Text(
            f"La conversión de divisas es igual a: ",
            text_align=ft.TextAlign.CENTER,
            size=15
        ),
        actions=[
            ft.ElevatedButton("Cerrar", on_click=closePopup),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    
    title = ft.Text(
        "RateFlash VZ",
        size=40,
        weight=ft.FontWeight.W_700,
        font_family="monospace"
    )
    
    spacer1 = ft.Container(
        height=40
    )
    
    tasa_control = ft.Text(
        tasa_valor, 
        size=25,
        weight=ft.FontWeight.W_600,
        font_family="monospace"
    )
    
    threading.Thread(target=fetch_data, args=(page, tasa_control)).start()
    page.update()

    ratesColumn = ft.Column(
        controls=[tasa_control],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5
    )
    
    spacer2 = ft.Container(
        height=40
    )
    
    textCalculator = ft.Text(
        "Que deseas calcular?",
        size=25,
        weight=ft.FontWeight.W_600,
        #color=ft.Colors.WHITE,
        font_family="monospace"
    )
    
    textField = ft.CupertinoTextField(
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLACK,
        placeholder_text="Ej: 123456.789",
        placeholder_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )
    
    dropdown1 = ft.Dropdown(
        label="Tengo",
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        text_size=13,
        focused_border_color=ft.Colors.WHITE,
        width=120,
        options=[
            ft.dropdown.Option("Dolares"),
            ft.dropdown.Option("Euros"),
            ft.dropdown.Option("Bolivares"),
        ],
    )
    
    dropdown2 = ft.Dropdown(
        label="Quiero",
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        text_size=14,
        focused_border_color=ft.Colors.WHITE,
        width=125,
        options=[
            ft.dropdown.Option("Dolares"),
            ft.dropdown.Option("Euros"),
            ft.dropdown.Option("Bolivares"),
        ],
    )
    
    dropdowns = ft.Row(
        controls=[
            dropdown1,
            dropdown2
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    btnCalculate = ft.ElevatedButton(
        "Calcular",
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        on_click=openPopup,
        width=110,
        height=35,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                size=15,
                weight=ft.FontWeight.W_600,
                font_family="monospace"
            ),
            
        ),
    )
    
    appContent = ft.Column(
        controls=[
            title,
            spacer1,
            ratesColumn,
            spacer2,
            textCalculator,
            textField,
            dropdowns,
            btnCalculate,
            resultPopup
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    page.add(appContent)

if __name__ == "__main__":
    ft.app(target=main)