# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.utils.translation import gettext_lazy as _

# from .models import Contacting

# @receiver(post_save, sender=Contacting)
# def send_contact_email(sender, instance, created, **kwargs):
#     def send_client_email(fm='no-reply@emarches.com'):
#         email_body = _('Thank you for contacting us.') + '\n'
#         email_body += _('Your message was received and our team will reach out to you as soon as possible.') + '\n\n'
#         email_body += _('Replies to this message will be ignored.') + '\n'
#         email_subject = _('Message submitted on') + ' eMarches.com'
#         return send_mail(email_subject, email_body, fm, [f'{instance.email}'])

#     def send_crm_email(fm='contact@emarches.com'):
#         email_body = _('Name') + f' : { instance.name }\n'
#         email_body += _('Email') + f' : { instance.email }\n'
#         email_body += _('Subject') + f' : { instance.subject }\n'
#         email_body += _('Message') + f' : { instance.message }\n'
#         email_body += _('Prefferred contact method') + f' : { instance.contact_method }\n'
#         email_body += _('Subscribe to Newsletter') + f' : { instance.subscribe_newsletter } \n'
#         email_body += _('Subscribe to Offers') + f' : { instance.subscribe_promotions } \n'
#         email_body += _('Submitted on') + f' : { instance.date_submitted } \n'
#         email_subject = _('New Contact on') + ' eMarches.com'
#         return send_mail(email_subject, email_body, fm, ['a.bouhou@emarches.com'])

#     if created:
#         # 1. Send an email to the client
#         n = send_client_email()
#         print(f'\n\n========================= send_client_email() to <{instance.email}> returned : {n} \n\n')

#         # 2. Send an email to the CRM person
#         # send_crm_email()