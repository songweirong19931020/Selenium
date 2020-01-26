"""
@File : ygmail.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/26
"""
import yagmail

#链接邮箱服务器
yag = yagmail.SMTP( user="swr19931020@126.com", password="a84906036", host='smtp.126.com')

# 邮箱正文
contents = ['This is the body, and here is just text http://somedomain/image.png',
            'You can find an audio file attached.', '/local/path/song.mp3']

# 发送邮件
yag.send('swr19931020@126.com', 'subject', contents)
#关闭
yag.close()