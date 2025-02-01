from . import models
from modeltranslation.translator import TranslationOptions,register

@register(models.PropertyCategory)
class PropertyCategoryTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(models.TravelCategory)
class TravelCategoryTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(models.Transfer)
class TransferTranslationOptions(TranslationOptions):
    fields = ('address', )

@register(models.RoomType)
class RoomTypeTranslationOptions(TranslationOptions):
    fields = ('room_type', )

@register(models.Rules)
class RulesTranslationOptions(TranslationOptions):
    fields = ('text', )

@register(models.City)
class CityTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(models.Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', )

@register(models.PopularFilter)
class PopularFilterOptions(TranslationOptions):
    fields = ('title', )

@register(models.Announcement)
class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'street')

@register(models.SpecialOffer)
class SpecialOfferTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'button_title')

@register(models.Setting)
class SettingTranslationOptions(TranslationOptions):
    fields = ('site_name', 'reklam_title', 'reklam_description', 'footer_text', 'reserve_info')