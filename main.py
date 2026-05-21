#!/usr/bin/env python3
import csv
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import print

import generador_pdf

console = Console()

def limpiar_pantalla():
    os.system('clear')

def mostrar_titulo():
    limpiar_pantalla()
    title_panel = Panel(
        "[bold cyan]SISTEMA DE CAPTURA - LABORATORIO NUBYX[/bold cyan]\n"
        "[dim]Sistema de captura de datos para laboratorio técnico[/dim]",
        border_style="cyan"
    )
    console.print(title_panel)

def seleccionar_opcion(titulo, opciones):
    table = Table(title=f"[yellow]{titulo}[/yellow]", show_header=False, box=None)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="bold white")
    for k, v in opciones.items():
        table.add_row(f"[{k}]", v)
    console.print(table)
    
    while True:
        choices = list(opciones.keys())
        opc = Prompt.ask("[green]Seleccione una opción[/green]", choices=choices)
        if opc in opciones:
            return opciones[opc]

def solicitar_datos_estres():
    datos = {}
    console.print(Panel("[bold yellow]INGRESO DE DATOS DE PRUEBAS DE ESTRÉS[/bold yellow]", border_style="yellow"))
    
    datos['vel_prueba'] = Prompt.ask("Vel. Prueba (ej. 300 Mbps)")
    datos['pot_rx'] = Prompt.ask("Pot. Rx (ej. -20 dB)")
    
    console.print("[yellow]--- Puertos LAN ---[/yellow]")
    for i in range(1, 5):
        datos[f'lan{i}_down'] = Prompt.ask(f"LAN{i} Download (Mbps)", default="")
        datos[f'lan{i}_up'] = Prompt.ask(f"LAN{i} Upload (Mbps)", default="")
        
    console.print("[yellow]--- WiFi ---[/yellow]")
    datos['wifi_24_down'] = Prompt.ask("WiFi 2.4GHz Download (Mbps)", default="")
    datos['wifi_24_up'] = Prompt.ask("WiFi 2.4GHz Upload (Mbps)", default="")
    datos['wifi_5_down'] = Prompt.ask("WiFi 5GHz Download (Mbps)", default="")
    datos['wifi_5_up'] = Prompt.ask("WiFi 5GHz Upload (Mbps)", default="")
    
    return datos

