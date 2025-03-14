from datetime import timedelta
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secretsFinkies import CORREO_FINKIES, CONTRASENA_CORREO, FLASK_KEY, LINK_FINKIES
from flask import Flask, request, jsonify
from itsdangerous import URLSafeTimedSerializer

def formatearDireccion(direccion:str) -> str:
    direccion = direccion.split(',')
    direccion_format = direccion[0] + ' #' + direccion[1] + ', ' + direccion[2] + ', ' + direccion[3] + ', ' + direccion[4] + ', ' + direccion[5]
    return direccion_format

def direccionDicttoStr(direccion:dict) -> str:
    direccion_format = direccion['calle'] + ' #' + direccion['numero'] + ', ' + direccion['colonia'] + ', ' + direccion['codigoPostal'] + ', ' + direccion['ciudad'] + ', ' + direccion['estado']
    return direccion_format

def separarDireccion(direccion:str) ->dict:
    direccion=direccion.split(',')
    print(direccion)
    direccionCompleta = {
        'calle': direccion[0],
        'numero': direccion[1],
        'colonia': direccion[2],
        'codigoPostal': direccion[3],
        'ciudad': direccion[4],
        'estado': direccion[5]
    }
    return direccionCompleta
def generarTokenRestablecimiento(correo:str):
    s = URLSafeTimedSerializer(FLASK_KEY)  # El token expirará en 1 hora (3600 segundos)
    token = s.dumps(correo)
    return token

def verificarTokenRestablecimiento(token):
    s = URLSafeTimedSerializer(FLASK_KEY)
    try:
        correo = s.loads(token, max_age=3600)  # El token expira después de 1 hora (3600 segundos)
    except:
        return None  # Token inválido o expirado
    return correo
def enviarCorreoContrasena(correo:str,nombre:str, token:str):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    msg = MIMEMultipart()
    msg['From'] = CORREO_FINKIES
    msg['To'] = correo
    msg['Subject'] = "Reestablecimiento de contraseña!"
    link=f"{LINK_FINKIES}/reestablecer-contrasena/{token}"
    body = f"Hola,{nombre}! Con el siguiente link podrás reestablece tu contraseña durante la siguiente hora.\n{link}\n"
    body += "Gracias,\nFinkies"
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body, 'plain'))
    s.starttls()
    s.login(CORREO_FINKIES, CONTRASENA_CORREO)
    text = msg.as_string()
    s.sendmail(CORREO_FINKIES, correo, text)
    s.quit()

def enviarCorreoCliente(carrito:dict,datos_envio:dict):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    msg = MIMEMultipart()
    msg['From'] = CORREO_FINKIES
    msg['To'] = datos_envio['email']
    msg['Subject'] = "Gracias por tu compra en Finkies!"
    body = f"Te agradecemos por tu preferencia, tu pedido esta en camino!\nContenidos de tu pedido:\n"
    subtotal = 0
    for id_producto, producto in carrito.items():
        costo = "{:.2f}".format(producto['producto']['costo'] * producto['cantidad'])
        body += f"{producto['producto']['nombre']}\t—\t${costo}\t—\tCantidad: {producto['cantidad']}\n"
        subtotal += producto['producto']['costo'] * producto['cantidad']
    subtotal_display = "{:.2f}".format(subtotal)
    body += f"Subtotal: ${subtotal_display}\n"
    body += "Envio: $50.00\n"
    total = "{:.2f}".format(subtotal + 50)
    body += f"Total: ${total}\n"
    body += f"Dirección de envío: {direccionDicttoStr(datos_envio['direccion'])}\n"
    body += "Gracias,\nFinkies"
    msg.attach(MIMEText(body, 'plain'))
    s.starttls()
    s.login(CORREO_FINKIES, CONTRASENA_CORREO)
    text = msg.as_string()
    s.sendmail(CORREO_FINKIES, datos_envio['email'], text)
    s.quit()

def enviarCorreoAdmin(carrito:dict, datos_envio:dict):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    msg = MIMEMultipart()
    msg['From'] = CORREO_FINKIES
    msg['To'] = CORREO_FINKIES
    msg['Subject'] = "Nuevo pedido en Finkies!"
    body = f"Ha recibido un nuevo pedido!\nContenidos del pedido:\n"
    subtotal = 0
    for id_producto, producto in carrito.items():
        costo = "{:.2f}".format(producto['producto']['costo'] * producto['cantidad'])
        body += f"{producto['producto']['nombre']}\t—\t${costo}\t—\tCantidad: {producto['cantidad']}\n"
        subtotal += producto['producto']['costo'] * producto['cantidad']
    subtotal_display = "{:.2f}".format(subtotal)
    body += f"Subtotal: ${subtotal_display}\n"
    body += "Envio: $50.00\n"
    total = "{:.2f}".format(subtotal + 50)
    body += f"Total: ${total}\n"
    body += f"Dirección de envío: {direccionDicttoStr(datos_envio['direccion'])}\n"
    body += f"Nombre del cliente: {datos_envio['nombres']} {datos_envio['apellidos']}\n"
    body += f"Correo del cliente: {datos_envio['email']}\n"
    body += f"Teléfono del cliente: {datos_envio['telefono']}\n"
    msg.attach(MIMEText(body, 'plain'))
    s.starttls()
    s.login(CORREO_FINKIES, CONTRASENA_CORREO)
    text = msg.as_string()
    s.sendmail(CORREO_FINKIES, CORREO_FINKIES, text)
    s.quit()

def agregarProductoACarrito(session,id_producto: int, producto, cantidad: int):
    if id_producto not in session['carrito']:
        session['carrito'][id_producto]={}
        session['carrito'][id_producto]['producto']=producto
        session['carrito'][id_producto]['producto']['costo']=float(producto['costo'])
        session['carrito'][id_producto]['cantidad']=0
    session['carrito'][id_producto]['cantidad'] =int(cantidad) + int(session['carrito'][id_producto]['cantidad'])
    session.modified=True