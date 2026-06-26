/* ===================================
   animations.js – 页面动效统一管理
   化隆一中官网 UI 重构
   依赖：无（纯原生 JS）
   =================================== */
'use strict';

const HualongAnimations = (() => {

  /* ---------- Intersection Observer 淡入动画 ---------- */
  const observeElements = () => {
    const elements = document.querySelectorAll('[data-animate]');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          // 若是数字滚动，触发计数
          if (entry.target.dataset.animate === 'count-up') {
            countUp(entry.target);
          }
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    elements.forEach(el => observer.observe(el));
  };

  /* ---------- 数字动态滚动 ---------- */
  const countUp = (el) => {
    const target = parseInt(el.dataset.target, 10);
    const duration = parseInt(el.dataset.duration, 10) || 1500;
    const step = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        el.textContent = target;
        clearInterval(timer);
      } else {
        el.textContent = Math.floor(current);
      }
    }, 16);
  };

  /* ---------- 平滑滚动 (备用，CSS已处理) ---------- */
  const smoothScroll = (targetSelector) => {
    const target = document.querySelector(targetSelector);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  };

  /* ---------- 导航栏滚动阴影 ---------- */
  const headerScrollEffect = () => {
    const header = document.querySelector('.site-header');
    if (!header) return;
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 10);
    });
  };

  /* ---------- 初始启动 ---------- */
  const init = () => {
    observeElements();
    headerScrollEffect();
  };

  return { init, smoothScroll };
})();

// 页面加载后启动
document.addEventListener('DOMContentLoaded', HualongAnimations.init);
