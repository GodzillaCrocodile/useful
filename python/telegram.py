# EStroev
import requests
import time

timestamp = time.strftime('%H:%M:%S %d/%m/%Y')
key = ''
chatID = ''
message = f'[*] [{timestamp}] test'
url = f'https://api.telegram.org/bot{key}/sendMessage'

proxy = {
 'http:': '',
 'https': ''
}

proxy = None

response = requests.post(url=url, data={'chat_id': chatID, 'text': message}, proxies=proxy).json()