
How to use:
1. install
2. add django\_db\_view to INSTALLED\_APPS
3. include path to urls.py
4. define admin.py for the models in your app


add a varible django_db_view_fields: to only display selected fields.
add function to show exact the returned value
add verbose name tas displayed table header

example
```
from django.db import models
class Model(models):
    name = ...
    tag = ...
    author = models.ForeignKey( ... )

    django_db_view_fields =  ['id', 'name', 'tag', 'get_author_name']

    def get_author_name(self):
        return self.author.name
    get_author_name.verbose_name = u'Auth'
```
