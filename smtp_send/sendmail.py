import logging
import os

import smtplib
# For guessing MIME type based on file name extension
import mimetypes

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

class SendMail:

    def __init__(self, server, port, login, password, 
                 toAddr, subject, message, attachment):
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        self.toAddr = toAddr
        self.subject = subject
        self.message = message
        self.attachment = attachment

    def __enter__(self):
        self.send(self.__prepare_msg());
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __prepare_msg(self):
        result = ''
        if self.attachment is not None:
            if os.path.isdir(self.attachment):
                outer = MIMEMultipart()
                outer['Subject'] = self.message
                outer['To'] = self.toAddr
                outer['From'] = self.login
                outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
                for filename in os.listdir(self.attachment):
                    path = os.path.join(self.attachment, filename)
                    if not os.path.isfile(path):
                        continue
                    # Guess the content type based on the file's extension.  Encoding
                    # will be ignored, although we should check for simple things like
                    # gzip'd or compressed files.
                    ctype, encoding = mimetypes.guess_type(path)
                    if ctype is None or encoding is not None:
                        # No guess could be made, or the file is encoded (compressed), so
                        # use a generic bag-of-bits type.
                        ctype = 'application/octet-stream'
                    maintype, subtype = ctype.split('/', 1)
                    if maintype == 'text':
                        with open(path) as fp:
                            # Note: we should handle calculating the charset
                            msg = MIMEText(fp.read(), _subtype=subtype)
                    elif maintype == 'image':
                        with open(path, 'rb') as fp:
                            msg = MIMEImage(fp.read(), _subtype=subtype)
                    elif maintype == 'audio':
                        with open(path, 'rb') as fp:
                            msg = MIMEAudio(fp.read(), _subtype=subtype)
                    else:
                        with open(path, 'rb') as fp:
                            msg = MIMEBase(maintype, subtype)
                            msg.set_payload(fp.read())
                        # Encode the payload using Base64
                        encoders.encode_base64(msg)
                    # Set the filename parameter
                    msg.add_header('Content-Disposition', 'attachment', filename=filename)
                    outer.attach(msg)
                # Now send or store the message
                result = outer.as_string()
            else:
                print("Add code to prepare sending one file")
        else:
            result = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n") % \
                       (self.login, self.toAddr, self.subject, self.message)

        return result

    def send(self, msg):
        with smtplib.SMTP(self.server, self.port) as smtp:
            logger.debug('Sending message')
            smtp.set_debuglevel(1)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.login, self.password)
            smtp.sendmail(self.login, self.toAddr, msg)
            smtp.quit()
            logger.debug('Message was successfully send.')