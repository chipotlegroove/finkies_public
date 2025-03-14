from ast import List
from flask import Flask, render_template, request, session, redirect, flash, jsonify, url_for
import os
import datetime
from Controladores.ordenControlador import *
from secretsFinkies import FLASK_KEY, SQLALCHEMY_URI
from Controladores.productoControlador import *
from Controladores.usuarioControlador import *
from Controladores.direccionControlador import *
from Controladores.pedidoControlador import *
from Controladores.direccionUsuarioControlador import *
from Controladores.favoritoControlador import *
from Controladores.administradorControlador import *
from Controladores.productoCarritoControlador import *
from Controladores.categoriaControlador import *
from Controladores.metadataControlador import *
from utils.correos import *
from utils.aws_functions import *
app = Flask(__name__)
app.secret_key=FLASK_KEY
app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_URI
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True
}
db.init_app(app)

@app.route('/')
def index():
    productos=listarProductos()
    productos=purgarInactivos(productos)
    lanzamientos= listarProductosPorRecientes(productos[:])
    productoDelMes= productos[0]
    return render_template('index.html',productos=productos,lanzamientos=lanzamientos,productoDelMes=productoDelMes)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        datos = request.form
        correo=datos.get('correo')
        contrasena=datos.get('contrasena')
        #comparar con bd
        correo_existe = encontrarUsuarioPorCorreo(correo)
        if not correo_existe:
            flash('El correo no existe')
            return render_template('login.html')
        else:
            #comparar con bd    
            contrasena_ingresada=encriptarContrasena(contrasena)
            contraseña_correcta = verificarContrasena(correo,contrasena_ingresada) #esta variable contiene toda la informacion del usuario, si esta vacia es porque la contraseña es incorrecta
            if contraseña_correcta:
                session.clear()
                session['logged_in']=True
                session['usuario']=crearDiccUsuario(contraseña_correcta)
                return redirect(url_for('index'))
            else:
                flash('La contraseña es incorrecta')
                return render_template('login.html')

    else:
         return render_template('login.html')

@app.route("/login_admin", methods=['GET','POST'])
def login_admin():
    if request.method == "POST":
        datos = request.form
        correo=datos.get('correo')
        contrasena=datos.get('contrasena')
        #comparar con bd
        correo_existe = encontrarAdmin(correo)
        if not correo_existe:
            flash('El correo no existe')
            return render_template('login_admin.html')
        else:
            #comparar con bd    
            contrasena_ingresada=encriptarContrasena(contrasena)
            contraseña_correcta = verificarAdmin(correo,contrasena_ingresada) #esta variable contiene toda la informacion del usuario, si esta vacia es porque la contraseña es incorrecta
            if contraseña_correcta:
                session.clear()
                session['logged_admin']=True
                session['admin']=crearDiccAdmin(contraseña_correcta)
                return redirect(url_for('panel_admin'))
            else:
                return redirect(url_for('login_admin'))
    else:
        return render_template('login_admin.html')


@app.route("/panel_admin", methods=['GET'])
def panel_admin():
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        productos=listarProductos()
        productos=purgarInactivos(productos)
        return render_template('panel_admin.html', productos=productos)
@app.route("/historial_ventas", methods=['GET'])
def historialVentas():
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        pedidos=crearListaPedidos()
        for pedido in pedidos:
            print(pedido)
        return render_template('historial_ventas.html',pedidos=pedidos)
    
@app.route("/detalles_venta/<id>", methods=['GET'])
def detallesVenta(id):
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        print(id)
        print("Aadss")
        pedido = crearDiccionarioPedido(id)
        print(pedido)
        direccion=separarDireccion(encontrarDireccionPorId(encontrarIdDireccionPorIdPedido(id)).direccion)
        return render_template('detalles_venta.html',pedido=pedido,direccion=direccion)
@app.route("/lista_productos", methods=['GET'])
def lista_productos():
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        productos=listarProductos()
        idProductoDelMes = conseguirIdProductoMes()
        print(idProductoDelMes)
        return render_template('lista_productos.html', productos=productos, idProductoDelMes=idProductoDelMes)

