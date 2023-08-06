
import re

from django.db.models import Q

from tecdoc.models import *
from tecdoc.constants import ADDITIONAL_CODES_MAX_LENGTH, CYRILLIC_MAP


def clean_code(text):

    result = re.sub(r'[\W_]+', '', text).lower()

    for k, v in CYRILLIC_MAP.items():
        result = result.replace(k, v)

    return result.upper()


def get_supplier(name):
    return Supplier.objects.filter(matchcode=name.upper()).first()


def get_manufacturer(name):
    return Manufacturer.objects.filter(matchcode=name.upper()).first()


def get_article_by_ean(supplier, bar_code):

    ean = ArticleEAN.objects.filter(supplier=supplier, ean=bar_code).first()

    if not ean:
        return None

    return Article.objects.filter(
        article_number=ean.article_number, supplier=supplier
    ).first()


def get_article_ean(supplier, article_number):
    return ArticleEAN.objects.filter(
        supplier=supplier, article_number=article_number
    ).first()


def get_article(supplier, clean_article_number):
    return Article.objects.filter(
        clean_article_number=clean_article_number, supplier=supplier
    ).first()


def get_crosses_text(supplier, article_number, initial=None, clean=False):

    text = initial or ''

    if not supplier or not article_number:
        return text

    oe_articles = ArticleOE.objects.filter(
        article_number=article_number,
        supplier=supplier
    )

    new_codes = set([a.oen_br for a in oe_articles])

    query = Q(article_number=article_number, supplier=supplier)

    for oe_article in oe_articles:
        query = query | Q(
            manufacturer_id=oe_article.manufacturer_id,
            oen_br=oe_article.oen_br
        )

    crosses = Cross.objects.filter(query)

    for cross in crosses:
        new_codes.add(cross.oen_br)
        new_codes.add(cross.article_number)

    new_codes |= set(text.replace('\r', '').split('\n'))

    new_codes = filter(bool, new_codes)

    if clean:
        new_codes = map(clean_code, new_codes)

    return '\n'.join(set(new_codes))


def clean_additional_codes(supplier, article_number, initial=None):
    return get_crosses_text(
        supplier,
        article_number,
        initial,
        clean=True
    )[:ADDITIONAL_CODES_MAX_LENGTH]
