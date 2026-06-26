from django.core.management.base import BaseCommand
from apps.news.models import NewsCategory

class Command(BaseCommand):
    help = '初始化新闻分类数据'

    def handle(self, *args, **options):
        categories = [
            ('news', '新闻动态', 'news'),
            ('notice', '通知公告', 'notice'),
            ('media', '媒体报道', 'media_report'),
        ]
        for slug, name, ctype in categories:
            NewsCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'category_type': ctype}
            )
        self.stdout.write(self.style.SUCCESS('新闻分类初始化完成'))