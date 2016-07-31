import smtplib
import sys
import logging
import argparse
import os
import threading
import time
import re
from smtp_send.settings import read_settings
from smtp_send.settings import get_settings_from_file

__version__ = "0.0.1.dev0"
logger = logging.getLogger(__name__)
DEFAULT_CONFIG_NAME = "config"

def parse_arguments():
    parser = argparse.ArgumentParser(
        description = 'Smtp send tool.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter

    )
    parser.add_argument('-c', '--config', dest = 'config',
                        help = 'Load configuration file. Default'
                             'value is {0}'.format(DEFAULT_CONFIG_NAME))

    parser.add_argument('-q', '--quiet', action = 'store_const',
                        const = logging.CRITICAL, dest = 'verbosity',
                        help = 'Be quiet')

    parser.add_argument('-v', '--verbose', action = 'store_const',
                        const = logging.DEBUG, dest = 'verbosity',
                        help = 'Make a lot of noise')

    parser.add_argument('--version', action = 'version',
                        version = __version__,
                        help = 'Print version number and exit')

    parser.add_argument('login', type = str, help = 'mail login')

    parser.add_argument('password', type = str, 
                        help = 'password to mail login')

    parser.add_argument('-p', dest = 'port', type = int, 
                        default = 587, help = 'smtp server port')

    parser.add_argument('-s', dest = 'server', type = str,  
                        default = "smtp.mail.ru",
                        help = 'smtp server')


    return parser.parse_args()

def sendMail(server, port, login, password, toAddr, subject, message):
    logger.debug('Sending...')
    subj = re.compile("Subject: ")
    fromM = re.compile("From: ")
    smtp = smtplib.SMTP(server, port)
    smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login, password)
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n") % \
          (login, toAddr, subject, message)
    smtp.sendmail(login, toAddr, msg)
    smtp.quit()
    logger.debug('Message was successfully send.')

def main():
    args = parse_arguments()

    logger.addHandler(logging.StreamHandler())
    
    if (args.verbosity):
        logger.setLevel(args.verbosity)
    else:
        logger.setLevel(logging.INFO)

    logger.debug('smtp_send version: %s', __version__)
    logger.debug('python version: %s', sys.version.split()[0])

    try:
        config_file = DEFAULT_CONFIG_NAME
        if args.config is not None and os.path.isfile(args.config):
            config_file = args.config
            settings = read_settings(config_file)        
        sendMail(args.server, args.port, 
                 args.login, args.password, 
                 args.login, 
                 "Subject", "Hello world")

    except Exception as e:
        logger.critical('%s', e)
        if args.verbosity == logging.DEBUG:
            raise
        else:
            sys.exit(getattr(e, 'exitcode', 1))

