# 增量核验记录

基线 `6510ec4c041c0b115f82f63ed0817056b75c8de7`。本轮完成6条来源线索核验并确认（`ycPr5-27vSI`、`bJ_seXo-Enc`、`P76Vbsk_3J0`、`FlQYU3m1e80`、`dX9CGRZwD-w`、`d6Pcp944sRI`）；完成50条原片搜索，其中7条确认（`d-ruFmgTpqA`、`d6Pcp944sRI`、`eR34r7HOU14`、`f8DQSM-b2cc`、`fAxHlLK3Oyk`、`fCd6B5HRaZ8`、`fT4lDU-QLUY`）；43条待审。本轮无网络异常或风控停止，全部50条原片均正常完成初筛。

净增9条原片、13个版本，没有撤回。标题复核覆盖全部新增版本，未发现集数或衍生内容冲突。13个新增版本实播通过，时长与分P完全一致。数据校验、65项单元测试和构建检查通过。未做逐帧对比。

当前处理4486条，确认1014条、1376个版本；全库覆盖率15.71%，全部已处理原片匹配率22.60%，本轮新增处理队列匹配率14.00%。仍有1968条未处理、3472条已处理但未确认。

## 2026-11-07 当前进度与暂停

最近一次公开版本为 `0130227`，含1063条确认原片；Pages曾核对 `data.json` SHA-256一致。本次按用户要求暂停全库核验。串行批次 `20261107T094313Z` 在50条配额中处理了6条，6条均待审、无请求错误，没有新增确认；进程已停止，剩余条目保留待续。

暂停时全库已处理5007/6454条，确认1063条。为发布最新统计，已重建根目录 `data.json`，确认版本内容未变，仅处理统计更新至5007；数据校验、65项单元测试、桌面/手机浏览器测试均通过。当前暂停状态写入本地忽略文件 `data/work/active-continuation.json`。恢复时先运行 `python3 scripts/search_health.py`，然后串行继续匹配；此前60条网络错误原片仍保留在阻塞清单，不自动重试，也不判为失效。

## 2026-11-07 恢复后进展

用户恢复全库任务后，搜索健康检查通过。批次 `20261107T124214Z` 完成4条（3条待审、1条确认）后在原片 `7GhAuZH6phs` 遇到 `URLError` 停止；该原片加入本地阻塞清单，当前共61条，不判失效、不自动重试。新增确认项为 `74Ig_QKndvE` → `BV1VZ4y1i7rb`，简介含明确原片链接，分P时长1860秒与原片一致，真实播放和CID检查通过，元数据哈希已记录。恢复后总计处理5011条、确认1064条；此次发布后 Pages 将更新确认统计。


## 2026-11-07 恢复后增量二

批次 `20261107T124800Z` 在第37条处理 `9IEFD_JVYd0` 时遇到 `URLError` 并停止；本批完成37条（35条待审、2条确认），剩余12条未处理。失败ID已加入本机阻塞清单，累计62条，未判失效、未重试。

新增确认：`7qZl_5xHoBw` → `BV1qKDtYgEPa`（Joe Rogan Experience #2223 - Elon Musk，9521秒）；`8ucCxtgN6sc` → `BV1Lx411g7gq`（TEENS REACT TO WINDOWS 95，507秒）。两条B站简介均有明确原片URL，均为单P且时长完全一致。真实播放检查通过，播放器实际请求CID分别为 `26620398704`、`25041042`。复核证据见 `reports/metadata-review-2026-11-07-resume2.json` 与 `reports/playback-increment-2026-11-07-resume2.json`；未做逐帧比较。

当前工作库进度5048/6454，确认1066。本增量已由提交 `624dbe5fc200687604b2f7ecfdfd4b65dfdd5976` 推送；Pages `data.json` 返回HTTP 200，SHA-256 `9a935e01bc7b135d4340a8d2f8315cec28dcfe872145d1ebeefe0fe2b16ae1ae` 与本地一致。


## 2026-11-07 恢复后增量三

批次 `20261107T134536Z` 在第20次尝试处理 `9x4_dozWkq0` 时遇到 `URLError`，此前完成19条（17条待审、2条确认），剩余30条未处理。失败ID已加入本机阻塞清单，累计63条，未判失效、未自动重试。

新增确认：`9KivesLMncs` → `BV18a4y1S7pt`（Alan Kay on Dijkstra，159秒）；`9T1vfsHYiKY` → `BV1Lz4y1d7mZ`（Shagged by a rare parrot，152秒）。两者简介均指向对应原片，单P、分P身份和时长已从公开详情核对；元数据快照证据见 `reports/metadata-review-2026-11-07-resume3.json`。两条均通过真实播放检查，播放器时长分别为159秒与152秒，实际请求CID分别为 `1330298511`、`192580245`；本批发布前检查待完成。

