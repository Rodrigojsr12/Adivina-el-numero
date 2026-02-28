import customtkinter as ctk
import random

# --- Configuración General ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- Estado del Juego  ---
numero_secreto = random.randint(1, 100)
vidas = 5
historial_intentos: list[int] = []

# --- Lógica del Juego ---
def procesar_intento():
    global vidas, numero_secreto
    
    # 1. Validar la entrada del usuario
    try:
        intento = int(entrada_numero.get())
        if intento < 1 or intento > 100:
            label_feedback.configure(text="¡Eh! El número debe estar entre 1 y 100.", text_color="#f1c40f")
            return
    except ValueError:
        label_feedback.configure(text="¡Eso no es un número! Concéntrate.", text_color="#f1c40f")
        return

    if vidas <= 0:
        return

    # 2. Registrar el intento
    if intento not in historial_intentos:
        historial_intentos.append(intento)
        # Mostrar los últimos 5 intentos para no saturar la pantalla
        ultimos: list[int] = historial_intentos[-5:]
        texto_historial = " - ".join(map(str, ultimos))
        label_historial.configure(text=f"Intentos anteriores: {texto_historial}")

    # 3. Lógica principal de "Caliente o Frío"
    distancia = abs(numero_secreto - intento)
    
    if distancia == 0:
        label_feedback.configure(text=f"¡IMPOSIBLE! ¡Leíste mi mente! El número era {numero_secreto}.", text_color="#2ecc71")
        entrada_numero.configure(state="disabled")
        boton_adivinar.configure(state="disabled")
        boton_reiniciar.pack(pady=10) # Mostrar botón de jugar de nuevo
        return
    else:
        # Restar una vida y actualizar corazones
        vidas -= 1
        actualizar_corazones(vidas)
        
        if vidas == 0:
            label_feedback.configure(text=f"¡GAME OVER! Te quedaste sin vidas.\nEl número era {numero_secreto}.", text_color="#e74c3c")
            entrada_numero.configure(state="disabled")
            boton_adivinar.configure(state="disabled")
            boton_reiniciar.pack(pady=10)
            return
        
        # Dar pistas según la distancia
        if distancia <= 5:
            mensaje = f"¡{intento} está HIRVIENDO! ¡Casi me quemas!"
            color = "#ff4757" 
        elif distancia <= 15:
            mensaje = f"{intento} está Caliente. Vas por buen camino."
            color = "#ffa502" 
        elif distancia <= 30:
            mensaje = f"{intento} está Tibio... Ni fu ni fa."
            color = "#eccc68" 
        else:
            mensaje = f"¡Uff! {intento} está en el Polo Norte. ¡Frío, frío!"
            color = "#70a1ff" 
            
        label_feedback.configure(text=mensaje, text_color=color)
        
    # Limpiar la caja de texto para el siguiente intento
    entrada_numero.delete(0, 'end')

def actualizar_corazones(vidas):
    texto_vidas = "❤ " * vidas + "🤍 " * (5 - vidas)
    label_vidas.configure(text=texto_vidas)

def reiniciar_juego():
    global numero_secreto, vidas, historial_intentos
    # Restablecer estado
    numero_secreto = random.randint(1, 100)
    vidas = 5
    historial_intentos.clear()
    
    # Restablecer Interfaz
    actualizar_corazones(vidas)
    label_feedback.configure(text="Estoy pensando en un número del 1 al 100...\n¡Atrévete a adivinarlo!", text_color="white")
    label_historial.configure(text="Intentos anteriores: Ninguno")
    
    entrada_numero.configure(state="normal")
    entrada_numero.delete(0, 'end')
    boton_adivinar.configure(state="normal")
    
    # Ocultar botón de reinicio
    boton_reiniciar.pack_forget()

# --- Interfaz de Usuario ---
root = ctk.CTk()
root.title("Batalla Mental: Adivina el Número")
root.geometry("500x550")
root.resizable(False, False)

frame_principal = ctk.CTkFrame(root, corner_radius=20)
frame_principal.pack(pady=30, padx=30, fill="both", expand=True)

# Título
label_titulo = ctk.CTkLabel(frame_principal, text="Duelo contra la Máquina", font=("Segoe UI", 24, "bold"))
label_titulo.pack(pady=(20, 5))

# Corazones
label_vidas = ctk.CTkLabel(frame_principal, text="❤ ❤ ❤ ❤ ❤ ", font=("Segoe UI", 30), text_color="#e74c3c")
label_vidas.pack(pady=5)

# Mensaje del Anfitrión
label_feedback = ctk.CTkLabel(frame_principal, text="Estoy pensando en un número del 1 al 100...\n¡Atrévete a adivinarlo!", font=("Segoe UI", 16), justify="center")
label_feedback.pack(pady=20)

# Entrada de Número
entrada_numero = ctk.CTkEntry(frame_principal, font=("Segoe UI", 24), width=100, height=50, justify="center")
entrada_numero.pack(pady=10)

# Botón de Adivinar
boton_adivinar = ctk.CTkButton(frame_principal, text="¡Adivinar!", font=("Segoe UI", 18, "bold"), height=40, command=procesar_intento, fg_color="#8e44ad", hover_color="#9b59b6")
boton_adivinar.pack(pady=15)

# Botón de Reiniciar (Oculto por defecto)
boton_reiniciar = ctk.CTkButton(frame_principal, text="Jugar de Nuevo", font=("Segoe UI", 16, "bold"), height=40, command=reiniciar_juego, fg_color="#27ae60", hover_color="#2ecc71")

# Historial de Intentos
label_historial = ctk.CTkLabel(frame_principal, text="Intentos anteriores: Ninguno", font=("Segoe UI", 12), text_color="gray")
label_historial.pack(side="bottom", pady=20)

root.bind('<Return>', lambda event: procesar_intento())

root.mainloop()
