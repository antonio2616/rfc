import pyautogui
import pyperclip
import subprocess
import time
import tkinter as tk
import webbrowser
import sqlite3
import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from datetime import datetime



# ========================= TEMA OSCURO ESTILO VS CODE / MATERIAL ==============================
COLOR_BG      = "#1E1E1E"   # fondo VSCode
COLOR_PANEL   = "#252526"   # paneles
COLOR_INPUT   = "#3C3C3C"   # entradas
COLOR_TEXT    = "#D4D4D4"   # texto principal
COLOR_PRIMARY = "#0A84FF"   # azul principal
COLOR_DIVIDER = "#3C3C3C"   # líneas divisoras

TOTAL_VENTA = 200

def enviar_ticket_whatsapp():
    # Obtener número de teléfono de la tabla
    telefono = obtener_telefono_seleccionado()
    if not telefono:
        return

    telefono = telefono.replace(" ", "").replace("-", "")

    # Obtener CURP para armar el nombre del archivo
    sel = tabla.focus()
    data = tabla.item(sel)["values"]
    curp = data[2][:10].upper()
    nombre_ticket = f"ticket_{curp}.png"
    ruta_ticket = os.path.join(TICKETS_FOLDER, nombre_ticket)

    # Validar existencia del ticket
    if not os.path.exists(ruta_ticket):
        show_error("Error", "Ese ticket aún no se ha generado.\nPrimero genera el ticket.")
        return

    # MENSAJE PREVIO AUTOMÁTICO
    mensaje = "Hola, aquí está tu ticket de Ciber Lerdo. A continuación te lo envío."
    mensaje_url = mensaje.replace(" ", "%20")

    # LINK WHATSAPP WEB
    url = f"https://web.whatsapp.com/send?phone=52{telefono}&text={mensaje_url}"

    # Priorizar Chrome
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome86 = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    if os.path.exists(chrome):
        webbrowser.get(f'"{chrome}" --new-window %s').open(url)
    elif os.path.exists(chrome86):
        webbrowser.get(f'"{chrome86}" --new-window %s').open(url)
    else:
        webbrowser.open(url)

    # ABRIR CARPETA DONDE ESTÁ EL TICKET
    subprocess.Popen(f'explorer /select,"{ruta_ticket}"')

    show_info(
        "WhatsApp",
        "WhatsApp Web se abrió correctamente.\n\n"
        "⭐ Ya está escrito el mensaje previo.\n"
        "⭐ El ticket está seleccionado en la carpeta.\n\n"
        "👉 Arrastra el archivo al chat y presiona ENVIAR."
    )


def obtener_telefono_seleccionado():
    sel = tabla.focus()
    if not sel:
        show_warning("Error", "Seleccione una venta primero.")
        return None
    
    data = tabla.item(sel)["values"]
    # posición 1 porque tu tabla es:
    # ID (0), Teléfono (1), CURP (2), Anticipo (3)...
    telefono = str(data[1])
    return telefono

def avisar_whatsapp_web():
    numero = obtener_telefono_seleccionado()
    if not numero:
        return
    
    numero = numero.replace(" ", "").replace("-", "")
    
    mensaje = "Hola, tu documento ya está listo para recogerlo en Ciber Lerdo."
    mensaje_url = mensaje.replace(" ", "%20")

    url = f"https://web.whatsapp.com/send?phone=52{numero}&text={mensaje_url}"

    # Abrir en Chrome si está instalado
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome86 = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    if os.path.exists(chrome):
        webbrowser.get(f'"{chrome}" --new-window %s').open(url)
    elif os.path.exists(chrome86):
        webbrowser.get(f'"{chrome86}" --new-window %s').open(url)
    else:
        # Si no hay Chrome, usar navegador por defecto
        webbrowser.open(url)

    show_info("WhatsApp", "Se abrió WhatsApp Web.\nSolo presiona ENVIAR.")


