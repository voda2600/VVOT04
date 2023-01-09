import base64
import json
import os
import boto3
import requests

def handler(event, context):
    session = boto3.session.Session(region_name='ru-central1')
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    object_id = event['messages'][0]['details']['object_id']
    bucket_id = event['messages'][0]['details']['bucket_id']
    acess_token = context.token['access_token']

    photo = s3.get_object(Bucket=bucket_id, Key=object_id)
    encoded_photo = get_file(photo['Body'])

    headers = {'Authorization': 'Bearer ' + acess_token}
    stt_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

    body_json = {
        'analyze_specs': [{
            'content': encoded_photo.decode('utf-8'),
            'features': [{
                'type': "FACE_DETECTION"
            }]
        }]
    }

    r = requests.post(
        url = stt_url,
        headers = headers,
        data = json.dumps(body_json, indent=4)
    )

    faces = json.loads(r.content.decode('utf-8'))['results'][0]['results'][0]['faceDetection']
    queue_url = os.environ['MY_QUEUE']
    if 'faces' in faces:
        sqs_session = boto3.session.Session(
            region_name='ru-central1',
            aws_access_key_id=os.environ['ACCESS_KEY'],
            aws_secret_access_key=os.environ['SECRET_KEY']
        )
        sqs_client = sqs_session.client(
            service_name='sqs',
            endpoint_url='https://message-queue.api.cloud.yandex.net',
            region_name='ru-central1'
        )

        for face in faces['faces']:
            message = json.dumps({
                'origin_key': object_id,
                'vertices': face['boundingBox']['vertices']
            })
            sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=message
            )

def get_file(file):
    file_content = file.read()
    return base64.b64encode(file_content)