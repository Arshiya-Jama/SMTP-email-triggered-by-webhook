from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from createLogs import LOG

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

logFile = open("log.txt", "w")

fileObj = LOG(logFile)

#Open file and read contents
path = Path(__file__).parent / "./config.yaml"

with path.open() as f:
    data = yaml.load(f, Loader=SafeLoader)
    fileObj.createLogs("Configuration loaded: " + data)

@app.route(data["webhookPath"], methods=['POST'])
def listner():

    #Extracting data from Webhook
    message = request.json
    fromaddr = data['from']
    
    # Get recipient email via API headers
    toaddrs  = request.headers.get('sendto')
    msg = MIMEText(message['message'] + '\n' + message['time'])
    msg['Subject'] = 'Cribl Notification: ' + message['_metric'] + ' ' + message['cribl_notification']
    
    fileObj.createLogs("message body loaded: " + msg)
        
    #Add this data into the smtp call
    try:
        with smtplib.SMTP(data["smtpHost"], data["smtpPort"]) as server:
            x = server.sendmail(fromaddr, toaddrs, msg.as_string())
            if x:
                #Each recipient that has failed will give a different error code
                errMsg = 'Error sending email \n' + str(x)
                fileObj.createLogs(errMsg)
				# Send error message back to Cribl so it can be handled there as well
                return errMsg
            else:
                errMsg = 'Email Sent Successfully'
                fileObj.createLogs(errMsg)
                return errMsg
    except:
        errMsg = 'SMTP config error or all recipients failed'
        fileObj.createLogs(errMsg)
		
        return errMsg
    
    logFile.close()

if __name__ == '__main__':
    app.run(host=data["flaskHost"], port=data["flaskPort"])
