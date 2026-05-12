# exam/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate

def init_test_data(sender, **kwargs):
    from exam.views import init_test_data as _init
    _init()

class ExamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exam'

    def ready(self):
        post_migrate.connect(init_test_data, sender=self)