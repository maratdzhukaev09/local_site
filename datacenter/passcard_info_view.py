from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from .models import format_duration

def get_this_passcard_visits(passcard):
    this_passcard_visits = []
    for visit in Visit.objects.filter(passcard=passcard):
        visit_dict = {
            "entered_at": visit.entered_at,
            "duration": format_duration(visit.get_duration()),
            "is_strange": visit.is_long()
        }
        this_passcard_visits.append(visit_dict)
    return this_passcard_visits

def passcard_info_view(request, passcode):
    
    passcard = Passcard.objects.filter(passcode=passcode)[0]

    context = {
        "passcard": passcard,
        "this_passcard_visits": get_this_passcard_visits(passcard)
    }
    return render(request, 'passcard_info.html', context)
