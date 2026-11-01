# Winslow Homer 水彩展素材包（供 Codex 建站使用）

**来源**：用户在休斯顿美术馆 MFAH《Of Light and Air: Winslow Homer from the Museum of Fine Arts, Boston》展览现场自行拍摄的照片。展览日期：2026-11-01 至 2027-02-07（请以馆方官网为准）。

## 已完成的整理

- **215 张 JPG，全部保留且只存一份**。原始图像字节未裁切或修色，按作品/展厅/策展文字/历史材料分类。
- **67 条作品/成组展品记录**，其中有两件同框作品和个别“after Winslow Homer”版画，不能一概声称都是霍默亲笔原作。
- **30 条主展推荐**：23 件核心候选 + 7 件解释媒介和历史背景的配套作品；主展中推荐 12 件写较深入的赏析，其他简写。详见 `editorial_shortlist.json`。
- **完整档案**：所有 67 条作品均可以进入可搜索的“观展目录”，但默认不应在正文逐条铺开。
- 展厅和文献辅助照片已分类（不建议全部直接公开展示）。
- 地图数据为**大致区域锚点**，不是作品实景的精确 GPS 坐标，尤其不能将“Florida”等州级地名作为具体画点。

## 使用顺序

1. 将整个 ZIP 解压到网站仓库之外的临时输入目录；**请 Codex 先阅读 `CODEX_PROMPT_CN.md`**。
2. Codex 先检查现有 `museum-notes` 的页面结构、布局、样式、组件、导航和图片路径，遵循现有网站设计，而不是重新发明主题。
3. 读取 `works.json` 和 `editorial_shortlist.json` 生成作品画廊；图片都在 `assets/works/<slug>/`。
4. 阅读 `SITE_OUTLINE_CN.md` 写序言、章节和交互地图；参考 `locations.json` 中的区分等级和备注。
5. 完成后人工检查所有图片是否与标题/展签正确匹配，并手动审核有疑义的几条早期版画或成组作品。

## 文件清单

- `assets/works/`：每件作品的 `main.jpg`、`label.jpg`，有特写的作品另有 `detail_*.jpg` 或 `alternate_*.jpg`。
- `assets/gallery/`：入口、展墙、走廊及展厅远景。
- `assets/exhibition-text/`：章节介绍展板（用于查证信息；**不要照搬长段展签文字**）。
- `assets/historical-material/`：水彩颜料、画箱、历史图录、展柜文献等（可在“技法”段落中精选使用）。
- `works.json / works.csv`：67 条作品及分组、媒介、主题地域、展示建议。
- `photos.json / photos.csv`：215 张图片一一对应的编号、原始文件名和新路径。
- `editorial_shortlist.json`：30 件主展作品，其中 12 件建议重点写。
- `sections.json`：七个章节的中文标题与功能。
- `locations.json / MAP_PLAN_CN.md`：地理标签及互动地图注意事项。
- `CONTACT_SHEETS/`：9 张浏览索引，编号 001–215 与 `photos.csv` 一致。
- `SITE_OUTLINE_CN.md`：内容与个人感受的编辑方案。
- `CODEX_PROMPT_CN.md`：可直接交给 Codex 的执行指令。

## 来源与审核提醒

用户自己拍摄的是原作现场照片，但照片的博物馆背景、展板文字、展柜文献和展厅环境仍应遵守馆方使用规则。不要改用官网或图录复制图片。霍默生于1836年、卒于1910年，不能因此自动推定馆方的展签、摄影或设计也都不受保护。

部分地理归属为策展主题上的**宽泛归类**（如“New York State countryside”“New England coast”），并非已核实的作画地点。`provenance_status` 仅说明转录信息来源，**不代表已学术核实收藏史**。前期图录/版画作品中，`after Winslow Homer` 应与霍默亲笔绘画区分。展签内容优先保留准确但用自己的语言概述，不要误写未读的学术论文。

馆方资料（供核验，不做作品图像来源）：
- https://www.mfah.org/art/exhibitions/of-light-and-air-winslow-homer-from-the-mfa-boston
- https://www.mfah.org/press/mfah-presents-watercolors-of-winslow-homer-from-renowned-holdings-of-mfa-boston
- https://www.mfa.org/exhibition/of-light-and-air-winslow-homer-in-watercolor
- https://www.mfa.org/press-release/of-light-and-air-winslow-homer-in-watercolor
