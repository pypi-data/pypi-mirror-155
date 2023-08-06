django-simplemenu-simplified
=============================

Cloned from https://github.com/althalus/django-simplemenu but make it more simple

A dead simple menu app for Django with ordering in admin interface and
ability to link menu item with model instance, view or URL.

It features user-proof admin interface with links for ordering items
and limited list of available pages to link to. You should register
your views, QuerySets, model instances or URLs to populate that list.

Installation
============

#. Run ``python setup.py install`` or just place simplemenu directory
   into a directory which is on your PYTHONPATH.
#. Add ``'simplemenu'`` to your ``INSTALLED_APPS`` setting.
#. Run ``python manage.py syncdb``.
#. Register your pages by adding calls to ``simplemenu.register``.
#. Add menu to your templates.

Note that this application requires Django 1.1 or newer.


Templates
=========

This app has only one tag::

    {% get_simplemenu as [varname] %}

It stores QuerySet of all menu items in a context variable. Example::

    {% load simplemenu_tags %}
    {% get_simplemenu as menu %}
    {% for item in menu %}
        <a href="{{ item.page.url }}">{{ item.name }}</a>
    {% endfor %}

Highlight visited menu items
----------------------------

It's relatively simple to handle menu item that links to current
page. First, you need to have URL of the page in your template
context. The most common way to do it is to add
``'django.core.context_processors.request'`` to the
`TEMPLATE_CONTEXT_PROCESSORS
<http://docs.djangoproject.com/en/1.1/ref/settings/#template-context-processors>`_
setting and to use `RequestContext
<http://docs.djangoproject.com/en/1.1/ref/templates/api/#id1>`_ in
your views. Then you could write in your template the following::

    {% load simplemenu_tags %}
    {% get_simplemenu as menu %}
    <ul>
    {% for item in menu %}
        <li {% ifequal item.page.url request.path %}class="selected"{% endifequal %}>
            <a href="{{ item.page.url }}">{{ item.name }}</a></li>
    {% endfor %}
    </ul>
