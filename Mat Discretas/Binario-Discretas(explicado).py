# ============================================================
# BINARIO-DISCRETAS.py
# ============================================================
# Este programa permite:
# 1. Convertir números decimales a IEEE-754 (32 o 64 bits).
# 2. Convertir números IEEE-754 a decimal.
# 3. Convertir un texto/nombre a códigos ASCII representados
#    mediante IEEE-754.
# 4. Convertir una cadena de IEEE-754 nuevamente a texto.
# ============================================================


# ------------------------------------------------------------
# FUNCIÓN: configuracion
# ------------------------------------------------------------
# Esta función establece la cantidad de bits que utiliza
# el exponente, la mantisa y el sesgo dependiendo de si
# trabajamos con IEEE-754 de 32 o 64 bits.
# ------------------------------------------------------------
def configuracion(bits):

    # Si se seleccionan 32 bits:
    # 1 bit de signo
    # 8 bits de exponente
    # 23 bits de mantisa
    # Sesgo = 127
    if bits == 32:
        return 8, 23, 127

    # Si se seleccionan 64 bits:
    # 1 bit de signo
    # 11 bits de exponente
    # 52 bits de mantisa
    # Sesgo = 1023
    elif bits == 64:
        return 11, 52, 1023

    # Si el usuario introduce una precisión diferente,
    # se genera un error.
    else:
        raise ValueError("La precision debe ser 32 o 64 bits")


