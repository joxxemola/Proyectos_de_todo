import os
from openpyxl import Workbook, load_workbook
from datetime import datetime

# RUTA SEGURA
ruta_carpeta = r"C:\Users\Usuario\OneDrive\Desktop\PY_2025"
archivo = "Restaurante.xlsx"
ruta = os.path.join(ruta_carpeta, archivo)

# ========================
# FUNCIONES GENERALES
# ========================
def limpiar():
    input("\nPresiona Enter para continuar...")
    os.system("cls" if os.name == "nt" else "clear")

def obtener_siguiente_codigo(hoja, prefijo, columna=0):
    """Obtiene el siguiente código automático basado en el último registro"""
    max_num = 0
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        if fila[columna] and str(fila[columna]).startswith(prefijo):
            try:
                num = int(str(fila[columna]).replace(prefijo, ""))
                if num > max_num:
                    max_num = num
            except:
                pass
    return f"{prefijo}{max_num + 1:03d}"

# ========================
# INICIALIZAR EXCEL
# ========================
def iniciar_excel():
    if os.path.exists(ruta):
        return load_workbook(ruta)
    
    libro = Workbook()
    libro.remove(libro.active)
    
    # HOJA TIPOS
    tipos = libro.create_sheet("Tipos")
    tipos.append(["CODIGO", "NOMBRE"])
    
    # Datos de ejemplo

    
    # HOJA PLATOS
    platos = libro.create_sheet("Platos")
    platos.append(["CODIGO", "NOMBRE", "COD_TIPO", "TIPO", "PRECIO"])
    
    # HOJA PEDIDOS
    pedidos = libro.create_sheet("Pedidos")
    pedidos.append(["COD_PEDIDO", "FECHA", "COD_PLATO", "NOMBRE_PLATO", "PRECIO", "CANTIDAD", "TOTAL"])
    
    # HOJA PROVEEDORES
    proveedores = libro.create_sheet("Proveedores")
    proveedores.append(["NIT", "NOMBRE", "DIRECCION", "TELEFONO", "CORREO", "TIPO_PRODUCTO"])
    
    # HOJA FACTURAS
    facturas = libro.create_sheet("Facturas")
    facturas.append(["COD_FACTURA", "FECHA", "COD_CLIENTE", "NOMBRE_CLIENTE", "COD_PEDIDO", "SUBTOTAL", "IVA", "TOTAL"])
    
    libro.save(ruta)
    return libro

# ========================
# 1. REGISTRAR TIPOS (Código automático)
# ========================
def registrar_tipos(libro):
    print("\n=== REGISTRAR TIPO DE PLATO ===")
    hoja = libro["Tipos"]
    
    # Mostrar tipos existentes
    print("\n📋 Tipos ya registrados:")
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        print(f"   {fila[0]} - {fila[1]}")
    
    n = int(input("\n¿Cuántos tipos nuevos desea registrar? "))
    
    for i in range(n):
        print(f"\n--- Tipo {i+1} ---")
        # Código automático
        codigo = obtener_siguiente_codigo(hoja, "TIP", 0)
        nombre = input("Ingrese el nombre del tipo (ejemplo: Entrada, Plato Fuerte, Postre, Bebida): ")
        
        # Validar que no esté vacío
        if not nombre.strip():
            print("El nombre no puede estar vacío")
            continue
            
        hoja.append([codigo, nombre])
        print(f"✅ Tipo registrado: {codigo} - {nombre}")
    
    libro.save(ruta)
    print("\n✨ Tipos guardados exitosamente ✨")
    print("\n📌 Lista actualizada de tipos:")
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        print(f"   {fila[0]} - {fila[1]}")

