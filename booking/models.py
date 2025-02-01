from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from bs4 import BeautifulSoup
from user.models import CustomUser


RATING_CHOISES = (
    (0, _('Unrated')),
    (3, _('3 Stars')),
    (4, _('4 Stars')),
    (5, _('5 Stars')),
    
)

MONTH_CHOICES = (
    (1, _('January')),
    (2, _('February')),
    (3, _('March')),
    (4, _('April')),
    (5, _('May')),
    (6, _('June')),
    (7, _('July')),
    (8, _('August')),
    (9, _('September')),
    (10, _('October')),
    (11, _('November')),
    (12, _('December')),
)

DAY_CHOICES = (
    (1, _('Week')),
    (2, _('Weekend')),
    (3, _('Custom')),
)

WEEK_DAY_CHOICES = (
    (1, _('Monday')),
    (2, _('Tuesday')),
    (3, _('Wednesday')),
    (4, _('Thursday')),
    (5, _('Friday')),
    (6, _('Saturday')),
    (7, _('Sunday')),
)

class RoomType(models.Model):
    room_type = models.CharField(max_length=255, verbose_name = 'Otağın növü',
                                 help_text='Single, Double və s.')

    def __str__(self) -> str:
        return self.room_type
    
    class Meta:
        verbose_name = "Otağın növü"
        verbose_name_plural = "Otağın növü"

class Transfer(models.Model):
    address = models.CharField(max_length=255, verbose_name = 'Ünvan')
    price = models.CharField(max_length=255, verbose_name = 'Qiyməti')

    def __str__(self) -> str:
        return self.address
    
    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfer"

class Subscribe(models.Model):
    email = models.EmailField(unique = True)
    created = models.DateTimeField(auto_now_add = True, verbose_name = 'Tarix', null = True)
    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "İzləyicilər"

class Setting(models.Model):
    site_name = models.CharField(max_length = 100, verbose_name = "Saytın adı")
    logo = models.ImageField(upload_to = 'site', verbose_name = 'Logo', null = True, blank = True)
    fav_icon = models.ImageField(upload_to = 'site', null = True, blank = True)
    reklam_title = models.CharField(max_length = 300, null = True, blank = True, verbose_name = "Reklam başlığı")
    reklam_description = models.TextField( null = True, blank = True, verbose_name = "Reklam açıqlaması")
    reklam_image = models.ImageField(upload_to = "reklam", null = True, blank = True, verbose_name = "Reklam şəkli")
    footer_text = models.TextField(null = True, blank = True, verbose_name="Footer hissəsindəki yazı")
    reserve_info = models.TextField(null = True, blank = True, verbose_name="Rezervasiya hissəsindəki yazı")
    
    class Meta:
        verbose_name = "Ayar"
        verbose_name_plural = "Ayarlar"

    def __str__(self) -> str:
        return "Ayarlar"

class ChildrenAge(models.Model):
    age = models.PositiveIntegerField(default = 0, verbose_name = 'Yas', unique = True)
    def __str__(self) -> str:
        return f'{self.age}'
    
    class Meta:
        verbose_name = "Yas"
        verbose_name_plural = "Usaq yaslari"
        ordering = ('age',)
    
class PropertyCategory(models.Model):
    title = models.CharField(max_length = 100, verbose_name = "Başlıq", unique = True)
    image = models.ImageField(upload_to = "property_categories", verbose_name = 'Şəkil', null = True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)
        verbose_name = "Əmlak növü"
        verbose_name_plural = "Əmlak növləri"

