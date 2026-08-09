## Binario-Discretas.py 
## Este programa permite convertir numeros decimales a su representacion
## binaria en formato IEEE-754 (32 o 64 bits) y viceversa.





def configuracion(bits):
    """Devuelve (bits_exponente, bits_mantisa, sesgo) segun la precision."""
    if bits == 32:
        return 8, 23, 127
    elif bits == 64:
        return 11, 52, 1023
    else:
        raise ValueError("La precision debe ser 32 o 64 bits")


def decimal_a_ieee754(x, bits=32):
    """
    Recibe x en base 10 (con parte entera y/o fraccionaria) y retorna:
      - la cadena de bits IEEE-754
      - un diccionario con el detalle (signo, exponente real, exponente
        sesgado, mantisa) para poder mostrar el paso a paso.
    """
    exp_bits, mant_bits, sesgo = configuracion(bits)

   
    signo = '1' if x < 0 else '0'
    x = abs(x)

    
    if x == 0:
        bitstring = signo + '0' * exp_bits + '0' * mant_bits
        detalle = {"signo": signo, "exponente_real": 0,
                   "exponente_sesgado": 0, "mantisa": '0' * mant_bits}
        return bitstring, detalle

    parte_entera = int(x)
    parte_fraccionaria = x - parte_entera

    
    bin_entera = bin(parte_entera)[2:] if parte_entera != 0 else ''

    
    bin_fraccionaria = ''
    temp = parte_fraccionaria
    max_iter = mant_bits + exp_bits + 64
    for _ in range(max_iter):
        temp *= 2
        bit = int(temp)
        bin_fraccionaria += str(bit)
        temp -= bit
        if temp == 0:
            break


    if parte_entera != 0:
        exponente_real = len(bin_entera) - 1
        digitos_mantisa = bin_entera[1:] + bin_fraccionaria
    else:
        primer_uno = bin_fraccionaria.find('1')
        if primer_uno == -1:
            exponente_real = 0
            digitos_mantisa = ''
        else:
            exponente_real = -(primer_uno + 1)
            digitos_mantisa = bin_fraccionaria[primer_uno + 1:]


    digitos_mantisa = digitos_mantisa.ljust(mant_bits + 2, '0')
    digitos_mantisa, acarreo = _redondear_mantisa(digitos_mantisa, mant_bits)
    if acarreo:
        exponente_real += 1
        digitos_mantisa = '0' * mant_bits

   
    exponente_sesgado = exponente_real + sesgo
    bin_exponente = format(exponente_sesgado, '0{}b'.format(exp_bits))

    bitstring = signo + bin_exponente + digitos_mantisa
    detalle = {
        "signo": signo,
        "exponente_real": exponente_real,
        "exponente_sesgado": exponente_sesgado,
        "exponente_binario": bin_exponente,
        "mantisa": digitos_mantisa
    }
    return bitstring, detalle


def _redondear_mantisa(bits_str, n):

    if len(bits_str) <= n:
        return bits_str.ljust(n, '0'), False

    conservados = bits_str[:n]
    bit_redondeo = bits_str[n]
    resto = bits_str[n + 1:]

    subir = False
    if bit_redondeo == '1':
        if '1' in resto:
            subir = True
        elif conservados[-1] == '1':
            subir = True

    if not subir:
        return conservados, False

    valor = int(conservados, 2) + 1
    if valor == (1 << n):
        return '0' * n, True
    return format(valor, '0{}b'.format(n)), False


def ieee754_a_decimal(cadena_bits, bits=32):
    """Recibe la cadena de 32 o 64 bits y retorna el numero x en base 10."""
    exp_bits, mant_bits, sesgo = configuracion(bits)

    if len(cadena_bits) != 1 + exp_bits + mant_bits:
        raise ValueError(
            "La cadena debe tener exactamente {} bits para precision de {} bits"
            .format(1 + exp_bits + mant_bits, bits)
        )

    signo_bit = cadena_bits[0]
    campo_exponente = cadena_bits[1:1 + exp_bits]
    campo_mantisa = cadena_bits[1 + exp_bits:]

    exponente_sesgado = int(campo_exponente, 2)
    exponente_real = exponente_sesgado - sesgo

    if exponente_sesgado == 0 and int(campo_mantisa, 2) == 0:
        return 0.0

    mantisa = 1.0
    for i, bit in enumerate(campo_mantisa):
        if bit == '1':
            mantisa += 2 ** (-(i + 1))

    valor = mantisa * (2 ** exponente_real)
    if signo_bit == '1':
        valor = -valor

    return valor


def formatear_bits(cadena_bits, bits=32):
    exp_bits, mant_bits, _ = configuracion(bits)
    signo = cadena_bits[0]
    exponente = cadena_bits[1:1 + exp_bits]
    mantisa = cadena_bits[1 + exp_bits:]
    return "{} | {} | {}".format(signo, exponente, mantisa)






