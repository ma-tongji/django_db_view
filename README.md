
How to use:
1. install
2. add django\_db\_view to INSTALLED\_APPS
3. include path to urls.py
4. registry your model in  admin.py

add a varible django_db_view_fields: to only display selected fields.
add function to show exact the returned value
add verbose name to displayed table header

example
```
from django.db import models
class Model(models):
    name = ...
    tag = ...
    author = models.ForeignKey( ... )

    django_db_view_fields =  {'table': ['id', 'name', 'tag', 'get_author_name']}

    def get_author_name(self):
        return self.author.name
    get_author_name.verbose_name = u'Auth'
```

if you want ot view a model in gallery display mode.
def a method get_view_galery_obj_image, with return a image model, the method startswith _ are hard-coded into template, so either it is in django_db_view_fields or not is ok, will filter out in views.
