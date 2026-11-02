import json
import boto3


def _body(event):
    b = event.get('body', event)
    return json.loads(b) if isinstance(b, str) else b


def lambda_handler(event, context):
    nombre_bucket = _body(event)['bucket']
    s3 = boto3.client('s3')
    objetos = []
    paginator = s3.get_paginator('list_objects_v2')
    for pagina in paginator.paginate(Bucket=nombre_bucket):
        for obj in pagina.get('Contents', []):
            objetos.append(obj['Key'])
    return {
        'statusCode': 200,
        'bucket': nombre_bucket,
        'lista_objetos': objetos
    }
