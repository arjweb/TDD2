from django.conf.urls import url
from lists.views import list_view, new_list, add_item

urlpatterns = [

    url(r'(\d+)/$', list_view, name='list_view'),
    url(r'new$', new_list, name='new_list'),
    url(r'(\d+)/add$', add_item, name='add_item'),
]
