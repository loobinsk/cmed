from datetime import timedelta

from django.utils import timezone
from django.db.models import Q, F

from medtus.models import Statistics

from .models import Posts


def boost_views_for_latest_news(views_count=None):
    '''
        Increase the number of views for news that were published today.
        Runs at 02:30. (In 03:00 create backup)
    '''

    if views_count is None or not isinstance(views_count, int):
        views_count = 30

    post_date = timezone.now().date() - timedelta(days=1)
    yesterday_posts = Posts.objects.filter(type=1, status=0) \
        .filter(
            Q(begindate__date=post_date) | Q(createdate__date=post_date)
        ).only('begindate', 'createdate')[:10]

    ids = []

    for post in yesterday_posts:
        if (post.begindate and post.begindate.date() == post_date) or \
                (not post.begindate and post.createdate.date() == post_date):
            # boost
            ids.append(post.id)

    if len(ids) >= 1:
        Statistics.objects.filter(
                material_id__in=ids,
                service_id=18
            ).update(viewings=F('viewings') + views_count)