# ========================
# 2. REGISTRAR PLATOS
# ========================
def registrar_platos(libro):
    print("\n=== REGISTRAR PLATO ===")
    tipo_hoja = libro["Tipos"]
    plato_hoja = libro["Platos"]
    
    # Mostrar tipos disponibles
    print("\n📋 Tipos disponibles para seleccionar:")
    tipos_disponibles = []
    for fila in tipo_hoja.iter_rows(min_row=2, values_only=True):
        print(f"   {fila[0]} - {fila[1]}")
        tipos_disponibles.append(fila)
    
    if not tipos_disponibles:
        print("⚠️ No hay tipos registrados. Por favor, registre tipos primero.")
        return
    
    n = int(input("\n¿Cuántos platos desea registrar? "))
    
    for i in range(n):
        print(f"\n--- Plato {i+1} ---")
        # Código automático para plato
        codigo = obtener_siguiente_codigo(plato_hoja, "PLA", 0)
        nombre = input("Nombre del plato: ")
        
        # Seleccionar tipo por código
        cod_tipo = input("Código del tipo (ejemplo: TIP001): ")
        tipo_nombre = None
        
        for fila in tipo_hoja.iter_rows(min_row=2, values_only=True):
            if fila[0] == cod_tipo:
                tipo_nombre = fila[1]
                break
        
        if not tipo_nombre:
            print("⚠️ Tipo no válido, por favor use un código de la lista")
            print("📌 Tipos disponibles:")
            for fila in tipo_hoja.iter_rows(min_row=2, values_only=True):
                print(f"   {fila[0]} - {fila[1]}")
            continue
        
        precio = float(input("Precio del plato: $"))
        
        plato_hoja.append([codigo, nombre, cod_tipo, tipo_nombre, precio])
        print(f"✅ Plato registrado: {codigo} - {nombre} ({tipo_nombre}) - ${precio:.2f}")
    
    libro.save(ruta)
    print("\n✨ Platos guardados exitosamente ✨")

# ========================
# 3. HACER PEDIDO
# ========================
def hacer_pedido(libro):
    print("\n=== HACER PEDIDO ===")
    plato_hoja = libro["Platos"]
    pedido_hoja = libro["Pedidos"]
    
    # Verificar si hay platos registrados
    platos_existentes = list(plato_hoja.iter_rows(min_row=2, values_only=True))
    if not platos_existentes:
        print("❌ No hay platos registrados. Por favor, registre platos primero.")
        return
    
    # Mostrar platos disponibles
    print("\n📋 Platos disponibles:")
    for fila in platos_existentes:
        print(f"   {fila[0]} - {fila[1]} ({fila[3]}) - ${fila[4]:.2f}")
    
    # Código automático para pedido
    cod_pedido = obtener_siguiente_codigo(pedido_hoja, "PED", 0)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n📋 Nuevo Pedido: {cod_pedido}")
    print(f"📅 Fecha: {fecha}")
    
    n = int(input("\n¿Cuántos platos diferentes lleva el pedido? "))
    total_pedido = 0
    items_agregados = 0
    
    for i in range(n):
        print(f"\n--- Ítem {i+1} ---")
        cod_plato = input("Código del plato: ")
        
        # Buscar el plato
        plato_info = None
        for fila in platos_existentes:
            if fila[0] == cod_plato:
                plato_info = fila
                break
        
        if not plato_info:
            print("❌ Plato no encontrado")
            continue
        
        cantidad = int(input("Cantidad: "))
        precio = plato_info[4]
        subtotal = precio * cantidad
        total_pedido += subtotal
        items_agregados += 1
        
        pedido_hoja.append([
            cod_pedido, fecha, cod_plato, plato_info[1], precio, cantidad, subtotal
        ])
        
        print(f"✅ Agregado: {plato_info[1]} x{cantidad} = ${subtotal:.2f}")
    
    if items_agregados > 0:
        libro.save(ruta)
        print(f"\n✨ Pedido {cod_pedido} creado exitosamente ✨")
        print(f"💰 Total del pedido: ${total_pedido:.2f}")
    else:
        print("\n❌ No se agregaron items al pedido")

# ========================
# 4. REGISTRAR PROVEEDOR
# ========================
def registrar_proveedor(libro):
    print("\n=== REGISTRAR PROVEEDOR ===")
    hoja = libro["Proveedores"]
    
    n = int(input("¿Cuántos proveedores desea registrar? "))
    
    for i in range(n):
        print(f"\n--- Proveedor {i+1} ---")
        nit = input("NIT del proveedor: ")
        nombre = input("Nombre del proveedor: ")
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        correo = input("Correo electrónico: ")
        tipo_producto = input("Tipo de producto que provee: ")
        
        hoja.append([nit, nombre, direccion, telefono, correo, tipo_producto])
        print(f"✅ Proveedor registrado: {nombre} - NIT: {nit}")
    
    libro.save(ruta)
    print("\n✨ Proveedores guardados exitosamente ✨")

