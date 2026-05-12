from django.shortcuts import render, get_object_or_404
from .models import FlowAlbum, Video


def album_list(request):
    """流动相册列表"""
    albums = FlowAlbum.objects.prefetch_related('images').all()
    context = {'albums': albums}
    return render(request, 'gallery/album_list.html', context)


def album_detail(request, slug):
    """相册详情，展示所有图片"""
    album = get_object_or_404(FlowAlbum, slug=slug)
    images = album.images.all()
    context = {'album': album, 'images': images}
    return render(request, 'gallery/album_detail.html', context)


def video_list(request):
    """视频集锦列表"""
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'gallery/video_list.html', context)