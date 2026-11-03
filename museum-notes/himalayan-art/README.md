# 喜马拉雅艺术

数据驱动的亲见作品录：六章、24篇细读、112条首版记录（111条作品／组合与一条佛堂陈设）。这些数字是首版概况，不是程序上限。

## 构建与检查

在仓库根目录运行：

```sh
python3 scripts/build_himalayan.py
python3 scripts/check_himalayan.py
python3 scripts/check_himalayan_browser.py
```

全站入口构建 `python3 scripts/build_museum.py` 最后调用本生成器。沿用 `museum.css`、Caravaggio 图片查看器、既有字体和纸色，不新增前端依赖。浏览器检查需要已有 Playwright Chromium；测试截图放 `/tmp`，不发布。

## 数据与稳定地址

- `data/works.json` 是公开作品允许清单；`w…/` 为稳定作品页。它保留作品身份、多个地域候选、收藏与展出机构、照片映射、资料证据，以及 `site_links` 跨专题实体对应。
- `data/reading_units.json` 与 `chapters.json` 分开管理细读和目录。`u…/` 为稳定细读页；仅入目录的作品无需长文。
- `data/photos.json` 仅含作品映射允许的129张自拍；`images/originals/` 保留原JPEG和SHA-256，400／900／1600 WebP不裁切、不升采样。细节图的具体图注在 `photo_captions.json`。
- `data/sources.json` 保存外部书目／馆藏链接。正文短注链接到页末完整题名。未加入交接包内OCR、联系表、研究核对页或书页图像。
- `data/places.json`、`map_groups.json`、`museums.json` 生成地图、列表和筛选。`navigation.json`、`derivatives.json` 是构建产物，不手改。
- `map_associations` 区分地域、候选产地和风格联系；`display_museum_id` 用于实际观看地图，`collection_museum_id` 用于独立收藏列表。`map_enabled:false` 的佛堂不落点，仍入目录。对同框、借展及来源不确定性用 `reader_notes` 呈现；不直接渲染 `editorial_notes`。
- `introduction.json` 保存用户原文的三段缘起、题记与译者署名。诗句已与中国藏学研究中心文章中的引句核对；该站HTTPS证书异常，本轮链接采用可访问的同页HTTP地址。
- `visits.json` 保存明确参观日期与新观察；`updates.json` 独立记录作品新增、研究更新或重访札记的发布日期。未知参观日期保持空缺，不采用上传文件名日期。
- 地区控件由 `map_groups.json` 生成大区域、`places.json` 生成关联地区／寺院。单一成员的分组不再重复显示第二级。`filter_label` 只改变控件显示名，稳定ID与 `?region=ngor` 等旧链接继续有效。

## 原始素材与公开范围

来源为本地 `Himalayan_Art_Codex_Handoff.zip`，原包及解压目录均未改动。五条题外作品及其十张照片没有导入。独立展签的 `do_not_publish:true` 优先于一般“现场资料”展示建议：这些JPEG继续留在本地 `reference_labels/`，网页用折叠文字整理资料；照片本身含作品局部与展签的混合图，只有明确进入作品映射且允许公开时才保留。公开目录不是整个压缩包的镜像。

本轮逐张检查22张联系表，并复核主要展签。另见 `data/corrections.json`：吉美MA1089为布本绘画，虚舟银镶衣缝佛为15世纪。两处均纠正了交接数据。完整的来源史及铭文释读未由这些基础记录替代。

## 以后补充

1. 先以馆号、题名和照片匹配旧件；重访保留原work_id，增加photo_id，勿另建一件。
2. 新作品复制相近记录，填写材料、原文题名、年代标签、来源及地域关系。设置 `tier:catalogue`，`reading_unit_ids:[]` 即可先入目录。
3. 原JPEG放 `images/originals/{photo_id}.jpg`；在 `photos.json` 记录哈希、尺寸、用途、work_ids及可确认的visit_id。独立展签继续保留本地，不绕过公开标记。
4. 新机构写入 `museums.json`；馆名列表、过滤选项、编号地图标记自动出现。仅收藏者不自动算作拍摄展馆。未知坐标不落点。
5. 新地区加入 `places.json`，按需要加入 `map_groups.json` 的成员。未归组地区会自动生成扩展区域入口。地图使用约略区域坐标，非作品出土地。
6. 在 `reader_notes` 写面向读者的具体问题；断代变化保留 `date_history`；不要把编辑约束塞进正文。
7. 更新细读时改正文和照片映射，不改变稳定URL；重新构建并检查。

检查脚本包含隔离临时目录中的新作品、新馆与重访照片试验，测试数据不会写入公开站点。

### 最近新增与重访

