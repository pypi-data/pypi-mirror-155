from django.db import models
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class MenuItem(models.Model):
    """
    A menu item.

    Each item is represented by caption ``name`` and a page it links
    to. Page could be any model with get_absolute_url method or a
    string (url, reversible name of the view).

    Use ``get_absolute_url()`` or ``page.url()`` to get url of the
    page.

    All items in the menu are ordered by ``rank``.
    """
    name = models.CharField(_('Caption'), max_length=64)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    urlstr = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')
    
    def __unicode__(self):
        return self.name


class URLItem(models.Model):
    """
    A dead simple class to let users input their own hand crafted URLs, rather
    than force hard coded URLs to be specified in the code.
    """
    name = models.CharField(_('Caption'), max_length=64)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.url)

    def get_absolute_url(self):
        return self.url
