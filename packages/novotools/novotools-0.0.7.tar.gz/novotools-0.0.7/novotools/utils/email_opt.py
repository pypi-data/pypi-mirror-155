import re
import os
import imaplib
import email
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import getaddresses

## email tools
#configure

def send_email(
    recipients,
    subject,
    text,
    user,
    password,
    send_host = 'smtp.exmail.qq.com',
    send_port = 465,
    text_type="plain",
    cc=[],
    files=None,
    ):
    """
    text_type = [plain,html]
    """
    #login
    smtp_obj = smtplib.SMTP_SSL(send_host,send_port)
    smtp_obj.login(user,password)
    # recipients = ['cm.bio@qq.com']
    msg = MIMEMultipart()
    msg['from'] = 'medical-sc-info@novogene.com'
    msg['to'] = ";".join(recipients)
    if cc:
        msg['cc'] = ";".join(cc)
    msg['subject'] = Header(subject)
    content = MIMEText(text,text_type,'utf-8')
    msg.attach(content)
    #添加附件
    if files:
        for f in files:
            with open(f,'rb') as indata:
                part = MIMEApplication(indata.read())
                part.add_header('Content-Disposition', 'attachment', filename=f)
                msg.attach(part)
    
    all_recipients = recipients + cc 
    smtp_obj.sendmail(msg['from'],all_recipients,str(msg))

    print('email send successfully!')

