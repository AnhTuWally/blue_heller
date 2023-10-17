from django.db import models
from django.core.validators import MinValueValidator
from common.models import BaseModel

# import timezone
from django.utils import timezone

# import logging
import logging
logger = logging.getLogger(__name__)

class TodoRepeat(BaseModel):
    repeat_type = models.CharField(max_length=20, choices=[("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly")])
    repeat_interval = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    repeat_days = models.CharField(max_length=50, blank=True, null=True)
    repeat_start_date = models.DateField(blank=True, null=True)
    repeat_end_date = models.DateField(blank=True, null=True)

    # 1-1 relationship with todo
    todo = models.OneToOneField("todo.Todo", on_delete=models.CASCADE,
                                null=True, blank=True, related_name="repeat")

    def __str__(self):
        return f"{self.repeat_type} every {self.repeat_interval}"
    

    def get_monday_date(self, date):
        """Get the monday date of the week that the date is in
        """
        # Get the day of the week of the date
        day_of_week = date.weekday()

        # Get the monday date of the week
        monday_date = date - timezone.timedelta(days=day_of_week)

        return monday_date

    def is_due(self):
        """Checking if the todo is due to be reset
        Warning, this function is not aware of the timewhen the todo was last reset
        Additional logic is needed to check if the todo was reset today
        """

        # TODO: test this 
        # If repeat end_date has passed
        if self.repeat_end_date is not None and self.repeat_end_date < timezone.now().date():
            return False

        # Repeat dayly will always return true
        if self.repeat_type == "daily":
            if self.repeat_interval == 1:
                return True

            # Not sure if this will work 
            datetime_delta = timezone.now().date() - self.repeat_start_date
            days_delta = datetime_delta.days

            logger.info(f"days_delta: {days_delta}")

            # If this is the same day as the repeat start date, return False
            if days_delta == 0:
                return False

            # If the days delta is divisible by the repeat interval, return true
            if days_delta % self.repeat_interval == 0:
                return True
        
        if self.repeat_type == "weekly":
            # Convert repeats days from string to list of ints
            repeat_days = [int(day) for day in self.repeat_days.split(",")]

            # If today is not in the repeat days, return False
            if timezone.now().date().weekday() not in repeat_days:
                return False
            
            # If the repeat interval is 1, return True
            if self.repeat_interval == 1:
                return True
            
            # Get the monday date of the week that the repeat start date is in
            start_monday_date = self.get_monday_date(self.repeat_start_date)
            now_monday_date = self.get_monday_date(timezone.now().date())

            monday_datetime_delta = now_monday_date - start_monday_date

            days_delta = monday_datetime_delta.days
            weeks_delta = days_delta // 7

            # If the weeks delta is 0, return False
            # The repeatable todo was created on the same week
            if weeks_delta == 0:
                return False

            # If the weeks delta is divisible by the repeat interval, return true
            if weeks_delta % self.repeat_interval == 0:
                return True


        if self.repeat_type == "monthly":

            if self.repeat_interval == 1:
                return True
            
            # TODO: Implement monthly repeat with more than 1 month interval

        # If none of the above conditions are met, return False
        return False
    

    def reset(self):
        """Reset the todo
        """
        self.todo.is_done = False
        self.todo.save()
        logger.debug(f"Reset todo {self.todo}")



