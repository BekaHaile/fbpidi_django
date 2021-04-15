from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string,get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def sendEmailVerification(request,user):
    try:
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
    except Exception:
        return

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


def sendEventNotification(participant):
    mail_message = f'The Event titled "{participant.event.title}" Will start on {participant.event.start_date.date()}.'
    mail_subject = f'Event Notification From IIMP'
    email = EmailMessage(mail_subject, mail_message, to=[participant.patricipant_email])
    email.content_subtype = "html"  
    try:
        email.send()
        print("Event notification Email sent to ", participant.patricipant_email)
        return True
    except Exception as e:
        print(f"Exception While Sending Email to {participant.patricipant_email} Due to the following exception \n =>", str(e))
        return False


def sendEventClosedNotification(event):
    mail_message = f"IIMP system has changed the status of the Event titled '{event.title}'. This occurs when the creator of the event didn't change the status ."
    mail_subject = f'Event Notification From IIMP'
    email = EmailMessage(mail_subject, mail_message, to=[event.created_by.email])
    email.content_subtype = "html"  
    try:
        email.send()
        print("Event closed Email sent to ", event.created_by.email)
        return True
    except Exception as e:
        print("Exception While Sending Email ", str(e))
        return False
    

def sendTenderEmailNotification(user_email, tender, message):
    mail_subject = f'Tender Notification From IIMP'
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.content_subtype = "html"  
    try:
        email.send()
        print("Tender Email sent to ", user_email)
        return True
    except Exception as e:
        print("Exception While Sending Tender Email ", str(e))
        return False


def sendRelayMessage(request, sender_message, reply_message):
    try:
        current_site = get_current_site(request)
        mail_message = reply_message
        mail_subject = f'Company Reply From {request.user.get_company()}'
        to_email = sender_message.email
        email = EmailMessage(mail_subject, mail_message, to=[sender_message.email])
        email.content_subtype = "html"  
        email.send()
        print("Company Replay message sent to Email ", sender_message.email)
        return True
    except Exception as e:
        print("Exception While Sending Email ", str(e))
        return False
    
def sendInquiryReplayEmail(request, inquiry, reply_message):
    try:
        current_site = get_current_site(request)
        mail_message = reply_message
        mail_subject = f'Inquiry Reply From {request.user.get_company()}'
        to_email = inquiry.sender_email
        email = EmailMessage(mail_subject, mail_message, to=[inquiry.sender_email])
        email.content_subtype = "html"  
        email.send()
        print("Inquiry Replay message sent to Email ", inquiry.sender_email)
        return True
    except Exception as e:
        print("Exception While Sending Inquiry Email ", str(e))
        return False



