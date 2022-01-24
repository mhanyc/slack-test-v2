from utils import get_secret
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
from os import linesep


# bolt init
secrets = get_secret()
slack_bot_token = get_secret()["SLACK_BOT_TOKEN"]
slack_app_token = get_secret()["SLACK_APP_TOKEN"]
app = App(token=slack_bot_token)


def psap_lookup(zip_code):
    try:
        int(zip_code)
    except ValueError as e:
        return Exception('Error processing command - Please provide a valid Zip Code')

    try:
        url = f'https://api.mhawebsvc.org/psap/responders?address={zip_code}'
        headers = {
            'x-api-key': 'LebD7f7ZgO1j2cPpgaU751EUjI5OpLqI4zX2Fcf7',
            'content-type': 'application/json',
            'Accept-Charset': 'UTF-8'
        }
        res = requests.get(url=url, headers=headers)
        return res.json()['info']
    except Exception as e:
        return Exception('Error processing PSAP command')


@app.command("/psap")
def psap_handler(ack, respond, command):
    # ack() required by bolt
    ack()

    zip = command['text']
    result = psap_lookup(zip)

    name = result['name']
    phone = result['phone_number']
    addr = result['address']

    output = f'[ PSAP Response for Zip Code {zip} ]{linesep}' \
        f'{name}{linesep}' \
        f'{phone}{linesep}' \
        f'{addr}'

    respond(output)


# def handler(event, context):
#     data = {
#         'output': 'Hello World',
#         'timestamp': datetime.datetime.utcnow().isoformat()
#     }
#     return {
#         'statusCode': 200,
#         'body': json.dumps(data),
#         'headers': {'Content-Type': 'application/json'}
#     }


if __name__ == "__main__":
    SocketModeHandler(app, slack_app_token).start()
