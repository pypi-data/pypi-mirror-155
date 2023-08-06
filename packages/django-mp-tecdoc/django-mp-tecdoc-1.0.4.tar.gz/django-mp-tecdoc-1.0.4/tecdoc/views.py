
from django.db import connections
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from tecdoc import models


@staff_member_required
def get_hint(request, supplier_id, article_number):

    supplier = models.Supplier.objects.get(pk=supplier_id)

    article = models.Article.objects.get(
        article_number=article_number, supplier=supplier)

    car_ids = models.ArticleLink.objects.filter(
        supplier_id=supplier.id,
        article_number=article.article_number,
        link_type='PassengerCar'
    ).values_list('link_id', flat=True)

    model_ids = models.PassangerCar.objects.filter(
        id__in=car_ids
    ).values_list('model_id', flat=True)

    car_models = models.CarModel.objects.filter(id__in=model_ids)

    manufacturers = {
        m.id: {
            'description': m.description,
            'models': []
        }
        for m in models.Manufacturer.objects.filter(
            id__in=car_models.values_list('manufacturer_id', flat=True),
            is_passenger_car=True
        ).order_by('description')
    }

    for car_model in car_models:
        manufacturers[car_model.manufacturer_id]['models'].append(car_model)

    return render(request, 'tecdoc/hint.html', {
        'article': article,
        'supplier': supplier,
        'manufacturers': manufacturers.values(),
        'oe_articles': get_oe_articles(article_number, supplier)
    })


def get_oe_articles(article_number, supplier):
    with connections['tecdoc'].cursor() as cursor:
        cursor.execute(
            """
                SELECT 
                    article_oe.OENbr AS oen_br,
                    manufacturers.description AS manufacturer
                FROM article_oe
                INNER JOIN manufacturers ON (
                    manufacturers.id = article_oe.manufacturerId AND
                    manufacturers.ispassengercar = 'True'
                )
                WHERE supplierid = %s AND datasupplierarticlenumber = %s
            """,
            [supplier.id, article_number]
        )
        return [
            dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()
        ]