当前工作库进度5067/6454，确认1068。本增量已由提交 `a24c700e258e00d112db573420a577dc39b09da9` 推送；Pages `data.json` 返回HTTP 200，SHA-256 `db3980b27ccd6e0f4bd3b5a2c2325133290320075adc409a175121b299675c61` 与本地一致，详情见 `reports/pages-check-2026-11-07-resume3.json`。


## 2026-11-07 恢复后增量四

批次 `20261107T141047Z` 完整处理50条：42条待审、8条确认，0请求错误、0未处理。新增确认依次为 `9yW--eQaA2I` → `BV1cGSbBrEJ9`、`A8dqzVlhFkA` → `BV1Mx411672f`、`ADqLBc1vFwI` → `BV13A411H7iz`、`AEtbFm_CjE0` → `BV1k7421N78B`、`Aaxw4zbULMs` → `BV1Bs411C74k`、`B8R148hFxPw` → `BV1ZE411u7w5`、`BKorP55Aqvg` → `BV18t411y7Ge`、`BYVZh5kqaFg` → `BV1sdypBJEyC`。每条均有匹配原片ID的公开B站简介和单P详情，时长差在规则阈值内；8条实播均通过，实际CID可见。中文AI配音说明已记录，符合项目对完整中文配音的规则。元数据快照与播放器结果见 `reports/metadata-review-2026-11-07-resume4.json`、`reports/playback-increment-2026-11-07-resume4.json`；未做逐帧内容比较。

当前工作库进度5117/6454，确认1076。本增量已由提交 `addc2b6a13e0c46b951cdf5ec3684031e74f662d` 推送；Pages `data.json` 返回HTTP 200，SHA-256 `d17994e9a834091da52f4e1ae6c4c628d278f58cc50760cd52c0bcb1b76986b0` 与本地一致，8条新增版本均已在线核验，详情见 `reports/pages-check-2026-11-07-resume4.json`。


## 2026-11-08 恢复后增量五

批次 `20261107T151617Z` 在处理第47次尝试 `DkUpZkeqhF4` 时遇到 `RemoteDisconnected` 后停止。此前完成46条，其中43条待审、4条确认；另有3条未处理。失败ID已加入本机阻塞清单，累计64条，不判失效、不自动重试。

新增确认：`CMdHDHEuOUE` → `BV1Yx411k7un`、`CZ3wIuvmHeM` → `BV1DM4y1f7xF`、`CzwtCBj5jEs` → `BV1bbaT6EETt`、`D2SoGHFM18I` → `BV1Dx411V7Ut`。四条B站简介均含对应原片ID，均为单P且时长差在容差内；实播全部通过，实际CID与记录一致。元数据和播放器证据见 `reports/metadata-review-2026-11-08-resume5.json`、`reports/playback-increment-2026-11-08-resume5.json`；未做逐帧内容比较。

当前工作库进度5163/6454，确认1080。本增量已由提交 `1afdb8afbb5d3dd07807a41c7ba97486148ad2ec` 推送；Pages `data.json` 返回HTTP 200，SHA-256 `067b6ad5dce9f2790c5d895f3811a2850eaf94402885658a7f380d31dbdde43f` 与本地一致，4条新增版本均已在线核验，详情见 `reports/pages-check-2026-11-08-resume5.json`。

## 2026-11-08 恢复后增量六

批次 `20261107T161601Z` 串行完成50/50，0请求错误、0未处理；48条待审、2条确认。此前64条网络错误原片均继续排除，没有自动重试。

新增确认：`FZ6lZJWL_Xk` → `BV1jg411A7gQ`（Tesla Unveils Dual Motor and Autopilot，828秒）；`FaOSCASqLsE` → `BV1FW411i7mF`（Star Wars Undercover Boss: Starkiller Base - SNL，291秒）。前者为单P，分P名称含精确原片ID；后者为单P，完整简介含精确YouTube原片URL。原片时长和分P时长均一致。实播均通过，播放器请求CID分别为 `464618595`、`30228166`，播放器时长均与分P一致。元数据、简介和播放器证据见 `reports/metadata-review-2026-11-08-resume6.json`、`reports/playback-increment-2026-11-08-resume6.json`；未做逐帧内容比较。

当前工作库进度5213/6454，确认1082；本增量发布前校验、65项单元测试、桌面/手机浏览器检查和实播核验均通过。提交 `7744f3186c4858af89173872cce0253569543a3f` 已推送；Pages `data.json` 返回HTTP 200，SHA-256 `2cfd654e4339fb5c85bd89721ae30823ef4dd36e4a6526039a635cbfd64a23c2` 与本地一致，两条新增版本均在线核验，详情见 `reports/pages-check-2026-11-08-resume6.json`。

