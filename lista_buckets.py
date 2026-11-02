import boto3


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = [b['Name'] for b in response['Buckets']]
    return {
        'statusCode': 200,
        'lista_buckets': buckets
    }
