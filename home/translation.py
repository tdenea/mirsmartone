from django.utils import translation
    
class TranslatedField(object):
    def __init__(self, field, it_field, de_field, fr_field, es_field):
        self.field = field
        self.it_field = it_field
        self.de_field = de_field
        self.fr_field = fr_field
        self.es_field = es_field
    def __get__(self, instance, owner):
        if translation.get_language() == 'it' and getattr(instance, self.it_field):
            return getattr(instance, self.it_field)
        elif translation.get_language() == 'de' and getattr(instance, self.de_field):
            return getattr(instance, self.de_field)
        elif translation.get_language() == 'fr' and getattr(instance, self.fr_field):
            return getattr(instance, self.fr_field)
        elif translation.get_language() == 'es' and getattr(instance, self.es_field):
            return getattr(instance, self.es_field)
        else:
            return getattr(instance, self.field)

