from django.utils.text import slugify


def generate_unique_slug(Blog, title):
    origin_slug = slugify(title)
    unique_slug = origin_slug
    num = 1
    while Blog.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, num)
        num += 1
    return unique_slug