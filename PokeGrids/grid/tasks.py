from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .views import archive_current_grid, schedule_next_task

@shared_task
def archive_current_grid_task():
    try:
        # Directly call the function from your view
        print("Archiving current grid...")
        archive_current_grid()

        print("Archiving complete.")
        schedule_next_task()
        return "Archiving completed successfully."

    except Exception as e:
        print(f"Error during archiving: {str(e)}")
        raise  # Re-raise the exception for Celery to handle