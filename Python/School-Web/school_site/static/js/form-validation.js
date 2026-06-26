/* ===================================
   form-validation.js – 前端表单校验
   =================================== */
'use strict';

const FormValidation = (() => {
  const validateMessageForm = (form) => {
    const name = form.querySelector('[name="name"]');
    const content = form.querySelector('[name="content"]');
    if (!name || !content) return true; // 若字段不存在则跳过

    let valid = true;
    if (!name.value.trim()) {
      markError(name, '请输入姓名');
      valid = false;
    } else clearError(name);
    if (!content.value.trim()) {
      markError(content, '请输入留言内容');
      valid = false;
    } else clearError(content);
    return valid;
  };

  const markError = (input, msg) => {
    input.style.borderColor = '#e74c3c';
    const feedback = input.parentNode.querySelector('.form-error') || document.createElement('span');
    feedback.className = 'form-error';
    feedback.style.color = '#e74c3c';
    feedback.style.fontSize = '0.8rem';
    feedback.textContent = msg;
    if (!input.parentNode.querySelector('.form-error')) {
      input.parentNode.appendChild(feedback);
    }
  };

  const clearError = (input) => {
    input.style.borderColor = '';
    const feedback = input.parentNode.querySelector('.form-error');
    if (feedback) feedback.remove();
  };

  const init = () => {
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
      form.addEventListener('submit', (e) => {
        if (form.dataset.validate === 'message') {
          if (!validateMessageForm(form)) e.preventDefault();
        }
      });
    });
  };

  return { init };
})();

document.addEventListener('DOMContentLoaded', FormValidation.init);