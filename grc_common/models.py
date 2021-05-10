from django.db import models


# Create your models here.
class ProfessionalArea(models.Model):
    """
        Model contains professional area info.
        Required:
            - is_visible
    """

    name = models.CharField(max_length=255, null=True)
    is_visible = models.BooleanField(default=True)


class Specialization(models.Model):
    """
        Model contains specialization info.
        Required:
            - is_visible
            - professional_area
    """

    name = models.CharField(max_length=255, null=True)
    professional_area = models.ForeignKey(ProfessionalArea, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)


class Industry(models.Model):
    """
        Model contains industry info.
        Required:
            - is_hidden
    """

    name = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    is_hidden = models.BooleanField(default=False)


class Language(models.Model):
    """
        Model contains language info.
    """

    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=255, null=True)


class Area(models.Model):
    """
        Model contains area info.
        Required:
            - type
    """

    name = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    # ValuedEnum<Integer> {
    # OTHER(0),
    # COUNTRY(1),
    # OKRUG(2),
    # OBLAST(3),
    # OBLAST_CENTRE(5),
    # RAION_CENTRE(6),
    # CITY(7);
    # }
    type = models.IntegerField(choices=[])


class KeySkill(models.Model):
    """
        Model contains key skill info.
    """

    name = models.CharField(max_length=255)
    searchable = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    general = models.BooleanField(default=False)


class Currency(models.Model):
    """
        Model contains currency info.
        Required:
            - code
            - rate
            - updated_at
    """
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=3)
    rate = models.FloatField()
    updated_at = models.DateTimeField()


class Account(models.Model):
    """
        This model contains account info.
        Required:
            - disabled
            - created_at
            - updated_at
            - primary_email
            - disabled
            - last_name
    """

    disabled = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    primary_email = models.TextField()
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)


class User(models.Model):
    """
        This model contains users info.
        Required:
            - created_at
            - area
            - account
            - language
    """

    # 0 - applicant
    # 1 - employer
    created_at = models.DateTimeField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)


class Company(models.Model):
    """
        This model contains company info.
        Required:
            - creation_time
            - area
            - name
            - category
    """

    manager_id = models.IntegerField(null=True)
    creation_time = models.DateTimeField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    category = models.IntegerField()
    url = models.CharField(max_length=255, null=True)
    small_logo_url = models.CharField(max_length=255, null=True)
    state = models.IntegerField(null=True)


class CompanyIndustry(models.Model):
    """
        This model contains company industry info.
        Required:
            - company
            - industry
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)


class CompanyManager(models.Model):
    """
        This model contains company industry info.
        Required:
            - user
            - company
            - type
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Есть одна роль ГКЛ (главное контактное лицо) - employer_manager.type=0
    #
    # Есть еще премодератор employer_manager.type=2
    type = models.IntegerField()
    phone = models.TextField(null=True)
    additional_phone = models.TextField(null=True)
