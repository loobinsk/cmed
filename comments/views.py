from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.conf import settings
from comments.models import Comments
from videos.models import Videos
from events.models import Events
from posts.models import Posts
from account.models import MyUser
from records.models import Records
from django.utils import timezone
from rss.models import Posts as rssPosts


def newcomment(request):
    if not request.POST.get('content', '').strip():
        raise Http404
    c = Comments.objects.create(user_id=MyUser(id=request.user.id), parent_id=request.POST['parent_id'],
                                service_id=request.POST['service_id'], object_id=request.POST['object_id'],
                                content=request.POST['content'], createdate=timezone.now())

    if request.POST['service_id'] == '10':
        objects = Videos.objects.filter(pk=c.object_id)
    if request.POST['service_id'] == '6':
        objects = Events.objects.filter(pk=c.object_id)
    if request.POST['service_id'] == '18':
        objects = Posts.objects.filter(pk=c.object_id)
    if request.POST['service_id'] == '23':
        objects = Records.objects.filter(pk=c.object_id)
    if request.POST['service_id'] == '27':
        from photos.models import PGalleries
        objects = PGalleries.objects.filter(pk=c.object_id)
    if request.POST['service_id'] == '69':
        objects = rssPosts.objects.filter(pk=c.object_id)

    context = {'objects': objects, 'service_id': request.POST['service_id'], 'loadhidden': int(request.GET.get('loadhidden', False))}
    return render(request, 'comments/newcomment.html', context)


def rmcomment(request):
    if request.method != 'POST':
        raise Http404
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comments, pk=comment_id)
    time_left = (timezone.now() - comment.createdate).seconds < getattr(settings, 'POST_DELETION_TIME', 30) * 60
    if comment.user_id != request.user or not time_left:
        return HttpResponse('error')
    comment.delete()
    return HttpResponse('OK')