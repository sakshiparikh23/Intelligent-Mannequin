import smtplib


def email_user(scenario_data):
    gmail_user = 'yuvitesting1@gmail.com'
    gmail_password = '@@Lionking25@@'

    sent_from = gmail_user
    a = 'yuvitesting1@gmail.com'
    to = [a]
    subject = 'Conversation Details'
    body = scenario_data
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        # For secure connection
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        #server_ssl.ehlo()  # optional
        # ...send emails
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        ab =  'Email sent!'
        return ab
    except:
        ab = 'Something went wrong...'
        return ab