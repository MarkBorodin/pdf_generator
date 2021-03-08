from django.db.models.signals import post_save
from django.dispatch import receiver

from pdf_generator.models import Designation, Page, Phase


@receiver(post_save, sender=Phase)
def phase_number(sender, instance, created, **kwargs):
    if created:
        phases_num = Phase.objects.filter(
            page__in=Page.objects.filter(offer=instance.page.offer)
        ).count()
        instance.number = phases_num
        instance.save()


@receiver(post_save, sender=Designation)
def designations_number(sender, instance, created, **kwargs):
    if created:
        designations_num = Designation.objects.filter(
            phase=instance.phase
        ).count()
        instance.number = designations_num
        instance.save()
