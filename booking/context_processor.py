from .models import Setting, City, DAY_CHOICES, WEEK_DAY_CHOICES,MONTH_CHOICES, ChildrenAge


def context_processor(request):
    if request.method == 'POST':
        print("salam")
    return {
        'setting': Setting.objects.first(),
        "cities":  City.objects.all(),
        "day_choises":  DAY_CHOICES,
        "week_day_choises":  WEEK_DAY_CHOICES,
        "month_choises":  MONTH_CHOICES,
        "children_choises":  ChildrenAge.objects.all(),
        'user_full_name' : request.session.get('user_full_name', None),
    }