# ------------------------------------------------------------
# FUNCIÓN: decimal_a_ieee754
# ------------------------------------------------------------
# Convierte un número decimal a su representación IEEE-754.
#
# Ejemplo:
# 5.5 -> representación IEEE-754 de 32 bits.
#
# También devuelve información detallada sobre:
# - Signo
# - Exponente real
# - Exponente sesgado
# - Mantisa
# ------------------------------------------------------------
def decimal_a_ieee754(x, bits=32):

    # Obtenemos la configuración correspondiente:
    # bits del exponente, bits de mantisa y sesgo.
    exp_bits, mant_bits, sesgo = configuracion(bits)


    # --------------------------------------------------------
    # DETERMINAR EL SIGNO
    # --------------------------------------------------------
    # En IEEE-754:
    # 0 = número positivo
    # 1 = número negativo
    signo = '1' if x < 0 else '0'

    # Trabajamos con el valor absoluto para convertir
    # posteriormente la parte numérica.
    x = abs(x)


    # --------------------------------------------------------
    # CASO ESPECIAL: CERO
    # --------------------------------------------------------
    # Si el número es 0, todos los bits del exponente
    # y de la mantisa serán 0.
    if x == 0:

        # Construimos:
        # signo + exponente + mantisa
        bitstring = signo + '0' * exp_bits + '0' * mant_bits

        # Guardamos información para mostrarla posteriormente.
        detalle = {
            "signo": signo,
            "exponente_real": 0,
            "exponente_sesgado": 0,
            "mantisa": '0' * mant_bits
        }

        return bitstring, detalle


    # --------------------------------------------------------
    # SEPARAR PARTE ENTERA Y PARTE FRACCIONARIA
    # --------------------------------------------------------

    # int(x) obtiene la parte entera.
    parte_entera = int(x)

    # Restamos la parte entera para obtener la parte decimal.
    parte_fraccionaria = x - parte_entera


    # --------------------------------------------------------
    # CONVERTIR PARTE ENTERA A BINARIO
    # --------------------------------------------------------

    # bin() convierte un número decimal a binario.
    # [2:] elimina el prefijo "0b".
    #
    # Ejemplo:
    # bin(5) -> "0b101"
    # bin(5)[2:] -> "101"
    bin_entera = (
        bin(parte_entera)[2:]
        if parte_entera != 0
        else ''
    )


    # --------------------------------------------------------
    # CONVERTIR PARTE FRACCIONARIA A BINARIO
    # --------------------------------------------------------
    # Para convertir una fracción decimal a binario
    # multiplicamos repetidamente por 2.
    #
    # Ejemplo:
    # 0.5 * 2 = 1.0 -> bit 1
    # 0.25 * 2 = 0.5 -> bit 0
    # 0.5 * 2 = 1.0 -> bit 1
    #
    # Resultado: 0.101
    # --------------------------------------------------------

    bin_fraccionaria = ''

    # Guardamos temporalmente la fracción.
    temp = parte_fraccionaria

    # Definimos un máximo de iteraciones para evitar
    # que el programa quede ejecutándose indefinidamente.
    max_iter = mant_bits + exp_bits + 64

    for _ in range(max_iter):

        # Multiplicamos la parte fraccionaria por 2.
        temp *= 2

        # La parte entera del resultado será el siguiente bit.
        bit = int(temp)

        # Agregamos el bit a la representación binaria.
        bin_fraccionaria += str(bit)

        # Eliminamos la parte entera para continuar
        # trabajando solamente con la fracción.
        temp -= bit

        # Si la fracción llegó exactamente a 0,
        # ya no es necesario seguir calculando.
        if temp == 0:
            break


    # --------------------------------------------------------
    # CALCULAR EL EXPONENTE REAL Y LA MANTISA
    # --------------------------------------------------------

    # Si existe parte entera:
    if parte_entera != 0:

        # El exponente es la posición del primer 1.
        #
        # Ejemplo:
        # 101.1
        # El primer 1 está en la posición 2.
        # Por lo tanto:
        # exponente = 2
        exponente_real = len(bin_entera) - 1

        # La mantisa contiene todos los bits después
        # del primer 1.
        digitos_mantisa = bin_entera[1:] + bin_fraccionaria

    else:

        # Si no existe parte entera, buscamos el primer 1
        # dentro de la parte fraccionaria.
        primer_uno = bin_fraccionaria.find('1')

        # Si no encontramos ningún 1:
        if primer_uno == -1:

            exponente_real = 0
            digitos_mantisa = ''

        else:

            # Calculamos el exponente negativo.
            #
            # Ejemplo:
            # 0.00101
            # El primer 1 aparece después de 3 posiciones,
            # por lo tanto el exponente es -3.
            exponente_real = -(primer_uno + 1)

            # La mantisa comienza después del primer 1.
            digitos_mantisa = bin_fraccionaria[primer_uno + 1:]


    # --------------------------------------------------------
    # PREPARAR LA MANTISA PARA EL REDONDEO
    # --------------------------------------------------------

    # Agregamos ceros al final para asegurarnos de tener
    # suficientes bits para realizar el redondeo.
    digitos_mantisa = digitos_mantisa.ljust(mant_bits + 2, '0')


    # Llamamos a la función que realiza el redondeo
    # de la mantisa.
    digitos_mantisa, acarreo = _redondear_mantisa(
        digitos_mantisa,
        mant_bits
    )


    # Si el redondeo produce un acarreo:
    if acarreo:

        # El exponente aumenta en 1.
        exponente_real += 1

        # La mantisa vuelve a comenzar en cero.
        digitos_mantisa = '0' * mant_bits


    # --------------------------------------------------------
    # CALCULAR EL EXPONENTE SESGADO
    # --------------------------------------------------------

    # IEEE-754 no almacena directamente el exponente real.
    # Utiliza:
    #
    # exponente sesgado = exponente real + sesgo
    #
    # Para 32 bits:
    # sesgo = 127
    #
    # Para 64 bits:
    # sesgo = 1023
    exponente_sesgado = exponente_real + sesgo


    # Convertimos el exponente sesgado a binario.
    # El formato garantiza que tenga exactamente
    # la cantidad de bits correspondiente.
    bin_exponente = format(
        exponente_sesgado,
        '0{}b'.format(exp_bits)
    )


    # --------------------------------------------------------
    # CONSTRUIR LA CADENA FINAL
    # --------------------------------------------------------
    # IEEE-754 tiene la estructura:
    #
    # SIGNO | EXPONENTE | MANTISA
    #
    # Ejemplo de 32 bits:
    # 0 | 10000001 | 011000...
    bitstring = (
        signo +
        bin_exponente +
        digitos_mantisa
    )


    # Guardamos todos los datos importantes para
    # mostrarlos en pantalla.
    detalle = {
        "signo": signo,
        "exponente_real": exponente_real,
        "exponente_sesgado": exponente_sesgado,
        "exponente_binario": bin_exponente,
        "mantisa": digitos_mantisa
    }

    return bitstring, detalle


