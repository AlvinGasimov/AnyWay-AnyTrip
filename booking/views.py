from django.shortcuts import render
from datetime import datetime
from django.views.generic import TemplateView, FormView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404,redirect
from .filters import AnnouncementFilter
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import City, PropertyCategory, TravelCategory, \
    Announcement, SpecialOffer, Subscribe, PopularFilter, Service, \
    RATING_CHOISES, DAY_CHOICES, WEEK_DAY_CHOICES,MONTH_CHOICES, ChildrenAge, \
    Order, Rules, RoomType, Room, HomeButtonLink, Advice,  Announcement, PopularFilter, Service, PropertyCategory

from .tasks import subscribe_send_offers
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from user.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

def rooms(request, pk):
    
    hotel = Announcement.objects.get(pk=pk)
    rooms = hotel.rooms.all()
    
    room_count = rooms.count()
    
    types = RoomType.objects.all()
    services = Service.objects.all()
    populars = PopularFilter.objects.all()
    
    
    service_list = request.GET.getlist('service')
    popular_list = request.GET.getlist('popular')
    type_list = request.GET.getlist('type')
    
    if service_list:
        rooms = rooms.filter(services__id__in=service_list).distinct()

    if popular_list:
        rooms = rooms.filter(popular_filters__id__in=popular_list).distinct()

    if type_list:
        rooms = rooms.filter(type__id__in=type_list).distinct()
    
    
    context = {
        "rooms": rooms,
        "room_count": room_count,
        "hotel": hotel,
        "types": types,
        "services": services,
        "populars": populars
    }
    
    return render(request, 'rooms.html', context=context)



def room_detail(request, pk):
    room = Room.objects.filter(pk=pk).first()
    
    room_images = room.images.all()
    
    try:
        first_image = room_images[0]
    except:
        first_image = None
        
    try:
        second_image = room_images[1]
    except:
        second_image = None
        
    try:
        third_image = room_images[2]
    except:
        third_image = None
        
    try:
        four_image = room_images[3]
    except:
        four_image = None
        
    

    alt_images = room_images[3:6]
    
    other_images = room_images[6:]
    
    
    
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.session.get("user_id"))
        phone = request.POST.get("phone_number")
        email = request.POST.get("email")
        room_type = request.POST.get("room_type")
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        room = request.POST.get("room")
        order_message = request.POST.get("order_message")
        
        
        if request.POST.get("check-in-date") and request.POST.get("check-out-date"):
            check_in_date, check_out_date = request.POST.get("check-in-date"), request.POST.get("check-out-date")
            check_in_date = datetime.strptime(check_in_date, "%m/%d/%Y")
            check_out_date = datetime.strptime(check_out_date, "%m/%d/%Y")

            room = Room.objects.get(id=room)
            total_amount = room.price * (check_out_date - check_in_date).days
            try:
                Order.objects.create(
                    user = user,
                    announcement=room.hotel,
                    room = room,
                    name=name,
                    surname=surname,
                    phone=phone,
                    mail=email,
                    room_type=RoomType.objects.get(id=int(room_type)),
                    from_date=check_in_date,
                    to_date=check_out_date,
                    total_amount=total_amount,
                    order_message = order_message
                )
        
                subject = "Sifarişiniz uğurla qəbul edildi"
                message = (
                    f"Siz {room.hotel.title} otelində {room.room_name} otağını "
                    f"{check_in_date.strftime('%d-%m-%Y')} tarixindən {check_out_date.strftime('%d-%m-%Y')} "
                    f"tarixinə qədər bron etmisiniz. Ödəniləcək məbləğ: {total_amount} ₼."
                )
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return JsonResponse({"status": "success", "message": "Sifarişiniz uğurla yaradıldı və təsdiq e-poçtu göndərildi."})
                
            except Exception as e:
                print("Xeta bas verdi", e)
        
    context = {
        "room": room,
        "first_image": first_image,
        "second_image": second_image,
        "third_image": third_image,
        "alt_images": alt_images,
        "other_images": other_images,
        "four_image": four_image
    }
    
    return render(request, 'room-details.html', context=context)




def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscribes = Subscribe.objects.filter(email = email)
        if not subscribes:
            subscribe = Subscribe(email=email)
            subscribe.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request, 'index.html')

def rules(request):
    context = {
        "rules": Rules.objects.first()
    }
    return render(request, "rules.html", context=context)

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["property_categories"] = PropertyCategory.objects.all()
        context["filtered_cities_top"] = City.objects.filter(in_home_section = True)[:2]
        context["filtered_cities_bottom"] = City.objects.filter(in_home_section = True)[2:5]
        context["travel_category"] = TravelCategory.objects.all()
        context["unique_accommodations"] = Announcement.objects.filter(unique_accommodation = True)
        context["special_offers"] = SpecialOffer.objects.all()[:2]
        context['home_button_link'] = HomeButtonLink.objects.first()
        return context