class TravelCategory(models.Model):
    title = models.CharField(max_length = 100, verbose_name = "Başlıq", unique = True)
    icon_image = models.ImageField(upload_to = 'travel_categories', verbose_name = "Şəkil", null = True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ("title",)
        verbose_name = "Səyahət Kateqoriyası"
        verbose_name_plural = "Səyahət Kateqoriyaları"

class City(models.Model):
    title = models.CharField(max_length = 100, verbose_name = "Şəhər", unique = True)
    image = models.ImageField(upload_to = 'cities', verbose_name = "Şəkil", null = True)
    in_home_section = models.BooleanField(default = False, verbose_name = "Ana səhifədə ayrı hissədə görünsün?")
    travel_category = models.ManyToManyField(TravelCategory, blank = True,related_name = "cities" , verbose_name = "Səyahət Kateqoriyası")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ("title",)
        verbose_name = "Şəhər"
        verbose_name_plural = "Şəhərlər"

class Service(models.Model):
    title = models.CharField(max_length = 50, verbose_name = "Başlıq", unique = True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Servis"
        verbose_name_plural = "Servislər"

class PopularFilter(models.Model):
    title = models.CharField(max_length = 50, verbose_name = "Başlıq", unique = True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Filter"
        verbose_name_plural = "Populyar Filterlər"

class SpecialOffer(models.Model):
    title = models.CharField(max_length = 500, verbose_name = "Başlıq")
    desktop_image = models.ImageField(upload_to = 'special_offers', verbose_name = 'Desktop şəkil', null = True)
    mobile_image = models.ImageField(upload_to = 'special_offers', verbose_name = 'Mobil şəkil', null = True)
    description = models.TextField(null = True, blank = True, verbose_name = "Açıqlama")
    button_title = models.CharField(max_length = 100, verbose_name = "Button başlığı",)
    button_linki = models.TextField(verbose_name = "Button linki", null = True, blank = True, default = '#')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Təklif"
        verbose_name_plural = "Xüsusi təkliflər"

class Announcement(models.Model):
    title = models.CharField(max_length = 500, verbose_name = "Başlıq")
    slug = models.SlugField(blank=True, null=True, unique = True)
    image = models.ImageField(upload_to = "Announcement", verbose_name = "Əsas şəkil", null = True)    
    description = RichTextField(verbose_name = "Açıqlama")
    room_count = models.PositiveIntegerField(default = 0, verbose_name = 'Otaq sayi')
    city = models.ForeignKey(City, on_delete = models.SET_NULL, null = True, blank = True,related_name = "announcements" , verbose_name = "Şəhər")
    street = models.TextField(verbose_name = "Küçə")
    rating = models.PositiveIntegerField(default = 0, null = True, verbose_name = "Reytinq",choices = RATING_CHOISES)
    distance_from_center = models.FloatField(default = 0, verbose_name = "Mərkəzdən məsafə")
    property_category = models.ForeignKey(PropertyCategory, on_delete = models.SET_NULL, null = True, blank = True,related_name = "announcements" , verbose_name = "Əmlak növü")
    is_travel_sustainable_property = models.BooleanField(default = False, verbose_name = 'Davamlı səyahət üçün?')
    whole_house_or_apartment = models.BooleanField(default = False, verbose_name = "Tam ev və ya mənzil")
    for_travel = models.BooleanField(default = False, verbose_name = "Səyahət üçün")
    unique_accommodation = models.BooleanField(default = False, verbose_name = "Unikal yaşayış yeri")
    transfer = models.ForeignKey(Transfer, on_delete=models.SET_NULL, related_name="announcements", null=True, blank=True, verbose_name = "Transfer")
    check_in_date = models.DateField(null = True, verbose_name = "Giriş tarixi")
    check_out_date = models.DateField(null = True, verbose_name = "Çıxış tarixi")
    created = models.DateTimeField(auto_now_add = True, verbose_name = "Yaradılma tarixi")
    updated = models.DateTimeField(auto_now = True, verbose_name = "Güncəllənmə tarixi")
    view_count = models.PositiveIntegerField(default = 0, verbose_name = "Görüntüləmə sayı")
    user_phone = models.CharField(max_length = 500, verbose_name = "Hotelin telefon nömrəsi", null=True, blank=True)
    user_email = models.CharField(max_length = 500, verbose_name = "Hotelin maili", null=True, blank=True)

    map_url = models.TextField(blank = True, null = True, verbose_name="Xərtinənin linki (iframe)")
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Otel"
        verbose_name_plural = "Otellər"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        soup = BeautifulSoup(self.map_url,'html.parser')
        iframe = soup.find('iframe')
        if iframe and 'src' in iframe.attrs:
            self.map_url = iframe['src']
        super(Announcement, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("announcement-detail", kwargs={"slug": self.slug})
    
    def incrementViewCount(self):
        self.view_count += 1
        self.save()


class Rules(models.Model):
    text = RichTextField(verbose_name="Qaydalar qanunlar")

    def __str__(self) -> str:
        return "Qaydalar qanunlar"
    
    class Meta:
        verbose_name = "Qaydalar qanunlar"
        verbose_name_plural = "Qaydalar qanunlar"


class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement,null = True,on_delete = models.CASCADE, verbose_name = "Elanlar", related_name = "announcement_images")
    image = models.ImageField(upload_to = "Announcement", verbose_name = "Şəkil")

    def __str__(self) -> str:
        return self.announcement.title
    
    class Meta:
        verbose_name = "Şəkil"
        verbose_name_plural = "Elan şəkilləri"
        ordering = ("id",)
        

        

class Room(models.Model):
    hotel = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="rooms", verbose_name="Otel")
    room_name = models.CharField(max_length=200, verbose_name="Otaq Adı")
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="rooms", verbose_name="Otaq Tipi")
    price = models.PositiveIntegerField(default=0, verbose_name="Qiymət")
    description = models.TextField(verbose_name="Məzmun")
    price = models.FloatField(verbose_name = "Görünən Qiymət", default=0)
    services = models.ManyToManyField(Service, related_name = "announcements", verbose_name = "Servislər", blank = True)
    popular_filters = models.ManyToManyField(PopularFilter, related_name = "announcements", verbose_name = "Populyar filterlər", blank = True)
    extra_days = models.PositiveIntegerField(default=1, verbose_name = "Ələvə günlər")
    adults_count = models.PositiveIntegerField(default = 0, verbose_name = "Böyük sayı")
    child_count = models.PositiveIntegerField(default = 0, verbose_name = "Uşaq sayı")
    children_ages = models.ManyToManyField(ChildrenAge, related_name = "announcements", verbose_name = "Usaq yaslari", blank = True)
    custom_min_day_count = models.PositiveIntegerField(default = 1, verbose_name = "Minimum qalma günü")
    custom_max_day_count = models.PositiveIntegerField(null = True, blank = True , verbose_name = "Maksimum qalma günü")
    

    def __str__(self):
        return self.room_name
    
    
    
    class Meta:
        verbose_name = "Otaq"
        verbose_name_plural = "Otaqlar"
    


class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name="images", on_delete=models.CASCADE, verbose_name="Otaq")
    image = models.ImageField(upload_to="Rooms", verbose_name="Şəkil")
    
    
    
    def __str__(self):
        return self.room.room_name
    
    
    
    class Meta:
        verbose_name = "Otaq Şəkili"
        verbose_name_plural = "Otaq Şəkilləri"
    



