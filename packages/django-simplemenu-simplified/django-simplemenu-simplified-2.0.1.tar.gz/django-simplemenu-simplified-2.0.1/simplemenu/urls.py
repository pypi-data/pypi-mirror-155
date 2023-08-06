from django.urls import path
from django.contrib.auth.decorators import login_required
from djangoautoconf.model_utils.url_for_models import add_all_urls

import models

urlpatterns = []


try:
    from django_auto_filter.views_django_auto_filter import DjangoAutoFilter
    urlpatterns += [path(r'^$', login_required(
        DjangoAutoFilter.as_view(
            model=models.MenuItem,
        )))]
except ImportError:
    pass

add_all_urls(urlpatterns, models)