@app.route("/actualizar_producto/<id>", methods=['POST'])
def actualizar_producto(id):
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            datos = request.form
            foto = request.files.get('product-image')
            #print(datos)
            tipoProducto=datos.get('product-type')
            nombre=datos.get('product-name')
            descripcionResumida=datos.get('short-description')
            costo=datos.get('product-cost')[1:]
            descripcionGeneral=datos.get('full-description')
            #subir foto a s3
            #if foto:
            #    carpeta=nombre_carpeta(tipoProducto)+"/"+foto.filename
            #    exito = subir_a_s3(foto,carpeta)
            #actualizar en la bd
            idCategoria=conseguirIdCategoria(tipoProducto)
            producto = Producto(idProducto=id,nombre=nombre,descripcionResumida=descripcionResumida,costo=costo,descripcionGeneral=descripcionGeneral,idCategoria=idCategoria)
            #if foto:
            #    producto.imagen='https://finkiesimages.s3.us-west-1.amazonaws.com/'+carpeta
            actualizarProducto(producto)

        resultado = {'procesado': True}
        return jsonify(resultado)

@app.route("/activar_producto/<id>", methods=['POST'])
def actualizar_activo(id):
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            datos = request.get_json()
            print(datos)
            activo=datos['activo']
            print(activo)
            producto = Producto(idProducto=id,activo=activo)
            actualizarProducto(producto)
            resultado = {'procesado': True}
        else:
            resultado = {'procesado': False}
        return jsonify(resultado)
@app.route("/cambiar_estado_pedido/<id>", methods=['POST'])
def cambiarEstadoPedido(id):
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == "POST":
            print("HOLA MUNDO")
            cambiarEstadoPedidoDB(id)
            resultado = {'procesado': True}
        else:
            resultado = {'procesado': False}
        return jsonify(resultado)
@app.route("/producto_del_mes",methods=['POST'])
def cambiarProductoMes():
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            datos = request.get_json()
            idProducto = datos['productoDelMes']
            resultado = {'procesado':actualizarProductoMes(idProducto)}
        else:
            resultado = {'procesado': False}
        return jsonify(resultado)

@app.route("/agregar_producto", methods=['GET','POST'])
def agregarProducto():
    if 'logged_admin' not in session:
        return redirect(url_for('index'))
    else:
        if request.method == "GET":
            return render_template('agregarProducto.html')
        if request.method == "POST":
            datos = request.form
            foto = request.files.get("product-image")
            print(datos)
            print(foto)
            tipoProducto=datos.get('product-type')
            nombre=datos.get('product-name')
            descripcionResumida=datos.get('short-description')
            costo=datos.get('product-cost')[1:]
            descripcionGeneral=datos.get('full-description')
            #subir foto a s3
            #carpeta=nombre_carpeta(tipoProducto)+"/"+foto.filename
            #exito = subir_a_s3(foto,carpeta)
            #actualizar en la bd
            idCategoria=conseguirIdCategoria(tipoProducto)
            producto = Producto(nombre=nombre,descripcionResumida=descripcionResumida,costo=costo,descripcionGeneral=descripcionGeneral,idCategoria=idCategoria)
            producto.imagen='https://finkiesimages.s3.us-west-1.amazonaws.com/Stickers/sticker_ghibli.jpeg'
            producto.fechaProducto=datetime.datetime.now()
            producto.activo=1            
            actualizarProducto(producto)
            flash('agregado')
            return redirect(url_for('agregarProducto'))

        


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        datos = request.form
        correo=datos.get('correo')
        contrasena=datos.get('contrasena')
        contrasena2=datos.get('contrasena2')
        if contrasena != contrasena2:
            flash('Las contraseñas no coinciden')
            return render_template('register.html')
        #verificar que no se repita el correo
        usuario_existente = encontrarUsuarioPorCorreo(correo)
        if usuario_existente:
            flash('El correo ya existe')
            return render_template('register.html')
        #insertar en la bd
        crearUsuario(datos)
        return redirect(url_for('login'))
        
    
    else:
        return render_template('register.html')

@app.route("/producto/<id>", methods=['GET','POST'])
def producto(id):
    if request.method=='GET':
        producto=crearDiccionarioProducto(encontrarProductoPorId(id))
        return render_template('producto.html', producto=producto)
    if request.method=='POST':
        if 'carrito' not in session:
            session['carrito']={}
        if id not in session['carrito']:
            session['carrito'][id]={}
            session['carrito'][id]['cantidad']=0