# ------------------------------------------------------------
# FUNCIÓN: _redondear_mantisa
# ------------------------------------------------------------
# Esta función se encarga de redondear la mantisa cuando
# tenemos más bits de los que permite IEEE-754.
# ------------------------------------------------------------
def _redondear_mantisa(bits_str, n):

    # Si ya tenemos la cantidad correcta de bits,
    # simplemente completamos con ceros si es necesario.
    if len(bits_str) <= n:
        return bits_str.ljust(n, '0'), False


    # Tomamos solamente los bits que podemos conservar.
    conservados = bits_str[:n]

    # El siguiente bit se utiliza para determinar
    # si debemos redondear.
    bit_redondeo = bits_str[n]

    # El resto son los bits que quedan después
    # del bit de redondeo.
    resto = bits_str[n + 1:]


    # Inicialmente suponemos que no debemos sumar 1.
    subir = False


    # --------------------------------------------------------
    # REGLA DE REDONDEO
    # --------------------------------------------------------
    # Si el bit de redondeo es 1:
    if bit_redondeo == '1':

        # Si después del bit de redondeo existe algún 1,
        # debemos aumentar la mantisa.
        if '1' in resto:
            subir = True

        # Si no hay más bits, aplicamos redondeo al par.
        elif conservados[-1] == '1':
            subir = True


    # Si no es necesario redondear:
    if not subir:
        return conservados, False


    # Convertimos la mantisa binaria a decimal,
    # sumamos 1 y posteriormente la convertimos
    # nuevamente a binario.
    valor = int(conservados, 2) + 1


    # Si al sumar 1 se produce un desbordamiento,
    # necesitamos enviar un acarreo al exponente.
    if valor == (1 << n):

        return '0' * n, True


    # Si no hay desbordamiento, devolvemos la mantisa
    # redondeada.
    return format(valor, '0{}b'.format(n)), False


# ------------------------------------------------------------
# FUNCIÓN: ieee754_a_decimal
# ------------------------------------------------------------
# Convierte una cadena de bits IEEE-754 nuevamente
# a un número decimal.
# ------------------------------------------------------------
def ieee754_a_decimal(cadena_bits, bits=32):

    # Obtenemos la configuración de IEEE-754.
    exp_bits, mant_bits, sesgo = configuracion(bits)


    # --------------------------------------------------------
    # VALIDAR LA LONGITUD
    # --------------------------------------------------------
    # Comprobamos que la cadena tenga exactamente:
    #
    # 1 bit de signo
    # + bits del exponente
    # + bits de la mantisa
    #
    # 32 bits o 64 bits.
    if len(cadena_bits) != 1 + exp_bits + mant_bits:

        raise ValueError(
            "La cadena debe tener exactamente {} bits "
            "para precision de {} bits"
            .format(
                1 + exp_bits + mant_bits,
                bits
            )
        )


    # --------------------------------------------------------
    # SEPARAR LOS CAMPOS
    # --------------------------------------------------------

    # Primer bit = signo.
    signo_bit = cadena_bits[0]

    # Siguientes bits = exponente.
    campo_exponente = cadena_bits[
        1:1 + exp_bits
    ]

    # Bits restantes = mantisa.
    campo_mantisa = cadena_bits[
        1 + exp_bits:
    ]


    # Convertimos el exponente binario a decimal.
    exponente_sesgado = int(
        campo_exponente,
        2
    )


    # Quitamos el sesgo para obtener el exponente real.
    exponente_real = (
        exponente_sesgado - sesgo
    )


    # --------------------------------------------------------
    # CASO ESPECIAL: CERO
    # --------------------------------------------------------
    if (
        exponente_sesgado == 0
        and int(campo_mantisa, 2) == 0
    ):
        return 0.0


    # --------------------------------------------------------
    # CALCULAR LA MANTISA
    # --------------------------------------------------------
    # En IEEE-754 normalizado, la mantisa comienza
    # implícitamente con 1.
    mantisa = 1.0


    # Recorremos cada bit de la mantisa.
    for i, bit in enumerate(campo_mantisa):

        # Si el bit es 1, agregamos su valor.
        if bit == '1':

            # Cada posición representa:
            #
            # 2^-1, 2^-2, 2^-3, ...
            mantisa += 2 ** (-(i + 1))


    # --------------------------------------------------------
    # CALCULAR EL VALOR FINAL
    # --------------------------------------------------------
    # Fórmula:
    #
    # valor = mantisa × 2^exponente
    valor = mantisa * (
        2 ** exponente_real
    )


    # Si el bit de signo es 1, el número es negativo.
    if signo_bit == '1':
        valor = -valor


    return valor


