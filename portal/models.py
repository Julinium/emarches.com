
import uuid, os
from django.db import models
from datetime import date, datetime
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from base.storage import OverwriteStorage


def rename_avatar(instance, filename):
    ext = filename.split('.')[-1]  # Get file extension
    new_filename = f'avatar-{instance.user.id}.{ext}'
    return os.path.join('users/avatars/', new_filename)


class Acheteur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    acro = models.CharField(max_length=63, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    secteur = models.CharField(max_length=63, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'base_acheteur'
                
    def __str__(self):
        return self.nom


class Agrement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    label = models.CharField(max_length=63, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'base_agrement'
                
    def __str__(self):
        return self.nom


class Categorie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    label = models.CharField(max_length=15, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'base_categorie'
                
    def __str__(self):
        return self.nom


class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True)
    date_limite_depot = models.DateTimeField(blank=True, null=True)
    cancelled = models.BooleanField(blank=True, null=True, default=False)
    reference = models.CharField(max_length=255, blank=True, null=True)
    total_estimation = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    caution_provisoire = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    nombre_lots = models.IntegerField(blank=True, null=True)
    objet = models.TextField(blank=True, null=True)
    lieu_execution = models.CharField(max_length=511, blank=True, null=True)
    reponse_electronique = models.CharField(max_length=127, blank=True, null=True)
    prix_acquisition_plans = models.FloatField(blank=True, null=True)
    retrait_dossiers_adresse = models.TextField(blank=True, null=True)
    depot_offres_adresse = models.TextField(blank=True, null=True)
    ouverture_plis_adresse = models.TextField(blank=True, null=True)
    contact_nom = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    contact_tel = models.CharField(max_length=255, blank=True, null=True)
    contact_fax = models.CharField(max_length=255, blank=True, null=True)
    portal_id = models.CharField(max_length=31, blank=True, null=True)
    portal_link = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    acheteur_public = models.ForeignKey(Acheteur, on_delete=models.DO_NOTHING, db_column='acheteur_public', blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.DO_NOTHING, db_column='categorie', blank=True, null=True)
    mode_passation = models.ForeignKey('Mode', on_delete=models.DO_NOTHING, db_column='mode_passation', blank=True, null=True)
    procedure_annonce = models.ForeignKey('Procedure', on_delete=models.DO_NOTHING, db_column='procedure_annonce', blank=True, null=True)
    type_annonce = models.ForeignKey('Type', on_delete=models.DO_NOTHING, db_column='type_annonce', blank=True, null=True)
    portal_size = models.CharField(max_length=31, blank=True, null=True)
    update_me = models.BooleanField(blank=True, null=True, default=False)
    # update_my_files = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        db_table = 'base_consultation'

    def __str__(self):
        n = self.nombre_lots
        nl = f'{n}-Lot'
        if n > 1 : nl += 's'
        return f'[{nl}][{self.reference}]: {self.objet}'
              
    @property
    def remaining_days(self):
        rays = self.date_limite_depot.date() - date.today()
        return rays.days
    
    @property
    def displayed_days(self):
        rays = date.today() - self.date_publication.date()
        return rays.days


class ConsultationDomaine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='domaines', blank=True, null=True)
    domaine = models.ForeignKey('Domaine', on_delete=models.CASCADE, related_name='consultations', blank=True, null=True)

    class Meta:
        db_table = 'base_consultation_domaine'


class Domaine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    acro = models.CharField(max_length=15, blank=True, null=True)
    label = models.CharField(max_length=15, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    categorie = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'base_domaine'
                
    def __str__(self):
        return self.nom


class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField()
    start_date = models.DateTimeField()
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'base_evaluation'


class Lot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lot_number = models.IntegerField()
    objet = models.TextField()
    description = models.TextField(blank=True, null=True)
    estimation = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    caution_provisoire = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    reserve_pme = models.BooleanField(blank=True, null=True)
    echantillons = models.JSONField()
    reunions = models.JSONField()
    visites = models.JSONField()
    variante = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, db_column='categorie', blank=True, null=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, db_column='consultation', blank=True, null=True)

    class Meta:
        db_table = 'base_lot'
        ordering = ['lot_number']
        
    def __str__(self):
        return f'[{self.lot_number}][E={self.estimation}]: {self.objet}'


class LotAgrement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agrement = models.ForeignKey(Agrement, on_delete=models.CASCADE, related_name='lots', blank=True, null=True)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='agrements', blank=True, null=True)

    class Meta:
        db_table = 'base_lot_agrement'


class LotQualification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='qualifications', blank=True, null=True)
    qualification = models.ForeignKey('Qualification', on_delete=models.CASCADE, related_name='lots', blank=True, null=True)

    class Meta:
        db_table = 'base_lot_qualification'


