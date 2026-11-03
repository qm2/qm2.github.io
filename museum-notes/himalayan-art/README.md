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
- `visits.json` 留作明确参观日期与新观察的独立记录。未知参观日期保持空缺，不采用上传文件名日期。

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

## 地图与已知资料限度

底图沿用 Homer 的 Natural Earth 1:110m land；河道沿用早期佛教专题的 Natural Earth 1:10m Rivers + lake centerlines 5.0.0（0.02度简化）。两者公共领域，链接：https://www.naturalearthdata.com/about/terms-of-use/ 。河道是现代地理参照，不复原历史河道；没有绘制传播路线或古代疆域。

仍待核：佛堂的确切展出机构；44-18旅行佛龛制作地域；故宫、大英、柏林借展照片的实际观看馆；部分仅有展签的单件馆录及铭文全文。1726说明段疑似错配，只采用文殊的基本题名、年代、地域。金贝尔与西雅图部分馆藏页本轮被站点访问保护阻拦，保留已有配对展签与原馆藏链接；不声称独立核读了无法打开的页面。
