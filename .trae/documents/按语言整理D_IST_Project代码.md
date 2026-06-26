# 按语言种类整理 D:\IST\Project 代码 + 修正地址敏感文件

## Context（背景）

D:\IST\Project 下混杂了大量不同语言的代码项目与散落文件。用户希望按语言分类整理：为 Python、C/嵌入式、Web/HTML 三类新建顶层文件夹，将对应项目和散落代码整体移入，并修正移动后失效的地址敏感文件（虚拟环境路径、启动脚本、文档中的绝对路径等）。用户已确认：

* **整理方式**：新建语言文件夹，整体移动项目。

* **venv 处理**：重建 venv 并按 requirements.txt 重新安装依赖。

## 目标目录结构

```
D:\IST\Project\
├── Python\          # 语言分类
│   ├── AutoClicker, bluemsun, campus-device, novel_manager, py,
│   │   School-Web, wechat_assistant, WriterFactory, Writerworks
│   └── transpose_font.py        （根目录散落 Python 文件）
├── C\               # 语言分类（注意：先移入原小写 c 目录，避免 Windows 大小写冲突）
│   ├── c            （原目录名保留）
│   ├── firmware, firmware_f407_game, firmware_keil
│   └── sfycx
├── Web\             # 语言分类
│   ├── HTML, ksh
│   └── 春季培训第一讲
└──（保留根目录）.git, .idea, .vscode, .trae,
                  整理脚本(*.ps1)/日志/csv/md, .envrc(如需)
```

## 语言分类明细

| 语言       | 项目                                                                                                                                      |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Python   | AutoClicker, bluemsun, campus-device, novel\_manager, py, School-Web, wechat\_assistant, WriterFactory, Writerworks, transpose\_font.py |
| C/嵌入式    | c, firmware, firmware\_f407\_game, firmware\_keil, sfycx                                                                                |
| Web/HTML | HTML, ksh, 春季培训第一讲                                                                                                                      |

## 实施步骤

### 1. 移动项目（PowerShell 脚本执行）

* 先处理 `C` 分类：`New-Item D:\IST\Project\C` 后依次把 `c`、`firmware`、`firmware_f407_game`、`firmware_keil`、`sfycx` 移入 `C\`。**顺序上先移入小写** **`c`**（避免 Windows 大小写不敏感造成 `C`/`c` 同名冲突）。

* 建 `Python\`，移入 9 个 Python 项目 + `transpose_font.py`。

* 建 `Web\`，移入 `HTML`、`ksh`、`春季培训第一讲`。

* 目标同名已存在则跳过（保留原有）。

### 2. 重建全部 Python venv 并重装依赖

针对有 venv 的 Python 项目（AutoClicker, campus-device, School-Web, wechat\_assistant, Writerworks，及其余项目若含 venv）：

1. 先 `Rename-Item venv venv.bak_<时间戳>` 做备份（避免依赖不可恢复）。
2. 在原 venv 的 `pyvenv.cfg`/`home` 基础上，用**对应基础 Python** 重建 venv：

   * campus-device、School-Web：`D:\IST\Miniconda\envs\bluemsun_env\python.exe`

   * AutoClicker、wechat\_assistant、Writerworks：`C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\python.exe`
3. `pip install -r requirements.txt`。对该项目缺失 `requirements.txt` 时，脚本内提示"需手动补装依赖"，并保留 venv.bak 供回退。
4. `novel_manager`、`WriterFactory` 等无 venv 或仅用系统环境，仅验证移动后路径引用。

### 3. 修正地址敏感文件（sed 式替换旧路径 → 新路径）

对以下类型的文件，把其中的 `D:\IST\Project\<项目>` 批量替换为 `D:\IST\Project\<分类>\<项目>`：

* **文档/启动脚本**：campus-device 下 `启动指令.txt`、`使用说明书.md`（含 `D:\`、`python` 等路径引用）；Writerworks、WriterFactory 等处如有雷同文档一并处理。

* **IDE/构建配置**：`.vscode/launch.json`、`tasks.json`（根目录及项目内）；firmware 系列的 `.cproject`、`Makefile`、`build.bat`（主要检查是否存在绝对路径；相对路径无需改）。

* **应用启动/打包文件**：WriterFactory `app_launcher.py`、`build.bat`、`WriterFactory.spec`；`AutoClicker.spec`。

* 替换用 PowerShell：`(Get-Content -Raw) -replace 'regex','new' | Set-Content`，仅对匹配旧路径的文件做替换。

### 4. 收尾

* 删除我本阶段的临时扫描脚本：`_scan_projects.ps1`、`_scan_addr.ps1`、`_scan_addr2.ps1`、`_scan_addr3.ps1`。

* 复核各分类目录完整性。

## 关键文件（地址敏感、待修正/重建）

* `AutoClicker\venv\pyvenv.cfg`、`AutoClicker.spec`

* `campus-device\venv\pyvenv.cfg`、`campus-device\启动指令.txt`、`campus-device\使用说明书.md`

* `School-Web\School-venv\pyvenv.cfg`、`School-Web\requirements.txt`

* `wechat_assistant\venv\pyvenv.cfg`

* `Writerworks\venv\pyvenv.cfg`、`Writerworks\requirements.txt`

* `WriterFactory\app_launcher.py`、`WriterFactory\build.bat`、`WriterFactory\WriterFactory.spec`

* `firmware\`、`firmware_keil\`、`firmware_f407_game\` 的构建/工程配置（若有绝对路径）

* `.vscode\launch.json`、`.vscode\tasks.json`（根目录）

## 验证

1. 移动后各分类目录文件数与移动前一致（用计数脚本比对）。
2. 对重建的每个 venv 执行 `venv\Scripts\python.exe -c "import flask, django"`（按项目依赖）确认能导入。
3. 抽查地址敏感文件已不含旧路径：`Select-String -Path <文件> -Pattern 'D:\\IST\\Project\\(?!Python|C|Web)'` 无旧引用残留。
4. 用 `D:\Miniconda\envs\bluemsun_env\python.exe`（或各项目对应解释器）跑一次各项目入口（如 `manage.py check`）确认可启动。

## 注意/风险

* `C` 与旧小写目录 `c` 在 Windows 大小写不敏感，必须先移入 `c` 再放其它。

* 重建 venv 需联网安装依赖；个别项目无 requirements.txt 时仅提示、保留备份。

* 移动整个 `.git`（Writerworks）后其 origin 仍指向占位 URL，无需修改。