首页在完整目录前显示最多三条公开更新；没有记录时连同首屏快捷入口一起隐藏。当前两条是2026-11-03首版核对展签的真实资料更新，不是新近到访记录。

`updates.json` 每条包含 `update_id`、`published_on`（资料发布日，YYYY-MM-DD）、`kind`（`new`／`research`／`revisit`）、`work_id`、`summary`、`visit_id`（可空）、`source_ids` 和 `public`。更新使用作品原有ID，自动链接作品页。

一次重访可在 `visits.json` 添加 `{visit_id, work_id, visited_on, photo_ids, observation, public}`：日期仅在确知时填写，否则用 `null`；`photo_ids` 指向独立照片记录，并同时加入原作品的照片列表。公开的 `observation` 自动出现在该作品的“重访札记”段落；更新条目通过 `visit_id` 可直接跳到它。照片、研究来源与作品基本资料仍在各自数据文件维护。

构建检查验证所有引用，并在临时副本中测试新馆、新地区、新作品、重访照片与观察、更新显示及空列表隐藏，不修改正式目录。页面、脚本和导航数据带同一内容版本，减少发布后旧缓存与新控件混用。

## 地图与已知资料限度

底图沿用 Homer 的 Natural Earth 1:110m land；河道沿用早期佛教专题的 Natural Earth 1:10m Rivers + lake centerlines 5.0.0（0.02度简化）。两者公共领域，链接：https://www.naturalearthdata.com/about/terms-of-use/ 。河道是现代地理参照，不复原历史河道；没有绘制传播路线或古代疆域。

仍待核：佛堂的确切展出机构；44-18旅行佛龛制作地域；故宫、大英、柏林借展照片的实际观看馆；部分仅有展签的单件馆录及铭文全文。1726说明段疑似错配，只采用文殊的基本题名、年代、地域。金贝尔与西雅图部分馆藏页本轮被站点访问保护阻拦，保留已有配对展签与原馆藏链接；不声称独立核读了无法打开的页面。

## 深读与背景导览，2026-11-03

本轮扩展至25篇细读，作品仍为112条。`w1552/` 是四臂文殊的唯一作品记录，新细读使用 `u25/`，在第三章中排列，既有单元不改ID。`u10/` 扩充法冠自身的仪式与纪年研究，保留塔约比较。

- `reading_units.json` 可选 `lead`、`lead_source_ids`、`sections`、`notes`、`comparison_intro` 和 `featured`。每个段落为 `{text, source_ids}`；资料注折叠，来源由生成器去重并集中列出，正文保留就近短注。没有这些字段的旧单元继续原样生成。
- `history.json` 独立存两条时间线和八个节点，生成 `history/`。每个节点包含时期、三个关键词、段落来源与 `{work_id, relation}` 关联；缩略图、作品名称及年代复用作品主数据。这里的宽分期不会覆盖作品的馆方断代。
- 所有关联作品页自动生成返回相应背景节点的链接；来源通过稳定锚点查阅。时间线采用原生 `details`，无JS也能展开；JS仅负责由作品深链接进入时打开对应时期。桌面双列按大致时代并看，手机按西藏、尼泊尔顺序纵排，不做等比例年代图。
- `RESEARCH_PLAN.md` 是本轮十组后续优先级、已有证据和待查问题的编辑清单，未将未研究内容挂作公开空栏目。

研究核对：CMA馆藏页与公开API用于1964.370的持物、78.1×67.6厘米尺寸和1964年Klejman购藏记录；未独立核读API列出的整套书目。吉美MA4929的法文官网与现场展签均含有色玻璃，英文页作水晶，差异保留。Juramie／Meahl-Blöndal论文已阅读页461–470；Graldi的Rubin文章用于通行祭司背景，但其主对象是另一顶大都会法冠，不挪用其毗卢遮那解释替代吉美的金刚萨埵说明。铭文完整释文、人名与寺名仍未取得。历史背景依据Met、Rubin各篇具名研究与CRCAO研究项目说明，具体来源放入sources.json。

未新增或改动任何照片；外部研究PDF与私用展签仍留在仓库外。生成器会更新所有本专题HTML的资源版本，因此差异文件数量大于实质扩写页数。

验证：全站生成器、专题139页内链与图片哈希、隔离增补试验、1440／390／360像素实际Chromium检查均通过；另人工查看两篇深读、时间线收起／展开及手机截图。正文来源已通过浏览检索或直接PDF阅读核对；脚本复查外链时Rubin返回403、Met返回429，属于自动访问限制，未将其误报为404失效。网页保留对应官方地址。首屏初始仅请求2张衍生图片，未加载原图；研究书页与外部作品图片均未加入提交。
