# import datetime
#
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
#
# #
# # @receiver(post_save, sender=TestResult)
# # def update_rating(sender, instance, created, **kwargs):
# #     if instance.state == TestResult.STATE.FINISHED:
# #         user = instance.user
# #         current_rating = user.rating
# #         new_rating = current_rating + instance.points()
# #         user.rating = new_rating
# #         user.save()
# from pdf_generator.models import Phase, Page, Offer
#
#
# @receiver(post_save, sender=Phase)
# def phase_num(sender, instance, created, **kwargs):
#     if created:
#         phases = Phase.objects.filter(
#             page=instance.page
#         ).count()
#         instance.number = int(phases) + 1
#         instance.save()