class IMAPEmail():
    """
    """
    def __init__(self,
                user,
                password,
                receive_host = 'imap.exmail.qq.com',
                receive_port = 993,
                basic_dir = os.getcwd()
    ):
        #login email client
        self.client = imaplib.IMAP4_SSL(receive_host,receive_port)
        self.client.login(user,password)
        self._savedir = os.path.join(basic_dir,"load_data_emails")

    def _check(self,tag,data):
        if tag == "OK":
            return True
        elif tag == "NO":
            raise Exception(data)

    def decode_boxname(self,boxname):
        """
        parse boxname 
        """
        decode_name = boxname.replace('&', '+').encode('utf-8').decode('utf-7')
        return decode_name
    
    def encode_boxname(self,boxname):
        encodename = boxname.encode("utf-7").replace('+', '&')
        return encodename
    
    def list_box(self):
        #select a inbox
        tag,data = self.client.list()
        if self._check(tag,data):
            for box in data:
                list_response_pattern = re.compile(
                r'.(?P<flags>.*?). "(?P<delimiter>.*)" "(?P<name>.*)"'
                )
                match = list_response_pattern.match(box.decode("utf-8"))
                flags, _, mailbox_name = match.groups()
                flags = flags.replace("\\","")
                # print(f"{mailbox_name:<20}: {flags}")

                status = self.client.status(
                '"{}"'.format(mailbox_name),
                '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)',
                )
                status = status[1][0].decode("utf-8")
                box_re = re.search(r'(?P<boxname>.+) \(.*\)',status)
                trans_boxname = self.decode_boxname(box_re.group('boxname'))
                
                print(f'{trans_boxname}:{status}')
                
    def get_all_msg(self,box,search_type):
        all_msg = []
        tag,data = self.client.select(box)
        if self._check(tag,data):
            tag,data = self.client.search(None,search_type)
            # print(tag,data)
            for num in data[0].split():
                tag,data = self.client.fetch(num,'(RFC822)')
                # print(data[0][1])
                msg = email.message_from_bytes(data[0][1])
                all_msg.append(msg)
        return all_msg
    
    def get_body(self,msg):
        if msg.is_multipart():
            print("It's a mutipart!")
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and ('attachment' not in cdispo):
                    body = part.get_payload(decode=True).decode("utf-8")  # decode
                    break
        # not multipart - i.e. plain text, no attachments, keeping fingers crossed
        else:
            body = msg.get_payload(decode=True).decode("utf-8")
        return body
    
    def get_subject(self,msg):
        # get subject
        text,enc = email.header.decode_header(msg['subject'])[0]
        print(text,enc)
        subject = text.decode(enc) if enc else text
        print(subject)
        return subject
    
    def get_sender_and_recipients(self,msg):
        # get recipients
        tos = msg.get_all('to',[])
        sender = msg.get_all("from",[])
        ccs = msg.get_all("cc",[])
        resent_tos = msg.get_all('resent-to', [])
        resent_ccs = msg.get_all('resent-cc', [])
        
        return getaddresses(tos + ccs + resent_tos + resent_ccs + sender)

    def search_email(self,
        search_key,
        box,
        search_type="ALL",
        download_attach=False):
        """
        This method is used to search emails according to
        a series of filters like box and emails' type
        ----
        box: which box you want to search
        search_key: which content you want to search, [regular expression]
        search_type: email type like UNSEEN ALL
        """
        re_obj_list = []
        tag,data = self.client.select(box)
        if self._check(tag,data):
            tag,data = self.client.search(None,search_type)
            # print(tag,data)
            for num in data[0].split():
                tag,data = self.client.fetch(num,'(RFC822)')
                # print(data[0][1])
                msg = email.message_from_bytes(data[0][1])

                ### email subject fetch
                text,enc = email.header.decode_header(msg['subject'])[0]
                # print(text,enc)
                subject = text.decode(enc) if enc else text
                if search_key in subject:
                    print(f'find {search_key} in {subject},mark email as Seen.')
                    typ, data = self.client.store(num,'+FLAGS', '(\\Seen)')
                    if download_attach:
                        self.get_email_attachment(msg)
                else:
                    ### It looks like the first return of msg.get_payload() is plain text
                    ### The second return is html format
                    body_text = msg.get_payload()[0].get_payload(decode=True).decode('utf-8')
                    for line in body_text.split("\n"):
                        # print(line)
                        if re.search(search_key,line):
                            print(f'find {search_key} in {subject},mark email as Seen.')
                            print(line)
                            typ, data = self.client.store(num,'+FLAGS', '(\\Seen)')
                            if download_attach:
                                self.get_email_attachment(msg)
                            
                    # elif line.startswith("&nbsp;") or line.startswith("From:"):
                    #     print("search completion!")
                    #     break

                # for payload in msg.get_payload():
                #     print(payload.get_payload(decode=True).decode("utf-8"))
    
    def scan_loaddata_email(self,
        box,
        search_type="UNSEEN"):
        attachments = []
        tag,data = self.client.select(box)
        if self._check(tag,data):
            tag,data = self.client.search(None,search_type)
            print(tag,data)
            for num in data[0].split():
                tag,data = self.client.fetch(num,'(RFC822)')
                # print(data[0][1])
                msg = email.message_from_bytes(data[0][1])
                attachments += self.get_email_attachment(msg)
                typ, data = self.client.store(num,'+FLAGS', '(\\Seen)')
                print(f'Download attachment completed, mark email as Seen.')
                
        print(attachments)
        return attachments    

    def get_email_attachment(self,msg,valid_extensions=[".xlsx"]):
        """
        下载邮件中的附件
        """
        attachments = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()

            # 如果文件名为纯数字、字母时不需要解码，否则需要解码
            try:
                fileName = email.header.decode_header(fileName)[0][0].decode(email.header.decode_header(fileName)[0][1])
            except:
                pass

            # 只获取指定拓展名的附件
            extension = os.path.splitext(os.path.split(fileName)[1])[1]
            if valid_extensions:
                if extension not in valid_extensions:
                    continue

            # 如果获取到了文件，则将文件保存在指定的目录下
            if fileName:
                fileName = fileName.replace(" ","_")
                if not os.path.exists(self._savedir):
                    os.makedirs(self._savedir)
                filePath = os.path.join(self._savedir, fileName)
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                attachments.append(filePath)

        return attachments