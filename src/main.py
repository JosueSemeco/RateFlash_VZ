import flet as ft
import pyBCV as pbv
import threading

# 1. Definimos la tasa como una variable global, inicialmente vacía o con un mensaje
tasa_valor = "Cargando tasa..."

# La función que obtendrá los datos de pyBCV en un hilo separado
def fetch_data(page: ft.Page, tasa_control: ft.Text):
    
    # Muestra un mensaje de carga inicial
    tasa_control.value = "Cargando tasas..."
    page.update()
    
    try:
        bcv = pbv.Currency()
        tasa_usd = bcv.get_rate(currency_code='USD')
        tasa_eur = bcv.get_rate(currency_code='EUR')
        
        tasa_control.value = f"USD: {tasa_usd}\nEUR: {tasa_eur}"
        tasa_control.size = 25
        
    except Exception as e:
        tasa_control.value = f"Error al cargar datos: {e}"
        tasa_control.color = ft.colors.RED_600

    page.update()


def main(page: ft.Page):
    page.title = "RateFlash VZ"
    page.theme_mode = "DARK"
    
    tasa_control = ft.Text(
        tasa_valor, 
        size=25,
        text_align=ft.TextAlign.CENTER
    )
    
    title = ft.Text(
        "RateFlash VZ",
        size=50,
        text_align=ft.TextAlign.CENTER
    )
    
    threading.Thread(target=fetch_data, args=(page, tasa_control)).start()

    page.add(
        ft.Container(
                title,
                alignment=ft.alignment.top_center,
            ),
        ft.SafeArea(
            ft.Container(
                tasa_control,
                alignment=ft.alignment.top_center,
                padding=20
            ),
            expand=True,
        )
    )
    
    page.update()


if __name__ == "__main__":
    ft.app(target=main)