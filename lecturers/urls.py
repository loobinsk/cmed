from django.conf.urls import include, url
from lecturers.views import LecturersList, DetailViewLecturer

urlpatterns = [
    url(r'^$', LecturersList.as_view(), name='lecturers'),
    url(r'^(?P<pk>\d+)/?$', DetailViewLecturer.as_view(), name='detaillecturer'),
]
