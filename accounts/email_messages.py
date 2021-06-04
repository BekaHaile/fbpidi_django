import string
import random

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string,get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.models import Subscribers
from company.models import Company

# the redirect_url for the web is 'activate' and for the api is 'api_activate', both views send the same
# welcome email, but the web activate view will render a web page, and the api does nothing.
SITE_DOMAIN = "/localhost:8000/"

def sendInvitationEmail(request, email, name = None):
    try:
        current_site = get_current_site(request)
        mail_subject = 'An invitation to use the IIMS system'
        message = f"You are invite to use the IIMS system, through the following link. "
        
        to_email = email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.content_subtype = "html"
        email.send()
        return True
    except Exception as e:
        print("#### Exception at sendInvitationEmail ",e)
        return False
    

def sendEmailVerification(request,user, redirect_url = 'activate'):
    try:
        current_site = get_current_site(request)
        mail_subject = 'Welcome To FBPIDI-IIMS - Email Verification Required'
        message = get_template('email/acct_activate_email.html').render({
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'redirect_url':redirect_url,
        })

        to_email = user.email
        email = EmailMessage(
        mail_subject, message, to=[to_email],
        )
        email.content_subtype = "html"
        email.send()
        print("email sent")
        # return email
        return True

    except Exception as e :
        print ("Exception sending email ",e)
        return False


def sendWelcomeEmail(request,user, acctivated=None):
    current_site = get_current_site(request)
    mail_subject = 'Welcome To FBPIDI-IIMS - Email Verified'
    message = get_template('email/acc_activated_email.html').render({
        'user': user,
        'acctivated':acctivated,
        'domain':current_site.domain
    })
    to_email = user.email
    email = EmailMessage(
    mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()
    return email


def sendSubscriptionActivationEmail(request, subscribtion, email):
    try: 
        current_site = get_current_site(request)
        mail_subject = f"Subscription Email Verification Required .{email}"
        letters = string.ascii_lowercase
        token = ''.join(random.choice(letters) for i in range(12))
        message = get_template('email/acct_activate_email.html').render({
            'user': "user bota",
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(subscribtion.id)),
            'token': token,
            'redirect_url':'activate_subscribtion'
        })
        email = EmailMessage( mail_subject, message, to=[ email ])
        email.content_subtype = "html"
        email.send(fail_silently=False)
        print("sent an Email")
        return True
    except Exception as e:
        print ("@@@@@ Exception while sending email activation email ", e)
        return False


def sendEventParticipationNotification(participant):
    mail_message = f'The Event titled "{participant.event.title}" Will start on {participant.event.start_date.date()}.'
    mail_subject = f'Event Notification From IIMP'
    email = EmailMessage(mail_subject, mail_message, to=[participant.patricipant_email])
    email.content_subtype = "html"  
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Exception While Sending Email to {participant.patricipant_email} Due to the following exception \n =>", str(e))
        return False


def sendEventNotification(event, message):
    mail_subject = f'Event Notification From IIMP'
    email = EmailMessage(mail_subject, message, to=[event.created_by.email])
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


def sendWeekBlogAndNews(blogs,week_blogs_count,news,week_news_count):
    try:
        subscribers_email =[ s.email for s in Subscribers.objects.filter(is_active = True)]
        mail_subject = f'Latest News and Blogs From FBPIDI'
        context = {
            'blogs': blogs,
            'week_blogs_count':week_blogs_count,
            'news':news,
            'week_news_count':week_news_count,
            'domain': SITE_DOMAIN,
            'fbpidi': Company.objects.get(main_category='FBPIDI'),
            'unsubscribe_link':'unsubscribe',
            'redirect_url':'activate_subscribtion'
        }
        message = get_template('email/news_email.html').render(context)
        email = EmailMessage( mail_subject, message, to = subscribers_email)
        email.content_subtype = "html"
        email.send(fail_silently=False)
        print("Email sent")
        return True

    except Exception as e:
        print("Exception inside sendWeekBlogAndNews  ", str(e))
        return False

