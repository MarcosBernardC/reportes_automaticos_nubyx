import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generar_pdf(datos):
    pdf_path = f"informe_{datos.get('nro_informe', 'generico')}.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    style_normal = ParagraphStyle('NormalText', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=11, alignment=1)
    style_bold = ParagraphStyle('BoldText', parent=style_normal, fontName='Helvetica-Bold', fontSize=9, leading=11)
    style_title = ParagraphStyle('TitleText', parent=style_normal, fontName='Helvetica-Bold', fontSize=14, leading=16)
    style_left = ParagraphStyle('LeftText', parent=style_normal, fontName='Helvetica', alignment=0)
    style_white_bold = ParagraphStyle('WhiteBold', parent=style_bold, textColor=colors.white)
    style_si_green = ParagraphStyle('SiGreen', parent=style_normal, backgroundColor=colors.HexColor("#c2f0c2"))

    def check_str(cond):
        return "<b>SI \u2714</b>" if cond else "NO \u2718"
    
    def check_mark(cond):
        return "\u2714" if cond else "\u2718"

    map_resp = {
        "Registro de equipo": "resp_registro",
        "Encendido y test de leds": "resp_encendido",
        "Limpieza Interna": "resp_limpieza_int",
        "Pruebas de estrés": "resp_estres",
        "Limpieza exterior": "resp_limpieza_ext",
        "Empaquetado": "resp_empaquetado"
    }

    nro_informe = datos.get("nro_informe", "N/A")
    fecha = datos.get("fecha", "N/A")
    hora = datos.get("hora", "N/A")
    
    # Extraer nombres únicos de responsables para cabecera superior
    revisores = []
    for k in map_resp.values():
        val = datos.get(k)
        if val and val not in revisores:
            revisores.append(val)
            
    if len(revisores) > 1:
        operario = "VARIOS TÉCNICOS"
    elif len(revisores) == 1:
        operario = revisores[0]
    else:
        operario = datos.get("operario", "N/A")
    
    header_data = [
        [
            Paragraph("<b>NUBYX</b>", style_title),
            Paragraph("INFORME DE PRUEBAS<br/>EQUIPOS NUBYX", style_title),
            Table([
                [Paragraph("N° INFORME", style_normal), Paragraph(nro_informe, style_normal)],
                [Paragraph("FECHA", style_normal), Paragraph(fecha, style_normal)],
                [Paragraph("HORA", style_normal), Paragraph(hora, style_normal)],
                [Paragraph("PROBADO POR", style_normal), Paragraph(operario, style_normal)]
            ], colWidths=[80, 100], rowHeights=[14, 14, 14, 14], 
               style=TableStyle([
                   ('BOX', (0,0), (-1,-1), 1, colors.black),
                   ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                   ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                   ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
               ]))
        ]
    ]

    header_table = Table(header_data, colWidths=[130, 230, 180])
    header_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))

    datos_equipo_titulo = Table([[Paragraph("<b>DATOS DEL EQUIPO</b>", style_bold)]], colWidths=[540], rowHeights=[18])
    datos_equipo_titulo.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    tipo = datos.get("tipo", "").upper()
    row_tipo_data = [
        [Paragraph("<b>TIPO</b>", style_bold), 
         Paragraph("ROUTER " + check_mark(tipo=="ROUTER"), style_normal), 
         Paragraph("ONT " + check_mark(tipo=="ONT"), style_normal), 
         Paragraph("<b>MARCA</b>", style_bold), 
         Paragraph("ZTE " + check_mark(datos.get("marca", "").upper()=="ZTE"), style_normal), 
         Paragraph("HUAWEI " + check_mark(datos.get("marca", "").upper()=="HUAWEI"), style_normal), 
         Paragraph("OTROS", style_bold), 
         Paragraph(check_mark(tipo not in ["ROUTER", "ONT"] and datos.get("marca", "").upper() not in ["ZTE", "HUAWEI"]), style_normal)]
    ]
    row_tipo = Table(row_tipo_data, colWidths=[67.5]*8, rowHeights=[18])
    row_tipo.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), colors.lightgrey),
        ('BACKGROUND', (3,0), (3,0), colors.lightgrey),
        ('BACKGROUND', (6,0), (6,0), colors.lightgrey),
    ]))

    modelo = datos.get("modelo", "").upper()
    serie = datos.get("serie", "N/A")
    row_modelo_data = [
        [Paragraph("<b>MODELO</b>", style_bold), 
         Paragraph("F670L " + check_mark("670" in modelo), style_normal), 
         Paragraph("F680 " + check_mark("680" in modelo), style_normal), 
         Paragraph("WS5200 " + check_mark("5200" in modelo), style_normal), 
         Paragraph("OTROS " + check_mark("670" not in modelo and "680" not in modelo and "5200" not in modelo), style_normal), 
         Paragraph("<b>SERIE</b>", style_bold), 
         Paragraph(serie, style_normal)]
    ]
    row_modelo = Table(row_modelo_data, colWidths=[67.5, 75, 75, 85, 57.5, 50, 130], rowHeights=[18])
    row_modelo.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,0), colors.lightgrey),
        ('BACKGROUND', (5,0), (5,0), colors.lightgrey),
    ]))

    sub_headers = Table([
        [Paragraph("<b>PROTOCOLOS DE PRUEBAS</b>", style_bold), Paragraph("<b>PRUEBAS DE ESTRÉS</b>", style_bold)]
    ], colWidths=[270, 270], rowHeights=[18])
    sub_headers.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    ec = datos.get("etapa_completada", "")
    
    etapas_ord = [
        "Registro de equipo",
        "Encendido y test de leds",
        "Limpieza Interna",
        "Pruebas de estrés",
        "Limpieza exterior",
        "Empaquetado"
    ]
    
    idx_actual = etapas_ord.index(ec) if ec in etapas_ord else 0
    
    etapas_done = {}
    for i, etapa in enumerate(etapas_ord):
        etapas_done[etapa] = check_str(i <= idx_actual)

    fila_vacia_izq = Paragraph("", style_normal)

    def get_resp(etapa):
        return datos.get(map_resp[etapa], "")

    def pv(k):
        v = datos.get(k, "")
        return f"{v} Mbps" if v and v != "N/A" and k not in ('vel_prueba', 'pot_rx') else str(v)

    bloque_contenido_data = [
        [Paragraph("1. Registro", style_left), Paragraph(get_resp("Registro de equipo"), style_normal), Paragraph(etapas_done["Registro de equipo"], style_si_green if "SI" in etapas_done["Registro de equipo"] else style_normal), Paragraph("", style_normal), 
         Paragraph("<b>Vel. Prueba</b>", style_bold), Paragraph(datos.get('vel_prueba',''), style_normal), Paragraph("<b>Pot. Rx</b>", style_bold), Paragraph(datos.get('pot_rx',''), style_normal)],
        [Paragraph("2. Test de Leds", style_left), Paragraph(get_resp("Encendido y test de leds"), style_normal), Paragraph(etapas_done["Encendido y test de leds"], style_si_green if "SI" in etapas_done["Encendido y test de leds"] else style_normal), Paragraph("", style_normal), 
         Paragraph("", style_white_bold), Paragraph("LAN1", style_white_bold), Paragraph("LAN2", style_white_bold), Paragraph("LAN3", style_white_bold)],
        [Paragraph("3. Limp. Interna", style_left), Paragraph(get_resp("Limpieza Interna"), style_normal), Paragraph(etapas_done["Limpieza Interna"], style_si_green if "SI" in etapas_done["Limpieza Interna"] else style_normal), Paragraph("", style_normal), 
         Paragraph("<b>Download</b>", style_normal), Paragraph(pv('lan1_down'), style_normal), Paragraph(pv('lan2_down'), style_normal), Paragraph(pv('lan3_down'), style_normal)],
        [Paragraph("4. P. estrés", style_left), Paragraph(get_resp("Pruebas de estrés"), style_normal), Paragraph(etapas_done["Pruebas de estrés"], style_si_green if "SI" in etapas_done["Pruebas de estrés"] else style_normal), Paragraph("", style_normal), 
         Paragraph("<b>Upload</b>", style_normal), Paragraph(pv('lan1_up'), style_normal), Paragraph(pv('lan2_up'), style_normal), Paragraph(pv('lan3_up'), style_normal)],
        [Paragraph("5. Limp. Exterior", style_left), Paragraph(get_resp("Limpieza exterior"), style_normal), Paragraph(etapas_done["Limpieza exterior"], style_si_green if "SI" in etapas_done["Limpieza exterior"] else style_normal), Paragraph("", style_normal), 
         Paragraph("", style_white_bold), Paragraph("LAN4", style_white_bold), Paragraph("WiFi 2.4GHz", style_white_bold), Paragraph("WiFi 5GHz", style_white_bold)],
        [Paragraph("6. Empaquetado", style_left), Paragraph(get_resp("Empaquetado"), style_normal), Paragraph(etapas_done["Empaquetado"], style_si_green if "SI" in etapas_done["Empaquetado"] else style_normal), Paragraph("", style_normal), 
         Paragraph("<b>Download</b>", style_normal), Paragraph(pv('lan4_down'), style_normal), Paragraph(pv('wifi_24_down'), style_normal), Paragraph(pv('wifi_5_down'), style_normal)],
        [fila_vacia_izq, fila_vacia_izq, fila_vacia_izq, fila_vacia_izq, 
         Paragraph("<b>Upload</b>", style_normal), Paragraph(pv('lan4_up'), style_normal), Paragraph(pv('wifi_24_up'), style_normal), Paragraph(pv('wifi_5_up'), style_normal)]
    ]

    bloque_contenido = Table(bloque_contenido_data, colWidths=[90, 80, 50, 50, 60, 70, 70, 70], rowHeights=[20]*7)
    bloque_contenido.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBEFORE', (4,0), (4,-1), 1, colors.black),
        ('BACKGROUND', (2,0), (2,5), colors.HexColor("#d4edda")),
        ('BACKGROUND', (4,0), (4,0), colors.HexColor("#e2e3e5")),
        ('BACKGROUND', (6,0), (6,0), colors.HexColor("#e2e3e5")),
        ('BACKGROUND', (4,1), (7,1), colors.HexColor("#1a1a1a")),
        ('BACKGROUND', (4,4), (7,4), colors.HexColor("#1a1a1a")),
    ]))

    footer_headers = Table([
        [Paragraph("<b>OBSERVACIONES</b>", style_bold), Paragraph("<b>TÉCNICO DE LABORATORIO</b>", style_bold)]
    ], colWidths=[270, 270], rowHeights=[18])
    footer_headers.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    map_obs = {
        "Registro de equipo": "obs_registro",
        "Encendido y test de leds": "obs_encendido",
        "Limpieza Interna": "obs_limpieza_int",
        "Pruebas de estrés": "obs_estres",
        "Limpieza exterior": "obs_limpieza_ext",
        "Empaquetado": "obs_empaquetado"
    }

    obs_lines = []
    # Revisar las obs viejas por retrocompatibilidad
    old_obs = datos.get("observaciones", "").strip()
    if old_obs and not any(old_obs in datos.get(o, "") for o in map_obs.values()):
        obs_lines.append(f"- {old_obs}")

    for etapa, key in map_obs.items():
        val = datos.get(key, "").strip()
        if val:
            obs_lines.append(f"<b>[{etapa}]</b> {val}")

    # --- SECCIÓN REFACORIZADA: Distribución en celdas individuales para el grid ---
    footer_body_data = []
    for i in range(6):
        txt_obs = Paragraph(obs_lines[i], style_left) if i < len(obs_lines) else Paragraph("", style_left)
        txt_firma = Paragraph("Firma:", style_left) if i == 0 else Paragraph("", style_left)
        footer_body_data.append([txt_obs, txt_firma])

    footer_body = Table(footer_body_data, colWidths=[270, 270], rowHeights=[18]*6)
    footer_body.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('LINEBEFORE', (1,0), (1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    # -------------------------------------------------------------------------------

    story = [
        header_table,
        Spacer(1, 10),
        datos_equipo_titulo,
        row_tipo,
        row_modelo,
        Spacer(1, 10),
        sub_headers,
        bloque_contenido,
        Spacer(1, 10),
        footer_headers,
        footer_body
    ]

    doc.build(story)
    return pdf_path