# ------------------------------------------------------------
# FUNCIÓN: formatear_bits
# ------------------------------------------------------------
# Separa la cadena IEEE-754 en sus tres partes:
#
# Signo | Exponente | Mantisa
#
# Esto facilita la lectura del resultado.
# ------------------------------------------------------------
def formatear_bits(cadena_bits, bits=32):

    # Obtenemos la configuración.
    exp_bits, mant_bits, _ = configuracion(bits)

    # Extraemos el signo.
    signo = cadena_bits[0]

    # Extraemos el exponente.
    exponente = cadena_bits[
        1:1 + exp_bits
    ]

    # Extraemos la mantisa.
    mantisa = cadena_bits[
        1 + exp_bits:
    ]

    # Retornamos todo separado por barras.
    return "{} | {} | {}".format(
        signo,
        exponente,
        mantisa
    )


# ------------------------------------------------------------
# FUNCIÓN: texto_a_ieee754
# ------------------------------------------------------------
# Convierte cada carácter de un texto en:
#
# carácter -> código ASCII -> IEEE-754
#
# Ejemplo:
#
# A -> ASCII 65 -> IEEE-754
# ------------------------------------------------------------
def texto_a_ieee754(texto, bits=32):

    # Creamos una lista vacía para guardar los resultados.
    resultado = []


    # Recorremos cada carácter del texto.
    for caracter in texto:

        # ord() obtiene el código ASCII del carácter.
        #
        # Ejemplo:
        # ord('A') = 65
        codigo_ascii = float(
            ord(caracter)
        )


        # Convertimos el código ASCII a IEEE-754.
        cadena_bits, _ = decimal_a_ieee754(
            codigo_ascii,
            bits
        )


        # Guardamos:
        # carácter, ASCII y representación IEEE-754.
        resultado.append(
            (
                caracter,
                ord(caracter),
                cadena_bits
            )
        )


    return resultado


# ------------------------------------------------------------
# FUNCIÓN: ieee754_a_texto
# ------------------------------------------------------------
# Realiza el proceso inverso:
#
# IEEE-754 -> decimal -> ASCII -> carácter
#
# Permite recuperar el texto original.
# ------------------------------------------------------------
def ieee754_a_texto(cadena_binaria, bits=32):

    # Obtenemos la cantidad de bits del exponente
    # y de la mantisa.
    exp_bits, mant_bits, _ = configuracion(bits)


    # Calculamos el tamaño de cada bloque.
    tam_bloque = (
        1 + exp_bits + mant_bits
    )


    # Separamos los bloques utilizando los espacios.
    bloques = cadena_binaria.split()


    # Variable donde construiremos el texto.
    texto = ''


    # Recorremos cada bloque.
    for bloque in bloques:

        # Comprobamos que:
        # 1. Tenga el número correcto de bits.
        # 2. Solamente contenga 0 y 1.
        if (
            len(bloque) != tam_bloque
            or not all(b in '01' for b in bloque)
        ):

            # Si no cumple, devolvemos None.
            return None


        try:

            # Convertimos IEEE-754 a decimal.
            valor = ieee754_a_decimal(
                bloque,
                bits
            )


            # Redondeamos para obtener el código ASCII entero.
            codigo_ascii = round(valor)


            # chr() convierte el código ASCII en carácter.
            texto += chr(codigo_ascii)


        # Si ocurre un error, la cadena no es válida.
        except (ValueError, OverflowError):
            return None


    return texto


