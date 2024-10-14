from django.utils import timezone


def filter_post(post):
    post = post.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    return post
