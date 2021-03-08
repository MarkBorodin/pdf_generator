import datetime


from django.db.models.signals import post_save
from django.dispatch import receiver


#
# @receiver(post_save, sender=TestResult)
# def update_rating(sender, instance, created, **kwargs):
#     if instance.state == TestResult.STATE.FINISHED:
#         user = instance.user
#         current_rating = user.rating
#         new_rating = current_rating + instance.points()
#         user.rating = new_rating
#         user.save()
from pdf_generator.models import Phase, Page, Offer, Designation


@receiver(post_save, sender=Phase)
def phase_number(sender, instance, created, **kwargs):
    if created:
        phases_num = Phase.objects.filter(
            page=instance.page
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