@app.route("/producto-administrador/<id>", methods=['GET','POST'])
def productoAdmin(id):
    if request.method=='GET':
        producto=crearDiccionarioProducto(encontrarProductoPorId(id))
        return render_template('producto-administrador.html', producto=producto)
    if request.method=='POST':
        if 'carrito' not in session:
            session['carrito']={}
        if id not in session['carrito']:
            session['carrito'][id]={}
            session['carrito'][id]['cantidad']=0

@app.route("/carrito", methods=['GET','POST'])
def carrito():
    if request.method == 'GET':
        if 'carrito' not in session:
            session['carrito']={}
        return render_template('carrito.html', carrito=session['carrito'])
    
@app.route("/pago", methods=['GET','POST'])
def pago():
    if request.method == "GET":
        if 'carrito' not in session or session['carrito']=={}:
            return redirect(url_for('index'))
        lista_direcciones = []
        if 'logged_in' in session:
            direcciones = direccionCompleta2(session['usuario']['idUsuario'])
            for direccion in direcciones:
                lista_direcciones.append(direcciones[direccion])         
        print(lista_direcciones)
        return render_template('pago.html', carrito=session['carrito'], direcciones=lista_direcciones)
    
@app.route("/guardar_pago", methods=['POST'])
def guardar_pago():
    if request.method == "POST":
        datos=request.get_json()
        idDireccionUsuario = int(datos['idDireccionUsuario'])
        print(idDireccionUsuario)
        print(datos)
        if 'logged_in' in session:
            idusuario=session['usuario']['idUsuario']
            datos_envio = direccionCompleta2(session['usuario']['idUsuario'])[idDireccionUsuario]
            idDireccion = datos_envio['idDireccion']
            idDireccionUsuario = datos_envio['idDireccionUsuario']
            print(datos_envio)
            guardarPedido(session['carrito'],idusuario,idDireccion,datos,idDireccionUsuario)          
            print('enviando correo a cliente')
            print(datos_envio)
            enviarCorreoCliente(session['carrito'],datos_envio)
            print('enviando correo a admin')
            print(datos_envio)
            enviarCorreoAdmin(session['carrito'],datos_envio)
            session['carrito']={}
            return jsonify({'procesado':'true'})
        else:
            if 'direccionenvio' in session:
                session.pop('direccionenvio')
            idusuario=22
            datos_envio = direccionCompleta2(idusuario)[idDireccionUsuario]
            idDireccion = datos_envio['idDireccion']
            idDireccionUsuario = datos_envio['idDireccionUsuario']
            print(datos_envio)
            guardarPedido(session['carrito'],idusuario,idDireccion,datos, idDireccionUsuario)
            print('enviando correo a cliente')
            enviarCorreoCliente(session['carrito'],datos_envio)
            print('enviando correo a admin')
            enviarCorreoAdmin(session['carrito'],datos_envio)
            session['carrito']={}
            return jsonify({'procesado':'true'})
            
@app.route('/recuperar-contrasena',methods=['POST','GET'])
def recuperarContrasena():
    if request.method == "GET":
        return render_template('recuperarContrasena.html')
    if request.method=="POST":
        correo=request.form
        correo=correo.get('correo')
        if correoExistente(correo):
            usuario=encontrarUsuarioPorCorreo(correo)
            token=generarTokenRestablecimiento(correo)
            enviarCorreoContrasena(correo,usuario.nombre,token)
            return redirect(url_for('index'))

@app.route('/reestablecer-contrasena/<token>', methods=['GET', 'POST'])
def reestablecerContrasenaToken(token):
    correo = verificarTokenRestablecimiento(token)
    usuario=encontrarUsuarioPorCorreo(correo)
    if correo:
        if request.method == 'POST':
            # Obtener la nueva contraseña desde el formulario
            datos = request.form
            # Aquí debes guardar la nueva contraseña en la base de datos para el usuario con el email proporcionado
            contrasena=datos.get('contrasena')
            contrasena2=datos.get('contrasena2')
            if contrasena != contrasena2:
                flash('Las contraseñas no coinciden')
                return render_template('reestablecerContrasena.html')
            actualizarContrasena(usuario,contrasena)
            return redirect(url_for('login'))
        if request.method == 'GET':
            return render_template('reestablecerContrasena.html')
    else:
        return redirect(url_for('index'))
    
