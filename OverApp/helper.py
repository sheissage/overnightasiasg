from django.core.mail import EmailMultiAlternatives
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders

class Helper():

	@staticmethod
	def send_booking_email(to, pdf):
		subject, from_email, to = 'Overnight.asia Itenerary', 'welcome@overnight.asia', to

		html_content = """
				<b>Greetings!!</b> 
				<br><br>
				<p>Attached is your booking confirmation. Thank you for booking with us! </p> 
				<br><br><br><br>
				<b>Overnight.asia Team</b>
			"""

		msg = EmailMultiAlternatives(subject, '', from_email, [to])
		msg.attach(MIMEText(html_content, 'html'))
		
		# attachFile = MIMEBase('application', 'pdf')
		# attachFile.set_payload(pdf)
		# Encoders.encode_base64(attachFile)
		# attachFile.add_header('Content-Disposition', 'attachment', filename='itenerary.pdf')
		msg.attach('itenerary.pdf', pdf, 'application/pdf')

		msg.send()