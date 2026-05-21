import sys
import os
import csv
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QLabel, QLineEdit, QComboBox, QTextEdit, 
    QPushButton, QGroupBox, QGridLayout, QMessageBox, QScrollArea,
    QCompleter
)
from PyQt6.QtCore import Qt

import generador_pdf

class NubyxApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Captura - Laboratorio Nubyx")
        self.resize(800, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Título
        lbl_titulo = QLabel("INFORME DE PRUEBAS AUTOMATIZADO - NUBYX")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(lbl_titulo)

        # Content Split
        h_layout = QHBoxLayout()
        
        # --- LEFT PANE ---
        left_layout = QVBoxLayout()
        left_group = QGroupBox("Datos del Equipo y Protocolo")
        form_izq = QFormLayout()
        
        self.operario = QLineEdit()
        self.tipo = QComboBox()
        self.tipo.addItems(["ONT", "ROUTER", "SWITCH", "OTROS"])
        
        self.marca = QComboBox()
        self.marca.addItems(["ZTE", "HUAWEI", "CISCO", "OTROS"])
        
        self.modelo = QComboBox()
        self.modelo.addItems(["ZTE F670L", "ZTE F680", "ZTE F6600P", "HUAWEI WS5200", "OTROS"])
        
        self.serie = QLineEdit()
        self.serie.editingFinished.connect(self.buscar_serie)
        self.serie.returnPressed.connect(self.buscar_serie)
        self.serie.textChanged.connect(lambda: self.serie.setStyleSheet(""))
        
        self.setup_completer()
        
        self.etapa = QComboBox()
        self.etapas_list = [
            "Registro de equipo", 
            "Encendido y test de leds", 
            "Limpieza Interna", 
            "Pruebas de estrés", 
            "Limpieza exterior", 
            "Empaquetado"
        ]
        self.etapa.addItems(self.etapas_list)
        self.etapa.currentIndexChanged.connect(self.check_etapa)
        
        form_izq.addRow("Operario:", self.operario)
        form_izq.addRow("Tipo:", self.tipo)
        form_izq.addRow("Marca:", self.marca)
        form_izq.addRow("Modelo:", self.modelo)
        form_izq.addRow("Serie:", self.serie)
        form_izq.addRow("Etapa de Protocolo:", self.etapa)
        
        left_group.setLayout(form_izq)
        left_layout.addWidget(left_group)
        
        # Observaciones (Bajo datos generales)
        obs_group = QGroupBox("Observaciones")
        obs_layout = QVBoxLayout()
        self.observaciones = QTextEdit()
        self.observaciones.setMaximumHeight(80)
        obs_layout.addWidget(self.observaciones)
        obs_group.setLayout(obs_layout)
        left_layout.addWidget(obs_group)
        
        left_layout.addStretch()
        h_layout.addLayout(left_layout, 1)
        
        # --- RIGHT PANE ---
        self.right_group = QGroupBox("Pruebas de Estrés")
        right_layout = QVBoxLayout()
        
        form_right = QFormLayout()
        self.vel_prueba = QLineEdit()
        self.vel_prueba.setPlaceholderText("ej. 300")
        self.pot_rx = QLineEdit()
        self.pot_rx.setPlaceholderText("ej. -20")
        form_right.addRow("Velocidad de Prueba (Mbps):", self.vel_prueba)
        form_right.addRow("Potencia Rx (dB):", self.pot_rx)
        right_layout.addLayout(form_right)
        
        # Grid para LAN y WiFi
        # Columns: Interface | Download | Upload
        grid_estres = QGridLayout()
        labels = ["Interfaz", "Download (Mbps)", "Upload (Mbps)"]
        for col, txt in enumerate(labels):
            lbl = QLabel(f"<b>{txt}</b>")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid_estres.addWidget(lbl, 0, col)
            
        self.red_inputs = {}
        interfaces = [
            ("LAN 1", "lan1"), ("LAN 2", "lan2"), 
            ("LAN 3", "lan3"), ("LAN 4", "lan4"),
            ("WiFi 2.4 GHz", "wifi_24"), ("WiFi 5 GHz", "wifi_5")
        ]
        
        for row, (label, key) in enumerate(interfaces, start=1):
            grid_estres.addWidget(QLabel(label), row, 0)
            inp_down = QLineEdit()
            inp_up = QLineEdit()
            self.red_inputs[f"{key}_down"] = inp_down
            self.red_inputs[f"{key}_up"] = inp_up
            grid_estres.addWidget(inp_down, row, 1)
            grid_estres.addWidget(inp_up, row, 2)
            
        right_layout.addLayout(grid_estres)
        self.right_group.setLayout(right_layout)
        
        h_layout.addWidget(self.right_group, 1)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(h_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
        # Button
        self.btn_generar = QPushButton("GENERAR INFORME Y GUARDAR")
        self.btn_generar.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; padding: 10px; font-size: 14px;")
        self.btn_generar.clicked.connect(self.generar_informe)
        main_layout.addWidget(self.btn_generar)
        
        self.check_etapa()
        
    def setup_completer(self):
        self.series_list = []
        csv_file = "reportes_equipos.csv"
        if os.path.isfile(csv_file):
            try:
                with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for fila in reader:
                        if fila.get('serie') and fila['serie'] not in self.series_list:
                            self.series_list.append(fila['serie'])
            except Exception:
                pass
                
        self.completer = QCompleter(self.series_list)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.serie.setCompleter(self.completer)
        self.completer.activated.connect(lambda: self.buscar_serie())

    def buscar_serie(self):
        serie_buscada = self.serie.text().strip().upper()
        if not serie_buscada:
            return
            
        csv_file = "reportes_equipos.csv"
        if not os.path.isfile(csv_file):
            return
            
        try:
            with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    if fila.get('serie') == serie_buscada:
                        # Auto-fill fields if a match is found
                        self.operario.setText(fila.get('operario', ''))
                        self._set_combo_text(self.tipo, fila.get('tipo', ''))
                        self._set_combo_text(self.marca, fila.get('marca', ''))
                        self._set_combo_text(self.modelo, fila.get('modelo', ''))
                        self._set_combo_text(self.etapa, fila.get('etapa_completada', ''))
                        
                        map_obs = {
                            "Registro de equipo": "obs_registro",
                            "Encendido y test de leds": "obs_encendido",
                            "Limpieza Interna": "obs_limpieza_int",
                            "Pruebas de estrés": "obs_estres",
                            "Limpieza exterior": "obs_limpieza_ext",
                            "Empaquetado": "obs_empaquetado"
                        }
                        # Leer la observacion actual
                        et = fila.get('etapa_completada', '')
                        self.observaciones.setPlainText(fila.get(map_obs.get(et, 'observaciones'), ''))
                        self.vel_prueba.setText(fila.get('vel_prueba', ''))
                        self.pot_rx.setText(fila.get('pot_rx', ''))
                        
                        for k, inp in self.red_inputs.items():
                            if k in fila:
                                inp.setText(fila.get(k, ''))
                        
                        self.check_etapa()
                        self.serie.setStyleSheet("background-color: #d4edda; color: black; font-weight: bold;")
                        print(f"[UI] Serie {serie_buscada} encontrada y cacheada.")
                        break
                    else:
                        self.serie.setStyleSheet("")
        except Exception as e:
            print(f"Error buscando serie: {e}")

    def _set_combo_text(self, combo, text):
        if not text: return
        idx = combo.findText(text)
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def check_etapa(self):
        etapa_val = self.etapa.currentText()
        # Habiliar sólo si la etapa de protocolo incluye estrés o alguna posterior donde se haya comprobado el estrés teóricamente.
        # Originalmente la TUI pedía datos SI es Pruebas de estrés. Evaluando la UI la dejamos activa para rellenado condicional.
        if "estrés" in etapa_val.lower():
            self.right_group.setEnabled(True)
        else:
            # Puedes optar por dejarlo activo si el técnico quiere llenarlos igual, pero sigamos la lógica
            self.right_group.setEnabled(False)

    def generar_informe(self):
        # Validations
        if not self.operario.text().strip():
            QMessageBox.warning(self, "Error", "El nombre de operario es obligatorio.")
            return
            
        if not self.serie.text().strip():
            QMessageBox.warning(self, "Error", "El número de serie del equipo es obligatorio.")
            return
            
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        nro_informe = f"IT{datetime.now().strftime('%y%m%d%H%M')}"
        
        datos = {
            "nro_informe": nro_informe,
            "fecha": fecha_actual,
            "hora": hora_actual,
            "operario": self.operario.text().strip().upper(),
            "tipo": self.tipo.currentText(),
            "marca": self.marca.currentText(),
            "modelo": self.modelo.currentText(),
            "serie": self.serie.text().strip().upper(),
            "etapa_completada": self.etapa.currentText(),
            "observaciones": self.observaciones.toPlainText().strip()
        }
        
        datos['vel_prueba'] = self.vel_prueba.text().strip()
        datos['pot_rx'] = self.pot_rx.text().strip()
        
        map_obs = {
            "Registro de equipo": "obs_registro",
            "Encendido y test de leds": "obs_encendido",
            "Limpieza Interna": "obs_limpieza_int",
            "Pruebas de estrés": "obs_estres",
            "Limpieza exterior": "obs_limpieza_ext",
            "Empaquetado": "obs_empaquetado"
        }
        
        map_resp = {
            "Registro de equipo": "resp_registro",
            "Encendido y test de leds": "resp_encendido",
            "Limpieza Interna": "resp_limpieza_int",
            "Pruebas de estrés": "resp_estres",
            "Limpieza exterior": "resp_limpieza_ext",
            "Empaquetado": "resp_empaquetado"
        }
        
        datos[map_resp[datos['etapa_completada']]] = datos['operario']
        datos[map_obs[datos['etapa_completada']]] = self.observaciones.toPlainText().strip()
        
        for k, inp in self.red_inputs.items():
            datos[k] = inp.text().strip()
            
        # CSV
        csv_file = "reportes_equipos.csv"
        file_exists = os.path.isfile(csv_file)
        
        filas = []
        actualizado = False
        
        try:
            if file_exists:
                with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    filas = list(reader)
                    
                for fila in filas:
                    if fila.get('serie') == datos['serie']:
                        datos['nro_informe'] = fila.get('nro_informe', datos['nro_informe'])
                        
                        for k, v in datos.items():
                            if v:
                                fila[k] = v
                        
                        fila['etapa_completada'] = datos['etapa_completada']
                        fila['fecha'] = datos['fecha']
                        fila['hora'] = datos['hora']
                        fila['operario'] = datos['operario']
                        fila['observaciones'] = datos['observaciones']
                        
                        actualizado = True
                        datos = fila
                        break
                        
            if not actualizado:
                filas.append(datos)

            with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=datos.keys())
                writer.writeheader()
                writer.writerows(filas)
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar CSV", str(e))
            return
            
        # PDF
        try:
            pdf_path = generador_pdf.generar_pdf(datos)
            QMessageBox.information(self, "Éxito", f"Reporte guardado en {csv_file}\nPDF generado: {pdf_path}")
            
            # Limpiar algunos campos clave
            self.serie.clear()
            self.observaciones.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error al generar PDF", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Try an application style that looks somewhat modern across OS
    app.setStyle('Fusion')
    
    window = NubyxApp()
    window.show()
    sys.exit(app.exec())
