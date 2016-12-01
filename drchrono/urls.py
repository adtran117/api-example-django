from django.conf.urls import include, url
from django.views.generic import TemplateView
from . import views

import views
import settings

routes = getattr(settings, 'REACT_ROUTES', [])

urlpatterns = [
    # url(r'^', TemplateView.as_view(template_name='index.html'), name='home'),
    # url(r'^home/', TemplateView.as_view(template_name='index.html'), name='home'),
    # url(r'^(%s)?$' % '|'.join(routes), TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^(%s)?$' % '|'.join(routes), views.getLandingPage),
    # url(r'^', views.getLandingPage),
    # url(r'^dashboard' views.getDashboard)
    url(r'^api/login', views.login),
    url(r'^api/logout', views.logout),
    url(r'^auth/drchrono/handleAuthCode/', views.handleAuthCode),
    url(r'^api/getPatients', views.getPatients),
    url(r'^api/getUserInfo', views.getUserInfo),
    url(r'^api/validateCheckInUser', views.validateCheckInUser),
    url(r'^api/updatePatientDemo', views.updatePatientDemo),
    # url(r'^api/test/', views.testingCookies),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]