# ------------------------------------------------------------
# FUNCIÓN: mostrar_menu
# ------------------------------------------------------------
# Muestra las opciones disponibles para el usuario.
# ------------------------------------------------------------
def mostrar_menu():

    print("=" * 70)
    print(" CONVERSOR UNIFICADO: IEEE-754 + CODIGO ASCII ")
    print("=" * 70)

    print("1. Convertir un numero DECIMAL a binario")
    print("2. Convertir un binario IEEE-754 a DECIMAL")
    print("3. Convertir un nombre a binario")
    print("4. Convertir un binario a nombre")
    print("0. Salir")

    print("-" * 70)


# ------------------------------------------------------------
# FUNCIÓN: opcion_decimal_a_ieee754
# ------------------------------------------------------------
# Se encarga de pedir al usuario un número decimal
# y convertirlo a IEEE-754.
# ------------------------------------------------------------
def opcion_decimal_a_ieee754():

    # Pedimos el número decimal.
    x = float(
        input("Ingrese el numero decimal (x): ")
    )


    # Pedimos la precisión:
    # 32 o 64 bits.
    bits = int(
        input("Precision (32 o 64 bits): ")
    )


    # Realizamos la conversión.
    cadena, detalle = decimal_a_ieee754(
        x,
        bits
    )


    # Mostramos los resultados.
    print("\n--- RESULTADO ---")

    print("Numero original       :", x)

    print(
        "Signo                 :",
        detalle["signo"],
        "(0 = positivo, 1 = negativo)"
    )

    print(
        "Exponente real (e)    :",
        detalle["exponente_real"]
    )

    print(
        "Sesgo (bias)          :",
        configuracion(bits)[2]
    )

    print(
        "Exponente almacenado  :",
        detalle["exponente_sesgado"]
    )

    print(
        "Mantisa (d1...dm)     :",
        detalle["mantisa"]
    )

    print(
        "Cadena IEEE-754 ({} b):".format(bits),
        cadena
    )

    print(
        "Formato signo|exp|mant:",
        formatear_bits(cadena, bits)
    )


# ------------------------------------------------------------
# FUNCIÓN: opcion_ieee754_a_decimal
# ------------------------------------------------------------
# Pide al usuario una cadena IEEE-754 y la convierte
# nuevamente a un número decimal.
# ------------------------------------------------------------
def opcion_ieee754_a_decimal():

    # Pedimos la cadena de bits.
    cadena = input(
        "Ingrese la cadena de bits IEEE-754: "
    ).strip()


    # Pedimos la precisión.
    bits = int(
        input("Precision (32 o 64 bits): ")
    )


    # Realizamos la conversión.
    x = ieee754_a_decimal(
        cadena,
        bits
    )


    # Mostramos el resultado.
    print("\n--- RESULTADO ---")

    print(
        "Cadena ingresada :",
        cadena
    )

    print(
        "Numero decimal x :",
        x
    )


