import telebot
import boto3

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

bucket_name = 'bucket-cloud-photo'
queue_url = '/queue-21-37'
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

client = boto3.client(
    service_name='sqs',
    endpoint_url='https://message-queue.api.cloud.yandex.net',
    region_name='ru-central1'
)

faces = []
while True:
    messages = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    ).get('Messages')
    if not messages:
        break
    for msg in messages:
        faces.append(msg.get('Body'))
        client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg.get('ReceiptHandle')
        )

print(faces)

for face in faces:
    get_object_response = s3.get_object(Bucket=bucket_name, Key=face)
    img = get_object_response['Body'].read()
    bot.send_photo('552532115', img, caption='Кто это?' + face)