@app.route('/favoritos',methods=['POST','GET'])
def despliegaFavoritos():
    if request.method == "GET":
        if 'logged_in' not in session:
            return redirect(url_for('index'))
        idUsuario=session['usuario']['idUsuario']
        favoritos=listarFavoritos(idUsuario)
        return render_template('wishlist.html',favoritos=favoritos)
    
@app.route('/eliminar_direccion', methods=['POST'])
def eliminarDireccion():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    idUsuario=session['usuario']['idUsuario']
    if request.method == "POST":
        idDireccuonUsuario=request.get_json()[0]['idDireccionUsuario']
        idDireccuonUsuario=int(idDireccuonUsuario)
        if idDireccuonUsuario in direccionCompleta2(idUsuario):
            print(idDireccuonUsuario)
            eliminarDirecciones(idDireccuonUsuario)
    return(url_for('mostrarDirecciones'))

@app.route('/recomprar_pedido',methods=['POST'])
def recomprar_pedido():
    if request.method=="POST":
        informacion=request.get_json()
        idPedido=informacion[0]['id_pedido']
        idCarrito=encontrarIdCarritoPorIdPedido(idPedido)
        productoCarritos=listarProductoCarrito(idCarrito)
        for productoCarrito in productoCarritos:
            producto=encontrarProductoPorId(productoCarrito.idProducto)
            producto=crearDiccionarioProducto(producto)
            cantidad=productoCarrito.cantidad
            idProducto=str(productoCarrito.idProducto)
            agregarProductoACarrito(session,idProducto,producto,cantidad)

        resultados={'procesado':'true'}
        return jsonify(resultados)
@app.route('/agregar_favorito',methods=['POST'])
def actualiza_favoritos():
    if request.method == "POST":
        favorito=request.get_json()
        idUsuario=session['usuario']['idUsuario']
        idProducto=favorito[0]['id_producto']
        cantidad=favorito[1]['cantidad']
        tipo=favorito[2]['tipo']
        if(tipo=="agregar"):
            idProducto=int(idProducto)
            cantidad=int(cantidad)
            agregarFavorito(idUsuario,idProducto,cantidad)
        if(tipo=="agregarACarrito"):
            if 'carrito' not in session:
                session['carrito']={}
            favoritos=listarFavoritos(idUsuario)
            for productoPre,cantidadPorProducto in favoritos:
                id_producto=str(productoPre.idProducto)
                cantidad=cantidadPorProducto
                producto = crearDiccionarioProducto(encontrarProductoPorId(id_producto))
                agregarProductoACarrito(session,id_producto,producto,cantidad)
        if(tipo=="limpiar"):
            limpiarFavoritos(idUsuario)
        if(tipo=="eliminarFavorito"):
            eliminarFavorito(idUsuario,idProducto)
        resultados={'procesado':'true'}
        return jsonify(resultados)


@app.route('/actualizar_carritodict',methods=['POST'])
def actualizar_carritodict():
    if request.method == "POST":
        if 'carrito' not in session:
            session['carrito']={}
        datos_actualizados = request.get_json()
        id_producto=str(datos_actualizados[0]['id_producto'])
        cantidad=datos_actualizados[1]['cantidad']
        tipo=datos_actualizados[2]['tipo']
        if tipo=='agregar':
            if id_producto not in session['carrito']:
                session['carrito'][id_producto]={}
                producto = crearDiccionarioProducto(encontrarProductoPorId(id_producto))
                session['carrito'][id_producto]['producto']=producto
                session['carrito'][id_producto]['producto']['costo']=float(producto['costo'])
                session['carrito'][id_producto]['cantidad']=0
            session['carrito'][id_producto]['cantidad']=int(cantidad)+int(session['carrito'][id_producto]['cantidad'])
        elif tipo=='actualizar':
            session['carrito'][id_producto]['cantidad']=int(cantidad)
        elif tipo=='limpiar':
            session['carrito'].clear()
        elif tipo=='eliminar':
            session['carrito'].pop(id_producto)
        session.modified=True
        resultados={'procesado':'true'}
        return jsonify(resultados)
    
