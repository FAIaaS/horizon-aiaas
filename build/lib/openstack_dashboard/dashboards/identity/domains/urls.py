# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from horizon.browsers import views

from openstack_dashboard.dashboards.identity.domains import views as legacyView
from openstack_dashboard.utils import settings as setting_utils


if setting_utils.get_dict_config('ANGULAR_FEATURES', 'domains_panel'):
    title = _("Domains")
    urlpatterns = [
        re_path('', views.AngularIndexView.as_view(title=title), name='index'),
    ]
else:
    urlpatterns = [
        re_path(r'^$', legacyView.IndexView.as_view(), name='index'),
        re_path(r'^create$',
                legacyView.CreateDomainView.as_view(), name='create'),
        re_path(r'^(?P<domain_id>[^/]+)/update/$',
                legacyView.UpdateDomainView.as_view(), name='update')
    ]
