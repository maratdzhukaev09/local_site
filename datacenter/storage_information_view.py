from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from .models import format_duration

def get_non_closed_visits(visits):
    non_closed_visits = []
    for visit in visits:
        non_closed_visit = {
            "who_entered": visit.passcard.owner_name,
            "entered_at": visit.entered_at,
            "duration": format_duration(visit.get_duration()),
            "is_strange": visit.is_long()
        }
        non_closed_visits.append(non_closed_visit)
    return non_closed_visits

def storage_information_view(request):
    non_closed_visits = get_non_closed_visits(Visit.objects.filter(leaved_at=None))
    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
