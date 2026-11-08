# 罗马石棺：石棺上的故事

静态专题，复用 museum.css 与已有 Caravaggio 图片查看器；roman.css / roman.js 仅作用于本专题。

## 数据与构建

- `data/works.json`：24条作品记录；r01–r23保留交接ID，r24为从1930照片重新核实的梵蒂冈942号。收藏、观看机构、馆内位置、制作地、发现地分开。未知字段留空，参观日期不来自文件名或确认日。
- `data/photos.json`：60张原片及5个诚实裁切的来源、SHA256、方向、裁切框与响应式资源。1931共享于r13/r23/关联棺盖，原片只存一份。
- `data/editorial.json`：细读、图注相关研究与资料注；`sources.json`保留来源读取范围、限制和本轮补充记录。
- `data/sections.json`、`comparisons.json`、`museums.json`：五条主题线、比较组、现代观看地点。地图、时间线、卡片数量从作品数据计算。
- `data/history.json`：历史与观看导读、制作传统对照表、现场六问与阅读范围；生成 `history/`。首页、24件作品与图录均有入口。`comparisons.json` 可包含有来源的分节札记，新增组 `battle-and-submission` 连接r11与r24。
- 图片仅为Merton自拍。1913展签衍生图顺时针旋转90°，原始JPEG不变。所有局部可回到原片。

```sh
python3 scripts/prepare_roman_sarcophagi.py  # 新照片/裁切的衍生图；需 Pillow
python3 scripts/build_roman_sarcophagi.py
python3 scripts/check_roman_sarcophagi.py
python3 scripts/build_museum.py            # 完整博物馆站点；包括本专题
```

新增作品：追加稳定ID、已有/新增museum_id、照片与来源、editorial记录，再加入相应章节。重访沿用原ID并追加照片，不增加作品计数。年代用date_kind区分circa、range、circa_range、period；宽时期的数值只帮助排序/定位，不替代文字断代。

图片生成器不会覆盖已有衍生图；调整裁切时请使用新裁切ID，以保留原记录并避免缓存混淆。不要改写原始JPEG。

## 配对修正与未决问题

- 1930与1931不是同一陈列。1930下方为942号；上方915号为巨人之战饰带，不计石棺；中层独立棺盖的编号及原配关系未确认。
- 1931下方933号、中央932号棺盖、上方914号前板是独立文物，932非933原配。914顶部在自拍里未完整入镜。
- 1922仅紧邻棺身、带铭文的完整横条按NASSCAL对应为本件棺盖；照片最上方两块残片配属未知。
- r09馆藏号待核，251是图录编号。r23年代采用参考图像档案，并非现行馆方记录。
- 休斯顿酒神前板及豹侧板为同一原石棺；现行两页均定180—195年，现场展签“2世纪晚期”单独记录。

原交接包文本与未经改写的清单在 `docs/roman-sarcophagi/handoff/`，不可当作当前权威数据覆盖以上修正。研究过程与实际读取范围见同目录research-*.json。网页不使用第三方作品图或书页。
