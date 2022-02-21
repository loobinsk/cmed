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

    start_date = timezone.now() - timedelta(days=30)
    end_date = timezone.now() - timedelta(days=1)
    month_posts = Posts.objects.filter(type=1, status=0) \
        .filter(
            Q(begindate__range=[start_date, end_date])
            | Q(createdate__range=[start_date, end_date])
        ).only('begindate', 'createdate')

    ids = []

    for post in month_posts:
        if (post.begindate and start_date <= post.begindate <= end_date) or \
                (not post.begindate and start_date <= post.createdate <= end_date):
            # boost
            ids.append(post.id)

    if len(ids) >= 1:
        Statistics.objects.filter(
                material_id__in=ids,
                service_id=18
            ).update(viewings=F('viewings') + views_count)
