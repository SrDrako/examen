import os
import datetime
import tkinter as tk
from tkinter import messagebox

num_pisos = 10
departamentos_por_piso = 4

departamentos_disponibles = [[0] * departamentos_por_piso for _ in range(num_pisos)]

clientes = []

precios_departamentos = {
    "A": 3800,
    "B": 3000,
    "C": 2800,
    "D": 3500
}

def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")

def mostrar_disponibilidad():
    disponibilidad_window = tk.Toplevel(main_window)
    disponibilidad_window.title("Disponibilidad de Departamentos")

    disponibilidad_label = tk.Label(disponibilidad_window, text="DISPONIBILIDAD DE DEPARTAMENTOS")
    disponibilidad_label.pack()

    precios_label = tk.Label(disponibilidad_window, text="Precios de los Departamentos:")
    precios_label.pack()

    precios_text = "• Tipo A: 3.800 UF\n• Tipo B: 3.000 UF\n• Tipo C: 2.800 UF\n• Tipo D: 3.500 UF"
    precios_info_label = tk.Label(disponibilidad_window, text=precios_text)
    precios_info_label.pack()

    disponibilidad_table = tk.Frame(disponibilidad_window)
    disponibilidad_table.pack()

    headers = ["PISO", "A", "B", "C", "D"]
    for i, header in enumerate(headers):
        header_label = tk.Label(disponibilidad_table, text=header)
        header_label.grid(row=0, column=i)

    for piso in range(num_pisos, 0, -1):
        fila = num_pisos - piso

        piso_label = tk.Label(disponibilidad_table, text=str(piso))
        piso_label.grid(row=fila+1, column=0)

        for tipo in ["A", "B", "C", "D"]:
            columna = ord(tipo) - ord("A")

            if departamentos_disponibles[fila][columna] == 0:
                estado_label = tk.Label(disponibilidad_table, text="[ ]")
            else:
                estado_label = tk.Label(disponibilidad_table, text="[X]")

            estado_label.grid(row=fila+1, column=columna+1)

def comprar_departamento():
    compra_window = tk.Toplevel(main_window)
    compra_window.title("Comprar Departamento")

    disponibilidad_label = tk.Label(compra_window, text="DISPONIBILIDAD DE DEPARTAMENTOS")
    disponibilidad_label.pack()

    mostrar_disponibilidad()

    def comprar():
        piso = piso_entry.get()
        tipo = tipo_entry.get()
        rut = rut_entry.get()
        nombre = nombre_entry.get()

        fila = num_pisos - int(piso)
        columna = ord(tipo) - ord("A")

        if departamentos_disponibles[fila][columna] != 0:
            messagebox.showerror("Error", "El departamento seleccionado no está disponible. Por favor, elija otro departamento.")
            return

        if not rut.isdigit() or len(rut) != 8:
            messagebox.showerror("Error", "RUN inválido. Por favor, ingrese un número de RUN válido (8 dígitos).")
            return

        if not nombre:
            messagebox.showerror("Error", "Nombre inválido. Por favor, ingrese un nombre válido.")
            return

        cliente = {
            "rut": rut,
            "piso": int(piso),
            "tipo": tipo,
            "nombre": nombre
        }

        clientes.append(cliente)
        departamentos_disponibles[fila][columna] = 1

        messagebox.showinfo("Compra realizada", "La compra del departamento se realizó correctamente.")

    piso_label = tk.Label(compra_window, text="Ingrese el número de piso (1 al 10):")
    piso_label.pack()
    piso_entry = tk.Entry(compra_window)
    piso_entry.pack()

    tipo_label = tk.Label(compra_window, text="Ingrese el tipo de departamento en mayúscula (A, B, C o D):")
    tipo_label.pack()
    tipo_entry = tk.Entry(compra_window)
    tipo_entry.pack()

    rut_label = tk.Label(compra_window, text="Ingrese el RUN del comprador (8 dígitos, sin guiones ni puntos):")
    rut_label.pack()
    rut_entry = tk.Entry(compra_window)
    rut_entry.pack()

    nombre_label = tk.Label(compra_window, text="Ingrese el nombre del comprador:")
    nombre_label.pack()
    nombre_entry = tk.Entry(compra_window)
    nombre_entry.pack()

    comprar_button = tk.Button(compra_window, text="Comprar", command=comprar)
    comprar_button.pack()