""" def abrir_whatsapp_desktop():
    try:
        subprocess.Popen([
            "explorer.exe",
            "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
        ])
        return True
    except Exception as e:
        show_error("Error", f"No pude abrir WhatsApp Desktop:\n{e}")
        return False
 """
""" def enviar_aviso_desktop(numero):
    import pyautogui
    import pyperclip
    import time

    if not numero:
        return

    numero = numero.replace(" ", "").replace("-", "")

    # Abrir WhatsApp Desktop
    if not abrir_whatsapp_desktop():
        return

    time.sleep(4)

    # -------------------------
    #   BUSCAR EL NÚMERO
    # -------------------------
    # Click en la barra de búsqueda
    pyautogui.click(200, 150)
    time.sleep(1)

    # Limpiar barra
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    time.sleep(0.3)

    # Escribir solo el número del cliente
    pyperclip.copy(numero)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    # Abrir conversación
    pyautogui.press("enter")
    time.sleep(1.5)

    # -------------------------
    #   ENVIAR EL MENSAJE
    # -------------------------
    # Click en caja de mensaje
    pyautogui.click(400, 700)
    time.sleep(0.5)

    mensaje = "Hola, tu documento ya está listo para recogerlo en Ciber Lerdo."
    pyperclip.copy(mensaje)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.4)

    pyautogui.press("enter")

    show_info("WhatsApp", "Mensaje enviado exitosamente por WhatsApp Desktop.")
 """
""" def crear_driver_whatsapp():
    opciones = Options()
    opciones.debugger_address = "127.0.0.1:9222"

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciones
    )
    return driver
 """
""" def enviar_aviso_selenium(numero):
    try:
        numero = numero.replace(" ", "").replace("-", "")

        driver = crear_driver_whatsapp()

        # Abrir el chat del cliente
        driver.get(f"https://web.whatsapp.com/send?phone=52{numero}")
        time.sleep(5)

        # Encontrar caja de mensaje
        caja = encontrar_caja_mensaje(driver)
        if caja:
            caja.click()
            caja.send_keys("Hola, tu documento ya está listo para recogerlo en Ciber Lerdo.")
            time.sleep(1)

        # Encontrar botón enviar
        enviar = encontrar_boton_enviar(driver)
        if enviar:
            enviar.click()
            show_info("WhatsApp", "Mensaje de aviso enviado automáticamente.")
            return

        show_error("Error", "No se pudo encontrar el botón de enviar.")

    except Exception as e:
        show_error("Error", f"No se pudo enviar el mensaje:\n{e}")
 """
""" def encontrar_caja_mensaje(driver):
    xpaths = [
        "//div[@title='Escribe un mensaje']",
        "//p[@class='selectable-text copyable-text']",
        "//div[contains(@class,'copyable-text selectable-text')]",
        "//div[@data-tab='10']",
        "//footer//p",
        "//footer//div[contains(@class,'selectable-text')]",
        "//div[@aria-placeholder='Escribe un mensaje']",
        "//div[contains(@aria-label,'mensaje')]",
        "//div[contains(@class,'_ak1l')]",
        "//div[contains(@class,'_ak1y')]",
    ]

    for xp in xpaths:
        try:
            return driver.find_element(By.XPATH, xp)
        except:
            pass

    return None
 """
""" def encontrar_boton_enviar(driver):
    xpaths = [
        "//span[@data-icon='send']",
        "//button[@aria-label='Enviar']",
        "//span[contains(@data-icon,'send')]",
        "//div[@aria-label='Enviar']",
        "//div[@role='button']//*[name()='svg']",
        "//button[contains(@class,'_ak1l')]",
        "//button[@data-tab='6']",
        "//span[@data-icon='send-outline']",
    ]

    for xp in xpaths:
        try:
            return driver.find_element(By.XPATH, xp)
        except:
            pass

    return None
 """

