from django.apps import AppConfig


class TrillianConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trillian'

    def ready(self):
        from .models import Trillian
        from accounts.models import Profile
        self.service_log = Trillian()
        profiles = Profile.objects.all()
        for profile in profiles:
            self.service_log.allowed_servers[profile.user.username] = profile.public_key
        print(self.service_log.allowed_servers)
