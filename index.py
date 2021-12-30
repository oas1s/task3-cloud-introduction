import telebot
import boto3

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

bucket_name = 'bucket-cloud-photo'
session = boto3.session.Session()

s3 = boto3.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)


def concat_name(filename, name):
    resp = s3.copy_object(Bucket=bucket_name, CopySource=bucket_name + '/' + filename,
                          Key=filename.split('.')[0] + '_name' + name + '.jpg')
    s3.delete_object(Bucket=bucket_name, Key=filename)
    print(resp)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['find'])
def start(message):
    name = message.text.split(' ')[1]
    faces = []
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        faces.append(key['Key'])

    for face in faces:
        if name in face:
            get_object_response = s3.get_object(Bucket=bucket_name, Key=face)
            img = get_object_response['Body'].read()
            bot.send_photo('552532115', img, caption='Это ' + name +' на общей фотографии')



@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    print(message)
    print(message.reply_to_message.caption.split('?')[1])
    print(message.text)
    filename = message.reply_to_message.caption.split('?')[1]
    concat_name(filename, message.text)


def handler(event, context):
    print(event)
    message = telebot.types.Update.de_json(event['body'])
    bot.process_new_updates([message])
    return {
        'statusCode': 200,
        'body': 'Hello World!',
    }
