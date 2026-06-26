/* ===================================
   main.js – 全局交互：菜单、返回顶部等
   =================================== */
'use strict';

document.addEventListener('DOMContentLoaded', () => {
  // 移动端菜单切换
  const hamburger = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');
  const closeNav = document.querySelector('.mobile-nav .close-btn');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => mobileNav.classList.add('open'));
    closeNav.addEventListener('click', () => mobileNav.classList.remove('open'));
    // 点击链接后自动关闭
    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => mobileNav.classList.remove('open'));
    });
  }

  // 返回顶部按钮 (动态生成)
  const backToTop = document.createElement('button');
  backToTop.className = 'btn-icon back-to-top';
  backToTop.innerHTML = '↑';
  backToTop.title = '返回顶部';
  backToTop.style.cssText = `
    position: fixed; bottom: 2rem; right: 2rem; z-index: 900;
    background: var(--color-primary); color: white; border-radius: 50%;
    width: 48px; height: 48px; font-size: 1.5rem; display: none;
    align-items: center; justify-content: center; border: none; cursor: pointer;
    box-shadow: var(--shadow-md);
  `;
  document.body.appendChild(backToTop);

  window.addEventListener('scroll', () => {
    backToTop.style.display = window.scrollY > 500 ? 'flex' : 'none';
  });
  backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
});