# ========================= BASE DE DATOS COMPARTIDA (MULTI-PC) ==============================
def get_tickets_path():
    base_folder = os.path.dirname(
        sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)
    )

    config_file = os.path.join(base_folder, "config.txt")

    # Si no existe config.txt → usa carpeta local
    if not os.path.exists(config_file):
        carpeta = os.path.join(base_folder, "tickets")
        os.makedirs(carpeta, exist_ok=True)
        return carpeta

    # Leer archivo
    with open(config_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("TICKETS_PATH="):
                path = line.replace("TICKETS_PATH=", "").strip()
                os.makedirs(path, exist_ok=True)
                return path

    # Respaldo: carpeta local
    carpeta = os.path.join(base_folder, "tickets")
    os.makedirs(carpeta, exist_ok=True)
    return carpeta

TICKETS_FOLDER = get_tickets_path()

def get_database_path():
    base_folder = os.path.dirname(
        sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)
    )

    config_file = os.path.join(base_folder, "config.txt")

    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("DB_PATH="):
                    return line.replace("DB_PATH=", "").strip()

    return os.path.join(base_folder, "ventas.db")


def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)


DB_NAME = get_database_path()

# ========================= PLACEHOLDER Y FOCUS RING ==============================
def set_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="#7F7F7F")  # gris placeholder
    entry.config(highlightthickness=1, highlightbackground=COLOR_DIVIDER, relief="flat", bd=0)

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg=COLOR_TEXT)
        entry.config(highlightthickness=2,
                     highlightbackground=COLOR_PRIMARY,
                     highlightcolor=COLOR_PRIMARY)

    def on_focus_out(event):
        if entry.get().strip() == "":
            entry.insert(0, text)
            entry.config(fg="#7F7F7F")
        entry.config(highlightthickness=1,
                     highlightbackground=COLOR_DIVIDER)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ========================= BOTONES CON HOVER ==============================
def style_button(btn, base_color=COLOR_PRIMARY, hover_color="#1F8CFF"):
    btn.config(bg=base_color, activebackground=hover_color, relief="flat", bd=0)
    def on_enter(e):
        btn.config(bg=hover_color)
    def on_leave(e):
        btn.config(bg=base_color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ========================= MESSAGEBOX OSCUROS (MATERIAL DARK) ==============================
def dark_messagebox(title, message, kind="info"):
    icon_map = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "⛔"
    }

    win = tk.Toplevel(root)
    win.title(title)
    win.configure(bg=COLOR_PANEL)
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()

    frame = tk.Frame(win, bg=COLOR_PANEL)
    frame.pack(padx=20, pady=15)

    lbl_icon = tk.Label(frame,
                        text=icon_map.get(kind, "ℹ️"),
                        bg=COLOR_PANEL, fg=COLOR_PRIMARY,
                        font=("Consolas", 24, "bold"))
    lbl_icon.grid(row=0, column=0, padx=(0, 10), sticky="n")

    lbl_msg = tk.Label(frame,
                       text=message,
                       bg=COLOR_PANEL,
                       fg=COLOR_TEXT,
                       justify="left",
                       font=("Consolas", 10),
                       wraplength=260)
    lbl_msg.grid(row=0, column=1, sticky="w")

    btn = tk.Button(frame, text="Aceptar", fg="white",
                    font=("Consolas", 10),
                    command=win.destroy)
    style_button(btn, base_color=COLOR_PRIMARY)
    btn.grid(row=1, column=0, columnspan=2, pady=(15, 0))

    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = root.winfo_rootx() + (root.winfo_width() - w) // 2
    y = root.winfo_rooty() + (root.winfo_height() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

    root.wait_window(win)

def show_info(title, msg):
    dark_messagebox(title, msg, "info")

def show_warning(title, msg):
    dark_messagebox(title, msg, "warning")

def show_error(title, msg):
    dark_messagebox(title, msg, "error")

# ========================= CREAR BD ==============================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telefono TEXT NOT NULL,
            curp TEXT NOT NULL,
            tipo TEXT NOT NULL,
            anticipo REAL NOT NULL,
            resto REAL NOT NULL,
            estado TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ========================= GUARDAR VENTA ==============================
def guardar_venta():
    tel = entry_telefono.get().strip()
    curp = entry_curp.get().strip().upper()
    anticipo_txt = entry_anticipo.get().strip().replace(",", ".")

    if not tel or not curp or not anticipo_txt:
        show_warning("Error", "Todos los campos son obligatorios.")
        return

#up

    try:
        anticipo = float(anticipo_txt)
    except:
        show_error("Error", "Anticipo inválido.")
        return

    if anticipo > TOTAL_VENTA:
        show_error("Error", "El anticipo no puede ser mayor que 200.")
        return

    resto = TOTAL_VENTA - anticipo
    estado = "PAGADO" if resto == 0 else "PENDIENTE"
    fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO ventas (telefono, curp, anticipo, resto, estado, fecha, tipo) VALUES (?,?,?,?,?,?,?)",
              (tel, curp, anticipo, resto, estado, fecha, tipo_var.get()))
    conn.commit()
    conn.close()

    cargar_ventas()
    actualizar_dashboard()
    limpiar()

