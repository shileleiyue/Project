import bleach
from django import template

register = template.Library()

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ol', 'ul', 'li', 'a', 'img', 'blockquote', 'pre', 'code', 'span', 'div'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height'],
    'div': ['class'],
    'span': ['class'],
}

@register.filter(name='safe_html')
def safe_html(value):
    """安全地渲染 HTML，只允许白名单标签和属性"""
    return bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)