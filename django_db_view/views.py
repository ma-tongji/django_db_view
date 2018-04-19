from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import importlib
from django.urls import reverse
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q


def show(request, app_name, model_name):
    '''charfield integerfield, boofield, textfield, foreignKey
    '''
    Models = importlib.import_module('{app_name}.models'.format(**locals()))
    Model = getattr(Models, model_name)

    query_dict = request.GET
    clean_dict = {}
    display_args = {}
    Model2 = Model
    for k in query_dict:
        if k in ('limit', 'order', 'page'):
            display_args[k] = query_dict[k]
            continue
        ks = k.split('__')
        for ek in ks:
            try:
                field_type = Model2._meta.get_field(ek).get_internal_type()
            except FieldDoesNotExist:
                break
            if field_type in ('CharField', 'TextField'):
                clean_dict[k] = query_dict[k]
                break
            elif field_type == 'IntegerField':
                clean_dict[k] = int(query_dict[k])
                break
            elif field_type == 'BooleanField':
                clean_dict[k] = bool(int(query_dict[k]))
                break
            elif field_type == ('ForeignKey', 'ManyToManyField'):
                Model2 = Models._meta.get_field(ek).related_model
            else:
                break
    if clean_dict:
        objs = Model.objects.filter(Q(**clean_dict))
    else:
        objs = Model.objects.all()

    if objs.exists():
        if hasattr(objs[0], 'django_db_view_fields'):
            fields = objs[0].django_db_view_fields
            headers = []
            for f in fields:
                try:
                    h = objs[0]._meta.get_field(f).verbose_name
                except FieldDoesNotExist:
                    h = getattr(objs[0], f).verbose_name
                headers.append(h)
        else:
            fields = [t.name for t in objs[0]._meta.fields]
            headers = [t.verbose_name for t in objs[0]._meta.fields]
        order = display_args.get('order')
        if order:
            objs = objs.order_by(order)
        limit = display_args.get('limit') or 100
        page = display_args.get('page') or 1

        paginator = Paginator(objs, limit)
        try:
            page_objs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer
            return render(request, 'django_db_view/debug.html', {'msg': 'show: Page is not an integer.'})
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_objs = paginator.page(paginator.num_pages)

        title = ', '.join('%s=%s' % x for x in clean_dict.items()) + ' / ' + ', '.join('%s=%s' % x for x in display_args.items())
        return render(request, 'django_db_view/show.html', {'page_objs': page_objs, 'fields': fields, 'headers': headers, 'title': title})
    else:
        return render(request, 'django_db_view/debug.html', {'msg': 'No objects find.'})


def edit(request, app_name, model_name, obj_id):
    app_name = app_name.lower()
    model_name = model_name.lower()
    return reverse('admin:{app_name}_{model_name}_change'.format(**locals()), args=[obj_id])


def delete(request, app_name, model_name, obj_id):
    app_name = app_name.lower()
    model_name = model_name.lower()
    return reverse('admin:{app_name}_{model_name}_delete'.format(**locals()), args=[obj_id])