def mostrar_compradores():
    if len(clientes) == 0:
        messagebox.showinfo("Listado de Compradores", "No se ha realizado ninguna compra aún.")
        return

    compradores_window = tk.Toplevel(main_window)
    compradores_window.title("Listado de Compradores")

    listado_label = tk.Label(compradores_window, text="Listado de Compradores (ordenados por RUN):")
    listado_label.pack()

    clientes_ordenados = sorted(clientes, key=lambda x: int(x["rut"]))

    for cliente in clientes_ordenados:
        info_label = tk.Label(compradores_window, text=f"RUN: {cliente['rut']}\n"
                                                        f"Piso: {cliente['piso']}\n"
                                                        f"Tipo: {cliente['tipo']}\n"
                                                        f"Nombre: {cliente['nombre']}\n"
                                                        "--------------------")
        info_label.pack()

def mostrar_ventas_totales():
    if len(clientes) == 0:
        messagebox.showinfo("Ventas Totales", "No se ha realizado ninguna compra aún.")
        return

    total_ventas = {tipo: 0 for tipo in precios_departamentos}
    total_departamentos_vendidos = {tipo: 0 for tipo in precios_departamentos}

    for cliente in clientes:
        tipo = cliente["tipo"]
        precio = precios_departamentos[tipo]
        total_ventas[tipo] += precio
        total_departamentos_vendidos[tipo] += 1

    ventas_window = tk.Toplevel(main_window)
    ventas_window.title("Ventas Totales")

    ventas_label = tk.Label(ventas_window, text="Ventas Totales:")
    ventas_label.pack()

    for tipo, total in total_ventas.items():
        cantidad = total_departamentos_vendidos[tipo]
        info_label = tk.Label(ventas_window, text=f"Tipo {tipo} {precios_departamentos[tipo]} UF: {cantidad} - {total} UF")
        info_label.pack()

    total_label = tk.Label(ventas_window, text="TOTAL: " + str(sum(total_ventas.values())) + " UF")
    total_label.pack()

def salir():
    opcion = messagebox.askquestion("Salir", "¿Estás seguro que deseas apagar el sistema?")
    if opcion == "yes":
        fecha_actual = datetime.date.today()
        messagebox.showinfo("Salida del Sistema", f"Gracias por utilizar el Sistema de Venta de Departamentos. ¡Hasta pronto!\nFecha de salida: {fecha_actual}")
        main_window.destroy()

def iniciar_sesion():
    iniciar_window = tk.Toplevel()
    iniciar_window.title("Iniciar Sesión")

    nombre_label = tk.Label(iniciar_window, text="Ingrese su nombre:")
    nombre_label.pack()
    nombre_entry = tk.Entry(iniciar_window)
    nombre_entry.pack()

    apellido_label = tk.Label(iniciar_window, text="Ingrese su apellido:")
    apellido_label.pack()
    apellido_entry = tk.Entry(iniciar_window)
    apellido_entry.pack()

    iniciar_button = tk.Button(iniciar_window, text="Iniciar", command=lambda: ejecutar_programa(nombre_entry.get(), apellido_entry.get()))
    iniciar_button.pack()

def ejecutar_programa(nombre, apellido):
    limpiar_pantalla()
    main_window.title("Sistema de Venta de Departamentos")

    bienvenida_label = tk.Label(main_window, text=f"Bienvenido, {nombre} {apellido}.")
    bienvenida_label.pack()

    comprar_button = tk.Button(main_window, text="Comprar Departamento", command=comprar_departamento)
    comprar_button.pack()

    disponibilidad_button = tk.Button(main_window, text="Mostrar Departamentos Disponibles", command=mostrar_disponibilidad)
    disponibilidad_button.pack()

    compradores_button = tk.Button(main_window, text="Mostrar Listado de Compradores", command=mostrar_compradores)
    compradores_button.pack()

    ventas_button = tk.Button(main_window, text="Mostrar Ventas Totales", command=mostrar_ventas_totales)
    ventas_button.pack()

    salir_button = tk.Button(main_window, text="Salir", command=salir)
    salir_button.pack()

main_window = tk.Tk()
iniciar_sesion()
main_window.mainloop()
