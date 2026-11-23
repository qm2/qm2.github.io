# 数据使用说明

`catalogue.json`为本包唯一主档案。其余列表、CSV、GeoJSON由它派生，实施时避免多处独立修改。

| 字段或文件 | 含义 |
|---|---|
| id / route | 稳定j01—j62；所有索引、地图、年表指向同一作品页 |
| publish_title | 对外标题；j62已依用户补充比对更新为最澄坐像 |
| title_zh | 工作目录名，可能含候选信息；发布以publish_title为准 |
| collection_museum / museum_code | 收藏机构或私人所有者，与亲见馆分开；NEUBARDT为j62私人所有者 |
| viewing_museum / viewing_museum_id | 实际观看地点；j01与j02已由用户确认在MFAH |
| photo_manifest.csv | 全部149张原图的路径、角色、尺寸与SHA-256；未改变原图字节 |
| photos / labels | 全部现场图与展签；j04、j05共用两张图，不重复计数 |
| personal_highlight | 用户称印象较深，不代表有序排名或全部最爱 |
| curatorial_addition | 本轮另选9条，理由见research/editorial-selection.md |
| favorite / personal_observation | 保留空；整体感受见序言，不伪造逐件用户原话 |
| is_wood_figure | 是否列为木雕造像核心；青铜j08及器物j18、j60不在单尊木雕统计中 |
| material_group | 区分青铜对照与木及混合材料；与是否人物造像是不同问题 |
| date_display | 保留约年、跨度、官网与展签不同版本 |
| year_start / year_end | 检索用范围，不是新增学术定年；不能以中值显示成确年 |
| timeline_enabled | 现62条均为true；保留范围，j62为13世纪，非人物生卒 |
| person_year_start / person_year_end | 人物生卒，与雕像断代分开；j24生年差异另见person_life_note |
| visit_date | 全部为空，文件名导出批次不是参观日期 |
| source_urls | 单件原始来源；文稿另以source_registry.json中的来源标识对应脚注 |
| is_comparison_only | j08青铜例，作为材质与收藏史旁读 |
| is_ritual_object | j18太鼓架与j60家用佛坛，不能当作单尊佛像 |
| viewing-museums.geojson | 15处本批实际观看馆址，覆盖62条档案 |
| lending-collections.geojson | 2处仅列收藏机构，默认关闭，不代表本批到访 |
| historical-context.geojson | 8处历史语境点，relation_note区分来源、原寺关联与信仰背景 |

馆址为约略馆区中心，不是实测入口。地图支持列表回退；历史关联点不应被自动连成文物流转路线。
