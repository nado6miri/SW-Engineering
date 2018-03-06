import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

imgfile = "car.jpg"
imgfile2 = "car2.gif"

smtpHost = "smtp.gmail.com"
senderAddr = "nado6miri@gmail.com"
recipientAddr = "nado6miri@naver.com"

msg = MIMEBase("multipart", "alternative")

msg['Subject'] = "Test Email......from gmail to naver"
msg['From'] = senderAddr
msg['To'] = recipientAddr

desc = "test email ............, 테스트 이메일 입니다."
text = MIMEText(desc, 'plain')
msg.attach(text)

with open("logo.html", 'rb') as htmlFD:
    buf = htmlFD.read()
    print(buf)
    buf = buf.decode('utf-8')
    buf = desc + buf
    print(buf)
    HtmlPart = MIMEText(buf, 'html', _charset='UTF-8')
    #HtmlPart = MIMEText(htmlFD.read(), 'html', _charset='UTF-8')
msg.attach(HtmlPart)

with open("logo2.html", 'rb') as htmlFD:
    HtmlPart = MIMEText(htmlFD.read(), 'html', _charset='UTF-8')
msg.attach(HtmlPart)
print(msg.as_string())

with open(imgfile, 'rb') as imgFD:
    ImagePart = MIMEImage(imgFD.read(), name=imgfile, _subtype='jpg')

msg.attach(ImagePart)
msg.add_header('Content-Disposition', 'attachment', filename=imgfile)


with open(imgfile2, 'rb') as imgFD:
    ImagePart = MIMEImage(imgFD.read(), name=imgfile2, _subtype='gif')

msg.attach(ImagePart)
msg.add_header('Content-Disposition', 'attachment', filename=imgfile2)

s = smtplib.SMTP(smtpHost, 587)
s.ehlo()
s.starttls()
s.ehlo()
s.login("nado6miri@gmail.com", "Sungbin@5504")
s.sendmail(senderAddr, [recipientAddr], msg.as_string())
s.close()
