from django.contrib import admin
from django.contrib.admin import TabularInline
from modeltranslation.admin import TranslationAdmin
from django.core.mail import send_mail
from . import models

admin.site.register(models.ChildrenAge)
admin.site.register(models.HomeButtonLink)
admin.site.register(models.Advice)


class RoomImagesInline(admin.TabularInline):
    model = models.RoomImage
    extra = 1
    
    
class RoomFeaturesInline(admin.TabularInline):
    model = models.RoomFeature
    extra = 1
    
    
    

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name','hotel', 'type', 'price')
    inlines = [RoomImagesInline, RoomFeaturesInline]
    

admin.site.register(models.Room, RoomAdmin)




class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created')
    actions = ['send_email_to_subscribers']

    def send_email_to_subscribers(self, request, queryset):
        subject = "Your Subject Here"
        message = "Your Message Here"
        from_email = "your@example.com"
        recipient_list = [subscriber.email for subscriber in queryset]

        send_mail(subject, message, from_email, recipient_list)
        self.message_user(request, f"Emails sent to {len(queryset)} subscribers.")

    send_email_to_subscribers.short_description = "Send email to selected subscribers"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['page_type'] = 'subscribe'
        
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(models.Subscribe, SubscriptionAdmin)

@admin.register(models.PropertyCategory)
class PropertyCategoryAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(models.Transfer)
class TransferAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(models.RoomType)
class RoomTypeAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    
@admin.register(models.Setting)
class SettingAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
@admin.register(models.TravelCategory)
class TravelCategoryAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(models.City)
class CityAdmin(TranslationAdmin):

    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(models.Service)
class ServiceAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(models.SpecialOffer)
class SpecialOfferAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    def has_add_permission(self, request, obj=None):
        if models.SpecialOffer.objects.count() < 2:
            return True
        return False

@admin.register(models.PopularFilter)
class PopularFilterAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(models.Rules)
class RulesAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class AnnouncementImageInline(TabularInline):
    extra = 1
    model = models.AnnouncementImage


@admin.register(models.Announcement)
class AnnouncementAdmin(TranslationAdmin):
    inlines = (AnnouncementImageInline,)
    list_display = ('title', 'city', 'user_phone', 'user_email', 'property_category', 'rating', 'unique_accommodation',)
    list_editable = ('unique_accommodation',)
    fields = ('title', 'image', 'description', 'room_count', 'city', 'street', 'rating', 'transfer', 'distance_from_center', 
              'property_category', 'is_travel_sustainable_property', 'whole_house_or_apartment', 
              'for_travel', 'unique_accommodation', 'view_count' , 'map_url', 'user_phone', 'user_email', 'created', 'updated', 'check_in_date', 'check_out_date')
    
    readonly_fields = ('view_count', 'created', 'updated',)
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'name', 'surname', 'phone', 'mail', 'from_date', 'to_date', 'total_amount', 'paid_amount')
    list_editable = ('paid_amount',)
    readonly_fields = ('who_read', )
    
    def save_model(self, request, obj, form, change):
        if change:
            original_obj = self.model.objects.get(pk=obj.pk)
            if obj.is_read != original_obj.is_read:
                if not obj.is_read:
                    obj.who_read = request.user.username
                    obj.is_read = True
        obj.save()