class Mode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    acro = models.CharField(max_length=15, blank=True, null=True)
    label = models.CharField(max_length=15, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'base_mode'
                
    def __str__(self):
        return self.nom


class Procedure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    acro = models.CharField(max_length=15, blank=True, null=True)
    label = models.CharField(max_length=15, blank=True, null=True)
    ouvert = models.CharField(max_length=15, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'base_procedure'

    def __str__(self):
        return self.nom


class Profile(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active              = models.BooleanField(null=True, default=True)
    company             = models.CharField(max_length=255, blank=True,default='')
    ice                 = models.CharField(max_length=64, blank=True, default='')
    date_est            = models.DateField(blank=True, null=True)
    city                = models.CharField(max_length=64, blank=True, default='')
    country             = models.CharField(max_length=64, blank=True, default='')
    role                = models.CharField(max_length=64, blank=True, default='')
    sector              = models.CharField(max_length=128, blank=True, default='')
    phone               = models.CharField(max_length=255, blank=True, default='')
    email               = models.CharField(max_length=255, blank=True, default='')
    whatsapp            = models.CharField(max_length=255, blank=True, default='')
    faximili            = models.CharField(max_length=255, blank=True, default='')
    website             = models.CharField(max_length=128, blank=True, default='')
    note                = models.CharField(max_length=1024, blank=True, default='')
    guest               = models.BooleanField(default=False, blank=True)
    avatar              = models.ImageField(upload_to=rename_avatar, storage=OverwriteStorage(), default='users/avatars/default.png')
    pref_order_by       = models.CharField(max_length=64, blank=True, default='-dl')
    pref_future_days    = models.IntegerField(blank=True, default=30)
    pref_items_per_page = models.IntegerField(blank=True, default=25)
    pref_show_past      = models.BooleanField(default=False)
    user                = models.OneToOneField(User, on_delete=models.CASCADE) # storage=OverwriteStorage()

    class Meta:
        db_table = 'base_profile'

    def __str__(self):
        return f'{self.user.username}'


class ProfileAgrements(models.Model):
    # id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='agrements')
    agrement = models.ForeignKey(Agrement, on_delete=models.CASCADE, related_name='profiles')

    class Meta:
        db_table = 'base_profile_agrements'
        unique_together = (('profile', 'agrement'),)


class ProfileDomains(models.Model):
    # id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='domains')
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE, related_name='profiles')

    class Meta:
        db_table = 'base_profile_domains'
        unique_together = (('profile', 'domaine'),)


class ProfileFavCon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation = models.CharField(max_length=512, blank=True, null=True)
    date_faved = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    note_faved = models.CharField(max_length=512, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', related_name='favs', blank=True, null=True)

    class Meta:
        db_table = 'base_profile_fav_con'


class ProfileQualifications(models.Model):
    # id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='qualifications')
    qualification = models.ForeignKey('Qualification', on_delete=models.CASCADE, related_name='profiles')

    class Meta:
        db_table = 'base_profile_qualifications'
        unique_together = (('profile', 'qualification'),)


class Qualification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    acro = models.CharField(max_length=15, blank=True, null=True)
    classe = models.CharField(max_length=1, blank=True, null=True)
    label = models.CharField(max_length=63, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    secteur = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        db_table = 'base_qualification'
                
    def __str__(self):
        return self.nom


class Reglage(models.Model):
    # id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cons_last_update = models.DateTimeField(blank=True, null=True)
    bdcs_last_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'base_reglage'


class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    label = models.CharField(max_length=15, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'base_type'
                
    def __str__(self):
        return self.nom


class UserDownloadFile(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation    = models.CharField(max_length=512, blank=True, null=True)
    user_agent      = models.CharField(max_length=512, blank=True, null=True)
    user_ip         = models.CharField(max_length=32, blank=True, null=True)
    file_name       = models.CharField(max_length=512, blank=True, null=True)
    file_size       = models.IntegerField(blank=True, null=True)
    date_started    = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='user', related_name='downloads', blank=True, null=True)

    class Meta:
        db_table            = 'base_user_download_file'
        verbose_name        = _("Download DCE")
        verbose_name_plural = _("Downloads DCE")
        
    @property
    def related(self):
        try: return Consultation.objects.filter(portal_id=self.consultation).first()
        except AttributeError: return None
    
    @property
    def related_id(self):
        return self.related.id if self.related else None


class Plan(models.Model):
    id                          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active                      = models.BooleanField()
    name                        = models.CharField(max_length=255, blank=True, null=True)
    test_days                   = models.IntegerField(default=15)
    max_items_daily             = models.IntegerField(default=25)
    max_items_monthly           = models.IntegerField(default=250)
    max_links_daily             = models.IntegerField(default=25)
    max_links_monthly           = models.IntegerField(default=250)
    max_downloads_daily         = models.IntegerField(default=25)
    max_downloads_monthly       = models.IntegerField(default=250)
    max_favos_simultanous       = models.IntegerField(default=10)
    max_favos_daily             = models.IntegerField(default=25)
    max_favos_monthly           = models.IntegerField(default=250)
    email_new_items_days        = models.IntegerField(default=7)
    email_list_of_new_items     = models.BooleanField()
    refine_by_category          = models.BooleanField()
    refine_by_lots_count        = models.BooleanField()
    refine_by_sectors           = models.BooleanField()
    refine_by_region            = models.BooleanField()
    refine_by_domains           = models.BooleanField()
    refine_by_qualifications    = models.BooleanField()
    refine_by_agrements         = models.BooleanField()
    support_phone_direct        = models.BooleanField()
    support_whatsapp            = models.BooleanField()
    support_email               = models.BooleanField(default=True)

    class Meta:
        db_table = 'base_plan'

    def __str__(self):
        return self.name


class Payment(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount          = models.DecimalField(max_digits=16, decimal_places=2)
    made_date       = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    made_mean       = models.CharField(max_length=255, blank=True, null=True)
    made_reference  = models.CharField(max_length=255, blank=True, null=True)
    verified        = models.BooleanField()
    info_verified   = models.CharField(max_length=255, blank=True, null=True)
    refunded        = models.BooleanField()
    info_refunded   = models.CharField(max_length=255, blank=True, null=True)
    profile         = models.ForeignKey('Profile', null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'base_payment'

    def __str__(self):
        return f'{self.profile}:{self.amount}'


class Subscription(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active      = models.BooleanField(default=True)
    start_date  = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    end_date    = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    payment     = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    plan        = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'base_subscription'

    def __str__(self):
        return f'{self.plan}:{self.payment}:{self.start_date}-{self.end_date}'


class Preferences(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # active      = models.BooleanField(default=True)
    # start_date  = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    # end_date    = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    # payment     = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    # plan        = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    
    # profile
    # last_edited
    # pref_language
    # pref_timezone
    # tenders_order_by
    # favs_order_by
    # items_per_page
    # welcome_view
    # show_header_images
    # confirm_downloads


    class Meta:
        db_table = 'base_user_settings'

    # def __str__(self):
    #     return f'{self.plan}:{self.payment}:{self.start_date}-{self.end_date}'