# ========================= LIMPIAR ==============================
def limpiar():
    entry_telefono.delete(0, tk.END)
    entry_curp.delete(0, tk.END)
    entry_anticipo.delete(0, tk.END)

# ========================= CARGAR TABLA ==============================
def cargar_ventas(filtro=None):
    for row in tabla.get_children():
        tabla.delete(row)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if filtro:
        c.execute("SELECT * FROM ventas WHERE curp LIKE ? ORDER BY id DESC",
                  (f"%{filtro.upper()}%",))
    else:
        c.execute("SELECT * FROM ventas ORDER BY id DESC")

    rows = c.fetchall()
    conn.close()

    for r in rows:
        estado = r[5]
        tag = "pendiente" if estado == "PENDIENTE" else "pagado"
        tabla.insert("", "end", values=r, tags=(tag,))

    actualizar_dashboard()

# ========================= OBTENER ID ==============================
def obtener_id():
    sel = tabla.focus()
    if not sel:
        return None
    return tabla.item(sel)["values"][0]

# ========================= MARCAR PAGADO ==============================
def marcar_pagado():
    vid = obtener_id()
    if not vid:
        show_warning("Error", "Seleccione una venta.")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE ventas SET anticipo=?, resto=?, estado='PAGADO' WHERE id=?",
              (TOTAL_VENTA, 0, vid))
    conn.commit()
    conn.close()

    cargar_ventas()
    
def abrir_whatsapp_web(numero, texto):
    numero = numero.replace(" ", "").replace("-", "")
    texto = texto.replace(" ", "%20")

    url = f"https://web.whatsapp.com/send?phone=52{numero}&text={texto}"

    # Ruta del Chrome
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    if os.path.exists(chrome):
        webbrowser.get(f'"{chrome}" --new-window %s').open(url)
    else:
        # Si falla, usa default
        webbrowser.open(url)

