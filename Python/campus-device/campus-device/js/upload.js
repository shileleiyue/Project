/* ========================================
   Upload - 文件上传组件
   ======================================== */

const Upload = (function() {
  const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
  const MAX_SIZE = 5 * 1024 * 1024; // 5MB
  const MAX_COUNT = 5;

  /**
   * 校验文件格式和大小
   * @param {File} file - 文件对象
   * @returns {{ valid: boolean, message: string }}
   */
  function validate(file) {
    if (!ALLOWED_TYPES.includes(file.type)) {
      return {
        valid: false,
        message: `不支持的文件格式: ${file.type}，仅支持 JPG、PNG、WebP`
      };
    }

    if (file.size > MAX_SIZE) {
      const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
      return {
        valid: false,
        message: `文件大小 ${sizeMB}MB 超出限制，最大支持 5MB`
      };
    }

    return { valid: true, message: '' };
  }

  /**
   * 预览文件（返回 base64）
   * @param {File} file - 文件对象
   * @returns {Promise<string>} base64 字符串
   */
  function preview(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        resolve(e.target.result);
      };
      reader.onerror = () => {
        reject(new Error('文件读取失败'));
      };
      reader.readAsDataURL(file);
    });
  }

  /**
   * 创建上传区域（支持拖拽和点击上传）
   * @param {string} containerSelector - 容器选择器
   * @param {Object} options - 配置项
   * @param {Function} options.onChange - 文件列表变化回调 (files: File[])
   * @param {Function} options.onError - 校验失败回调 (message: string)
   * @param {number} [options.maxCount=MAX_COUNT] - 最大文件数
   */
  function createUploadArea(containerSelector, options) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    const opts = options || {};
    const maxCount = opts.maxCount || MAX_COUNT;
    const onChange = opts.onChange || function() {};
    const onError = opts.onError || function(msg) { alert(msg); };

    let selectedFiles = [];

    const html = `
      <div class="upload-area">
        <div class="upload-zone">
          <div class="upload-icon">+</div>
          <p class="upload-text">点击或拖拽文件到此处上传</p>
          <p class="upload-hint">支持 JPG、PNG、WebP 格式，单文件不超过 5MB，最多 ${maxCount} 张</p>
        </div>
        <div class="upload-preview-list"></div>
      </div>
    `;

    container.innerHTML = html;

    const uploadZone = container.querySelector('.upload-zone');
    const previewList = container.querySelector('.upload-preview-list');

    /**
     * 处理文件选择
     * @param {FileList} fileList
     */
    function handleFiles(fileList) {
      const files = Array.from(fileList);

      // 校验数量
      if (selectedFiles.length + files.length > maxCount) {
        onError(`最多只能上传 ${maxCount} 张图片`);
        return;
      }

      const validFiles = [];
      for (const file of files) {
        const result = validate(file);
        if (!result.valid) {
          onError(result.message);
          return;
        }
        validFiles.push(file);
      }

      selectedFiles = selectedFiles.concat(validFiles);
      renderPreviews();
      onChange(selectedFiles);
    }

    /**
     * 渲染预览图
     */
    function renderPreviews() {
      previewList.innerHTML = '';

      selectedFiles.forEach((file, index) => {
        const item = document.createElement('div');
        item.className = 'upload-preview-item';

        preview(file).then((base64) => {
          const img = document.createElement('img');
          img.src = base64;
          img.alt = '预览';
          img.className = 'upload-preview-img';
          item.appendChild(img);

          const removeBtn = document.createElement('span');
          removeBtn.className = 'upload-preview-remove';
          removeBtn.textContent = 'x';
          removeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            selectedFiles.splice(index, 1);
            renderPreviews();
            onChange(selectedFiles);
          });
          item.appendChild(removeBtn);
        });

        previewList.appendChild(item);
      });
    }

    // 点击上传
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = ALLOWED_TYPES.join(',');
    fileInput.multiple = true;
    fileInput.style.display = 'none';

    uploadZone.addEventListener('click', () => {
      fileInput.click();
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        handleFiles(fileInput.files);
        fileInput.value = '';
      }
    });

    // 拖拽上传
    uploadZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
      uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadZone.classList.remove('dragover');
      if (e.dataTransfer.files.length > 0) {
        handleFiles(e.dataTransfer.files);
      }
    });
  }

  // 注入上传区域样式
  (function injectStyle() {
    if (document.getElementById('upload-style')) return;
    const style = document.createElement('style');
    style.id = 'upload-style';
    style.textContent = `
      .upload-zone {
        border: 2px dashed #d1d5db;
        border-radius: 10px;
        padding: 32px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        background-color: #fafbfc;
      }
      .upload-zone:hover,
      .upload-zone.dragover {
        border-color: #2563eb;
        background-color: #eff6ff;
      }
      .upload-icon {
        font-size: 36px;
        color: #9ca3af;
        font-weight: 300;
        margin-bottom: 8px;
      }
      .upload-text {
        font-size: 14px;
        color: #374151;
        margin-bottom: 4px;
      }
      .upload-hint {
        font-size: 12px;
        color: #9ca3af;
      }
      .upload-preview-list {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 12px;
      }
      .upload-preview-item {
        position: relative;
        width: 80px;
        height: 80px;
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
      }
      .upload-preview-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .upload-preview-remove {
        position: absolute;
        top: 2px;
        right: 2px;
        width: 20px;
        height: 20px;
        background-color: rgba(0,0,0,0.5);
        color: #fff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        cursor: pointer;
        line-height: 1;
      }
      .upload-preview-remove:hover {
        background-color: rgba(220,38,38,0.8);
      }
    `;
    document.head.appendChild(style);
  })();

  return { ALLOWED_TYPES, MAX_SIZE, MAX_COUNT, validate, preview, createUploadArea };
})();