## 2026-11-08 恢复后增量七

批次 `20261107T171059Z` 在第19次尝试处理 `G6D1YI-41ao` 时遇到 `URLError` 后停止。此前完成18条（17条待审、1条确认），另有31条未处理。失败ID已加入本机阻塞清单，累计65条；不判失效、不自动重试。

新增确认：`Fpu5a0Bl8eY` → `BV1884y1V7m9`（NENA | 99 Luftballons [1983]，235秒）。B站完整简介含对应 `youtu.be` 原片链接，单P，原片与分P时长一致，标注德语版中文字幕。实播通过，播放器实际请求CID `1004042987`，实测时长235秒。元数据和播放器证据见 `reports/metadata-review-2026-11-08-resume7.json`、`reports/playback-increment-2026-11-08-resume7.json`；未做逐帧内容比较。

当前工作库进度5231/6454，确认1083；本增量发布前数据校验、65项单元测试、桌面/手机浏览器检查和实播核验均通过。提交 `0f9a66e7796c8a21f708fb605d77fe4d6ddb060d` 已推送；Pages `data.json` 返回HTTP 200，SHA-256 `4409ff18026e9417a4be17ed96b2525163145989a8ec48c204079102b0bac613` 与本地一致，新增版本已在线核验，详情见 `reports/pages-check-2026-11-08-resume7.json`。

## 2026-11-08 恢复后增量八

批次 `20261107T173102Z` 在第31次尝试处理 `HMGIbOGu8q0` 时遇到 `URLError` 后停止。此前完成30条（28条待审、3条确认），另有19条未处理。失败ID已加入本机阻塞清单，累计66条；不判失效、不自动重试。

新增确认：`GYkq9Rgoj8E` → `BV1EM4y1v7eK`（WWDC 2023 — June 5，7571秒）；`GeCP-0nuziE` → `BV1DRoQYjE49`（The TRUTH About How LTT Makes Money，991秒）；`H8eP99neOVs` → `BV13a411Y7SN`（Focusing is about saying no，184秒，对比原片186秒）。三条B站完整简介均含对应YouTube原片URL，均为单P且在时长容差内。实播全部通过，播放器实际请求CID依次为 `1154298918`、`29105328091`、`718087353`，实测时长与分P一致。元数据和播放器证据见 `reports/metadata-review-2026-11-08-resume8.json`、`reports/playback-increment-2026-11-08-resume8.json`；未做逐帧内容比较。

当前工作库进度5261/6454，确认1086；本增量发布前数据校验、65项单元测试、桌面/手机浏览器检查和实播核验均通过。提交 `3f391420f8650a0f565a55e88c0ea5b82e9000ad` 已推送；Pages `data.json` 返回HTTP 200，SHA-256 `d0cf80fd3def66b83cfbb32225b3da4c4b78cc8708c566f543fc05450957f20a` 与本地一致，3条新增版本均在线核验，详情见 `reports/pages-check-2026-11-08-resume8.json`。

## 2026-11-08 恢复后增量九

批次 `20261107T180533Z` 在第37次尝试处理 `IrHRQSm6LIs` 时遇到 `URLError` 后停止。此前完成36条（35条待审、2条确认），另有13条未处理。失败ID已加入本机阻塞清单，累计67条；不判失效、不自动重试。

新增确认：`Hrbq66XqtCo` → `BV1XSoDBgEVg`（Jensen Huang – Will Nvidia’s moat persist?，6193秒）；`ISznqY3kESI` → `BV1Yi4y1f7Nc`（RHex Rough-Terrain Robot，105秒，对比原片113秒）。B站完整简介均含对应YouTube原片URL，均为单P且时长差在容差内。实播均通过，播放器实际请求CID `37807260392`、`505254418`，实测时长与分P一致。证据见 `reports/metadata-review-2026-11-08-resume9.json`、`reports/playback-increment-2026-11-08-resume9.json`；未做逐帧内容比较。

当前工作库进度5297/6454，确认1088；本增量发布前数据校验、65项单元测试、桌面/手机浏览器检查和实播核验均通过。提交 `65f7ddac452635256ee21ff14115b4e279f3ead9` 已推送；Pages `data.json` 返回HTTP 200，SHA-256 `e28f22435637390c3c0196ddbac0c1c460645a3ac611abd81d9d722db0cee471` 与本地一致，两条新增版本均在线核验，详情见 `reports/pages-check-2026-11-08-resume9.json`。
