import json
import base64
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')


def _body(event):
    # Soporta integración lambda (event['body'] dict) y proxy (string JSON)
    b = event.get('body', event)
    return json.loads(b) if isinstance(b, str) else b


def _err(e):
    return {'statusCode': 400, 'error': str(e)}


def crear_bucket(event, context):
    d = _body(event)
    try:
        # us-east-1 no requiere CreateBucketConfiguration
        s3.create_bucket(Bucket=d['bucket'])
        return {'statusCode': 200, 'mensaje': 'Bucket creado', 'bucket': d['bucket']}
    except (ClientError, KeyError) as e:
        return _err(e)


def crear_directorio(event, context):
    d = _body(event)
    try:
        key = d['directorio'].strip('/') + '/'   # en S3 un "directorio" es una key que termina en /
        s3.put_object(Bucket=d['bucket'], Key=key)
        return {'statusCode': 200, 'mensaje': 'Directorio creado',
                'bucket': d['bucket'], 'directorio': key}
    except (ClientError, KeyError) as e:
        return _err(e)


def subir_archivo(event, context):
    d = _body(event)
    try:
        carpeta = d.get('directorio', '').strip('/')
        key = f"{carpeta}/{d['nombre_archivo']}" if carpeta else d['nombre_archivo']
        data = base64.b64decode(d['contenido_base64'])
        s3.put_object(Bucket=d['bucket'], Key=key, Body=data)
        return {'statusCode': 200, 'mensaje': 'Archivo subido',
                'bucket': d['bucket'], 'key': key}
    except (ClientError, KeyError) as e:
        return _err(e)
