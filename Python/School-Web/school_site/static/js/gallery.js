/* ===================================
   gallery.js – 相册、视频灯箱效果
   =================================== */
'use strict';

const Gallery = (() => {
  const initLightbox = () => {
    const galleryItems = document.querySelectorAll('[data-lightbox]');
    if (!galleryItems.length) return;

    // 创建灯箱容器 (如果尚未存在)
    let lightbox = document.querySelector('.lightbox-modal');
    if (!lightbox) {
      lightbox = document.createElement('div');
      lightbox.className = 'lightbox-modal';
      lightbox.innerHTML = `
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-content" src="" alt="">
        <div class="lightbox-caption"></div>
      `;
      document.body.appendChild(lightbox);

      // 关闭事件
      lightbox.querySelector('.lightbox-close').addEventListener('click', () => {
        lightbox.style.display = 'none';
      });
      lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) lightbox.style.display = 'none';
      });
    }

    galleryItems.forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const imgSrc = item.dataset.lightbox || item.getAttribute('href');
        const caption = item.dataset.caption || '';
        lightbox.querySelector('.lightbox-content').src = imgSrc;
        lightbox.querySelector('.lightbox-caption').textContent = caption;
        lightbox.style.display = 'flex';
      });
    });
  };

  return { init: initLightbox };
})();

document.addEventListener('DOMContentLoaded', Gallery.init);