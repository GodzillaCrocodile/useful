from configparser import ConfigParser
from logging.handlers import TimedRotatingFileHandler
import logging

script_path = os.path.dirname(os.path.realpath(__file__))
settings_path = os.path.join(script_path, 'settings/settings.ini')


def config(fileName, section):
    parser = ConfigParser()
    parser.read(fileName)
    # print('[*] Parsing config section %s from %s' % (section, fileName))

    settings = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            settings[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, fileName))

    return settings


def telegram(text):
    timestamp = time.strftime('%H:%M:%S %d/%m/%Y')
    message = f'[{timestamp}] {text}'
    response = requests.post(url=telegramURL, data={'chat_id':telegramChatID, 'text': message}, proxies=proxy).json()


def log_setup():
    # log_handler = logging.handlers.WatchedFileHandler(os.path.join(script_path, 'log.txt'))
    log_handler = TimedRotatingFileHandler('/opt/postgres_dns/logs/log.txt', when='w0', interval=1, backupCount=56)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(filename)s[LINE:%(lineno)d] %(message)s')
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)


def log(log_setting, message):
    if log_setting == 'print':
        print(message)
    elif log_setting == 'logging':
        logging.info(message)
    elif log_setting == 'telegram':
        telegram(message)
    elif log_setting == 'both':
        print(message)
        logging.info(message)
        telegram(message)
