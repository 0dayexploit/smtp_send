import sys
import logging
import argparse
import os
import threading
import time
import re
from smtp_send.sendmail import*

__version__ = "0.0.1.dev0"
logger = logging.getLogger(__name__)
DEFAULT_CONFIG_NAME = "config"

def parse_arguments():
    parser = argparse.ArgumentParser(
        description = 'Smtp send tool.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter

    )
    parser.add_argument('-q', '--quiet', action = 'store_const',
                        const = logging.CRITICAL, dest = 'verbosity',
                        help = 'Be quiet')

    parser.add_argument('-V', '--verbose', action = 'store_const',
                        const = logging.DEBUG, dest = 'verbosity',
                        help = 'Make a lot of noise')

    parser.add_argument('-v', '--version', action = 'version',
                        version = __version__,
                        help = 'Print version number and exit')

    parser.add_argument('-c', '--config', dest = 'config',
                        help = 'Load configuration file. Default'
                        'value is {0}'.format(DEFAULT_CONFIG_NAME))

    parser.add_argument('login', type = str, help = 'mail login')

    parser.add_argument('password', type = str, 
                        help = 'password to mail login')

    parser.add_argument('-p', dest = 'port', type = int, 
                        default = 587, help = 'smtp server port')

    parser.add_argument('-s', dest = 'server', type = str,  
                        default = "smtp.mail.ru",
                        help = 'smtp server')

    parser.add_argument('-A', dest = 'attachment',  
                        default = None,
                        help = 'could be directory or file')

    parser.add_argument('-M', dest = 'message', type = str,  
                        default = "",
                        help = 'Message text')

    parser.add_argument('-S', dest = 'subject', type = str,  
                        default = "",
                        help = 'Subject text')

    parser.add_argument('-R', dest = 'recipient', type = str, 
    					default = None, 
                    	help = 'Mail recipient login')

    return parser.parse_args()

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

        recipient = args.recipient
        if args.recipient is None:
        	recipient = args.login

        with SendMail(args.server, args.port, 
                      args.login, args.password, recipient, 
                      args.subject, args.message, 
                      args.attachment):
        	pass

    except Exception as e:
        logger.critical('%s', e)
        if args.verbosity == logging.DEBUG:
            raise
        else:
            sys.exit(getattr(e, 'exitcode', 1))

