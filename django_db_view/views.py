from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import importlib
from django.urls import reverse
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q


def show(request, app_name, model_name):
    '''CharField, TextField, IntegerField, BooleanField, ForeignKey, ManyToManyField
    '''
    Models = importlib.import_module('{app_name}.models'.format(**locals()))
    Model = getattr(Models, model_name)

    query_dict = request.GET
    clean_dict = {}
    display_args = {}
    for k in query_dict:
        Model2 = Model
        if k in ('limit', 'order', 'page', 'display'):
            display_args[k] = query_dict[k]
            continue
        ks = k.split('__')
        for ek in ks:
            if ek in ('pk', 'id'):
                clean_dict[k] = int(query_dict[k])
                break
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
            elif field_type in ('ForeignKey', 'ManyToManyField'):
                Model2 = Model2._meta.get_field(ek).related_model
            else:
                break
    # temp fix for get all sub tags, only work for tags__id now
    if 'tags__id' in clean_dict:
        tag_id = clean_dict.pop('tags__id')
        Model2 = Model._meta.get_field('tags').related_model
        all_tag_ids = [t.id for t in Model2.objects.get(id=tag_id).get_all_child_tags()]
        clean_dict['tags__id__in'] = all_tag_ids

    if clean_dict:
        objs = Model.objects.filter(Q(**clean_dict)).distinct()
    else:
        objs = Model.objects.all()

    display = display_args.get('display') or 'table'
    fields = [t.name for t in Model._meta.fields]
    if hasattr(Model, 'django_db_view_fields') and display in Model.django_db_view_fields:
        fields = [t for t in Model.django_db_view_fields.get(display) if not t.startswith('_')]  # filter out _ for gallery display 
    headers = []
    for f in fields:
        try:
            h = Model._meta.get_field(f).verbose_name
        except FieldDoesNotExist:
            h = getattr(Model, f).verbose_name
        headers.append(h)

    if objs.exists():
        order = display_args.get('order')  # or '-id'
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
        return render(request, 'django_db_view/show_as_%s.html' % display, {'page_objs': page_objs, 'fields': fields, 'headers': headers, 'title': title, 'model_meta': Model._meta})
    else:
        return render(request, 'django_db_view/debug.html', {'msg': 'No objects find.'})


#def edit(request, app_name, model_name, obj_id):
#    app_name = app_name.lower()
#    model_name = model_name.lower()
#    return reverse('admin:{app_name}_{model_name}_change'.format(**locals()), args=[obj_id])
#
#
#def delete(request, app_name, model_name, obj_id):
#    app_name = app_name.lower()
#    model_name = model_name.lower()
#    return reverse('admin:{app_name}_{model_name}_delete'.format(**locals()), args=[obj_id])