# ========================= GENERAR TICKET ==============================
def generar_ticket():
    vid = obtener_id()
    if not vid:
        show_warning("Error", "Selecciona una venta.")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT telefono, curp, anticipo, resto, estado, tipo, fecha FROM ventas WHERE id=?", (vid,))
    data = c.fetchone()
    conn.close()

    telefono, curp, anticipo, resto, estado, tipo, fecha = data

    # Ajuste 58mm (384 px)
    W, H = 384, 700
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Tipografías limpias
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 22)
        font_sub   = ImageFont.truetype("arialbd.ttf", 18)
        font_text  = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_title = font_sub = font_text = font_small = ImageFont.load_default()

    y = 10

    # ---------------------- LOGO ----------------------
    try:
        logo = Image.open("logo.png")
        logo = logo.resize((150, 150))
        img.paste(logo, (int((W - 150) / 2), y))
        y += 170
    except:
        draw.text((W//2 - 50, y), "CIBER LERDO", font=font_title, fill="black")
        y += 60

    # ---------------------- DATOS DEL NEGOCIO ----------------------
    draw.text((W//2 - 60, y), "CIBER LERDO", font=font_sub, fill="black")
    y += 25

    draw.text((W//2 - 130, y), "Lerdo 110, Centro, Misantla, Ver.", font=font_small, fill="black")
    y += 20

    draw.text((W//2 - 70, y), "Tel: 235-115-5320", font=font_small, fill="black")
    y += 20

    draw.text((W//2 - 140, y), "Horario: Lun–Dom 9:00 AM - 8:00 PM", font=font_small, fill="black")
    y += 35

    # Línea
    draw.line((20, y, W - 20, y), fill="black", width=2)
    y += 15

    # ---------------------- TITULO ----------------------
    draw.text((W//2 - 80, y), "COMPROBANTE", font=font_title, fill="black")
    y += 40

    # ---------------------- DATOS DEL TICKET ----------------------
    draw.line((20, y, W - 20, y), fill="black", width=2)
    y += 15

    draw.text((25, y), f"ID Venta:  {vid}", font=font_text, fill="black")
    y += 28

    draw.text((25, y), f"Fecha:  {fecha}", font=font_text, fill="black")
    y += 28

    draw.text((25, y), f"Teléfono:  {telefono}", font=font_text, fill="black")
    y += 28

    draw.text((25, y), f"CURP:  {curp}", font=font_text, fill="black")
    y += 40

    draw.text((25, y), f"Doc. Solicitado:  {tipo}", font=font_text, fill="black")
    y += 28


    # Línea
    draw.line((20, y, W - 20, y), fill="black", width=2)
    y += 20

    # ---------------------- TOTALES ----------------------
    draw.text((25, y), f"Total:       $200.00", font=font_text, fill="black"); y += 28
    draw.text((25, y), f"Anticipo:    ${anticipo:.2f}", font=font_text, fill="black"); y += 28
    draw.text((25, y), f"Resta:       ${resto:.2f}", font=font_text, fill="black"); y += 28
    draw.text((25, y), f"Estado:      {estado}", font=font_text, fill="black"); y += 40

    draw.line((20, y, W - 20, y), fill="black", width=2)
    y += 30

    # Mensaje final
    draw.text((W//2 - 100, y), "¡Gracias por su compra!", font=font_small, fill="black")

    # ---------------------- GUARDAR ----------------------
    curp4 = curp[:10].upper()
    archivo = os.path.join(TICKETS_FOLDER, f"ticket_{curp4}.png")
    img.save(archivo)

    show_info("Ticket listo", f"El ticket se guardó en:\n{archivo}")
  
# ========================= BUSCAR CURP ==============================
def buscar_curp():
    cargar_ventas(entry_buscar.get().strip())

# ========================= DASHBOARD ==============================
def actualizar_dashboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    hoy = datetime.now().strftime("%d-%m-%Y")

    t, a, r = conn.execute(
        "SELECT COUNT(*), SUM(anticipo), SUM(resto) FROM ventas WHERE fecha LIKE ?",
        (hoy + "%",)
    ).fetchone()

    pag = conn.execute(
        "SELECT COUNT(*) FROM ventas WHERE estado='PAGADO' AND fecha LIKE ?",
        (hoy + "%",)
    ).fetchone()[0]

    pen = conn.execute(
        "SELECT COUNT(*) FROM ventas WHERE estado='PENDIENTE' AND fecha LIKE ?",
        (hoy + "%",)
    ).fetchone()[0]

    conn.close()

    lbl_ventas.config(text=f"Ventas hoy:\n{t or 0}")
    lbl_ingresos.config(text=f"Ingresos:\n${a or 0}")
    lbl_pagadas.config(text=f"Pagadas:\n{pag}")
    lbl_pendientes.config(text=f"Pendientes:\n{pen}")
    
    
#======================================Validacion=======================  
def validar_anticipo(event):
    texto = entry_telefono.get()

    # Solo números
    if not texto.isdigit():
        entry_anticipo.delete(0, tk.END)
        entry_anticipo.insert(0, ''.join(filter(str.isdigit, texto)))


def validar_telefono(event):
    texto = entry_telefono.get()

    # Solo números
    if not texto.isdigit():
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, ''.join(filter(str.isdigit, texto)))
    # Máximo 10 dígitos
    if len(texto) > 10:
        entry_telefono.delete(10, tk.END)

def validar_curp(event):
    texto = entry_curp.get().upper()
    

    # Solo letras A-Z y números permitidos en CURP
    permitido = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    nuevo = ''.join(c for c in texto if c in permitido)

    entry_curp.delete(0, tk.END)
    entry_curp.insert(0, nuevo)
    
        
    if len(texto) > 18:
        entry_curp.delete(18, tk.END)


def validar_buscar(event):
    texto = entry_buscar.get().upper()
    

    # Solo letras A-Z y números permitidos en CURP
    permitido = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    nuevo = ''.join(c for c in texto if c in permitido)

    entry_buscar.delete(0, tk.END)
    entry_buscar.insert(0, nuevo)
    
        
    if len(texto) > 18:
        entry_buscar.delete(18, tk.END)
# ========================= INTERFAZ GRÁFICA ==============================
root = tk.Tk()
root.title("Control de Ventas - Ciber Lerdo")
root.configure(bg=COLOR_BG)
root.resizable(False, False)

# Fuente global tipo editor
root.option_add("*Font", "Consolas 11")

# PANEL SUPERIOR
panel_superior = tk.Frame(root, bg=COLOR_BG)
panel_superior.pack(pady=10, padx=15, fill="x")

panel_registro = tk.Frame(panel_superior, bg=COLOR_PANEL, bd=1, relief="ridge")
panel_registro.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(panel_registro, text="📝 REGISTRAR NUEVA VENTA",
         font=("Consolas", 14, "bold"),
         bg=COLOR_PANEL, fg=COLOR_PRIMARY).pack(pady=10)

icon_tel = ImageTk.PhotoImage(file=resource_path("phone.png"))
icon_curp = ImageTk.PhotoImage(file=resource_path("curp.png"))
icon_money = ImageTk.PhotoImage(file=resource_path("money.png"))

# TELÉFONO
frame_tel = tk.Frame(panel_registro, bg=COLOR_PANEL)
frame_tel.pack(fill="x", padx=10, pady=10)
tk.Label(frame_tel, image=icon_tel, bg=COLOR_PANEL).pack(side="left", padx=(0, 8))
entry_telefono = tk.Entry(frame_tel, width=25, bg=COLOR_INPUT, fg=COLOR_TEXT,
                          insertbackground=COLOR_TEXT)
entry_telefono.pack(side="left", fill="x", expand=False)
entry_telefono.bind("<KeyRelease>", validar_telefono)
set_placeholder(entry_telefono, "Número de teléfono")



# CURP
frame_curp = tk.Frame(panel_registro, bg=COLOR_PANEL)
frame_curp.pack(fill="x", padx=10, pady=5)
tk.Label(frame_curp, image=icon_curp, bg=COLOR_PANEL).pack(side="left", padx=(0, 8))
entry_curp = tk.Entry(frame_curp, width=25, bg=COLOR_INPUT, fg=COLOR_TEXT,
                      insertbackground=COLOR_TEXT)
entry_curp.pack(side="left", fill="x", expand=False)
entry_curp.bind("<KeyRelease>", validar_curp)
set_placeholder(entry_curp, "CURP del cliente")

# ANTICIPO
frame_ant = tk.Frame(panel_registro, bg=COLOR_PANEL)
frame_ant.pack(fill="x", padx=10, pady=5)
tk.Label(frame_ant, image=icon_money, bg=COLOR_PANEL).pack(side="left", padx=(0, 8))
entry_anticipo = tk.Entry(frame_ant, width=25, bg=COLOR_INPUT, fg=COLOR_TEXT,
                          insertbackground=COLOR_TEXT)
entry_anticipo.pack(side="left", fill="x", expand=False)
entry_anticipo.bind("<KeyRelease>", validar_anticipo)
set_placeholder(entry_anticipo, "Anticipo")


# ======================= TIPO DE DOCUMENTO =======================
frame_tipo = tk.Frame(panel_registro, bg=COLOR_PANEL)
frame_tipo.pack(fill="x", padx=10, pady=(5, 10))

tk.Label(frame_tipo, text="Tipo de documento:",
         bg=COLOR_PANEL, fg=COLOR_PRIMARY,
         font=("Consolas", 10, "bold")).pack(anchor="w")

tipo_doc = tk.StringVar(value="ACTA")   # valor por defecto

op1 = tk.Radiobutton(frame_tipo, text="ACTA",
                     variable=tipo_doc, value="ACTA",
                     bg=COLOR_PANEL, fg=COLOR_TEXT,
                     activebackground=COLOR_PANEL,
                     selectcolor=COLOR_BG,
                     font=("Consolas", 10))
op1.pack(anchor="w")

op2 = tk.Radiobutton(frame_tipo, text="RFC",
                     variable=tipo_doc, value="RFC",
                     bg=COLOR_PANEL, fg=COLOR_TEXT,
                     activebackground=COLOR_PANEL,
                     selectcolor=COLOR_BG,
                     font=("Consolas", 10))
op2.pack(anchor="w")


# BOTÓN GUARDAR
btn_guardar = tk.Button(panel_registro, text="💾 GUARDAR VENTA", fg="white",
                        font=("Consolas", 11, "bold"),
                        command=guardar_venta)
style_button(btn_guardar, base_color=COLOR_PRIMARY)
btn_guardar.pack(pady=15)

# PANEL BUSCAR
panel_buscar = tk.Frame(panel_superior, bg=COLOR_PANEL, bd=1, relief="ridge")
panel_buscar.pack(side="right", fill="y", padx=5)

tk.Label(panel_buscar, text="🔎 BUSCAR POR CURP",
         bg=COLOR_PANEL, fg=COLOR_PRIMARY,
         font=("Consolas", 12, "bold")).pack(pady=10)

entry_buscar = tk.Entry(panel_buscar, width=20, bg=COLOR_INPUT, fg=COLOR_TEXT,
                        insertbackground=COLOR_TEXT)
entry_buscar.pack(pady=5, padx=10)
entry_buscar.bind("<KeyRelease>", validar_buscar)
set_placeholder(entry_buscar, "Ingrese CURP")

btn_buscar = tk.Button(panel_buscar, text="Buscar", fg="white",
                       font=("Consolas", 11, "bold"),
                       command=buscar_curp)
style_button(btn_buscar, base_color=COLOR_PRIMARY)
btn_buscar.pack(pady=10)

# LÍNEA DIVISORA
tk.Frame(root, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=15, pady=(5, 5))

# DASHBOARD
dashboard = tk.Frame(root, bg=COLOR_PANEL, bd=1, relief="ridge")
dashboard.pack(pady=5, padx=15, fill="x")

tk.Label(dashboard, text="📊 RESUMEN DEL DÍA",
         bg=COLOR_PANEL, fg=COLOR_PRIMARY,
         font=("Consolas", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=5)

lbl_ventas = tk.Label(dashboard, text="Ventas hoy:\n0", bg=COLOR_PANEL, fg=COLOR_TEXT)
lbl_ingresos = tk.Label(dashboard, text="Ingresos:\n$0", bg=COLOR_PANEL, fg=COLOR_TEXT)
lbl_pagadas = tk.Label(dashboard, text="Pagadas:\n0", bg=COLOR_PANEL, fg=COLOR_TEXT)
lbl_pendientes = tk.Label(dashboard, text="Pendientes:\n0", bg=COLOR_PANEL, fg=COLOR_TEXT)

lbl_ventas.grid(row=1, column=0, padx=20, pady=10)
lbl_ingresos.grid(row=1, column=1, padx=20, pady=10)
lbl_pagadas.grid(row=1, column=2, padx=20, pady=10)
lbl_pendientes.grid(row=1, column=3, padx=20, pady=10)

# OTRA LÍNEA DIVISORA
tk.Frame(root, bg=COLOR_DIVIDER, height=1).pack(fill="x", padx=15, pady=(5, 5))

# TABLA
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background=COLOR_PANEL,
                foreground=COLOR_TEXT,
                fieldbackground=COLOR_PANEL,
                rowheight=25,
                bordercolor=COLOR_DIVIDER)

style.configure("Treeview.Heading",
                background=COLOR_PRIMARY,
                foreground="white",
                font=("Consolas", 10, "bold"))

style.map("Treeview",
          background=[("selected", "#264F78")],
          foreground=[("selected", "white")])

cols = ("ID","Teléfono","CURP","Tipo","Anticipo","Resta","Estado","Fecha")
tabla = ttk.Treeview(root, columns=cols, show="headings", height=12)
tabla.pack(pady=10, padx=10, fill="x")

for col in cols:
    tabla.heading(col, text=col)

tabla.column("ID", width=40, anchor="center")
tabla.column("Teléfono", width=110)
tabla.column("CURP", width=140)
tabla.column("Tipo", width=80, anchor="center")
tabla.column("Anticipo", width=80, anchor="e")
tabla.column("Resta", width=80, anchor="e")
tabla.column("Estado", width=100, anchor="center")
tabla.column("Fecha", width=150)

tabla.tag_configure("odd", background="#2D2D2D")
tabla.tag_configure("even", background="#252526")
tabla.tag_configure("pendiente", background="#5A1E1E", foreground="#EFA5A5")
tabla.tag_configure("pagado", background="#1E4A1E", foreground="#A5EFA5")

# BOTONES INFERIORES
frame_btn = tk.Frame(root, bg=COLOR_BG)
frame_btn.pack(pady=10)

btn_pagado = tk.Button(frame_btn, text="✅ Marcar Pagado",
                       fg="black", width=18,
                       font=("Segoe UI Emoji", 10),
                       command=marcar_pagado)
style_button(btn_pagado, base_color="#22C55E", hover_color="#16A34A")
btn_pagado.grid(row=0, column=0, padx=5)

btn_ticket = tk.Button(frame_btn, text="🧾 Generar Ticket",
                       fg="white", width=18,
                       font=("Segoe UI Emoji", 10),
                       command=generar_ticket)
style_button(btn_ticket, base_color="#2563EB", hover_color="#1D4ED8")
btn_ticket.grid(row=0, column=1, padx=5)

btn_ticket_whatsapp = tk.Button(frame_btn, text="📨 Enviar Ticket",
                       fg="black", width=18,
                       font=("Segoe UI Emoji", 10),
                       command=enviar_ticket_whatsapp)
style_button(btn_ticket_whatsapp, base_color="#06B6D4", hover_color="#0891B2")
btn_ticket_whatsapp.grid(row=0, column=3, padx=5)


btn_avisar = tk.Button(frame_btn, text=" 📢 Avisar",
                       fg="black", width=18,
                       font=("Segoe UI Emoji", 10),
                       command= avisar_whatsapp_web)
style_button(btn_avisar, base_color="#E9BD0D", hover_color ="#EAB308")
btn_avisar.grid(row=0, column=5, padx=5)


# ========================= INICIO ==============================
init_db()
cargar_ventas()
root.mainloop()
