import uuid

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from portal.models import Consultation


class Favorisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation = models.CharField(max_length=512, blank=True, null=True)
    date_faved = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', related_name='favorisation', blank=True, null=True)
    ip_address = models.CharField(max_length=48, blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'crm_favorisation'
    
    
    @property
    def related(self):
        try: return Consultation.objects.filter(portal_id=self.consultation).first()
        except AttributeError: return None


class Unfavorisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation = models.CharField(max_length=512, blank=True, null=True)
    date_unfaved = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', related_name='unfavorisation', blank=True, null=True)
    ip_address = models.CharField(max_length=48, blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'crm_unfavorisation'
    
    
    @property
    def related(self):
        try: return Consultation.objects.filter(portal_id=self.consultation).first()
        except AttributeError: return None


class Contacting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    replied = models.BooleanField(blank=True, null=True, default=False)
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    subject = models.CharField(max_length=256, blank=True, null=True)
    message = models.CharField(max_length=1024, blank=True, null=True)
    contact_method = models.CharField(max_length=64, blank=True, null=True)
    subscribe_newsletter = models.BooleanField(blank=True, null=True, default=False)
    subscribe_promotions = models.BooleanField(blank=True, null=True, default=False)
    date_submitted = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    actions = models.CharField(max_length=512, blank=True, default='', null=True)
    results = models.CharField(max_length=512, blank=True, default='', null=True)
    notes = models.CharField(max_length=1024, blank=True, default='', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', related_name='contacting', blank=True, null=True)
    ip_address = models.CharField(max_length=48, blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'crm_contacting'

    def __str__(self):
        return f'{ self.name } + { self.subject }'


class Spamming(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    honeypot = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    subject = models.CharField(max_length=256, blank=True, null=True)
    message = models.CharField(max_length=1024, blank=True, null=True)
    contact_method = models.CharField(max_length=64, blank=True, null=True)
    subscribe_newsletter = models.BooleanField(blank=True, null=False)
    subscribe_promotions = models.BooleanField(blank=True, null=False)
    date_submitted = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', related_name='spamming', blank=True, null=True)
    ip_address = models.CharField(max_length=48, blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'crm_spamming'


class SearchQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    query_full_url  = models.CharField(max_length=255, blank=True, null=True)
    query_hostname  = models.CharField(max_length=255, blank=True, null=True)
    query_full_path = models.CharField(max_length=255, blank=True, null=True)
    query_language  = models.CharField(max_length=15, blank=True, null=True)

    query_object = models.CharField(max_length=512, blank=True, null=True)
    query_reference = models.CharField(max_length=512, blank=True, null=True)
    query_estimate_min = models.CharField(max_length=24, blank=True, null=True)
    query_estimate_max = models.CharField(max_length=24, blank=True, null=True)
    query_category = models.CharField(max_length=512, blank=True, null=True)
    query_procedure = models.CharField(max_length=512, blank=True, null=True)
    query_deadline_min = models.CharField(max_length=10, blank=True, null=True)
    query_deadline_max = models.CharField(max_length=10, blank=True, null=True)
    query_published_min = models.CharField(max_length=10, blank=True, null=True)
    query_published_max = models.CharField(max_length=10, blank=True, null=True)
    query_client = models.CharField(max_length=64, blank=True, null=True)
    query_execution_location = models.CharField(max_length=64, blank=True, null=True)

    query_electronic_response = models.CharField(max_length=64, blank=True, null=True)
    query_single_lot_only = models.BooleanField(blank=True, null=True, default=False)
    query_reserved_to_smb = models.BooleanField(blank=True, null=True, default=False)
    query_results_per_page = models.CharField(max_length=512, blank=True, null=True)
    query_order_by = models.CharField(max_length=512, blank=True, null=True)

    date_submitted = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    results_count = models.IntegerField(blank=True, null=True, default=0)
    updated_since = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', related_name='search_query', blank=True, null=True)
    user_agent = models.CharField(max_length=512, blank=True, null=True)
    ip_address   = models.CharField(max_length=48, blank=True, null=True)
    ip_country   = models.CharField(max_length=24, blank=True, null=True)
    ip_city      = models.CharField(max_length=24, blank=True, null=True)
    ip_latitude  = models.CharField(max_length=16, blank=True, null=True)
    ip_longitude = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        db_table = 'crm_search_query'

    def __str__(self):
        if self.query_full_url: return self.query_full_url
        return f'SearchQuery_{ self.date_submitted }'

    @property
    def queryterms(self):
        q = ''
        if self.query_object: q += f' object={self.query_object}'
        if self.query_reference: q += f' reference={self.query_reference}'
        if self.query_estimate_min: q += f' estimate_min={self.query_estimate_min}'
        if self.query_estimate_max: q += f' estimate_max={self.query_estimate_max}'
        # if self.query_category: q += f' category={self.query_category}'
        # if self.query_procedure: q += f' procedure={self.query_procedure}'
        if self.query_deadline_min: q += f' deadline_min={self.query_deadline_min}'
        if self.query_deadline_max: q += f' deadline_max={self.query_deadline_max}'
        if self.query_published_min: q += f' published_min={self.query_published_min}'
        if self.query_published_max: q += f' published_max={self.query_published_max}'
        if self.query_client: q += f' client={self.query_client}'
        if self.query_execution_location: q += f' execution_location={self.query_execution_location}'
        # if self.query_electronic_response: q += f' electronic_response={self.query_electronic_response}'
        if self.query_single_lot_only: q += f' single_lot_only={self.query_single_lot_only}'
        if self.query_reserved_to_smb: q += f' reserved_to_smb={self.query_reserved_to_smb}'
        # if self.query_results_per_page: q += f' results_per_page={self.query_results_per_page}'
        # if self.query_order_by: q += f' order_by={self.query_order_by}'
    
        return q



# TODO: Login, Logout, Consultation Details, Lists Downloads, Pages Vues, Bidding Link clicks