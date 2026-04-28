import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

# RUTA
ruta_carpeta = r"C:\Users\Usuario\OneDrive\Desktop\PY_2025"
archivo = "Restaurante.xlsx"
ruta = os.path.join(ruta_carpeta, archivo)

# ========================
# LIMPIAR
# ========================
def limpiar():
    input("\nEnter para continuar...")
    os.system("cls" if os.name == "nt" else "clear")

# ========================
# INICIAR EXCEL
# ========================
def iniciar_excel():
    if os.path.exists(ruta):
        return load_workbook(ruta)

    libro = Workbook()
    libro.remove(libro.active)

    # PLATOS
    platos = libro.create_sheet("Platos")
    platos.append(["CODIGO", "NOMBRE", "TIPO", "PRECIO"])

    # PEDIDOS
    pedidos = libro.create_sheet("Pedidos")
    pedidos.append(["COD_PEDIDO", "COD_PLATO", "NOMBRE", "PRECIO", "CANTIDAD", "TOTAL", "FECHA"])

    # PROVEEDORES
    proveedores = libro.create_sheet("Proveedores")
    proveedores.append(["CEDULA/NIT", "NOMBRE", "DIRECCION", "TELEFONO", "CORREO", "PRODUCTO"])

    # FACTURA (ACTUALIZADA)
    factura = libro.create_sheet("Factura")
    factura.append(["COD_FACTURA", "FECHA", "CEDULA", "NOMBRE", "COD_PEDIDO", "SUBTOTAL", "IVA", "TOTAL"])

    # TIPOS DE COMIDA
    tipos = libro.create_sheet("Tipos_Comida")
    tipos.append(["CODIGO", "TIPO"])

    libro.save(ruta)
    return libro

