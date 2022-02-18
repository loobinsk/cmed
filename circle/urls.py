from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from circle import views, ajax

urlpatterns = [
                       url(r'^invite/$', login_required(views.InviteView.as_view()), name='invite'),
                       url(r'^confirmmycircle/$', login_required(ajax.confirmmycircle), name='confirmmycircle'),
                       url(r'^calendar/$', login_required(views.CalendarView.as_view()), name='calendar'),
                       url(r'^removedialog/$', login_required(ajax.removedialog), name='removedialog'),
                       url(r'^removefrommycircle/$', login_required(ajax.removefrommycircle), name='removefrommycircle'),
                       url(r'^inviteintomycircle/$', login_required(ajax.inviteintomycircle), name='inviteintomycircle'),
                       url(r'^dialog/(?P<authBid>\d+)$', login_required(views.DialogView.as_view()), name='dialog'),
                       url(r'^dialog/admin$', login_required(views.AdminDialogView.as_view()), name='admindialog'),
                       url(r'^dialog/nmo$', login_required(views.NmoDialogView.as_view()), name='nmo'),
                       url(r'^alldialogs/$', login_required(views.AllDialogsView.as_view()), name='alldialogs'),
                       url(r'^nmodialogs/$', login_required(views.NmoDialogsView.as_view()), name='nmodialogs'),
                       url(r'^mycircle/$', login_required(views.MyCircleView.as_view()), name='mycircle'),
                       url(r'^mycircle/(?P<userid>\d+)$', login_required(views.MyCircleView.as_view()),
                           name='mycircle'),
                       url(r'^interesting/$', views.interesting, name='Interesting'),
]
