from django.conf.urls import include, url
from django.views.generic import TemplateView
from . import views

import views
import settings

routes = getattr(settings, 'REACT_ROUTES', [])

urlpatterns = [
    url(r'^(%s)?$' % '|'.join(routes), views.getLandingPage),
    url(r'^api/login', views.login),
    url(r'^api/logout', views.logout),
    url(r'^auth/drchrono/handleAuthCode/', views.handleAuthCode),
    url(r'^api/getPatients', views.getPatients),
    url(r'^api/getUserInfo', views.getUserInfo),
    url(r'^api/validateCheckInUser', views.validateCheckInUser),
    url(r'^api/updatePatientDemo', views.updatePatientDemo),
    url(r'^api/getAppointments', views.getAppointments),
    url(r'^api/stopTimer', views.stopTimer),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]