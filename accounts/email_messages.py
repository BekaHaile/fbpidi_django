from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def sendEmailVerification(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Email Verification Required.'
    message = get_template('email/acct_activate_email.html').render({
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    to_email = user.email
    email = EmailMessage(
    mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()
    return email

def sendWelcomeEmail(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Your Account has been Activated'
    message = get_template('email/acc_activated_email.html').render({
        'user': user,
    })
    to_email = user.email
    email = EmailMessage(
    mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()
    return email
    
def sendEventNotification(request, participant):
    
    current_site = get_current_site(request)
    mail_message = f'The Event titled "{participant.event.event_name}" Will start after {participant.notifiy_in}.'
    mail_subject = f'Event Notification From IIMP'
    to_email = participant.patricipant_email
    email = EmailMessage(mail_subject, mail_message, to=[participant.patricipant_email])
    email.content_subtype = "html"  
    try:
        email.send()
        print("Email sent to ", participant.patricipant_email)
    except Exception as e:
        print("Exception While Sending Email ", str(e))
    participant.notified = False
    participant.save()
    return email
