import flet as ft
import pyBCV as pbv
import threading
import re

tasa_valor = "Cargando tasa..."
euroConvert = None
dolarConvert = None

def fetch_data(page: ft.Page, tasa_control: ft.Text):
    
    global euroConvert, dolarConvert
    
    tasa_control.value = "Cargando tasas..."
    page.update()
    
    try:
        bcv = pbv.Currency()
        tasa_usd = bcv.get_rate(currency_code='USD')
        tasa_eur = bcv.get_rate(currency_code='EUR')
        
        tasa_control.value = f"USD: {tasa_usd}\nEUR: {tasa_eur}"
        tasa_control.size = 20
        
    except Exception as e:
        tasa_control.value = f"Error al cargar datos: {e}"
        tasa_control.color = ft.colors.RED_600

    euroConvert = float(tasa_eur)
    dolarConvert = float(tasa_usd)

    page.update()

def main(page: ft.Page):
    page.title = "RateFlash VZ"
    page.theme_mode = "DARK"
    #page.window.width = 412
    #page.window.resizable = False
    page.bgcolor = ft.Colors.TRANSPARENT
    page.fonts = {"horizon": "Horizon.otf"}
    page.theme = ft.Theme(font_family="horizon")
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def openPopup(e):
        page.dialog = resultPopup
        resultPopup.open = True
        page.update()
        
    def closePopup(e):
        resultPopup.open=False
        page.update()
    
    logo = ft.Image(
        src="iconLetters.png",
        height=175,
        width=175,
        opacity=.80
    )
    
    title = ft.Text(
        "RATEFLASH VZ",
        size=28,
        #weight=ft.FontWeight.W_900,
    )
    
    spacer1 = ft.Container(
        height=40
    )
    
    tasa_control = ft.Text(
        tasa_valor, 
        size=20,
        weight=ft.FontWeight.W_600,
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
        size=16,
        weight=ft.FontWeight.W_600,
    )
    
    textField = ft.TextField(
        bgcolor=ft.Colors.TRANSPARENT,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        width=350,
        text_style=ft.TextStyle(
            color=ft.Colors.GREY_300,
            font_family='horizon'
        ),
        hint_text="Ej: 123456.789",
        hint_style=ft.TextStyle(
            color=ft.Colors.GREY_400, 
            font_family='horizon'
        ),
        keyboard_type=ft.KeyboardType.NUMBER,
        enable_interactive_selection=False
    )
    
    dropdown1 = ft.Dropdown(
        label="Tengo",
        label_style=ft.TextStyle(size=10),
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        text_size=7,
        focused_border_color=ft.Colors.WHITE,
        width=150,
        options=[
            ft.dropdown.Option(key="Dolares", text="Dolares", content=ft.Text("Dolares", size=10)),
            ft.dropdown.Option(key="Euros", text="Euros",content=ft.Text("Euros", size=10)),
            ft.dropdown.Option(key="Bolivares", text="Bolivares",content=ft.Text("Bolivares", size=10)),
        ],
    )
    
    dropdown2 = ft.Dropdown(
        label="Quiero",
        label_style=ft.TextStyle(size=9.5),
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        text_size=7,
        focused_border_color=ft.Colors.WHITE,
        width=150,
        options=[
            ft.dropdown.Option(key="Dolares", text="Dolares", content=ft.Text("Dolares", size=10)),
            ft.dropdown.Option(key="Euros", text="Euros",content=ft.Text("Euros", size=10)),
            ft.dropdown.Option(key="Bolivares", text="Bolivares",content=ft.Text("Bolivares", size=10)),
        ],
    )
    
    dropdowns = ft.Row(
        controls=[
            dropdown1,
            dropdown2
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    contentPopup = ft.Text(
            f"Usted\nno ha ingresado\nningun valor aun",
            text_align=ft.TextAlign.CENTER,
            size=15
        )
    
    def process(e):
        
        rateOrigin = dropdown1.value
        rateDestiny = dropdown2.value
        value = (textField.value or "").strip()
        
        # Validaciones tempranas: campo vacío, caracteres inválidos o solo un punto
        if not value:
            results = "Ningun valor ha sido ingresado"
            contentPopup.value = results
            page.dialog = resultPopup
            resultPopup.open = True
            page.update()
            return
        
        if value == "." or re.search(r"[^0-9.]", value) or value.count(".") > 1:
            results = "Error!\nInformacion\nInvalida,\nIngrese\nNuevamente"
            contentPopup.value = results
            page.dialog = resultPopup
            resultPopup.open = True
            page.update()
            return
        
        try:
            moneyCalculate = float(textField.value)
            
        except ValueError:
            results = f"Ningun valor ha sido ingresado"
        
        if rateOrigin == None or rateDestiny == None:
            results = f"Ningun valor ha sido ingresado"
        
        elif rateOrigin == "Dolares" and rateDestiny == "Bolivares":
            results = f"{moneyCalculate} {rateOrigin}\nequivalen a\n{round(moneyCalculate * dolarConvert, 3)} {rateDestiny}"
            
        elif rateOrigin == "Bolivares" and rateDestiny == "Dolares":
            results = f"{moneyCalculate} {rateOrigin}\nequivalen a\n{round(moneyCalculate / dolarConvert, 3)} {rateDestiny}"
            
        elif rateOrigin == "Euros" and rateDestiny == "Bolivares":
            results = f"{moneyCalculate} {rateOrigin}\nequivalen a\n{round(moneyCalculate * euroConvert, 3)} {rateDestiny}"
            
        elif rateOrigin == "Bolivares" and rateDestiny == "Euros":
            results = f"{moneyCalculate} {rateOrigin}\nequivalen a\n{round(moneyCalculate / euroConvert, 3)} {rateDestiny}"
            
        elif rateOrigin == "Dolares" and rateDestiny == "Euros":
            results = f"{moneyCalculate} {rateOrigin}\nequivalen a\n{round(moneyCalculate * (dolarConvert / euroConvert), 3)} {rateDestiny}"
            
        elif rateOrigin == "Euros" and rateDestiny == "Dolares":
            results = f"{moneyCalculate} {rateOrigin}\nequivalen a\n{round(moneyCalculate * (euroConvert / dolarConvert), 3)} {rateDestiny}"
            
        elif rateOrigin == rateDestiny:
            results = f"{moneyCalculate} {rateOrigin}\nequivalen a\n{moneyCalculate} {rateDestiny}"
        
        contentPopup.value = results
        
        page.dialog = resultPopup
        resultPopup.open = True
        page.update()
    
    btnCalculate = ft.ElevatedButton(
        "Calcular",
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        on_click=process,
        width=150,
        height=35,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                size=15,
                weight=ft.FontWeight.W_600,
                font_family="horizon"
            ),
            
        ),
    )
    
    resultPopup = ft.AlertDialog(
        title=ft.Text(
            "Conversion",
            size=20, 
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_600
        ),
        content=contentPopup,
        actions=[
            ft.ElevatedButton("Cerrar", 
                              on_click=closePopup,
                              bgcolor=ft.Colors.RED,
                              color=ft.Colors.WHITE
                              ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    
    appContent = ft.Column(
        controls=[
            title,
            logo,
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
    
    #page.add(appContent)
    
    bg_image = ft.Image(
        src="bg.png",
        opacity=0.45,
        expand=True,
        fit=ft.ImageFit.COVER
    )
    
    content_container = ft.Container(
        padding = ft.Padding(15, 60, 15, 0),
        content=appContent,
        alignment=ft.alignment.top_center
    )
    
    page.add(
        ft.Stack(
            controls=[
                bg_image,
                content_container
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="src/assets")