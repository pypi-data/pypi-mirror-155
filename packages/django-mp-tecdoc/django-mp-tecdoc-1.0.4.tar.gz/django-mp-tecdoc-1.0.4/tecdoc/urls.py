
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from tecdoc import views


app_name = 'tecdoc'


urlpatterns = [

    path('hint/<int:supplier_id>/<str:article_number>/', views.get_hint,
         name='hint')

]

app_urls = i18n_patterns(
    path('tecdoc/', include((urlpatterns, app_name)))
)
