
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from tecdoc.constants import ADDITIONAL_CODES_MAX_LENGTH


class AdditionalCodesField(models.TextField):

    def __init__(
            self,
            verbose_name=_('Additional codes'),
            blank=True,
            db_index=True,
            max_length=ADDITIONAL_CODES_MAX_LENGTH,
            *args,
            **kwargs):

        super().__init__(
            verbose_name=verbose_name,
            blank=blank,
            db_index=db_index,
            max_length=max_length,
            *args,
            **kwargs)


class Tecdoc(models.Model):

    article_number = models.CharField(max_length=100, blank=True, null=True)

    supplier_id = models.IntegerField(blank=True, null=True)

    additional_codes = AdditionalCodesField()

    def has_article(self):
        return bool(self.article_number and self.supplier_id)

    def tecdoc_cell(self):
        try:
            return render_to_string('tecdoc/cell.html', {'object': self})
        except Exception:
            return ''

    tecdoc_cell.admin_order_field = 'supplier_id'
    tecdoc_cell.short_description = _('Tecdoc')

    class Meta:
        abstract = True


class Manufacturer(models.Model):

    description = models.CharField(max_length=255)

    matchcode = models.CharField(max_length=255)

    is_passenger_car = models.BooleanField(db_column='ispassengercar')

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'manufacturers'


class Supplier(models.Model):

    description = models.CharField(max_length=255)

    matchcode = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'suppliers'


class ArticleAttribute(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        db_column='supplierid')

    article_number = models.CharField(
        max_length=255,
        db_column='datasupplierarticlenumber',
        primary_key=True)

    description = models.TextField(
        db_column='description')

    value = models.TextField(
        db_column='displayvalue')

    def __str__(self):
        return self.article_number

    class Meta:
        db_table = 'article_attributes'


class ArticleEAN(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        db_column='supplierid')

    article_number = models.CharField(
        max_length=255,
        db_column='datasupplierarticlenumber',
        primary_key=True)

    ean = models.CharField(max_length=255)

    def __str__(self):
        return self.ean

    class Meta:
        db_table = 'article_ean'


class Cross(models.Model):

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        db_column='manufacturerId')

    oen_br = models.CharField(
        max_length=255,
        db_column='OENbr')

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        db_column='SupplierId')

    article_number = models.CharField(
        max_length=255,
        db_column='PartsDataSupplierArticleNumber',
        primary_key=True)

    def __str__(self):
        return self.article_number

    class Meta:
        db_table = 'article_cross'


class Article(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        db_column='supplierId')

    article_number = models.CharField(
        max_length=255,
        db_column='DataSupplierArticleNumber',
        primary_key=True)

    clean_article_number = models.CharField(
        max_length=255,
        db_column='FoundString')

    description = models.TextField(
        db_column='NormalizedDescription')

    def get_attributes(self):
        return ArticleAttribute.objects.filter(
            article_number=self.article_number,
            supplier_id=self.supplier_id)

    def get_crosses(self):
        return ArticleAttribute.objects.filter(
            article_number=self.article_number,
            supplier_id=self.supplier_id)

    def get_ean_codes(self):
        return ArticleEAN.objects.filter(article_number=self.article_number)

    def get_images(self):
        return Image.objects \
         .filter(
            article_number=self.article_number,
            supplier_id=self.supplier_id)

    def __str__(self):
        return self.article_number

    class Meta:
        db_table = 'articles'


class ArticleOE(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        db_column='supplierId')

    article_number = models.CharField(
        max_length=255,
        db_column='DataSupplierArticleNumber',
        primary_key=True)

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        db_column='manufacturerId')

    oen_br = models.CharField(
        max_length=255,
        db_column='OENbr')

    def __str__(self):
        return self.article_number

    class Meta:
        db_table = 'article_oe'


class CarModel(models.Model):

    description = models.TextField()

    full_description = models.TextField(db_column='fulldescription')

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        db_column='manufacturerid')

    def __str__(self):
        return self.full_description

    class Meta:
        db_table = 'models'


class PassangerCar(models.Model):

    model = models.ForeignKey(
        CarModel,
        on_delete=models.PROTECT,
        db_column='modelid')

    description = models.TextField()

    full_description = models.TextField(db_column='fulldescription')

    def __str__(self):
        return self.full_description

    class Meta:
        db_table = 'passanger_cars'


class ArticleLink(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        db_column='supplierId')

    article_number = models.CharField(
        max_length=255,
        db_column='DataSupplierArticleNumber',
        primary_key=True)

    link_type = models.CharField(
        max_length=255,
        db_column='linkageTypeId')

    link_id = models.IntegerField(
        db_column='linkageId'
    )

    def __str__(self):
        return self.article_number

    class Meta:
        db_table = 'article_li'


class Image(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        db_column='supplierId')

    article_number = models.CharField(
        max_length=255,
        db_column='DataSupplierArticleNumber')

    picture_name = models.CharField(
        max_length=255,
        db_column='PictureName',
        primary_key=True)

    def __str__(self):
        return self.picture_name

    class Meta:
        db_table = 'article_images'
