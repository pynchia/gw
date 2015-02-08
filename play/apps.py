from django.apps import AppConfig


class PlayConfig(AppConfig):
    name = 'play'

    def ready(self):
        import play.signals
        #  mysignals = self.get_model('Player')

