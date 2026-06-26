"""
作家工厂 应用级配置管理。

配置分两层：
1. 引导配置（bootstrap）：固定存放在 %LOCALAPPDATA%/WriterFactory/config.json，
   仅用于记录"用户自定义的数据目录"，使得 settings.py 在启动最早期就能定位真正的
   数据目录（数据库、媒体、完整配置都在那里）。
2. 完整配置：存放在 <数据目录>/config.json，包含主题、分页、字号等全部偏好。

之所以这样设计，是因为数据库路径必须在 Django 初始化前确定；而数据目录本身可被
用户修改，所以需要一个"位置固定、永不迁移"的引导文件来指向它。
"""
import os
import sys
import json
import shutil
from pathlib import Path

# 引导目录（固定，不随用户设置改变）
def _bootstrap_dir() -> Path:
    if getattr(sys, 'frozen', False):
        base = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
    else:
        # 开发模式：项目根目录
        base = Path(__file__).resolve().parent.parent
        return Path(base)
    return Path(base) / 'WriterFactory'


BOOTSTRAP_DIR = _bootstrap_dir()
BOOTSTRAP_CONFIG = BOOTSTRAP_DIR / 'config.json'

# 配置默认值
DEFAULTS = {
    # 数据存储目录（空字符串表示使用默认位置）
    'data_dir': '',
    # 个性化：主题色（主色 / 强调色）
    'theme_primary': '#5b7fff',
    'theme_accent': '#7c5cfc',
    # 界面字号缩放（0.9 / 1.0 / 1.1 / 1.2）
    'font_scale': 1.0,
    # 作品列表每页条数
    'page_size': 10,
    # 编辑器是否自动保存
    'autosave': True,
    # 昵称（展示用，可选）
    'display_name': '',
}


def _read_json(path: Path) -> dict:
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.json.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def get_custom_data_dir() -> Path | None:
    """从引导配置读取用户自定义数据目录；未设置返回 None。"""
    boot = _read_json(BOOTSTRAP_CONFIG)
    custom = (boot.get('data_dir') or '').strip()
    if custom:
        p = Path(custom)
        try:
            p.mkdir(parents=True, exist_ok=True)
            return p
        except OSError:
            return None
    return None


def resolve_data_dir(default_dir: Path) -> Path:
    """settings.py 启动时调用：确定最终数据目录。"""
    custom = get_custom_data_dir()
    return custom if custom is not None else default_dir


def load_config(data_dir: Path) -> dict:
    """加载完整配置（合并默认值）。"""
    cfg = dict(DEFAULTS)
    cfg.update(_read_json(Path(data_dir) / 'config.json'))
    # 类型修正
    try:
        cfg['font_scale'] = float(cfg.get('font_scale', 1.0))
    except (TypeError, ValueError):
        cfg['font_scale'] = 1.0
    try:
        cfg['page_size'] = int(cfg.get('page_size', 10))
    except (TypeError, ValueError):
        cfg['page_size'] = 10
    cfg['autosave'] = bool(cfg.get('autosave', True))
    return cfg


def save_config(data_dir: Path, updates: dict) -> dict:
    """合并保存完整配置，返回最新配置。"""
    path = Path(data_dir) / 'config.json'
    current = _read_json(path)
    current.update(updates)
    _write_json(path, current)
    return load_config(data_dir)


def set_data_dir_pointer(new_dir: str) -> None:
    """在引导配置中写入新的数据目录指针。"""
    BOOTSTRAP_DIR.mkdir(parents=True, exist_ok=True)
    boot = _read_json(BOOTSTRAP_CONFIG)
    boot['data_dir'] = str(new_dir)
    _write_json(BOOTSTRAP_CONFIG, boot)


def migrate_data(src_dir: Path, dst_dir: Path) -> None:
    """把数据库、媒体、配置从旧目录迁移到新目录。

    复制而非移动：复制成功后保留原目录作为备份，更安全。
    """
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)

    for name in ('db.sqlite3', 'config.json', 'secret_key.txt'):
        s = src_dir / name
        if s.exists():
            shutil.copy2(s, dst_dir / name)

    # 媒体目录
    src_media = src_dir / 'media'
    if src_media.exists():
        dst_media = dst_dir / 'media'
        dst_media.mkdir(exist_ok=True)
        for item in src_media.rglob('*'):
            rel = item.relative_to(src_media)
            target = dst_media / rel
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
