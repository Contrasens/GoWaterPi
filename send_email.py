import smtplib

smtpUser = 'GoWaterPi@gmail.com'
smtpPass = 'Dinu1234'

toAddress   = 'dinu.sarbu@gmail.com'
fromAddress = smtpUser

subject = 'Python Test'
header 	= 'To: ' + toAddress + '\n' + 'From: ' + fromAddress + '\n' + 'Subject: ' + subject
body 	= 'Email from the Python script :)'

print header + '\n' + body

s = smtplib.SMTP('smtp.gmail.com',587)

s.ehlo()
s.starttls()
s.ehlo()

s.login(smtpUser, smtpPass)
s.sendmail(fromAddress, toAddress, header + '\n\n' + body)

s.quit()



