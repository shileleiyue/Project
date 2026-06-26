# D:\ 全盘整理清单（核对稿）
说明：本清单纯属"规划核对"，不含任何执行。你确认后我再生成可执行脚本。
规则（已确认）：
  - 系统目录、app、A_Mycomputer 主体不迁出
  - A_Mycomputer：外部文件可移入，内部只做内部整理，绝不移出
  - 有语义中文名（音乐/PPT/作业）保留原名
  - 无意义名（截图/哈希/编号exe）按规则英文化

===================================================================
一、根目录已建英文分类目录 -> 重新分配（并入 A_Mycomputer）
===================================================================
以下分类目录中的个人文件，重新分配到 A_Mycomputer 或合适位置：

[Photos] -> 移入 A_Mycomputer\图片（班级/照片资料）
  25年级1班“我为同学做实事”成果展示.zip
  一班团辅照片.zip
  一班研学照片.zip

[Research] -> 移入 A_Mycomputer\文档\课题研究
  单变量统计（包含图片），交叉分析（包含图片），相关性分析，.zip
  图表.zip
  打包.zip

[Archive] -> 移入 A_Mycomputer\桌面（AI创作资料）
  AI映暖光1.zip
  AI映暖光2.zip

[Music\kugoumusic] -> 移入 A_Mycomputer\音乐\kugoumusic
  （内含 468 个音频，保留语义名不动）

[School] -> 移入 A_Mycomputer\桌面（学校录取/课程资料）
  B_24pdftool
  录取学校·概况
  计算机导论

[Misc] -> 移入 A_Mycomputer\下载\临时
  cmd_start_for.ini
  imsdk_report
  install.log

===================================================================
二、A_Mycomputer 内部整理（只进不出，内部移动+重命名）
===================================================================
1. 图片\Screenshots：481 张截图 屏幕截图 YYYY-MM-DD HHMMSS.png
   -> Screenshot_YYYYMMDD_HHMMSS.png   （清单：命名映射清单_截图.csv）

2. 图片：哈希匿名图片（0b15078f.png 等，在桌面/Camera Roll/课程目录）
   -> 按所在目录语义前缀+序号，例：
      桌面\0b15078f.png            -> Desktop_img_01.png
      东北师范大学\01580....jpeg   -> NEU_media_01.jpg

3. 文档目录：保留语义中文名
   （含迎新晚会.pptx、Word/Excel/PDF 等，有中文名不动）

===================================================================
三、可迁移应用处理（不可移动跳过，可移动归位）
===================================================================
[ 跳过-已安装实例（移动必失效）]
  IST（API等开发工具/Git/IntelliJ/MinIConda/Trae...）
  财经（EMWeb.exe 东方财富股票软件实例）
  app（已确认不动）
  game / SteamLibrary / WeGameApps（游戏库实例）
  Virtual Machine / LegionZone / A-STM32F407（工程+MDK）
  Lenovo / LenovoSoftstore / MapData（厂商目录）

[ 可移动-纯安装包/绿色件]
  LeStoreDownload 内 41 个 exe（联想商店下载的安装包/绿色件）
     -> 移入 A_Mycomputer\下载\软件安装包
  IST\安装包（含 installers：pycharm/conda 等）
     -> 移入 A_Mycomputer\下载\软件安装包
  编译器安装包 目录（Dev-Cpp/IDEA/JDK/VSCode 安装包）
     -> A_Mycomputer\下载\软件安装包（或将目录并入）
  根目录 BaiduNetdiskDownload / QLDownload / QLDownloadGame（若为空则跳过）

===================================================================
四、根目录散落文件（已清理完毕）
===================================================================
原本散落 zip/exe/ini 已按上一轮移动完成，无遗留。

===================================================================
待你确认的点
===================================================================
1. 英文分类目录(Photos/Research/Archive/Music/School/Misc) 并入 A_Mycomputer 后，
   这些英文目录本身是否删除？（A_Mycomputer 只进不出，删的是根目录空壳，不违反）
2. 哈希图片按目录前缀+序号命名是否可接受？
3. LeStoreDownload/IST安装包/编译器安装包 移入 A_Mycomputer\下载 是否正确？
4. 桌面上 6 个 ~$ 开头（Office 临时锁文件，如 ~$25013636.docx）建议删除或忽略？