# ------------------------------------------------------------
# FUNCIÓN: opcion_texto_a_ieee754
# ------------------------------------------------------------
# Pide un nombre o texto y convierte cada carácter
# a ASCII y posteriormente a IEEE-754.
# ------------------------------------------------------------
def opcion_texto_a_ieee754():

    # Pedimos al usuario el texto.
    nombre = input(
        "Ingrese el nombre/texto: "
    )


    # Verificamos que no esté vacío.
    if nombre == '':

        print(
            "El texto no puede estar vacio."
        )

        return


    # Pedimos la precisión.
    bits = int(
        input("Precision (32 o 64 bits): ")
    )


    # Convertimos el texto.
    detalle = texto_a_ieee754(
        nombre,
        bits
    )


    # Mostramos los resultados.
    print("\n--- RESULTADO ---")


    # Recorremos cada carácter.
    for caracter, codigo, cadena_bits in detalle:

        print(
            f"'{caracter}' "
            f"(ASCII {codigo:>3}) -> "
            f"{cadena_bits}"
        )


    # Unimos todos los bloques IEEE-754
    # utilizando un espacio.
    cadena_completa = ' '.join(
        c for _, _, c in detalle
    )


    print(
        "\nCadena completa "
        "(bloques separados por espacio):"
    )

    print(cadena_completa)


# ------------------------------------------------------------
# FUNCIÓN: opcion_ieee754_a_texto
# ------------------------------------------------------------
# Convierte una cadena de bloques IEEE-754
# nuevamente a texto.
# ------------------------------------------------------------
def opcion_ieee754_a_texto():

    # Pedimos los bloques IEEE-754.
    cadena = input(
        "Ingrese la cadena IEEE-754 "
        "(bloques separados por espacio): "
    ).strip()


    # Pedimos la precisión.
    bits = int(
        input("Precision (32 o 64 bits): ")
    )


    # Convertimos IEEE-754 a texto.
    resultado = ieee754_a_texto(
        cadena,
        bits
    )


    # Si el resultado es None,
    # significa que hubo un error.
    if resultado is None:

        print(
            "\nError: la cadena ingresada "
            "no es valida "
            "(verifique que cada bloque tenga "
            "el numero correcto de bits y solo "
            "contenga 0s y 1s)."
        )


    # Si todo está correcto,
    # mostramos el texto recuperado.
    else:

        print(
            "\nTexto decodificado:"
        )

        print(resultado)


# ------------------------------------------------------------
# FUNCIÓN: menu
# ------------------------------------------------------------
# Controla las opciones que selecciona el usuario.
# ------------------------------------------------------------
def menu():

    # Primero mostramos el menú.
    mostrar_menu()


    # Pedimos al usuario que seleccione una opción.
    opcion = input(
        "Seleccione una opcion: "
    ).strip()


    # --------------------------------------------------------
    # OPCIÓN 1
    # --------------------------------------------------------
    if opcion == '1':

        opcion_decimal_a_ieee754()


    # --------------------------------------------------------
    # OPCIÓN 2
    # --------------------------------------------------------
    elif opcion == '2':

        opcion_ieee754_a_decimal()


    # --------------------------------------------------------
    # OPCIÓN 3
    # --------------------------------------------------------
    elif opcion == '3':

        opcion_texto_a_ieee754()


    # --------------------------------------------------------
    # OPCIÓN 4
    # --------------------------------------------------------
    elif opcion == '4':

        opcion_ieee754_a_texto()


    # --------------------------------------------------------
    # OPCIÓN 0
    # --------------------------------------------------------
    elif opcion == '0':

        # False indica que debemos terminar
        # el programa.
        return False


    # Si el usuario escribe otra cosa:
    else:

        print(
            "Opcion invalida"
        )


    # True significa que el menú debe continuar.
    return True


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================
# __name__ == "__main__" permite que esta parte se ejecute
# solamente cuando este archivo se ejecuta directamente.
# ============================================================
if __name__ == "__main__":

    # Imprimimos dos líneas en blanco.
    print("\n\n")


    # Variable que controla si el programa continúa.
    seguir = True


    # Mientras seguir sea True, mostramos el menú.
    while seguir:

        # Ejecutamos el menú y guardamos su resultado.
        seguir = menu()

        # Dejamos una línea en blanco entre cada ejecución.
        print()


    # Cuando seguir sea False, llegamos al final.
    print(
        "Fin del programa."
    )