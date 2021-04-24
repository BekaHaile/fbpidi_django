
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from datetime import datetime
from django.utils import timezone

from background_task.models import Task, CompletedTask
from collaborations.tasks import (check_event_startdate, check_event_enddate, check_event_participation, check_tender_startdate, 
                                  check_tender_enddate, clear_completed_tasks, send_news_and_blogs_weekly )

# key: value pair for background task verbose name: background_task method
BACKGROUND_TASK_DICTIONARY = {
    'CLEAR_COMPLETED_TASKS': clear_completed_tasks,

    'EVENT_PARTICIPATION': check_event_participation,
    'EVENT_START_DATE':check_event_startdate,
    'EVENT_END_DATE': check_event_enddate,
    # 'WEEKLY_NEWS_BLOGS':send_news_and_blogs_weekly

    # 'TENDER_START_DATE': check_tender_startdate,
    # 'TENDER_END_DATE': check_tender_enddate,
}
TODAY = timezone.now()
BACKGROUND_TASK_TIME  = TODAY # will be changed when running inside __main__

def clear_background_tasks():
    Task.objects.all().delete()
    print("Successfully cleared all background tasks")

def clear_completed_tasks():
    CompletedTask.objects.all().delete()  
    print("Successfully cleared Completed Tasks")   


# the following functions call the same background tasks as the '__main__', but they can be called from other apps, like the admin_site
# inorder to control background messaging. 

# The Task table is the background_task table inside the databse
# the CompleteTask table is the background_task_completetask table inside the database

def start_task( task_verbose_name,repeat, schedule = 1,  ): 
    if not Task.objects.filter(verbose_name=task_verbose_name).exists():
        print(f"creating new task with verbose name {task_verbose_name} ")
        background_task_method = BACKGROUND_TASK_DICTIONARY [ task_verbose_name ]
        # this is when the background task is created with a verbose name, so that we can identify it later for updating or aborting it.
        background_task_method(verbose_name = task_verbose_name, schedule = schedule, repeat = repeat )
        return True
    else:
        print(f"task with verbose name {task_verbose_name} already exists")
        task = Task.objects.get(verbose_name=task_verbose_name)
        task.run_at = schedule
        task.repeat = repeat
        task.save()
        return True
        

def abort(task_verbose_name):
        if Task.objects.filter(verbose_name = task_verbose_name).exists():
            background_tasks = Task.objects.filter(verbose_name = task_verbose_name)
            for task in background_tasks:
                task.delete()
            if CompletedTask.objects.filter(verbose_name = task_verbose_name).exists():
                for task in CompletedTask.objects.filter( verbose_name = task_verbose_name):
                    task.delete()
            print(f"Aborted {task_verbose_name} ")
            return True
        
        print(f"No task found with the given verbose name {task_verbose_name}")
    

# inorder to stop all background tasks, commenting the for loop is not enough, u have to run 
# the clear_background_tasks cmd, so that the tasks saved in the db to be run are deleted.
if __name__ == '__main__':    
    
    print("Starting the background tasks ....")
    clear_background_tasks()
    clear_completed_tasks()
    BACKGROUND_TASK_TIME = TODAY.replace(hour=3,minute=0,second=0) # set the time to when u want to send emails
   
    print("Task scheduled at 6:00 am ",BACKGROUND_TASK_TIME)
    for verbose_name in BACKGROUND_TASK_DICTIONARY.keys():
        start_task(task_verbose_name=verbose_name,schedule=1, repeat = Task.DAILY) 
    send_news_and_blogs_weekly(verbose_name='WEEKLY_NEWS_BLOGS', repeat =Task.WEEKLY)
  



#     for verbose_name in BACKGROUND_TASK_DICTIONARY.keys():
#         start_task(task_verbose_name=verbose_name,schedule=1, repeat = 3) 
#     send_news_and_blogs_weekly(verbose_name='WEEKLY_NEWS_BLOGS', schedule=1, repeat =10)
# # 

























# ------------ background tasks for Event participant notification
# for a single background task , i.e. without generalizing as abort and start_task, we can define a start_task and abort for 
# each background task, the following is an example for  starting event participation background task

def start_check_event_participation(repeat = 10): 
    # if the task is running, just update the repeat timing else create new
    if Task.objects.filter(verbose_name='EVENT_PARTICIPATION').exists():
        print("task already exists")
        task = Task.objects.get(verbose_name='EVENT_PARTICIPATION')
        task.repeat = repeat
        task.save()
        return True
        
    else:
        print("creating new task")
        check_event_participation(repeat = repeat , verbose_name = "EVENT_PARTICIPATION")
        return True
    