def texto_a_ieee754(texto, bits=32):
    """
    Convierte cada caracter de 'texto' a su codigo ASCII (como float) y luego
    a su representacion binaria IEEE-754 de 'bits' bits.
    Retorna una lista de tuplas (caracter, codigo_ascii, cadena_ieee754).
    """
    resultado = []
    for caracter in texto:
        codigo_ascii = float(ord(caracter))
        cadena_bits, _ = decimal_a_ieee754(codigo_ascii, bits)
        resultado.append((caracter, ord(caracter), cadena_bits))
    return resultado


def ieee754_a_texto(cadena_binaria, bits=32):
    """
    Convierte una cadena de bloques IEEE-754 (separados por espacio) de vuelta
    a texto: cada bloque se interpreta como float IEEE-754 (que representa un
    codigo ASCII), se redondea al entero mas cercano y se convierte a
    caracter (chr).
    Retorna None si algun bloque no es valido.
    """
    exp_bits, mant_bits, _ = configuracion(bits)
    tam_bloque = 1 + exp_bits + mant_bits

    bloques = cadena_binaria.split()
    texto = ''
    for bloque in bloques:
        if len(bloque) != tam_bloque or not all(b in '01' for b in bloque):
            return None
        try:
            valor = ieee754_a_decimal(bloque, bits)
            codigo_ascii = round(valor)
            texto += chr(codigo_ascii)
        except (ValueError, OverflowError):
            return None
    return texto





def mostrar_menu():
    print("=" * 70)
    print(" CONVERSOR UNIFICADO: IEEE-754 + CODIGO ASCII ")
    print("=" * 70)
    print("1. Convertir un numero DECIMAL a binario ")
    print("2. Convertir un binario IEEE-754 a DECIMAL")
    print("3. Convertir un nombre a binario")
    print("4. Convertir un binario a nombre")
    print("0. Salir")
    print("-" * 70)


def opcion_decimal_a_ieee754():
    x = float(input("Ingrese el numero decimal (x): "))
    bits = int(input("Precision (32 o 64 bits): "))
    cadena, detalle = decimal_a_ieee754(x, bits)
    print("\n--- RESULTADO ---")
    print("Numero original       :", x)
    print("Signo                 :", detalle["signo"],
          "(0 = positivo, 1 = negativo)")
    print("Exponente real (e)    :", detalle["exponente_real"])
    print("Sesgo (bias)          :", configuracion(bits)[2])
    print("Exponente almacenado  :", detalle["exponente_sesgado"])
    print("Mantisa (d1...dm)     :", detalle["mantisa"])
    print("Cadena IEEE-754 ({} b):".format(bits), cadena)
    print("Formato signo|exp|mant:", formatear_bits(cadena, bits))


def opcion_ieee754_a_decimal():
    cadena = input("Ingrese la cadena de bits IEEE-754: ").strip()
    bits = int(input("Precision (32 o 64 bits): "))
    x = ieee754_a_decimal(cadena, bits)
    print("\n--- RESULTADO ---")
    print("Cadena ingresada :", cadena)
    print("Numero decimal x :", x)


def opcion_texto_a_ieee754():
    nombre = input("Ingrese el nombre/texto: ")
    if nombre == '':
        print("El texto no puede estar vacio.")
        return
    bits = int(input("Precision (32 o 64 bits): "))
    detalle = texto_a_ieee754(nombre, bits)
    print("\n--- RESULTADO ---")
    for caracter, codigo, cadena_bits in detalle:
        print(f"'{caracter}' (ASCII {codigo:>3}) -> {cadena_bits}")
    cadena_completa = ' '.join(c for _, _, c in detalle)
    print("\nCadena completa (bloques separados por espacio):")
    print(cadena_completa)


def opcion_ieee754_a_texto():
    cadena = input(
        "Ingrese la cadena IEEE-754 (bloques separados por espacio): "
    ).strip()
    bits = int(input("Precision (32 o 64 bits): "))
    resultado = ieee754_a_texto(cadena, bits)
    if resultado is None:
        print("\nError: la cadena ingresada no es valida (verifique que cada "
              "bloque tenga el numero correcto de bits y solo contenga 0s y 1s).")
    else:
        print("\nTexto decodificado:")
        print(resultado)


def menu():
    mostrar_menu()
    opcion = input("Seleccione una opcion: ").strip()

    if opcion == '1':
        opcion_decimal_a_ieee754()
    elif opcion == '2':
        opcion_ieee754_a_decimal()
    elif opcion == '3':
        opcion_texto_a_ieee754()
    elif opcion == '4':
        opcion_ieee754_a_texto()
    elif opcion == '0':
        return False
    else:
        print("Opcion invalida")

    return True



if __name__ == "__main__":
    print("\n\n")
    seguir = True
    while seguir:
        seguir = menu()
        print()
    print("Fin del programa.")