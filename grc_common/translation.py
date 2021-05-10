from modeltranslation.translator import register, TranslationOptions
from grc_common.models import ProfessionalArea, Area, Industry, Language, Specialization


@register(Area)
class AreaTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProfessionalArea)
class ProfessionalAreaTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Industry)
class IndustryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Specialization)
class SpecializationTranslationOptions(TranslationOptions):
    fields = ('name',)
