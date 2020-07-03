from django.db import models
from datetime import datetime, timedelta
from django.utils.timezone import localtime

def format_duration(duration):
    total_seconds = duration.total_seconds()
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds % 3600) / 60)
    return f"{hours}ч {minutes}м"

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )
    
    def get_duration(self):
        if self.leaved_at == None:
            return datetime.now() - localtime(self.entered_at).replace(tzinfo=None)
        else:
            return localtime(self.leaved_at).replace(tzinfo=None) - localtime(self.entered_at).replace(tzinfo=None)
    
    def is_long(self, seconds=3600):
        total_seconds = self.get_duration().total_seconds()
        return total_seconds > seconds
