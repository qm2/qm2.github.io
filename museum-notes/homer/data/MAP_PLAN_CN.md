# 霍默艺术地理地图：实施说明

这张地图不是“霍默画作的精确创作地点地图”。它是**个人专题的题材地理索引**：让读者理解一个热爱山林、湖泊、海岸的画家如何游历不同环境。地点以**宽泛区域位置**呈现，出品坐标在 `locations.json`。

## 交互设计

- 网页正文在序文后放一张互动地图，地图两种显示视图：**大西洋全览**（美国东北部、英国、加拿大和加勒比）及 **北美东北部放大**。
- 点击地区 pin → 弹出地点简介 + 该地所对应的**用户自拍作品缩略图**和中文章节链接。收藏馆所在地**不是**作品风景地点。
- 地点 filter：海岸 / 森林&独木舟 / 河流&动物 / 南方暖光。与正文画廊筛选可以共享地域标记。
- 清晰显示“地点为区域示意，非作品的精确作画坐标”。鼠标/触摸用户都能使用，手机上支持缩放与列表 fallback。
- 用户已有地图组件时复用；如果没有可以用轻量 Leaflet + OpenStreetMap（网络受限时需要可阅读的静态降级页），不要额外安装大而全的地理动画库。

## 地理名称和注意

- **阿迪朗达克山脉，纽约州**：`The Blue Boat`, `Adirondack Lake`, `Old Settlers`, `Woodsman and Fallen Tree`。
- **Lac Saint-Jean（圣让湖），魁北克**：加拿大钓鱼系列、`Grand Discharge`。对部分主题只标到湖区，不能指定某处河湾。
- **Mashteuiatsh / Pointe-Bleue，魁北克**：Innu 社群相关作品；网页保留展签历史英文名，但正文使用“Innu（因努）社群”，不将历史的 Montagnais 与所有加拿大原住民族混同。
- **缅因州南部海岸 / Prouts Neck**：海浪、漂木、沙丘；Old Orchard Beach 是独立海滩，若需要详细视图可另做点。
- **Gloucester，马萨诸塞州**：渔船、水彩与小艇。
- **Cullercoats、Tynemouth、Bridlington 和 Flamborough Head，英格兰东北部**：渔民与海岸画，有些作品具体海滩只以展签为准。
- **Santiago de Cuba，古巴**：街角与海关建筑。
- **Bahamas / Nassau / Fox Hill**：Fox Hill 的地点较明确，但《The Sponge Diver》无法由照片证明精确海岸位置，保持宽泛定位。
- **Bermuda，百慕大**：海岸。
- **Florida / Everglades，佛罗里达**：Palm Trees、湿地与猎人；不是同一地点。

## 源码数据

`locations.json`：可遍历的区域锚点；`works.json`：逐幅作品含 `region` 键。请不要擅自添加每幅画的精确拍摄或创作坐标；标签 `precision=conceptual` 或 `unknown` 的点默认不显示 pin。