class RoomFeature(models.Model):
    room = models.ForeignKey(Room, related_name="features", on_delete=models.CASCADE, verbose_name="Otaq")
    title = models.CharField(max_length=100, verbose_name="Özəllik")



    def __str__(self):
        return self.room.room_name
    
    
    
    class Meta:
        verbose_name = "Otaq Özəlliyi"
        verbose_name_plural = "Otaq Özəllikləri"
        
        

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders", verbose_name="Müştəri")
    announcement = models.ForeignKey(Announcement, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders", verbose_name="Otaq")
    name = models.CharField(max_length = 100, verbose_name = "Adı")
    surname = models.CharField(max_length = 100, verbose_name = "Soy Adı")
    mail = models.CharField(max_length = 100, verbose_name = "Maili", null=True, blank=True)
    phone = models.CharField(max_length = 50, verbose_name = "Telefon nömrəsi")
    from_date = models.DateField(verbose_name = "Başlanğıc tarixi")
    to_date = models.DateField(verbose_name = "Bitiş tarixi")
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    order_message = models.TextField(verbose_name="Müştərinin şərhi", null=True, blank=True)
    total_amount = models.FloatField(verbose_name = "Ödəniləcək məbləğ")
    paid_amount = models.FloatField(verbose_name = "Ödənilən məbləğ", null=True, blank=True)

    is_read = models.BooleanField(verbose_name="Baxılıb?", default=False)
    who_read = models.CharField(verbose_name="Kim baxıb?", max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"
    
    class Meta:
        verbose_name = "Sifariş"
        verbose_name_plural = "Sifarişlər"
        ordering = ("-id",)




class HomeButtonLink(models.Model):
    title = models.CharField(max_length = 100, verbose_name = "Başlıq", null=True, blank=True)
    link = models.URLField(max_length=600, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Ana Səhifədə olan buttonun linki"
        
        
class Advice(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tövisyyələr")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Tövisyyələr"