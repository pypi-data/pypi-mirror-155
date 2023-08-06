# MP-tecdoc

Django tecdoc app.

### Installation

Install with pip:

```
pip install django-mp-tecdoc
```

Add settings:
```
INSTALLED_APPS = [
    ...,
    'tecdoc',
]
```

```
DATABASE_ROUTERS = [
    ...,
    'tecdoc.routers.TecDocRouter'
]
```

```
DATABASES = {
    ...,
    'tecdoc': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tecdoc',
        'USER': 'dev'
    }
}
```

Usage in form clean method:
```
from tecdoc.utils import get_crosses_text

data['additional_codes'] = get_crosses_text(
            data.get('code'), data.get('additional_codes'))
```

Querysets:

```
from tecdoc.models import Cross
Cross.objects.find('JBJ721').codes()
```