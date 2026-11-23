# 帕拉黑石造像

24件作品、48张作者现场照片；20件核心、2件地域延展、2件前史比较。五条阅读线索、24篇短文、神话参考、历史导览、四组并看、十二家观看博物馆的地图与完整图录。

## 编辑与生成

- `data/catalogue.json`：作品身份、照片配对、专题分组和观看信息。九条 `canonical_ref` 在构建时读取 `../himalayan-art/data/works.json`，不另造藏品身份；保留原作品ID和双向入口。
- `data/media.json`：48张原片的文件名、SHA256、角色及响应式尺寸。照片文件名不作为参观日期。
- `data/readings.json` / `stories.json` / `chapters.json`：中文短文、故事、首页编排。
- `data/museums.json`：实际观看馆址；作品收藏机构另列。地图不代表古代制作地或出土地。
- `content/guide.md`：历史与观看。
- `data/sources.json`：具体来源、查阅范围、核对日期。`[[来源ID]]` 生成短引用，原资料集中列在资料页。
- `data/atlas-index.json` 是生成文件，不直接编辑。
- `pala.css` 和 `pala.js` 仅影响本专题。沿用网站字体、底色、图片查看器；地图复用 Natural Earth 公有领域底图，键盘可操作，缺少脚本／底图时仍保留图录和馆址链接。

从仓库根目录运行：

```sh
python3 scripts/build_pala_stone.py
python3 scripts/check_pala_stone.py
python3 scripts/check_pala_browser.py http://127.0.0.1:8774
```

整站生成：`python3 scripts/build_museum.py`。本专题生成器在南亚入口生成器之后执行，保留主首页与南亚艺术的入口。共用作品的返回入口由 `build_himalayan.py` 读取本专题目录生成。

## 照片与发布

素材包与原片留在仓库外的 `museum/pala-black-stone-handoff/`；`scripts/prepare_pala_images.py` 从原片生成 WebP，不裁切、不补画、不改变颜色。48张原片和144张衍生图放在既有R2域名 `images.mertonmuseum.com/museum-notes/pala-stone/`，不把图片二进制再放进Git。

本批新照片补充了旧记录，而不是覆盖旧照片。要添加未来重访：将照片加入media并绑定已有ID，记录实际提供的观看日期；不要复制同件作品。新作品加入catalogue/readings，相应博物馆若为新馆再加入museums；数量、筛选项、地图数据由构建生成。

## 本轮核对

作者确认：3264、3266、3268、3270均在MFAH的Living with the Gods借展中拍摄；3276在纽约大都会，3298在新奥尔良。日期未提供，留空。两件同题八大事迹碑分别为Met 2009.541与SAMA借展L.2019.4.1。

檀香山展签清晰记有4315.1，题为童子文殊，未给具体产地和石种，列为相关作品。阿克兰野猪化身的馆藏号尚待核录。私人收藏不补写未公布的编号和原寺院。
