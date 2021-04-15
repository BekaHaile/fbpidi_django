from background_task import background
from company.models import CompanyEvent, EventParticipants
from collaborations.models import Tender
from django.utils import timezone
from accounts.email_messages import sendEventNotification, sendEventParticipationNotification, sendTenderEmailNotification
from django.db.models import Q
from django.utils import timezone
from background_task.models import Task, CompletedTask

@background
def clear_completed_tasks():
    print("____________________")
    CompletedTask.objects.all().delete()    
    print("Completed tasks cleared successfully")


@background()
def check_event_startdate():
    print("____________________")
    print("Started automatic Event Opening for Upcoming tenders ...")
    if CompanyEvent.objects.exists():
        events = CompanyEvent.objects.filter( status='Upcoming') 
        today = timezone.now().date()
        success = 0
        for event in events:
            if event.start_date.date() <= today and event.status != 'Open':
                event.status = "Open"
                event.save()
                success+=1
                sendEventNotification( event= event,  message = f"IIMP system has changed the status of the Event titled '{event.title}'. This occurs when the creator of the event didn't change the status .")
        print(f"Finished automatic Events Opening process, checked {events.count()} Upcoming tenders and successfully Opened {success} tenders. ", timezone.now().date())
    else:
        print("Tried to automatically Open Events, but no Tender was Found!")



# verbose name = event enddate
@background()
def check_event_enddate():
    """
    If some company events exist, it checks thier end date and for those whose enddate is greater than today,
    it will change the status of the event to "Closed" and send and email notification to the creator user of the 
    event

    This backgeound function is set to be repeated everyday at 12:00 with verbose name event enddate
    """
    print("____________________")
    print("Started automatic Event closing ...")
    if CompanyEvent.objects.exists():
        open_events = CompanyEvent.objects.filter( Q( status = 'Upcoming') | Q(status = "Open") )
        today = timezone.now().date()
        for event in open_events: 
            if today >= event.end_date.date():
                print("event to be closed found ", event.title," ", event.end_date.date())
                event.status = "Closed"
                event.save() 
                sendEventNotification(event = event, message = f"IIMP system has changed the status of the Event titled '{event.title}'. This occurs when the creator of the event didn't change the status .")
        print("Finished automatic Event Closing process for ", timezone.now().date())
    else:
        print("Tried to check enddates of Events, but no Company Event was Found!")


# it's verbose name is 'event notification'
@background()
def check_event_participation():
    
    print("\n -----------------------------------------------")
    print("Started to check any unnotified Event participants ...")
    success = 0
    failed = 0
    if EventParticipants.objects.exists():
        today = timezone.now().date()
        event_participants = EventParticipants.objects.filter( notified=False, event__status = "Upcoming") #or open
        for participant in event_participants:
            if participant.notify_on <= today: #lesser than is used, because if we check event participation notification once a day and 
                                                      # if the system could not send on the notify date, then it will send even if the notify me date has passed, but the event is in upcoming status
                # make it send the email for multiple participants
                if sendEventParticipationNotification(participant):
                    participant.notified = True
                    participant.save()
                    success+=1
                else:
                    print("Couldn't send event notification ")
                    failed+=1
        print("\nFinished checking unnotified event participats for ", timezone.now().date())
        print(f" Checked a total of {event_participants.count()} Unnotified participants, \n Successfull Notifications = {success} \n Failed Notifications = {failed}")  
        print("\n -----------------------------------------------\n")
    else:
        print("Tried to send event notification for a participants, but no participant was Found!")


# for event participants who were not notified when the event was in upcoming or open (due to wrong email or connection problem), but the 
# event is now closed, then they should not be fetched by  check_event_participation(), since it fetchs unnotified participants
def close_passed_event_participation():
    pass


@background()
def check_tender_startdate():
    print("____________________")
    print("Started automatic Tender Opening for Upcoming tenders ...")
    if Tender.objects.exists():
        tenders = Tender.objects.filter( status='Upcoming') 
        today = timezone.now().date()
        success = 0
        for tender in tenders:
            if tender.start_date.date() <= today and tender.status != 'Open':
                tender.status = "Open"
                tender.save()
                success+=1
                sendTenderEmailNotification(user_email= tender.created_by.email, tender= tender, message= f"IIMP system has changed the status of the Tender titled '{tender.title}' to 'Open'. This occurs when the start date you set for a tender has reached.\n Then the system will automatically change the status for data consistency .")
        print(f"Finished automatic Tender Opening process, checked {tenders.count()} Upcoming tenders and successfully Opened {success} tenders. ", timezone.now().date())
    else:
        print("Tried to automatically Open Tenders, but no Tender was Found!")


@background()         
def check_tender_enddate():
    print("____________________")
    print("Started automatic Tender closing for Open tenders ...")
    success = 0
    if Tender.objects.exists():
        tenders = Tender.objects.filter( Q(status = 'Open') | Q(status = 'Upcoming') )
        today = timezone.now().date()
        for tender in tenders:
            if tender.end_date.date() <= today and tender.status != 'Closed':
                tender.status = "Closed"
                tender.save() 
                success += 1
                sendTenderEmailNotification(user_email =tender.created_by.email, tender = tender, message = f"IIMP system has changed the status of the Tender titled '{tender.title}' to 'Closed'. This occurs when the end date you set for a tender has reached. \n Then the system will automatically change the status for data consistency .")
        print(f"Finished automatic Tender Closing process, checked {tenders.count()} Open and Upcoming and closed {success} tenders  ", timezone.now().date())
    else:
        print("Tried to automatically Close Tenders, but no Tender was Found!")


