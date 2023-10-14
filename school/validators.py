from rest_framework.serializers import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        true_url = 'https://www.youtube.com/'
        tmp_val = dict(value).get(self.field)
        if not tmp_val.startswith(true_url):
            raise ValidationError('Неправильная ссылка')
