import smtplib
import config

smtpUser = ''	# Add here email address to send emails from
smtpPass = ''	# Add here password of the above email account

if (smtpUser == '') or (smtpPass == ''): 
    print "smtpUser or smtpPass not configured!"
    exit(1)


toAddress   = config.EMAIL_TO_ADDRESS
fromAddress = smtpUser

subject = config.EMAIL_SUBJECT_AFTER_WATERING
header 	= 'To: ' + toAddress + '\n' + 'From: ' + fromAddress + '\n' + 'Subject: ' + subject
body 	= config.EMAIL_BODY_TEXT + config.EMAIL_BODY_DATA + config.EMAIL_BODY_SIGN

# print header + '\n' + body

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login(smtpUser, smtpPass)
s.sendmail(fromAddress, toAddress, header + '\n\n' + body)

s.quit()

print "email sent!"

