import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
import base64
from email.mime.image import MIMEImage
import traceback


class SendMail(object):
    def __init__(self, title=None, content=None,
                 file=None, image=None, ssl_port=465):

        '''
               :param username: 用户名
               :param passwd: 密码
               :param recv: 收件人，多个要传list ['a@qq.com','b@qq.com]
               :param title: 邮件标题
               :param content: 邮件正文
               :param image: 图片路径，绝对路径，默认为无图片
               :param file: 附件路径，如果不在当前目录下，要写绝对路径，默认没有附件
               :param ssl: 是否安全链接，默认为安全链接
               :param email_host: smtp服务器地址，默认为qq服务器
               :param ssl_port: 安全链接端口，默认为465
        '''

        self.username = "wangchuanxin1995@163.com"  # 用户名（发件人的邮箱账号或用户名）
        self.passwd = "EQTVOGTDMKFWDWUV"  # 16位的SMTP授权码（不含空格）
        self.recv = ['keertem1911@126.com']
 # 收件人，多个要传list ['a @ qq.com','b @ qq.com]
        self.title = title  # 邮件标题
        self.content = content  # 邮件正文
        self.file = file  # 绝对路径
        self.image = image  # 图片路径（绝对路径）
        self.email_host = 'smtp.163.com'  # smtp服务器地址,默认为qq邮箱的服务器
        self.ssl = True,  # 是否安全链接
        self.ssl_port = ssl_port  # 安全链接端口
        # 构造一个MIMEMultipart对象代表邮件本身
        self.message = MIMEMultipart()

        # 添加文件到附件
        if self.file:
            file_name = os.path.split(self.file)[-1]  # 只取文件名，不取路径
            try:
                f = open(self.file, 'rb').read()
            except Exception as e:
                traceback.print_exc()
            else:
                att = MIMEText(f, "base64", "utf-8")
                att["Content-Type"] = 'application/octet-stream'
                # base64.b64encode(file_name.encode()).decode()
                new_file_name = '=?utf-8?b?' + base64.b64encode(file_name.encode()).decode() + '?='
                # 处理文件名为中文名的文件
                att["Content-Disposition"] = 'attachment; filename="%s"' % (new_file_name)
                self.message.attach(att)

        # 添加图片到附件

        if self.image:
            count=1
            for img in image:
                image_name = os.path.split(img)[-1]  # 只取文件名和后缀，不取路径
                try:
                    with open(img, 'rb') as f:
                        # 图片添加到附件
                        mime = MIMEBase('image', 'image', filename=image_name)
                        mime.add_header('Content-Disposition', 'attachment', filename=image_name)
                        mime.set_payload(f.read())
                        encoders.encode_base64(mime)
                        self.message.attach(mime)
                    with open(img, 'rb') as f:
                        # 将图片显示在邮件正文中
                        msgimage = MIMEImage(f.read())
                        msgimage.add_header('Content-ID', '<image{}>'.format(count))  # 指定文件的Content-ID,<img>,在HTML中图片src将用到
                        self.message.attach(msgimage)
                    count+=1
                except Exception as e:
                    traceback.print_exc()

    def send_mail(self):
        self.message.attach(MIMEText(self.content, 'html', 'utf-8'))  # 正文内容   plain代表纯文本,html代表支持html文本
        self.message['From'] = self.username  # 发件人
        self.message['To'] = ','.join(self.recv)  # 收件人
        self.message['Subject'] = self.title  # 邮件标题
        self.smtp = smtplib.SMTP_SSL(self.email_host, port=self.ssl_port)
        # 发送邮件服务器的对象
        self.smtp.login(self.username, self.passwd)
        try:
            self.smtp.sendmail(self.username, self.recv, self.message.as_string())
            pass
        except Exception as e:
            resultCode = 0
            traceback.print_exc()
        else:
            result = "邮件发送成功！"
            print(result)
            resultCode = 1
        self.smtp.quit()
        return resultCode  # 定义一个邮件发送结果参数，1为发送成功，0为发送失败。


import pathlib
#只发送对多10个
def createEmail(rootPath,img_suffix="jpg",title="检查结果",sendlength=10):
    content = '''
               <h1>物体监测</h1>
               <p>图片展示：</p>
               <p>
             '''
    path = pathlib.Path(rootPath)
    list = path.glob("*.{}".format(img_suffix))
    images=[]
    count=1
    for f in list:
        content+='<img style="width:80%;height:260px" src="cid:image{}">'.format(count)
        images.append(str(path / f))
        count+=1
        if count>sendlength:
            break
    content += "</p>"
    if len(images)>0:
        m = SendMail(title, content=content, image=images)
        print("send...")
        m.send_mail()