@app.route('/perfil', methods=['GET','POST'])
def perfil():
    if request.method=='GET':
        return render_template("perfil.html",usuario=session['usuario'])
    if request.method=='POST':
        datos=request.form
        actualizarDatosUsuario(datos,session)
        return redirect(url_for('perfil'))

@app.route("/pedidos", methods=['GET','POST'])
def pedidos():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    if request.method == "GET":
        pedidos = crearListaPedidos1(session['usuario']['idUsuario'])
        return render_template('pedidos.html', pedidos=pedidos)
    
@app.route("/pedido/<id>", methods=['GET','POST'])
def pedido(id):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    #validar que el pedido sea del usuario
    pedidos = listaIdPedidos(session['usuario']['idUsuario'])
    print(pedidos)
    if int(id) not in pedidos:
        return redirect(url_for('pedidos'))
    if request.method == "GET":
        pedido = crearDiccionarioPedido(id)
        return render_template('pedido.html', pedido=pedido)

@app.route('/categoria/<tipoProducto>')
def filtrarProductos(tipoProducto):
    productos=listarProductos()
    productos=purgarInactivos(productos)
    productos=listarProductosCategoria(productos,tipoProducto)
    if (len(productos)!=0):
        return render_template('tipoProducto.html',tipoProducto=tipoProducto, productos=productos)
    return redirect(url_for('index'))

@app.route('/direcciones')
def mostrarDirecciones():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    idUsuario=session['usuario']['idUsuario']
    direcciones=direccionCompleta2(idUsuario)
    return render_template('direcciones.html',direcciones=direcciones)

@app.route('/editar-direccion/<id>', methods=['GET','POST'])
def editarDireccion(id):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    idUsuario=session['usuario']['idUsuario']
    if request.method == "GET":
        try:
            id=int(id)
        except ValueError:
            return redirect(url_for('mostrarDirecciones'))
        if id in direccionCompleta2(idUsuario):
            direccion=direccionCompleta2(idUsuario)[id]
            return render_template('editarDireccion.html',direccion=direccion)
        return redirect(url_for('mostrarDirecciones'))
    if request.method =="POST":
        datos=request.form
        crearDireccion(datos)
        editarDireccionUsuario(datos,id)
        return redirect(url_for('mostrarDirecciones'))


@app.route('/agregar-direccion-invitado', methods=['GET','POST'])
def agregarDireccionInvitado():
    if request.method == "GET":
        return render_template('agregarDireccion.html')
    if request.method =="POST":
        datos=request.form
        crearDireccion(datos)
        idDireccion=crearDireccionUsuario(datos,22)
        session['direccionenvio']=direccionCompleta3(idDireccion)
        print(session['direccionenvio'])
        return redirect(url_for('pago'))

@app.route('/editar-direccion-invitado', methods=['GET','POST'])
def editarDireccionInvitado():
    if request.method == "GET":
        if 'direccionenvio' in session:
            direccion=session['direccionenvio']
            return render_template('editarDireccion.html',direccion=direccion)
        return redirect(url_for('agregarDireccionInvitado'))
    if request.method =="POST":
        datos=request.form
        crearDireccion(datos)
        idDireccion=crearDireccionUsuario(datos,22)
        session['direccionenvio']=direccionCompleta3(idDireccion)
        print(session['direccionenvio'])
        return redirect(url_for('pago'))

@app.route('/agregar-direccion', methods=['GET','POST'])    
@app.route('/agregar-direccion/<ruta_anterior>', methods=['GET','POST'])
def agregarDireccion(ruta_anterior=''):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    idUsuario=session['usuario']['idUsuario']
    if request.method == "GET":
        return render_template('agregarDireccion.html')
    if request.method =="POST":
        datos=request.form
        crearDireccion(datos)
        crearDireccionUsuario(datos,idUsuario)
        if ruta_anterior=='pago':
            return redirect(url_for('pago'))
        return redirect(url_for('mostrarDirecciones'))


if __name__ == '__main__':
    app.run(debug=True)
