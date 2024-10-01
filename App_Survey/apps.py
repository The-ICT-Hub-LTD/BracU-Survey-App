from django.apps import AppConfig


class AppSurveyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_Survey'

    def ready(self):
        import App_Survey.signals
