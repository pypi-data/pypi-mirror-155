# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_ufilter',
 'django_ufilter.backends',
 'django_ufilter.filtersets',
 'django_ufilter.integrations']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0']

extras_require = \
{':python_version <= "3.9"': ['django>=3.2,<4.0'],
 ':python_version >= "3.8"': ['django>=4,<5']}

setup_kwargs = {
    'name': 'django-ufilter',
    'version': '0.4.0',
    'description': 'django-ufilter provides a safe way to filter data.',
    'long_description': '=================\nDjango UFilter\n=================\n\n.. image:: https://badge.fury.io/py/django-ufilter.svg\n   :target: http://badge.fury.io/py/django-ufilter\n.. image:: https://readthedocs.org/projects/django-ufilter/badge/?version=latest\n   :target: http://django-ufilter.readthedocs.io/en/latest/?badge=latest\n\nDjango UFilter provides a safe way to filter data via human-friendly URLs.\n\n* Free software: MIT license\n* GitHub: https://github.com/Qu4tro/django-ufilter/\n* Documentation: http://django-ufilter.readthedocs.io/\n\nOverview\n--------\n\nThe main goal of Django UFilter is to provide an easy URL interface\nfor filtering data. It allows the user to safely filter by model\nattributes and also allows to specify the lookup type for each filter\n(very much like Django\'s filtering system in ORM).\n\nFor example the following will retrieve all items where the id is\n``5`` and title contains ``"foo"``::\n\n    example.com/listview/?id=5&title__contains=foo\n\nIn addition to basic lookup types, Django UFilter allows to\nuse more sophisticated lookups such as ``in`` or ``year``.\nFor example::\n\n    example.com/listview/?id__in=1,2,3&created__year=2013\n\nRequirements\n------------\n\n* Python 2.7, 3.x, pypy or pypy3\n* Django 1.8+ (there are plans to support older Django versions)\n* Django REST Framework 2 or 3 (only if you want to use DRF integration)\n\nInstalling\n----------\n\nEasiest way to install this library is by using ``pip``::\n\n    $ pip install django-ufilter\n\nUsage Example\n-------------\n\nTo make example short, it demonstrates Django UFilter integration\nwith Django REST Framework but it can be used without DRF (see below).\n\n::\n\n  from django_ufilter.integrations.drf import DRFFilterBackend\n\n\n  class UserViewSet(ModelViewSet):\n      queryset = User.objects.all()\n      serializer_class = UserSerializer\n      filter_backends = [DjangoFilterBackend]\n      filter_fields = [\'username\', \'email\']\n\nAlternatively filterset can be manually created and used directly\nto filter querysets::\n\n  from django.http import QueryDict\n  from django_ufilter.filtersets import ModelFilterSet\n\n\n  class UserFilterSet(ModelFilterSet):\n      class Meta(object):\n          model = User\n\n  query = QueryDict(\'email__contains=gmail&joined__gt=2015-01-01\')\n  fs = UserFilterSet(data=query, queryset=User.objects.all())\n  filtered_users = fs.filter()\n\nAbove will automatically allow the use of all of the Django UFilter features.\nSome possibilities:\n\n* get user with id 5\n\n    example.com/users/?id=5\n\n* get user with id either 5, 10 or 15\n\n    example.com/users/?id__in=5,10,15\n\n* get user with id between 5 and 10\n\n    example.com/users/?id__range=5,10\n\n* get user with username "foo"\n\n    example.com/users/?username=foo\n\n* get user with username containing case insensitive "foo"\n\n    example.com/users/?username__icontains=foo\n\n* get user where username does NOT contain "foo"\n\n    example.com/users/?username__icontains!=foo\n\n* get user who joined in 2015 as per user profile\n\n    example.com/users/?profile__joined__year=2015\n\n* get user who joined in between 2010 and 2015 as per user profile\n\n    example.com/users/?profile__joined__range=2010-01-01,2015-12-31\n\n* get user who joined in after 2010 as per user profile\n\n    example.com/users/?profile__joined__gt=2010-01-01\n\nAvailable lookups:\n\n* contains: Match when string contains given substring.\n* day: Match by day of the month.\n* endswith: Match when string ends with given substring.\n* exact: Match exactly the value as is.\n* gt: Match when value is greater then given value.\n* gte: Match when value is greater or equal then given value.\n* hour: Match by the hour (24 hour) value of the timestamp.\n* icontains: Case insensitive match when string contains given substring.\n* iendswith: Case insensitive match when string ends with given substring.\n* iexact: Case insensitive match exactly the value as is.\n* iin: Case insensitive match when value is any of given comma separated values.\n* in: Match when value is any of given comma separated values.\n* iregex: Case insensitive match string by regex pattern.\n* isnull: Match when value is NULL.\n* istartswith: Case insensitive match when string starts with given substring.\n* lt: Match when value is less then given value.\n* lte: Match when value is less or equal then given value.\n* minute: Match by the minute value of the timestamp.\n* month: Match by the month value of the timestamp.\n* range: Match when value is within comma separated range.\n* regex: Match string by regex pattern.\n* second: Match by the second value of the timestamp.\n* startswith: Match when string starts with given substring.\n* week_day: Match by week day (1-Sunday to 7-Saturday) of the timestamp.\n* year: Match by the year value of the timestamp.\n* len: Match the length of a given ArrayField\n\nFeatures\n--------\n\n* **Human-friendly URLs**\n\n  Filter querystring format looks\n  very similar to syntax for filtering in Django ORM.\n  Even negated filters are supported! Some examples::\n\n    example.com/users/?email__contains=gmail&joined__gt=2015-01-01\n    example.com/users/?email__contains!=gmail  # note !\n\n* **Related models**\n\n  Support related fields so that filtering can be applied to related\n  models. For example::\n\n    example.com/users/?profile__nickname=foo\n\n* **Decoupled filtering**\n\n  How URLs are parsed and how data is filtered is decoupled.\n  This allows the actual filtering logic to be decoupled from Django\n  hence filtering is possible not only with Django ORM QuerySet but\n  any set of data can be filtered (e.g. plain Python objects)\n  assuming corresponding filtering backend is implemented.\n\n* **Usage-agnostic**\n\n  This library decouples filtering from any particular usage-pattern.\n  It implements all the basic building blocks for creating\n  filtersets but it does not assume how they will be used.\n  To make the library easy to use, it ships with some integrations\n  with common usage patterns like integration with Django REST Framework.\n  This means that its easy to use in custom applications with custom\n  requirements (which is probably most of the time!)\n',
    'author': 'Miroslav Shubernetskiy',
    'author_email': 'miroslav@miki725.com',
    'maintainer': 'Xavier Francisco',
    'maintainer_email': 'xavier.n.francisco@gmail.com',
    'url': 'https://github.com/Qu4tro/django-ufilter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