# ========================
# REGISTRAR PROVEEDOR
# ========================
def registrar_proveedor(libro):
    hoja = libro["Proveedores"]

    cedula = input("Cédula/NIT: ")
    nombre = input("Nombre: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    producto = input("Producto que ofrece: ")

    hoja.append([cedula, nombre, direccion, telefono, correo, producto])
    libro.save(ruta)

    print("Proveedor guardado ✔")

# ========================
# REGISTRAR PLATOS
# ========================
def registrar_platos(libro):
    hoja = libro["Platos"]
    hoja_tipos = libro["Tipos_Comida"]

    n = int(input("¿Cuántos platos?: "))

    for _ in range(n):
        codigo = input("Código: ")
        nombre = input("Nombre: ")
        tipo = input("Tipo: ")
        precio = float(input("Precio: "))

        hoja.append([codigo, nombre, tipo, precio])
        hoja_tipos.append([codigo, tipo])

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

    print("\nNUEVO PEDIDO")
    print("-"*30)

    cod_pedido = input("Código del pedido: ")
    n = int(input("¿Cuántos productos?: "))
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _ in range(n):
        print("\n--- Producto ---")
        cod_plato = input("Código del plato: ")
        plato = buscar_plato(platos, cod_plato)

        if not plato:
            print(" No existe")
            continue

        cantidad = int(input("Cantidad: "))
        precio = plato[3]
        total = precio * cantidad

        pedidos.append([cod_pedido, cod_plato, plato[1], precio, cantidad, total, fecha_actual])

        print(f"✅ {plato[1]} x{cantidad} = ${total:.2f}")

    libro.save(ruta)
    platos = libro["Platos"]
    pedidos = libro["Pedidos"]

    cod_pedido = input("Código del pedido: ")
    n = int(input("¿Cuántos productos?: "))
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

        pedidos.append([cod_pedido, cod_plato, plato[1], precio, cantidad, total, fecha_actual])

        print(f"{plato[1]} x{cantidad} = {total}")

    libro.save(ruta)

# ========================
# IMPRIMIR FACTURA
# ========================
def imprimir_factura(libro):
    pedidos = libro["Pedidos"]
    factura_hoja = libro["Factura"]

    cod_pedido = input(" Código del pedido: ").strip()
    cedula = input(" Cédula cliente: ")
    nombre = input(" Nombre cliente: ")

    print("\n" + "="*50)
    print("           FACTURA")
    print("="*50)

    subtotal = 0
    contador = 0

    print("\n DETALLE DEL PEDIDO:\n")
    print("-"*50)

    for fila in pedidos.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == cod_pedido:
            print(f"{fila[2]:15} | Cant: {fila[4]:2} | ${fila[5]:8.2f}")
            subtotal += fila[5]
            contador += 1

    print("-"*50)

    print(f" Productos: {contador}")

    if contador == 0:
        print("⚠ No se encontraron pedidos con ese código")
        return

    iva = subtotal * 0.14
    total = subtotal + iva

    print("\n RESUMEN:")
    print("-"*50)
    print(f"{'Subtotal:':20} ${subtotal:10.2f}")
    print(f"{'IVA (14%):':20} ${iva:10.2f}")
    print(f"{'TOTAL:':20} ${total:10.2f}")
    print("="*50)

    cod_factura = "F" + datetime.now().strftime("%Y%m%d%H%M%S")
    fecha = datetime.now().strftime("%Y-%m-%d")

    factura_hoja.append([cod_factura, fecha, cedula, nombre, cod_pedido, subtotal, iva, total])
    libro.save(ruta)
    pedidos = libro["Pedidos"]
    factura_hoja = libro["Factura"]

    cod_pedido = input("Código del pedido: ")
    cedula = input("Cédula cliente: ")
    nombre = input("Nombre cliente: ")

    print("\n====== FACTURA ======\n")
    print("DETALLE:\n")

    subtotal = 0

    for fila in pedidos.iter_rows(min_row=2, values_only=True):
        if str(fila[0]) == cod_pedido:
            print(f"Cod:{fila[1]} | {fila[2]} | Cant:{fila[4]} | V.Unit:{fila[3]} | Total:{fila[5]}")
            subtotal += fila[5]

    iva = subtotal * 0.14
    total = subtotal + iva

    print("\n---------------------")
    print(f"Subtotal: ${subtotal:,.2f}")
    print(f"IVA (14%): ${iva:,.2f}")
    print(f"TOTAL A PAGAR: ${total:,.2f}")
    print("---------------------")

    cod_factura = "F" + datetime.now().strftime("%Y%m%d%H%M%S")
    fecha = datetime.now().strftime("%Y-%m-%d")

    # GUARDAR EN EXCEL (ACTUALIZADO)
    factura_hoja.append([cod_factura, fecha, cedula, nombre, cod_pedido, subtotal, iva, total])
    libro.save(ruta)

# ========================
# MENÚ
# ========================
def menu():
    libro = iniciar_excel()

    while True:
        print("\n" + "="*40)
        print("   SISTEMA DE RESTAURANTE")
        print("="*40)
        print("1  Registrar platos")
        print("2  Hacer pedido")
        print("3  Registrar proveedor")
        print("4  Imprimir factura")
        print("5  Salir")
        print("="*40)

        op = input(" Seleccione una opción: ")

        if op == "1":
            registrar_platos(libro)
        elif op == "2":
            hacer_pedido(libro)
        elif op == "3":
            registrar_proveedor(libro)
        elif op == "4":
            imprimir_factura(libro)
        elif op == "5":
            print("\n Saliendo del sistema...")
            break
        else:
            print(" Opción inválida")

        limpiar()

# ========================
# EJECUTAR
# ========================
if __name__ == "__main__":
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    menu()
    import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

# RUTA
ruta_carpeta = r"C:\Users\Usuario\OneDrive\Desktop\PY_2025"
archivo = "Restaurante.xlsx"
ruta = os.path.join(ruta_carpeta, archivo)

# ========================
# LIMPIAR
# ========================
def limpiar():
    input("\nEnter para continuar...")
    os.system("cls" if os.name == "nt" else "clear")

# ========================
# INICIAR EXCEL
# ========================
def iniciar_excel():
    if os.path.exists(ruta):
        return load_workbook(ruta)

    libro = Workbook()
    libro.remove(libro.active)

    # PLATOS
    platos = libro.create_sheet("Platos")
    platos.append(["CODIGO", "NOMBRE", "TIPO", "PRECIO"])

    # PEDIDOS
    pedidos = libro.create_sheet("Pedidos")
    pedidos.append(["COD_PEDIDO", "COD_PLATO", "NOMBRE", "PRECIO", "CANTIDAD", "TOTAL", "FECHA"])

    # PROVEEDORES
    proveedores = libro.create_sheet("Proveedores")
    proveedores.append(["CEDULA/NIT", "NOMBRE", "DIRECCION", "TELEFONO", "CORREO", "PRODUCTO"])

    # FACTURA (ACTUALIZADA)
    factura = libro.create_sheet("Factura")
    factura.append(["COD_FACTURA", "FECHA", "CEDULA", "NOMBRE", "COD_PEDIDO", "SUBTOTAL", "IVA", "TOTAL"])

    # TIPOS DE COMIDA
    tipos = libro.create_sheet("Tipos_Comida")
    tipos.append(["CODIGO", "TIPO"])

    libro.save(ruta)
    return libro

# ========================
# REGISTRAR PROVEEDOR
# ========================
def registrar_proveedor(libro):
    hoja = libro["Proveedores"]

    cedula = input("Cédula/NIT: ")
    nombre = input("Nombre: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    producto = input("Producto que ofrece: ")

    hoja.append([cedula, nombre, direccion, telefono, correo, producto])
    libro.save(ruta)

    print("Proveedor guardado ✔")

# ========================
# REGISTRAR PLATOS
# ========================
def registrar_platos(libro):
    hoja = libro["Platos"]
    hoja_tipos = libro["Tipos_Comida"]

    n = int(input("¿Cuántos platos?: "))

    for _ in range(n):
        codigo = input("Código: ")
        nombre = input("Nombre: ")
        tipo = input("Tipo: ")
        precio = float(input("Precio: "))

        hoja.append([codigo, nombre, tipo, precio])
        hoja_tipos.append([codigo, tipo])

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

        pedidos.append([cod_pedido, cod_plato, plato[1], precio, cantidad, total, fecha_actual])

        print(f"{plato[1]} x{cantidad} = {total}")

    libro.save(ruta)

# ========================
# IMPRIMIR FACTURA
# ========================
def imprimir_factura(libro):
    pedidos = libro["Pedidos"]
    factura_hoja = libro["Factura"]

    cod_pedido = input("Código del pedido: ").strip()
    cedula = input("Cédula cliente: ")
    nombre = input("Nombre cliente: ")

    print("\n====== FACTURA ======\n")
    print("DETALLE:\n")

    subtotal = 0
    contador = 0  # 👈 cuenta registros encontrados

    print("Pedidos encontrados:\n")

    for fila in pedidos.iter_rows(min_row=2, values_only=True):
        if str(fila[0]).strip() == cod_pedido:
            print(f"Cod:{fila[1]} | {fila[2]} | Cant:{fila[4]} | V.Unit:{fila[3]} | Total:{fila[5]}")
            subtotal += fila[5]
            contador += 1

    # 👇 Mostrar recuento
    print("\n---------------------")
    print(f"Cantidad de productos en el pedido: {contador}")

    # 👇 Si no hay datos
    if contador == 0:
        print("⚠ No se encontraron pedidos con ese código")
        return

    iva = subtotal * 0.14
    total = subtotal + iva

    print("---------------------")
    print(f"Subtotal: ${subtotal:,.2f}")
    print(f"IVA (14%): ${iva:,.2f}")
    print(f"TOTAL A PAGAR: ${total:,.2f}")
    print("---------------------")

    cod_factura = "F" + datetime.now().strftime("%Y%m%d%H%M%S")
    fecha = datetime.now().strftime("%Y-%m-%d")

    factura_hoja.append([cod_factura, fecha, cedula, nombre, cod_pedido, subtotal, iva, total])
    libro.save(ruta)
    pedidos = libro["Pedidos"]
    factura_hoja = libro["Factura"]

    cod_pedido = input("Código del pedido: ")
    cedula = input("Cédula cliente: ")
    nombre = input("Nombre cliente: ")

    print("\n====== FACTURA ======\n")
    print("DETALLE:\n")

    subtotal = 0

    for fila in pedidos.iter_rows(min_row=2, values_only=True):
        if str(fila[0]) == cod_pedido:
            print(f"Cod:{fila[1]} | {fila[2]} | Cant:{fila[4]} | V.Unit:{fila[3]} | Total:{fila[5]}")
            subtotal += fila[5]

    iva = subtotal * 0.14
    total = subtotal + iva

    print("\n---------------------")
    print(f"Subtotal: ${subtotal:,.2f}")
    print(f"IVA (14%): ${iva:,.2f}")
    print(f"TOTAL A PAGAR: ${total:,.2f}")
    print("---------------------")

    cod_factura = "F" + datetime.now().strftime("%Y%m%d%H%M%S")
    fecha = datetime.now().strftime("%Y-%m-%d")

    # GUARDAR EN EXCEL (ACTUALIZADO)
    factura_hoja.append([cod_factura, fecha, cedula, nombre, cod_pedido, subtotal, iva, total])
    libro.save(ruta)

# ========================
# MENÚ
# ========================
def menu():
    libro = iniciar_excel()

    while True:
        print("\n" + "="*40)
        print("   SISTEMA DE RESTAURANTE")
        print("="*40)
        print("1  Registrar platos")
        print("2  Hacer pedido")
        print("3  Registrar proveedor")
        print("4  Imprimir factura")
        print("5  Salir")
        print("="*40)

        op = input(" Seleccione una opción: ")

        if op == "1":
            registrar_platos(libro)
        elif op == "2":
            hacer_pedido(libro)
        elif op == "3":
            registrar_proveedor(libro)
        elif op == "4":
            imprimir_factura(libro)
        elif op == "5":
            print("\n Saliendo del sistema...")
            break
        else:
            print(" Opción inválida")

        limpiar()
    libro = iniciar_excel()

    while True:
        print("\n=== RESTAURANTE ===")
        print("1. Registrar platos")
        print("2. Hacer pedido")
        print("3. Registrar proveedor")
        print("4. Imprimir factura")
        print("5. Salir")

        op = input("Opción: ")

        if op == "1":
            registrar_platos(libro)
        elif op == "2":
            hacer_pedido(libro)
        elif op == "3":
            registrar_proveedor(libro)
        elif op == "4":
            imprimir_factura(libro)
        elif op == "5":
            break

        limpiar()

# ========================
# EJECUTAR
# ========================
if __name__ == "__main__":
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    menu()