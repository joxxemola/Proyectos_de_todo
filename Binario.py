"""
Programa que convierte un nombre completo a su representación binaria (ASCII)
y también realiza el proceso inverso: de binario a texto.
"""


def texto_a_binario(texto):
    """Convierte una cadena de texto a su representación binaria (8 bits por carácter)."""
    binario = []
    for caracter in texto:
        codigo_ascii = ord(caracter)
        # Convertimos a binario y rellenamos con ceros a la izquierda hasta 8 bits
        binario.append(format(codigo_ascii, '08b'))
    return ' '.join(binario)


def binario_a_texto(cadena_binaria):
    """Convierte una cadena binaria (bytes separados por espacios) a texto."""
    bytes_binarios = cadena_binaria.split()
    texto = ''
    for byte in bytes_binarios:
        # Validamos que el byte tenga solo 0s y 1s
        if not all(bit in '01' for bit in byte):
            return None
        codigo_ascii = int(byte, 2)
        texto += chr(codigo_ascii)
    return texto


def menu():
    while True:
        print("\n===== CONVERSOR NOMBRE <-> BINARIO (ASCII) =====")
        print("1. Convertir nombre a binario")
        print("2. Convertir binario a nombre")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            nombre = input("Ingrese el nombre completo: ")
            if nombre == '':
                print("El nombre no puede estar vacío.")
                continue
            resultado = texto_a_binario(nombre)
            print(f"\nRepresentación binaria:\n{resultado}")

        elif opcion == '2':
            cadena = input("Ingrese la cadena binaria (bytes separados por espacio): ")
            resultado = binario_a_texto(cadena)
            if resultado is None:
                print("\nError: la cadena ingresada no es un binario válido "
                      "(solo debe contener 0s y 1s, agrupados en bytes de 8 bits).")
            else:
                print(f"\nNombre decodificado:\n{resultado}")

        elif opcion == '3':
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu()