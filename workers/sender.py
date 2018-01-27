
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
import json
import logging
import urllib2
import traceback
import base64

from sendgrid.helpers.mail import *
from email.header import Header
from handlers.base import BaseHandler
from appengine_config import APP_CONFIG, DEV_ENV
from google.appengine.api import urlfetch
from lib import chardet

_DEFAULT_ENCODING_ASSUMPTION = "gb18030"

_ENCODING_MAP = {
    "gb18030": ["big5", "gb2312", "euc-tw", "hz-gb-2312", "iso-2022-cn"]
}

_SENDGRID_API_KEY = "********************************************"

class SenderTask(BaseHandler):

    def post(self):

        logging.info("[Sender] got new job")

        job_request = json.loads(self.request.get("job"))

        email = job_request["email"]

        file_name = job_request["file"]
        file_name = file_name.encode("utf-8")

        # somehow when send email on dev env, we need to encode the file name first
        # prod env seems doing this automatically
        # if DEV_ENV:
        #     file_name = str(Header(file_name, "utf-8"))

        links = job_request["links"]

        logging.info("[Sender] raw file name: %s", file_name)
        logging.info("[Sender] encoded file name: %s", file_name)
        logging.info("[Sender] download links: %s", links)

        urlfetch.set_default_fetch_deadline(599)
        sg = sendgrid.SendGridAPIClient(apikey=_SENDGRID_API_KEY)

        for link in links:

            try:

                logging.info("[Sender] trying link %s", link)

                request = urllib2.Request(link)
                response = urllib2.urlopen(request)

                from_email = Email(APP_CONFIG["EMAIL"]["SENDER"])
                to_email = Email(email)
                subject = file_name
                content = Content("text/plain", file_name)
                mail = Mail(from_email, subject, to_email, content)

                if self.txt_file(file_name):
                    logging.info("[Sender] resource is a txt file, encode to utf-8 before send")
                    filecontent = self.to_unicode(response.read())
                    filecontent = base64.b64encode(filecontent)

                    attachment = Attachment()
                    attachment.content = filecontent
                    attachment.type = 'application/text'
                    attachment.filename = file_name
                    attachment.disposition = 'attachment'
                    attachment.content_id = 'request'
                    mail.add_attachment(attachment)
                else:
                    logging.info("[Sender] unknown resource format, send straight away")
                    filecontent = base64.b64encode(response.read())

                    attachment = Attachment()
                    attachment.content = filecontent
                    attachment.type = 'application/octet-stream'
                    attachment.filename = file_name
                    attachment.disposition = 'attachment'
                    attachment.content_id = 'request'
                    mail.add_attachment(attachment)                    

                response = sg.client.mail.send.post(request_body=mail.get())
                logging.info("Sending email response status: %s",response.status_code)
                logging.info("Sending email response body: %s",response.body)
                logging.info("Sending email response headers: %s", response.headers)
                return

            except urllib2.HTTPError as e:
                print(e.read())
            except Exception:
                logging.error(traceback.format_exc())


    def txt_file(self, file_name):

        _, extension = os.path.splitext(file_name)
        if not extension:
            return False
        try:
            return extension[1:].lower() == "txt"
        except Exception:
            logging.error("[Sender] check txt file error %s", file_name)
            logging.error(traceback.format_exc())
        return False

    def to_unicode(self, file_content):

        encoding_info = chardet.detect(file_content)
        logging.info("[Sender] file encoding detection result: %s", encoding_info)

        if not encoding_info or "encoding" not in encoding_info:
            logging.info("[Sender] failed to detect file encoding, fall back to default encoding")
            return file_content.decode(_DEFAULT_ENCODING_ASSUMPTION).encode("utf-8")

        encoding = encoding_info.get("encoding").lower()

        if encoding.startswith("utf"):
            logging.info("[Sender] file in utf already, no need to convert")
            return file_content

        for parent_encoding, child_encodings in _ENCODING_MAP.iteritems():
            if encoding in child_encodings:
                logging.info("[Sender] switch to parent encoding %s", parent_encoding)
                return file_content.decode(parent_encoding).encode("utf-8")

        try:
            return file_content.decode(encoding).encode("utf-8")
        except Exception:
            logging.error(traceback.format_exc())
            logging.info("[Sender] failed to convert from %s to utf-8, fall back to default coding", encoding)
            return file_content.decode(_DEFAULT_ENCODING_ASSUMPTION).encode("utf-8")