def search_result(request):
    template_name = "search_result.html"
    paginate_by = 10

    check_in_date = request.GET.get("date-range-in")
    check_out_date = request.GET.get("date-range-out")
    city_name = request.GET.get("city")
    
    
    announcements = Announcement.objects.all()

    if check_in_date and check_out_date:
        check_in_date = datetime.strptime(check_in_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        check_out_date = datetime.strptime(check_out_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        announcements = announcements.filter(check_in_date__lte=check_in_date, check_out_date__gte=check_out_date)

    if city_name:
        announcements = announcements.filter(city__title__icontains=city_name)

    custom_night = request.GET.get("custom_night")
    custom_week_day = request.GET.get("custom_week_day")
    preferred_nights = request.GET.get("preferred_nights")
    paginator = Paginator(announcements, paginate_by)
    page_number = request.GET.get('page')
    announcements = paginator.get_page(page_number)
    advices = Advice.objects.all()

    context = {
        'announcements_qs': announcements,
        'popular_filters': PopularFilter.objects.all(),
        'services': Service.objects.all(),
        'property_categories': PropertyCategory.objects.all(),
        'ratings': RATING_CHOISES,
        'advices' : advices
    }

    if check_in_date and check_out_date:
        context['date-range-in'] = check_in_date
        context['date-range-out'] = check_out_date


    return render(request, template_name, context)

class AnnouncementDetailPageView(TemplateView):
    model = Announcement
    template_name = 'detail.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):
        context = super(AnnouncementDetailPageView, self).get_context_data(**kwargs)
        announcement = get_object_or_404(Announcement, slug = self.kwargs.get("slug"))
        context["announcement"] = announcement
        context["room_type"] = RoomType.objects.all()
        context["cities"] = City.objects.all()
        context["similar_announcements"] = Announcement.objects.exclude(slug = self.kwargs.get("slug")).filter(property_category = announcement.property_category, city = announcement.city)
        return context
    
    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.incrementViewCount()
        return item
    
    def post(self, request, *args, **kwargs):
        child_count = self.request.POST.get("children_number")
        adult_count = self.request.POST.get("adult_number")
        phone = self.request.POST.get("phone_number")
        email = self.request.POST.get("email")
        room_type = self.request.POST.get("room_type")
        surname = self.request.POST.get("surname")
        name = self.request.POST.get("name")
        announcement = self.request.POST.get("announcement")
        order_message = self.request.POST.get("order_message")
                
        if self.request.POST.get("check-in-date") and self.request.POST.get("check-out-date"):
            check_in_date, check_out_date = self.request.POST.get("check-in-date"), self.request.POST.get("check-out-date")
            check_in_date = datetime.strptime(check_in_date, "%m/%d/%Y")
            check_out_date = datetime.strptime(check_out_date, "%m/%d/%Y")

        # if date_range and phone and email and name and surname and announcement:
        announcement = Announcement.objects.get(id=announcement)
        total_amount = (announcement.price * int(child_count) + announcement.price * int(adult_count)) * (check_out_date - check_in_date).days
        Order.objects.create(
            announcement=announcement,
            name=name,
            surname=surname,
            phone=phone,
            mail=email,
            room_type=RoomType.objects.get(id=int(room_type)),
            from_date=check_in_date,
            to_date=check_out_date,
            little_human_count=child_count,
            big_human_count=adult_count,
            total_amount=total_amount,
            order_message = order_message
        )
        return redirect('announcement-detail', slug=self.kwargs.get('slug'))

from rest_framework.response import Response
from rest_framework.views import APIView

class PriceResponse(APIView):
    def get(self, request, *args, **kwargs):
        children_number = request.query_params.get('children_number')
        adult_number = request.query_params.get('adult_number')
        date_range = request.query_params.get('date-range')
        announcement = request.query_params.get('announcement')

        print(children_number, adult_number, date_range, announcement, '--------------------------------------------------------')

        if date_range:
            print("asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasasdfasdfasdfasdf")
            check_in_date, check_out_date = request.query_params.get("date-range").split(" - ")
            check_in_date = datetime.strptime(check_in_date, "%m/%d/%Y")
            check_out_date = datetime.strptime(check_out_date, "%m/%d/%Y")

            if check_in_date != check_out_date:
                print("------------------------------------------------------------------------------------------------------")
                if children_number and adult_number and announcement:
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    announcement = Announcement.objects.get(id=announcement)
                    price = (announcement.price * int(adult_number) + announcement.child_price * int(children_number))
                    price *= (check_out_date - check_in_date).days
                    return Response({"price": price})
                return Response({"message": "Invalid data"})
            return Response({"message": "Dates cannot equal each other"})
        
        return Response({"message": "Invalid date"})

def send_email_to_subscribers(request):
    if request.method == 'POST':
        email_subject = request.POST.get('email_subject')
        email_message = request.POST.get('email_message')

        subscribe_send_offers.delay(
            email_subject,
            email_message
        )
        
        return redirect("https://anywayanytrip.az/admin/booking/subscribe/")
    