# ========================
# 5. IMPRIMIR FACTURA
# ========================
def imprimir_factura(libro):
    print("\n=== IMPRIMIR FACTURA ===")
    pedido_hoja = libro["Pedidos"]
    factura_hoja = libro["Facturas"]
    
    cod_pedido = input("Ingrese el código del pedido: ")
    
    # Buscar todos los ítems del pedido
    items_pedido = []
    subtotal = 0
    
    for fila in pedido_hoja.iter_rows(min_row=2, values_only=True):
        if fila[0] == cod_pedido:
            items_pedido.append(fila)
            subtotal += fila[6]
    
    if not items_pedido:
        print("❌ Pedido no encontrado")
        return
    
    # Calcular IVA (14%)
    iva = subtotal * 0.14
    total = subtotal + iva
    
    # Datos del cliente
    print("\n--- Datos del Cliente ---")
    cod_cliente = input("Código del cliente: ")
    nombre_cliente = input("Nombre del cliente: ")
    
    # Código automático para factura
    cod_factura = obtener_siguiente_codigo(factura_hoja, "FAC", 0)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Guardar factura
    factura_hoja.append([
        cod_factura, fecha, cod_cliente, nombre_cliente, cod_pedido, subtotal, iva, total
    ])
    
    # IMPRIMIR FACTURA EN PANTALLA
    print("\n" + "="*60)
    print("                     FACTURA")
    print("="*60)
    print(f"Código Factura: {cod_factura}")
    print(f"Fecha: {fecha}")
    print(f"Código Pedido: {cod_pedido}")
    print(f"Código Cliente: {cod_cliente}")
    print(f"Nombre Cliente: {nombre_cliente}")
    print("-"*60)
    print("DETALLE DEL PEDIDO:")
    print("-"*60)
    
    for item in items_pedido:
        print(f"  {item[3]} x{item[5]} = ${item[6]:.2f}")
    
    print("-"*60)
    print(f"SUBTOTAL:                     ${subtotal:.2f}")
    print(f"IVA (14%):                    ${iva:.2f}")
    print("="*60)
    print(f"TOTAL A PAGAR:                ${total:.2f}")
    print("="*60)
    print("          ¡GRACIAS POR SU COMPRA!")
    print("="*60)
    
    libro.save(ruta)
    print("\n✨ Factura guardada exitosamente ✨")

# ========================
# VER TODOS LOS REGISTROS
# ========================
def ver_registros(libro):
    print("\n=== VER REGISTROS ===")
    print("1. Ver Tipos")
    print("2. Ver Platos")
    print("3. Ver Pedidos")
    print("4. Ver Proveedores")
    print("5. Ver Facturas")
    
    op = input("Opción: ")
    
    if op == "1":
        hoja = libro["Tipos"]
        print("\n=== TIPOS DE PLATOS ===")
        print("-" * 40)
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            print(f"Código: {fila[0]} | Nombre: {fila[1]}")
    
    elif op == "2":
        hoja = libro["Platos"]
        print("\n=== PLATOS REGISTRADOS ===")
        print("-" * 80)
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            print(f"Código: {fila[0]} | Nombre: {fila[1]} | Tipo: {fila[3]} | Precio: ${fila[4]:.2f}")
    
    elif op == "3":
        hoja = libro["Pedidos"]
        print("\n=== PEDIDOS REALIZADOS ===")
        print("-" * 100)
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            print(f"Pedido: {fila[0]} | Fecha: {fila[1]} | Plato: {fila[3]} | Cant: {fila[5]} | Total: ${fila[6]:.2f}")
    
    elif op == "4":
        hoja = libro["Proveedores"]
        print("\n=== PROVEEDORES REGISTRADOS ===")
        print("-" * 80)
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            print(f"NIT: {fila[0]} | Nombre: {fila[1]} | Tel: {fila[3]} | Producto: {fila[5]}")
    
    elif op == "5":
        hoja = libro["Facturas"]
        print("\n=== FACTURAS EMITIDAS ===")
        print("-" * 100)
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            print(f"Factura: {fila[0]} | Fecha: {fila[1]} | Cliente: {fila[3]} | Total: ${fila[7]:.2f}")

# ========================
# MENÚ PRINCIPAL
# ========================
def menu():
    libro = iniciar_excel()
    
    while True:
        print("\n" + "="*50)
        print("       SISTEMA DE RESTAURANTE")
        print("="*50)
        print("1. Registrar Tipos")
        print("2. Registrar Platos")
        print("3. Hacer Pedido")
        print("4. Registrar Proveedor")
        print("5. Imprimir Factura")
        print("6. Ver Registros")
        print("7. Salir")
        print("="*50)
        
        op = input("Seleccione una opción: ")
        
        if op == "1":
            registrar_tipos(libro)
        elif op == "2":
            registrar_platos(libro)
        elif op == "3":
            hacer_pedido(libro)
        elif op == "4":
            registrar_proveedor(libro)
        elif op == "5":
            imprimir_factura(libro)
        elif op == "6":
            ver_registros(libro)
        elif op == "7":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")
        
        if op != "7":
            limpiar()

# ========================
# EJECUTAR
# ========================
if __name__ == "__main__":
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(f"📁 Carpeta creada: {ruta_carpeta}")
    
    menu()