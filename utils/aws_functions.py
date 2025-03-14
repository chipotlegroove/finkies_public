import boto3
from secretsFinkies import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY

def subir_a_s3(archivo,key):
    s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket = 'finkiesimages'
    s3.upload_fileobj(archivo, bucket, key, ExtraArgs={'ContentType':'image/png'})
    
def nombre_carpeta(tipoProducto):
    carpetas = {
        "collares":"collares",
        "pulseras":"Pulseras",
        "aretes":"Aretes",
        "stickers":"Stickers"
    }
    return carpetas[tipoProducto]