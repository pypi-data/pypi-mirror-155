from distutils import extension
import os 
import smtplib
from datetime import datetime as datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mimetypes = {
    #images
    'png': {'type': 'image', 'extension': 'png'},
    'jpg': {'type': 'image', 'extension': 'jpg'},
    #plain files
    'csv': {'type': 'application', 'extension': 'csv'},
    'txt': {'type': 'application', 'extension': 'txt'},
    #MS Office
    'xlsx': {'type': 'application', 'extension': 'vnd.ms-excel'},
    'xls': {'type': 'application', 'extension': 'vnd.ms-excel'},
    #Other
    'pdf': {'type': 'application', 'extension': 'octate-stream'},
}

class Email:
    server = None
    server_addr = ''
    server_port = None
    html_template = ''
    plain_template = ''
    default_attachments = None

    def __init__(self, sender, server_addr, server_port):
        self.sender = sender
        self.server_addr = server_addr
        self.server_port = server_port

        self.server = smtplib.SMTP(
            self.server_addr, 
            self.server_port
            )

    def set_msg_templates(self, html_template, plain_template):
        self.html_template = html_template
        self.plain_template = plain_template

    def _generate_body(self, variables = {}):
        html = self.html_template
        plain = self.plain_template

        if len(variables)>0:
            html = html.format(**variables)
            plain = plain.format(**variables)

        return html, plain

    def _process_attachment(self, fpath, attachment_id):
        fname = os.path.basename(fpath)
        with open(fpath, 'rb') as f:
            ext = fname.split('.')[-1]

            mime = MIMEBase(
                mimetypes[ext]['type'],
                mimetypes[ext]['extension'],
                filename = fname)

            #Add Headers
            mime.add_header('Content-Disposition', 'attachment', filename=fname)
            mime.add_header('X-Attachment-Id', f'{attachment_id}')
            mime.add_header('Content-ID', f'<{attachment_id}>')

            mime.set_payload(f.read())
            encoders.encode_base64(mime)

            return mime 

    def send_email(self, recips, subject, cc=None, variables={}, attachments=None):
        if not isinstance(recips, list):
            recips = [recips] 

        #Set up message basics
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender
        msg['To'] = ", ".join(recips)
        msg['Subject'] = subject

        #Add recipients to CC if needed
        if cc is not None:
            if not isinstance(cc, list):
                cc = [cc]

            msg['Cc'] = ", ".join(cc)
            recips = recips + cc
        
        # Msg Body
        html,plain = self._generate_body(variables=variables)
        msg.attach(MIMEText(html, 'html'))
        msg.attach(MIMEText(plain, 'plain'))

        #TODO add attachment handling
        for idx, attachment in enumerate(attachments):
            mime = self._process_attachment(attachment, idx+1)
            msg.attach(mime)

        self.server.sendmail(self.sender, recips, msg.as_string())
        return None
