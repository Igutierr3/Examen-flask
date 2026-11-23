from flask import Flask, render_template, request

app = Flask(__name__)

PRECIO_TARRO = 9000

USUARIOS_REGISTRADOS = {
    "juan": {"password": "admin", "rol": "Administrador"},
    "pepe": {"password": "user", "rol": "Usuario"},
}


def calcular_compra_pintura(nombre: str, edad: int, cantidad: int) -> dict:
    total_sin_descuento = cantidad * PRECIO_TARRO

    if edad < 18:
        porcentaje_descuento = 0.0
    elif 18 <= edad <= 30:
        porcentaje_descuento = 0.15
    else:  # edad > 30
        porcentaje_descuento = 0.25

    monto_descuento = total_sin_descuento * porcentaje_descuento
    total_a_pagar = total_sin_descuento - monto_descuento

    return {
        "nombre": nombre,
        "total_sin_descuento": total_sin_descuento,
        "monto_descuento": monto_descuento,
        "total_a_pagar": total_a_pagar,
    }


def verificar_credenciales(usuario: str, password: str) -> str:
    cuenta = USUARIOS_REGISTRADOS.get(usuario)
    if cuenta and cuenta["password"] == password:
        return f"Bienvenido {cuenta['rol']} {usuario}"
    return "Usuario o contraseña incorrectos"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = None
    error = None

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        edad_str = request.form.get("edad", "").strip()
        cantidad_str = request.form.get("cantidad", "").strip()

        try:
            edad = int(edad_str)
            cantidad = int(cantidad_str)

            if not nombre or edad < 0 or cantidad < 0:
                error = "Por favor, ingresa datos válidos."
            else:
                resultado = calcular_compra_pintura(nombre, edad, cantidad)
        except ValueError:
            error = "La edad y la cantidad deben ser números enteros válidos."

    return render_template("ejercicio1.html", resultado=resultado, error=error)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    mensaje = None

    if request.method == "POST":
        usuario = request.form.get("nombre", "").strip()
        password = request.form.get("password", "")
        mensaje = verificar_credenciales(usuario, password)

    return render_template("ejercicio2.html", mensaje=mensaje)


if __name__ == "__main__":
    app.run(debug=True)