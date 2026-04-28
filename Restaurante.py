import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

# RUTA SEGURA
ruta_carpeta = r"C:\Users\Usuario\OneDrive\Desktop\PY_2025"
archivo = "Restaurante.xlsx"
ruta = os.path.join(ruta_carpeta, archivo)

# ========================
# FUNCIONES GENERALES
# ========================
def limpiar():
    input("\nEnter para continuar...")
    os.system("cls" if os.name == "nt" else "clear")

def ultima_fila(hoja):
    return hoja.max_row + 1

# ========================
# INICIALIZAR EXCEL
# ========================
def iniciar_excel():
    if os.path.exists(ruta):
        return load_workbook(ruta)

    libro = Workbook()
    libro.remove(libro.active)

    # HOJA PLATOS
    platos = libro.create_sheet("Platos")
    platos.append(["CODIGO", "NOMBRE", "TIPO", "PRECIO"])

    # HOJA PEDIDOS (CON FECHA)
    pedidos = libro.create_sheet("Pedidos")
    pedidos.append(["COD_PEDIDO", "COD_PLATO", "NOMBRE", "PRECIO", "CANTIDAD", "TOTAL", "FECHA"])

    # HOJA TIPO
    tipo = libro.create_sheet("Tipo")
    tipo.append(["CODIGO", "TIPO"])

    libro.save(ruta)
    return libro

# ========================
# REGISTRAR PLATOS
# ========================
def registrar_platos(libro):
    hoja = libro["Platos"]

    # Crea la hoja Tipo si no existe
    if "Tipo" not in libro.sheetnames:
        hoja_tipo = libro.create_sheet("Tipo")
        hoja_tipo.append(["CODIGO", "TIPO"])
    else:
        hoja_tipo = libro["Tipo"]

    n = int(input("¿Cuántos platos?: "))

    for _ in range(n):
        codigo = input("Código: ")
        nombre = input("Nombre: ")
        tipo = input("Tipo (Plato Fuerte/Entrada): ")
        precio = float(input("Precio: "))

        hoja.append([codigo, nombre, tipo, precio])
        hoja_tipo.append([codigo, tipo])

    libro.save(ruta)
    print("Platos guardados ✔")

# ========================
# BUSCAR PLATO
# ========================
def buscar_plato(hoja, codigo):
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        if str(fila[0]) == str(codigo):
            return fila
    return None

# ========================
# HACER PEDIDO
# ========================
def hacer_pedido(libro):
    platos = libro["Platos"]
    pedidos = libro["Pedidos"]

    cod_pedido = input("Código del pedido: ")
    n = int(input("¿Cuántos productos?: "))

    # FECHA ACTUAL
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _ in range(n):
        cod_plato = input("Código del plato: ")
        plato = buscar_plato(platos, cod_plato)

        if not plato:
            print("No existe")
            continue

        cantidad = int(input("Cantidad: "))
        precio = plato[3]
        total = precio * cantidad

        pedidos.append([
            cod_pedido,
            cod_plato,
            plato[1],
            precio,
            cantidad,
            total,
            fecha_actual
        ])

        print(f"Agregado: {plato[1]} x{cantidad} = {total}")

    libro.save(ruta)

# ========================
# VER PEDIDO
# ========================
def ver_pedido(libro):
    hoja = libro["Pedidos"]
    codigo = input("Código pedido: ")

    total_general = 0

    print("\nDETALLE DEL PEDIDO\n")

    for fila in hoja.iter_rows(min_row=2, values_only=True):
        if str(fila[0]) == codigo:
            print(f"{fila[2]} x{fila[4]} = {fila[5]}  |  Fecha: {fila[6]}")
            total_general += fila[5]

    print(f"\nTOTAL A PAGAR: {total_general}")

# ========================
# MENÚ
# ========================
def menu():
    libro = iniciar_excel()

    while True:
        print("\n=== RESTAURANTE ===")
        print("1. Registrar platos")
        print("2. Hacer pedido")
        print("3. Ver pedido")
        print("4. Salir")

        op = input("Opción: ")

        if op == "1":
            registrar_platos(libro)
        elif op == "2":
            hacer_pedido(libro)
        elif op == "3":
            ver_pedido(libro)
        elif op == "4":
            break

        limpiar()

# ========================
# EJECUTAR
# ========================
if __name__ == "__main__":
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    menu()