import os
import datetime
import random
import time
import smtplib
import pdfkit
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr

# Specify the path to wkhtmltopdf executable
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
pdfkit_config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

base_directory = os.path.dirname(os.path.realpath(__file__))

def send_mail(sender_name, sender_email, receiver, subject, message_content, cc_email, html, company_name, reply_to, smtp_server, smtp_port, smtp_user, smtp_password, pdf_path=None, static_file_path=None, send_attachment=False, add_cc=False):
    try:
        message = EmailMessage()
        if html:
            message.add_alternative(message_content, subtype='html')
        else:
            message.set_content(message_content)
        
        message['From'] = formataddr((sender_name, sender_email))
        if add_cc:
            message['CC'] = cc_email
        message['Reply-To'] = reply_to
        message['To'] = receiver
        message['Subject'] = subject

        # Attach PDF and static file if send_attachment is True
        if send_attachment:
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                message.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

            if static_file_path and os.path.exists(static_file_path):
                with open(static_file_path, 'rb') as f:
                    static_data = f.read()
                message.add_attachment(static_data, maintype='application', subtype='pdf', filename=os.path.basename(static_file_path))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)
        
        with open("emails_send.txt", "a", encoding="utf-8") as f:
            f.write(f"{receiver} | {sender_name} | {company_name} | {datetime.datetime.now().date().strftime('%d-%m-%Y')}\n")
        print(f'Message sent to {receiver}')

    except Exception as error:
        print(f'An error occurred: {error}')

reply_to = "Andrea Brannen <andrea.b@anbconsult.org>"  # Set your fixed reply-to email here
subjects = ["Past Due Invoice - Leadership Excellence (Build a Better Team, Achieve Better Results) External"]
sender_name = "Andrea Brannen"  # Set your sender name here

# SMTP server configuration
smtp_server = "mail.dtyinsaat.com"
smtp_port = 587
smtp_user = sender_email = "orhan@dtyinsaat.com"
smtp_password = "dty2024"

# Set your box variable here
box = "anbconsult.org"

# Specify the name of the PDF file (if any)
pdf_filename = "Service Consult INV114721.pdf"

# Specify the path to the static file (if any)
static_file_path = os.path.join(base_directory, "W9.pdf")

# Set whether to send attachments and CC
send_attachment = True
add_cc = True

messages = []
for file in os.listdir(os.path.join(base_directory, "messages")):
    if file.endswith(".txt"):
        file = os.path.join(base_directory, "messages", file)
        messages.append(open(file, encoding="utf-8").read().strip())

# Read the HTML template from an external file (if any)
html_template_path = os.path.join(base_directory, "template.html")
if os.path.exists(html_template_path):
    with open(html_template_path, encoding="utf-8") as f:
        html_template = f.read()
else:
    html_template = None

for x in open("input.txt", encoding="latin-1").readlines():  # Changed encoding to 'latin-1'
    x = x.strip()
    email, name, company_name, domain, username, ceo = x.split(" | ")
    text = random.choice(messages).replace("{email}", email).replace("{name}", name).replace("{company_name}", company_name).replace("{domain}", domain).replace("{username}", username).replace("{box}", box).replace("{ceo}", ceo)
    html = False
    if text[0] == "<":
        html = True

    subject = random.choice(subjects).replace("{company_name}", company_name)
    cc_email = f"Accounting <accounting@{box}>"

    # Replace placeholders in HTML template if provided and convert to PDF
    if html_template:
        personalized_html = html_template.replace("{name}", name).replace("{email}", email).replace("{company_name}", company_name).replace("{domain}", domain).replace("{username}", username).replace("{ceo}", ceo)
        pdf_path = os.path.join(base_directory, pdf_filename)
        pdfkit.from_string(personalized_html, pdf_path, configuration=pdfkit_config)
    else:
        pdf_path = None

    send_mail(sender_name, sender_email, email, subject, text, cc_email, html, company_name, reply_to, smtp_server, smtp_port, smtp_user, smtp_password, pdf_path, static_file_path, send_attachment, add_cc)
    time.sleep(10)

    # Clean up the PDF file if it was created
    if pdf_path and os.path.exists(pdf_path):
        os.remove(pdf_path)
