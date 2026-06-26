from django import template
from django.templatetags.static import static
from apps.gallery.models import StaticImage

register = template.Library()


@register.simple_tag
def static_image(usage):
    """
    根据 usage 获取本地图片的静态 URL。
    用法：{% static_image 'logo' %}
    """
    try:
        img = StaticImage.objects.get(usage=usage)
        return static('gallery/' + img.image_path)
    except StaticImage.DoesNotExist:
        return static('gallery/placeholder.png')  # 可放一个默认占位图