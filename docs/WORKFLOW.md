# 数据、审核与发布操作说明

## 数据接口

- `data/source/videos.jsonl` 是完整原片库，主键 `vid`；原站导出不含时长，匹配时从原站公开视频详情获取核验所需时长，仅存本地缓存。
- `data/work/library.json` 按原片ID保存候选。每个候选以 `bvid` 识别，并记录定位后的 `page`、`cid`、时长、语言类型、依据、检查时间与状态。
- 状态为 `confirmed`（已确认）、`review`（待审核）、`unmatched`（未找到）和 `invalid`（已明确失效）。请求失败单独记录错误，不当作失效。
- 根 `data.json` 是前端接口：`schema_version: 1`，含 `stats`、有内容的 `areas`、`videos` 和旧BV到原片的 `legacy` 映射。视频以 `id` 为主键，`versions` 只包含确认且可用的分P版本；第一项为默认版本。
- 一个原片可有多个BV；同一BV可用不同分P对应不同原片。同一BV同一分P若指向多个原片，构建时全部隐藏，等待纠正。
- `data/confirmed.json` 保存最小确认记录与处理状态用于复现；待审核候选和接口原始内容仅存在本地，不会放入前端数据。

## 一次批量更新

先检查 Git 状态，备份本地 `data/work/`；不要同时运行多个匹配或审核进程。来源刷新会在本地保留上一版快照，Git保存已发布快照。

```sh
python3 scripts/fetch_source.py
python3 scripts/pipeline.py import
python3 scripts/pipeline.py match --limit 50
```

每批上限50条，优先已有候选，再按原站质量分排序。先依次搜索原片标题、作者加标题，每个查询最多取5个候选。串行请求至少间隔1.2秒；使用程序内临时访客会话，不读取本机个人Cookie。API成功响应缓存7天，过期后重新检查。

`match` 默认跳过已完成原片和已检查候选；中断后再次运行会从未完成条目继续。`--existing-only` 仅复核已导入的旧候选，`--recheck` 重新评估已有条目（仍复用未过期缓存）。更新前如需强制刷新某条接口，可移走本地对应缓存；不要清空缓存后大量重试。

HTTP 401/403/412/429及接口风控/登录代码会立即停止批次，退出码2。超时等普通请求错误记录后继续，最后也返回2。查看 `reports/STATUS.md`、`reports/summary.json` 与本地 `data/work/batches/`，解除阻塞后再人工触发。已完成条目不会丢失。

## 对应关系与审核

自动确认必须满足：B站简介明确指向该YouTube原片，分P可定位，原片和分P时长差不超过 `max(60秒, 8%)`，无年份、集次、明显删减或多个原片链接冲突。合集还要求分P标题与原片核心词吻合。相似标题、UP主名相同以及旧“高可信度”都不能单独作为确认依据。

以下流程由执行者真实检查资料或内容后操作，不得编造审核说明：

```sh
python3 scripts/pipeline.py export-review
python3 scripts/pipeline.py inspect 原片ID BV号 --page 2
python3 scripts/pipeline.py review 原片ID BV号 confirmed --page 2 --evidence '具体核验依据：片头作者、讲座名、对应集次及原片来源链接等'
```

`inspect` 获取指定分P详情并重新评估，支持添加手工找到的BV线索。无法定位分P、年份或集次冲突、明显删减的条目不能直接人工放行；先找到正确版本或修正对应数据。待审核和失效也可通过 `review 原片ID BV号 review` 或 `invalid` 标记。人工确认在后续复核中仅在分P的CID不变且没有硬冲突时保留。

选择语言版本时，“官方”字样不能证明账号归属；自动识别只有UP主名与原作者名规范化一致才标为官方。不同名称的官方账号需人工核实后修正本地候选类型，并留下依据。

## 构建、验证与发布

```sh
python3 scripts/pipeline.py build
python3 scripts/pipeline.py check
python3 -m unittest discover -s tests -v
node --check app.js
```

从本地候选构建；新克隆没有本地库时使用最小确认清单重建。构建复制 `web/` 中三个页面文件到根目录，公开数据不包含个人凭据、内部路径或待审详情。检查桌面和手机上的分类、搜索、版本切换、分P跳转、收藏及嵌入播放，再核对发布数据统计。

发布采用普通提交与普通推送到 `main`，由 GitHub Pages 自动部署；仅在任务授权覆盖发布时执行。推送前先获取远程状态并确认没有他人新增提交，不强推。发布后核对Actions状态、新网址HTTP状态和 `data.json` 的SHA-256与本地一致。

初始回退基线是 `65dfbd6e285e8f793f369b4107281cdc11ef6a03`。普通 `git revert` 对应发布提交可恢复上一版；不要重写历史。远程HTTPS无登录时可使用已配置的GitHub SSH认证，无需复制令牌。

## 当前限制

原站与B站元数据可能过期；简介链接和时长核验无法保证所有画面相同。真实播放抽查按验收报告记录，不把测试播放器地址成功当成视频已播放。分类翻译是本项目维护的展示层，保留原站ID以便增量更新。

取消时长门槛后，新匹配流程会正常处理短视频；首批旧候选主要是长视频，短视频覆盖需要后续批次。项目不运行定时任务，不承诺全库都存在B站对应版本。

## 搜索受限时的公开线索核验

搜索接口返回412后停止该批搜索。可以独立整理已获得的公开资料，不反复请求同一搜索端点：

```sh
# 只从本地缓存的公开合集元数据提取候选，不发起网络请求，不自动批准
python3 scripts/pipeline.py seed-related
# 逐个获取候选详情并核验，不调用B站搜索
python3 scripts/pipeline.py match --existing-only --limit 50 --delay 2
# 对已缓存证据重新应用匹配规则，不发起任何网络请求
python3 scripts/pipeline.py reassess-cached
# 核验公开网页里找到的线索文件，每批最多50个
python3 scripts/pipeline.py verify-leads data/work/web-leads.json --limit 50 --delay 2
```

线索文件是JSON数组，每项包含 `bvid` 或旧式数字 `aid`、公开来源 `url`；可附 `vid` 和 `page` 指定待核验的原片与分P。例如：

```json
[{"bvid":"BV1Ys411k7yQ","vid":"fNk_zzaMoSs","url":"https://www.bilibili.com/video/BV1Ys411k7yQ"}]
```

未指定原片时，只从详情中的原片URL、明确的 `YouTube: ID` 标注，以及分P文件名或有明确标题分段的简介中识别原片ID。网页索引、推荐合集和标题相似度都只提供候选；仍需原片身份、分P、时长和冲突检查。

合集简介中的“上篇／下篇”或“P1／P2”若分别明确标注原片ID，只能将该ID用于相应分P。文件名保留 `[原片ID]` 或末尾 `-原片ID` 时可用于定位；不能从合集总时长或分P顺序猜测。手工指定分P会锁定选择。

`verify-leads` 的详情请求若也出现风控，会锁住后续详情批次。先检查并归档本地 `lead-receipt.json`，确认环境恢复后再由人工触发；不要自动清除锁定或循环重试。执行回执与搜索受阻情况会纳入进展报告。