def main():
    mostrar_titulo()

    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M:%S")
    nro_informe = f"IT{datetime.now().strftime('%y%m%d%H%M')}"

    operario = Prompt.ask("\n[bold cyan]Nombre de operario a revisar el equipo[/bold cyan]").strip().upper()

    console.print()
    tipos = {"1": "ONT", "2": "ROUTER", "3": "SWITCH", "4": "OTROS"}
    tipo = seleccionar_opcion("TIPO DE EQUIPO", tipos)

    console.print()
    marcas = {"1": "ZTE", "2": "HUAWEI", "3": "CISCO", "4": "OTROS"}
    marca = seleccionar_opcion("MARCA", marcas)

    console.print()
    modelos = {"1": "ZTE F670L", "2": "ZTE F680", "3": "ZTE F6600P", "4": "HUAWEI WS5200", "5": "OTROS"}
    modelo = seleccionar_opcion("MODELO", modelos)

    while True:
        serie = Prompt.ask("\n[bold cyan]Ingrese el Número de Serie[/bold cyan]").strip().upper()
        if serie:
            break
        console.print("[bold red]El número de serie es obligatorio. Intente de nuevo.[/bold red]")

    console.print()
    etapas = {
        "1": "Registro de equipo",
        "2": "Encendido y test de leds",
        "3": "Limpieza Interna",
        "4": "Pruebas de estrés",
        "5": "Limpieza exterior",
        "6": "Empaquetado"
    }
    etapa_seleccionada = seleccionar_opcion("ETAPA ACTUAL DEL PROTOCOLO", etapas)

    datos_estres = {
        'vel_prueba': '', 'pot_rx': '',
        'lan1_down': '', 'lan1_up': '', 'lan2_down': '', 'lan2_up': '',
        'lan3_down': '', 'lan3_up': '', 'lan4_down': '', 'lan4_up': '',
        'wifi_24_down': '', 'wifi_24_up': '', 'wifi_5_down': '', 'wifi_5_up': ''
    }
    
    if etapa_seleccionada == "Pruebas de estrés":
        console.print()
        datos_estres = solicitar_datos_estres()

    # --- SECCIÓN MODIFICADA: Mayor espaciado vertical y estructura visual ---
    console.print()
    console.print(Panel("[bold yellow]OBSERVACIONES DEL TÉCNICO[/bold yellow]", border_style="yellow"))
    console.print()
    observaciones = Prompt.ask("[green]Ingrese observaciones (Presione ENTER si no hay)[/green]", default="")
    console.print()
    # ------------------------------------------------------------------------

    registro_completo = {
        "nro_informe": nro_informe,
        "fecha": fecha_actual,
        "hora": hora_actual,
        "operario": operario,
        "tipo": tipo,
        "marca": marca,
        "modelo": modelo,
        "serie": serie,
        "etapa_completada": etapa_seleccionada,
        "observaciones": observaciones,
        **datos_estres
    }

    map_resp = {
        "Registro de equipo": "resp_registro",
        "Encendido y test de leds": "resp_encendido",
        "Limpieza Interna": "resp_limpieza_int",
        "Pruebas de estrés": "resp_estres",
        "Limpieza exterior": "resp_limpieza_ext",
        "Empaquetado": "resp_empaquetado"
    }

    map_obs = {
        "Registro de equipo": "obs_registro",
        "Encendido y test de leds": "obs_encendido",
        "Limpieza Interna": "obs_limpieza_int",
        "Pruebas de estrés": "obs_estres",
        "Limpieza exterior": "resp_limpieza_ext",
        "Empaquetado": "obs_empaquetado"
    }
    
    registro_completo[map_resp[registro_completo['etapa_completada']]] = registro_completo['operario']
    registro_completo[map_obs[registro_completo['etapa_completada']]] = registro_completo['observaciones']
    etapas_list = ["Registro de equipo", "Encendido y test de leds", "Limpieza Interna", "Pruebas de estrés", "Limpieza exterior", "Empaquetado"]

    csv_file = "reportes_equipos.csv"
    file_exists = os.path.isfile(csv_file)

    filas = []
    actualizado = False
    
    if file_exists:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            filas = list(reader)
            
        for fila in filas:
            if fila.get('serie') == registro_completo['serie']:
                registro_completo['nro_informe'] = fila.get('nro_informe', registro_completo['nro_informe'])
                
                for k, v in registro_completo.items():
                    if v:
                        fila[k] = v
                
                fila['etapa_completada'] = registro_completo['etapa_completada']
                fila['fecha'] = registro_completo['fecha']
                fila['hora'] = registro_completo['hora']
                fila['operario'] = registro_completo['operario']
                fila['observaciones'] = registro_completo['observaciones']
                
                actualizado = True
                registro_completo = fila
                break
                
    if not actualizado:
        filas.append(registro_completo)

    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=registro_completo.keys())
        writer.writeheader()
        writer.writerows(filas)

    console.print(f"\n[green][+] ¡Registro guardado con éxito en '{csv_file}'![/green]")
    console.print(f"[green][+] Informe generado automáticamente: {nro_informe}[/green]")
    
    # Generate PDF
    with console.status("[bold cyan]Generando PDF del reporte...[/bold cyan]", spinner="dots"):
        pdf_path = generador_pdf.generar_pdf(registro_completo)
    
    console.print(f"[bold green][+] ¡PDF generado con éxito: {pdf_path}![/bold green]")

if __name__ == "__main__":
    main()