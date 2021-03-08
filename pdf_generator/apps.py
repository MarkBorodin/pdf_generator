from django.apps import AppConfig


class PdfGeneratorConfig(AppConfig):
    name = 'pdf_generator'

    def ready(self):
        import pdf_generator.signals  # noqa
