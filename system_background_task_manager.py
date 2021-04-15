
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()

from background_task.models import Task, CompletedTask
from collaborations.tasks import check_event_enddate, check_event_participation, check_tender_startdate

DAILY = 60 * 60 * 24 # seconds
WEEKLY = DAILY * 7
THREE  = 3

# key: value pair for background task verbose name: background_task method
BACKGROUND_TASK_DICTIONARY = {
    'EVENT_PARTICIPATION': check_event_participation,
    'EVENT_END_DATE': check_event_enddate,
    'TENDER_START_DATE': check_tender_startdate,
    'TENDER_END_DATE': None,
}

def clear_background_tasks():
    Task.objects.all().delete()
    print("Successfully cleared all background tasks")
    
def clear_completed_tasks():
    CompletedTask.objects.all().delete()
    print("Completed tasks cleared successfully")


# the following functions call the same background tasks as the '__main__', but they can be called from other apps, like the admin_site
# inorder to control background messaging. 

# The Task table is the background_task table inside the databse
# the CompleteTask table is the background_task_completetask table inside the database

def start_task(task_verbose_name, repeat = 10):
    if not Task.objects.filter(verbose_name=task_verbose_name).exists():
        print("creating new task")
        background_task_method = BACKGROUND_TASK_DICTIONARY [ task_verbose_name ]
        # this is when the background task is created with a verbose name, so that we can identify it later for updating or aborting it.
        background_task_method(verbose_name = task_verbose_name, repeat = repeat )
        return True

    else:
        print("task already exists")
        task = Task.objects.get(verbose_name=task_verbose_name)
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
    

if __name__ == '__main__':    
    # clear_background_tasks()
    # clear_completed_tasks()
    print("Starting the background tasks ....")
    # abort(task_verbose_name='TENDER_START_DATE')
    start_task(task_verbose_name='TENDER_START_DATE', repeat = 2)
    # abort(task_verbose_name='EVENT_PARTICIPATION')
    
    
























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
    

