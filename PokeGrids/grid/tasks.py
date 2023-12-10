from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .views import archive_current_grid
from datetime import timedelta
from django.utils import timezone
from .models import ArchivedGrid, Grid

@shared_task
def archive_current_grid_task():
    # Move the logic for archiving the grid here
    print("Archived Grid")
    archive_current_grid()