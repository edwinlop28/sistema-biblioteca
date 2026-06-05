from flask import Flask, render_template, request, redirect, url_for, session, flash
from biblioteca import Biblioteca
from empleado import Empleado
from cliente import Cliente
from empleado import Empleado
from cliente import Cliente
from flask_bcrypt import Bcrypt
from  libro import Libro

bcrypt = Bcrypt()

app = Flask(__name__)
app.secret_key = "biblioteca123"

biblioteca = Biblioteca() 

if not biblioteca.hay_libros():
    biblioteca.cargar_libros()

@app.route("/", methods=["GET", "POST"])
def login():
     
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        usuario = biblioteca.login(email, password, bcrypt)

        if usuario:
            session["email"]  = usuario.get_email()
            session["tipo"]   = usuario.tipo_usuario()
            session["nombre"] = usuario.get_nombre()
            session["rol"]    = usuario.get_rol()

            if usuario.tipo_usuario() == "Empleado":
                return redirect(url_for("dashboard_empleado"))

        else:
            return render_template("login.html", error="Credenciales incorrectas")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/empleado")
def dashboard_empleado():
    if "email" not in session:
        return redirect(url_for("login"))   
    else:
        return render_template("dashboard_empleado.html", nombre=session["nombre"])

@app.route("/libros")
def libros():
    if "email" not in session:
        return redirect(url_for("login"))
    
    libros = biblioteca.obtener_libros()
    return render_template("libros.html", libros=libros)

@app.route("/empleados/nuevo", methods=["GET", "POST"])
def empleado_nuevo():
    if "email" not in session:
        return redirect(url_for("login"))
    
    if session["rol"] != "admin":
        return redirect(url_for("dashboard_empleado"))
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        cedula = request.form["cedula"]
        rol = request.form["rol"]
        turno = request.form["turno"]
       
        empleado = Empleado(0, nombre, cedula, email, password, turno, rol)
        resultado = biblioteca.registrar_empleado(empleado)
        flash(resultado, "success" if "registrado" in resultado else "danger")
        return redirect(url_for("dashboard_empleado"))
    
    return render_template("empleado_nuevo.html")

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def cliente_nuevo():
    if "email" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        cedula = request.form["cedula"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        cliente = Cliente(0,nombre, cedula, email, telefono, direccion)
        resultado = biblioteca.registrar_cliente(cliente)
        flash(resultado, "success" if "registrado" in resultado else "danger")
        return redirect(url_for("dashboard_empleado"))
    
    return render_template("cliente_nuevo.html")

@app.route("/prestamo", methods=["GET", "POST"])
def prestamo():
    
    if "email" not in session:
        return redirect(url_for("login"))
    
    isbn = request.args.get("isbn", "")
    
    if request.method =="POST":
        cedula_cliente = request.form["cedula_cliente"]
        isbn_libro = request.form["isbn_libro"]
        email_empleado = session["email"]
        empleado = biblioteca.buscar_empleado_db(email_empleado)

        resultado = biblioteca.hacer_prestamo(empleado, cedula_cliente, isbn_libro)
        flash(resultado, "success" if "exitosamente" in resultado else "danger")
        return redirect(url_for("dashboard_empleado"))
    
    return render_template("prestamo.html", isbn=isbn)

@app.route("/devolucion", methods=["GET", "POST"])
def devolucion():
    if "email" not in session:
        return redirect(url_for("login"))
    
    prestamo = None
    if request.method == "POST":

        if "isbn" in request.form:
            isbn = request.form["isbn"]
            prestamo = biblioteca.buscar_prestamo_por_isbn(isbn)

            if not prestamo:
                flash("No se encontró préstamo activo con ese ISBN ", "danger")
                return redirect(url_for("devolucion"))
            
        elif "id_prestamo" in request.form: 
            id_prestamo = request.form["id_prestamo"]
            email_empleado = session["email"]
            empleado = biblioteca.buscar_empleado_db(email_empleado)
            resultado = biblioteca.recibir_devolucion(empleado, id_prestamo)
            flash(resultado, "success" if "exitosamente" in resultado else "danger")
            return redirect(url_for("dashboard_empleado"))
    
    return render_template("devolucion.html", prestamo=prestamo)

@app.route("/prestamos/activos")
def prestamos_activos():
    
    if "email" not in session:
        return redirect(url_for("login"))
    
    prestamos = biblioteca.obtener_prestamos_activos()
    return render_template("prestamos_activos.html", prestamos=prestamos)

@app.route("/ver/clientes")
def ver_clientes():
    if "email" not in session:
        return redirect(url_for("login"))
    
    clientes = biblioteca.obtener_clientes()
    return render_template("ver_clientes.html", clientes = clientes)

@app.route("/libros/eliminar", methods=["GET", "POST"])
def eliminar_libros():
    if "email" not in session:
        return redirect(url_for("login"))
    
    if session["rol"] != "admin":
        return redirect(url_for("dashboard_empleado"))
    
    if request.method == "POST":
        isbn = request.form["isbn"]
        resultado = biblioteca.eliminar_libro(isbn)
        flash(resultado, "success" if "eliminado" in resultado else "danger")
        return redirect(url_for("eliminar_libros"))

    libros = biblioteca.obtener_libros()
    return render_template("eliminar_libros.html", libros=libros)

@app.route("/prestamos/historial")
def historial_prestamos():
    if "email" not in session:
        return redirect(url_for("login"))
    prestamos = biblioteca.obtener_historial_prestamos()
    return render_template("historial_prestamos.html", prestamos=prestamos)
    

@app.route("/libros/nuevo", methods=["GET", "POST"])
def nuevo_libro():

    if "email" not in session:
        return redirect(url_for("login"))
    
    if session["rol"] != "admin":
        return redirect(url_for("dashboard_empleado"))

    if request.method == "POST":

        isbn = request.form["isbn"]

        if biblioteca.existe_libro_db(isbn):
            flash("Este libro ya existe en la base de datos", "danger")
            return redirect(url_for("nuevo_libro"))
        
        if "titulo" in request.form and request.form["titulo"]:

            libro = Libro(isbn,request.form["titulo"],request.form["autor"],request.form["editorial"],request.form["año_publicacion"],int(request.form["cantidad"]))
            biblioteca.agregar_libro(libro)
            flash("Libro agregado exitosamente", "success")
            return redirect(url_for("dashboard_empleado"))
        
        resultado_api = biblioteca.buscar_en_api(isbn)
        if resultado_api:
            titulo, autor, editorial, año = resultado_api
            libro = Libro(isbn, titulo, autor, editorial, año, 0)
            return render_template("libro_nuevo.html", libro=libro, mostrar_formulario=True)
        else:
            return render_template("libro_nuevo.html", libro=None, isbn=isbn, mostrar_formulario=True)
    
    return render_template("libro_nuevo.html", mostrar_formulario=False)





if __name__ == "__main__":
    app.run(debug=False,port=3000)


