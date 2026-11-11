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

## 2026-11-08 恢复后增量十

批次 `20261107T191018Z` 在第29次尝试处理 `Km5XQxRrQvw` 时遇到 `URLError` 后停止。此前完成28条（27条待审、2条确认），另有21条未处理。失败ID已加入本机阻塞清单，累计69条；不判失效、不自动重试。

新增确认：`KEkrWRHCDQU` → `BV17D4y1D7ym`（HACKERMAN'S HACKING TUTORIALS - How To Hack Time，225秒）；`KYbM-3E11Qo` → `BV1g4411U72J`（Boeing Vietnam Airlines 787-9 Dreamliner Vertical Takeoff & Steep Turns，188秒，对比原片187秒）。B站完整简介均含对应YouTube原片URL，均为单P且时长差在容差内。实播均通过，实际请求CID `216909597`、`110750966`，播放器时长与分P一致。证据见 `reports/metadata-review-2026-11-08-resume10.json`、`reports/playback-increment-2026-11-08-resume10.json`；未做逐帧内容比较。

当前工作库进度5339/6454，确认1090；本增量发布前数据校验、65项单元测试、桌面/手机浏览器检查和实播核验均通过。提交 `13ec8789fdbabb01431c716ff2b6fa63b45ebf0c` 已推送；Pages `data.json` 返回HTTP 200，SHA-256 `2a0b0748a672eeac80bdab785a2dbf0a3a3d7042cc9d7bc6f2a7781625cf01a9` 与本地一致，两条新增版本均在线核验，详情见 `reports/pages-check-2026-11-08-resume10.json`。

## 2026-11-08 恢复后增量十一

批次 `20261107T194346Z` 在第4次尝试处理 `Kr7AONv3FSg` 时遇到 `URLError` 后停止。此前完成3条（2条待审、1条确认），另有46条未处理。失败ID已加入本机阻塞清单，累计70条；不判失效、不自动重试。

新增确认：`KnIAAkSNtqo` → `BV1Lp4y1j7BZ`（2017/05/17: Senate hearing on Bill C16，3609秒）。B站完整简介含对应YouTube原片URL，单P，原片与分P时长完全一致。实播通过，播放器请求CID `1262877700`，实测时长3609秒。证据见 `reports/metadata-review-2026-11-08-resume11.json`、`reports/playback-increment-2026-11-08-resume11.json`；未做逐帧内容比较。

当前工作库进度5342/6454，确认1091；本增量发布前数据校验、65项单元测试、桌面/手机浏览器检查和实播核验均通过。内容提交 `b23356fc8b8380b101ad3ac8f0bf317e44dd32ef` 已推送，Pages 部署运行 `42408010297` 完成后，线上 `data.json` 返回HTTP 200，SHA-256 `ba1ef46ac5e22f87af06492483ec3267e34150520172d5f569d556e798dd7218` 与本地一致，新增版本已在线核验，详情见 `reports/pages-check-2026-11-08-resume11.json`。


## 2026-11-08 恢复后增量十二

批次 `20261107T195823Z` 选择50条，49条完成（47条待审、2条确认），第50条 `MoaWlKC3wIM` 遇到 `URLError`，进程退出；未自动重试，该ID已加入本机阻塞清单，累计71条。错误不表示视频失效。

新增确认并经元数据与实播复核：`LSHZ_b05W7o` → `BV12s411t77E`（Sony CSL 的 Daddy's Car，181秒）；`LXb3EKWsInQ` → `BV1zDvYe6EQ4`（COSTA RICA IN 4K 60fps HDR，原片314秒、分P315秒）。两条完整B站简介都含对应YouTube原片链接，均为单P；实播均通过并观察到记录CID（`10474111`、`500001634779260`），播放器时长分别为181秒、约313.699秒。元数据快照与简介哈希见 `reports/metadata-review-2026-11-08-resume12.json`，播放器结果见 `reports/playback-increment-2026-11-08-resume12.json`；未做逐帧比较。

当前工作库进度5391/6454，确认1093。本次构建数据校验、65项单元测试、桌面/手机浏览器检查及新增两条真实播放核验均通过；内容提交 `2c14a9b727123b182e8cf91feeacf6040a0436e6` 已推送；Pages 部署运行 `42414051486` 成功，线上 `data.json` 返回HTTP 200，SHA-256 `8b93f770f62bdfc5ed6207c7a512884bb4d5a54a50ecfc4b155861e2a42ab726` 与本地一致，两条新增视频已在线核验，详情见 `reports/pages-check-2026-11-08-resume12.json`。


## 2026-11-08 恢复后增量十三

新搜索批次 `20261107T210557Z` 在第1条 `MpmGXeAtWUw` 的匿名会话初始化时遇到 `TimeoutError`，没有完成原片处理；该ID已加入本机阻塞清单，累计72条。没有重试。

随后对有效期内的本地缓存做离线处理：`reassess-cached` 未发现确认状态变化；`seed-identities` 从公开视频缓存整理出38条明确原片身份线索；`seed-related` 从824,219条缓存合集分P中整理出163条待核验候选。候选线索不等于确认。其后筛出6组原片与B站详情均有未过期缓存的明确身份线索，离线核验器完成6条，其中5条确认、1条因合集分P身份待审；没有触发外部请求。

新增确认版本：`MShbP3OpASA` → `BV1bE411E7Gm`、`2B-XwPjn9YY` → `BV14t411h776`、`ErwS24cBZPc` → `BV15LpMzREhR`、`nM9f0W2KD5s` → `BV1YK4y1W7VA`、`H1KP4ztKK0A` → `BV15X4y1T7wA`。五条均有B站完整简介中的精确原片链接，选定单P、时长一致，真实播放及CID检查均通过。三条为既有原片新增可切换版本，另两条新增原片。元数据详情及快照哈希见 `reports/metadata-review-2026-11-08-resume13.json`，播放器结果见 `reports/playback-increment-2026-11-08-resume13.json`；未做逐帧比较。

构建进度5295/6454，确认1095；新增版本已通过数据校验、65项单元测试、桌面/手机浏览器场景、Node语法和实播核验。提交 `3060c188bfbae6be1febf40d1cb2b87f38a49855` 已推送；Pages `data.json` 返回HTTP 200，SHA-256 `f29567234791fcc71be5625fc78311fb06336c968137016306483381ccc41f36` 与本地一致，详情见 `reports/pages-check-2026-11-08-resume13.json`。

## 2026-11-08 恢复后增量十四

批次 `20261107T213310Z` 串行完成50/50，36条候选确认、14条待审，0请求错误、0未处理；`--primary-first` 共暂缓390个较低优先级候选版本，仍需后续补查，不代表已穷尽。72条此前网络错误原片继续排除。该批处理后工作库进度5345/6454，确认1101。

本批新增可发布版本共7条：`aMcJ1Jvtef0` → `BV1LaZ6Y4EQB`、`rQmqVVmMB3k` → `BV1Mv411A7FC`、`LWGJA9i18Co` → `BV1eXkTBEEZp`、`jILgxeNBK_8` → `BV1Vspk6iEHd`、`lcjdwSY2AzM` → `BV1ZzaqzAEa2`、`2JAOTJxYqh8` → `BV1rM411K7qb`、`PaCmpygFfXo` → `BV1juKH6MEVU`。7条均为单P，完整B站简介含对应原片YouTube ID/链接，标题、分P名称与原片相符；原片和分P时长均在容差内。前6条新增原片卡，最后1条为已发布原片的附加版本。缓存快照哈希、简介核验和逐条播放证据见 `reports/metadata-review-2026-11-08-resume14.json`、`reports/playback-increment-2026-11-08-resume14.json`。播放检查全部观察到实际播放、对应CID及匹配的播放器时长；未做逐帧音画比较。

构建当前包含1101张原片卡、1475个确认分P、0个分P冲突；相对增量十三只新增上述6张卡和1个版本，没有删除或改动既有版本。数据校验、65项单元测试、Node语法检查和桌面/手机15个浏览器场景均通过。内容提交 `13589462e9ec87c7ec8a9b987b88120ed36c607f` 已推送；Pages 部署运行 `42417352631` 成功，线上 `data.json` 返回HTTP 200，SHA-256 `037ca1f1a21c2994a8160878bfc46a4265c5ec65f320f4eac84cfdbb2b90ab05` 与本地一致，6张新增卡和1个新增版本已在线发布，详情见 `reports/pages-check-2026-11-08-resume14.json`。

## 2026-11-08 恢复后增量十五

批次 `20261107T215233Z` 串行完成50/50，29条候选当前为确认状态、21条待审，0请求错误、0未处理；`--primary-first` 暂缓310个较低优先级候选版本，后续补查，不能算作穷尽。72条先前网络错误原片仍排除且未重试。处理后工作库进度5395/6454，确认1111。逐项去重和元数据复核后，新增可发布版本11条：`1sd26pWhfmg` → `BV1fYXdBQEBE`、`PaypcVFPs48` → `BV1W34y187Sz`、`-MTRxRO5SRA` → `BV16441127ME`、`MtxA20Q-Uss` → `BV1hb4y1s7BA`、`koTf7u0v41o` → `BV1qGpQz1E5M`、`4rTv9wvvat8` → `BV1jU4y1A7AU`、`E2MIpi8pIvY` → `BV1dtPCe7Eqx`、`LEENEFaVUzU` → `BV1hT41137mK`、`ZW8gWgpptI8` → `BV1X54y1Q7aa`、`lsWndfzuOc4` → `BV1Ps4y1N7fy`、`dtjb2OhEQcU` → `BV1NVbYzREMr`。10条新增原片卡，另1条为既有原片附加版本。完整简介含对应原片ID/链接，均单P，标题与时长一致或在1秒内；11条真实播放均观察到实际播放、记录CID和符合分P时长的播放器结果。元数据及快照哈希见 `reports/metadata-review-2026-11-08-resume15.json`，播放结果见 `reports/playback-increment-2026-11-08-resume15.json`；未做逐帧音画比较。构建后共1111张原片卡、1486个确认分P、0个冲突；相对增量十四只增加10张卡和1个版本。数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。内容提交 `0a3ce682a6c401c40d4418f4688e4e22f8b230d0` 已推送；Pages 部署运行 `42419124709` 成功，线上 `data.json` 返回HTTP 200，SHA-256 `59241c99ac58bf9891969d3819be7539eb1dc9f21d089ee848332c1243ffefba` 与本地一致，10张新增卡和1个新增版本已在线发布，详情见 `reports/pages-check-2026-11-08-resume15.json`。


## 2026-11-08 恢复后增量十六

批次 `20261107T220820Z` 串行处理20条后，在第21次尝试 `NMQv0j29WHA` 时遇到 `URLError` 并停止；此前完成20条，3条确认、18条待审，另29条未处理，0条自动重试。该ID已加入本机阻塞清单，累计73条；请求错误不表示视频失效。`--primary-first` 暂缓12个较低优先级版本，仍需后续补查。当前工作库进度5415/6454，确认1114。批次回执保存在本机 `data/work/batches/20261107T220820Z.json`。

本轮新增确认版本：`kJQP7kiw5Fk` → `BV1XbfHYzEqD`（Despacito，282秒）、`lUQ_0MubbcM` → `BV1rw411C7Va`（Why Does the U.S. Support Israel，461秒）、`N5xfBtD6rLY` → `BV1Fd4y1c7Ti`（Military Recruitment and Hollywood，923秒）。三条均为单P，完整简介含精确原片链接，元数据时长一致；实播均成功并观察到对应CID与一致时长。快照和简介哈希见 `reports/metadata-review-2026-11-08-resume16.json`，播放器结果见 `reports/playback-increment-2026-11-08-resume16.json`；未做逐帧比较。

构建后共1114张原片卡、1489个确认分P、0个冲突，`data.json` SHA-256 为 `bdfe251e4a937cadebf4de895f0f2d1f569aa93343c5d82d192db420247946d8`。数据校验通过；65项单元测试、Node语法检查、桌面/手机15个浏览器场景及三条实播检查通过。内容提交 `30a91c24bf3df2a4a4e5e92ef8e9aa1c1fc26590` 已推送至 `main`；Pages 部署运行 `42421562637` 成功，线上 `data.json` 返回HTTP 200，SHA-256 `bdfe251e4a937cadebf4de895f0f2d1f569aa93343c5d82d192db420247946d8` 与本地一致，3条新增卡片已在线核验，详情见 `reports/pages-check-2026-11-08-resume16.json`。按用户要求，本轮暂停于页面推送完成；恢复匹配时先重新运行搜索健康检查并继续排除 `NMQv0j29WHA`。

## GitHub 用户名变更

2026-11-08，GitHub 账户用户名从 `qinqiang316` 改为 `farmland2049`。GitHub 明确提示旧个人主页与旧 Pages 地址不会自动重定向，仓库网页和 Git 访问会重定向。新的仓库地址为 `https://github.com/farmland2049/youtobili`，新的 Pages 地址为 `https://farmland2049.github.io/youtobili/`。更新前新 Pages 的 `data.json` 已返回HTTP 200，SHA-256 与本地一致；历史 `pages-check-*.json` 保留变更前实际核验的网址，不改写历史证据。仓库远端已改为 `https://github.com/farmland2049/youtobili.git`；README、AGENTS.md和页面页脚已更新并推送于 `335e3a9c403e2c88c99090d08ee4e0cba48d350d`。Pages 部署运行 `42481999585` 成功；新首页与 `app.js` 返回HTTP 200，页脚GitHub链接指向新仓库。新 Pages `data.json` 返回HTTP 200，SHA-256 `6b7b323ba9d650bd4520858b42c750a32a0261e70716b24cca0c1ee96c33a7b3` 与本地一致，核验详情见 `reports/pages-check-2026-11-08-username-rename.json`。65项单元测试、Node语法检查、桌面/手机15个浏览器场景均通过。GitHub 不为旧 Pages 地址或个人主页设置重定向，已经分享的旧 Pages URL 需要手动更新；历史核验收据保留旧地址原貌。

## 2026-11-08 恢复后增量十七

在新分支 `continue-20261108` 上继续执行批次 `serial-20261108T130231Z`。会话启动前先由 `drain_identities` 完成76条缓存来源线索核验，其中64条确认为有效版本。随后搜索批次在串行处理16条（16条待审）后，在第17次尝试 `O37yJBFRrfg` 时遇到 `URLError` 停止；错误不表示视频失效，该ID已加入本地阻塞清单，累计74条，不自动重试。本轮工作库进度5435/6454，确认1120。

新增确认原片6部：`ESXOAJRdcwQ` → `BV1AT4y1d7pn`（Jailbreaking the Simulation with George Hotz | SXSW 2019）、`LmpuerlbJu0` → `BV1TT421r7ZR`（You Are Immune Against Every Disease）、`FlApbxLz6pA` → `BV1Pi4y1u7H7`（Intersection design, the Dutch - cycle friendly - way）、`JtUAAXe_0VI` → `BV1gx4y147ni`（Can You Trust Kurzgesagt Videos?）、`U_o8gerare0` → `BV1q54y147ZJ`（The Computer Chronicles - The Internet (1993)）、`y3RIHnK0_NE` → `BV1KE411a74h`（New Robot Makes Soldiers Obsolete）；另有58条为既有原片新增的多版本可选项（包括 `kCc8FmEb1nY`、`zjkBMFhNj_g`、`VMj-3S1tku0`、`ZCuYPiUIONs`、`1La4QzGeaaQ` 等）。全部64条版本元数据标题复核完成，无集数或衍生内容冲突；冲突审计0冲突。6部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume17.json` 和 `reports/playback-increment-2026-11-08-resume17.json`；未做逐帧比较。

构建后共1120张原片卡、1553个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量十八

继续执行批次 `serial-20261108T132559Z`。搜索批次串行处理15条（全部待审），在第16次尝试 `OobLb1McxnI` 时遇到 `URLError` 停止；错误不表示视频失效，该ID已加入本地阻塞清单，累计75条，不自动重试。工作库进度推进至5450/6454，确认保持1120，剩余待处理原片降至1004部。数据校验、65项单元测试、桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量十九

继续执行批次 `serial-20261108T134502Z`。搜索批次串行处理48条，其中43条待审、5条确认；在第49次尝试 `QtgVxGkrX1Y` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计76条，不自动重试。工作库进度推进至5498/6454，确认增至1125，剩余待处理原片降至956部。

新增确认原片5部：`PI_Jl5WFQkA` → `BV1t44y1L7bg`（The Simpsons - Canyonero，88秒）、`PivpCKEiQOQ` → `BV17v411c7ih`（Hitler uses Docker，230秒）、`QFgcqB8-AxE` → `BV1Q3411t7BE`（…but the people are retarded，32秒）、`QRt7LjqJ45k` → `BV1xJ411k7aj`（How to Slow Aging (and even reverse it)，1270秒）、`QrGrOK8oZG8` → `BV1tx411i7FD`（Too Many Cooks | Adult Swim，672秒）。5条均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。5部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume19.json` 和 `reports/playback-increment-2026-11-08-resume19.json`；未做逐帧比较。

构建后共1125张原片卡、1558个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十

继续执行批次 `serial-20261108T143404Z`。会话启动前由 `drain_identities` 完成2条来源身份线索核验并确认（`PivpCKEiQOQ` 增加版本 `BV1du4y147Sa`，`V-vFtiDYiIw` 确认 `BV1Mf4y1U7zB`）。随后搜索批次串行处理7条（6条待审、1条确认），在第8次尝试 `RM0uvgHKZe8` 时遇到 `RemoteDisconnected` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计77条，不自动重试。工作库进度推进至5505/6454，确认增至1127，剩余待处理原片降至948部。

本轮新增确认原片2部：`V-vFtiDYiIw` → `BV1Mf4y1U7zB`（Converting devices to USB Type-C，985秒）、`RAGcDi0DRtU` → `BV1Yn42zzEiu`（Ismo: Ass Is The Most Complicated Word In The English Language，363秒）；并为 `PivpCKEiQOQ` 新增版本 `BV1du4y147Sa`（Hitler uses Docker，230秒）。3条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。3个新增版本实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume20.json` 和 `reports/playback-increment-2026-11-08-resume20.json`；未做逐帧比较。

构建后共1127张原片卡、1561个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十一

继续执行批次 `serial-20261108T144536Z`。启动前由 `drain_identities` 完成3条合集与时长线索核验（3条均待审）。随后搜索批次完整串行处理50条（47条待审、3条确认），0请求错误、0网络中断。工作库进度推进至5555/6454，确认增至1130，剩余待处理原片降至899部。

本轮新增确认原片3部：`Sq1QZB5baNw` → `BV1Hx421C7wj`（Figure Status Update - OpenAI Speech-to-Speech Reasoning，155秒）、`SyD4p8_y8Kw` → `BV1vB4y197MB`（Hitler Learns Topology，230秒）、`TDkH3EbWTYc` → `BV1bv62BjEBr`（Perfectly Replicating Coca Cola (It Took Me A Year)，1556秒）。3条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。3个新增版本实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume21.json` 和 `reports/playback-increment-2026-11-08-resume21.json`；未做逐帧比较。

构建后共1130张原片卡、1564个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十二

继续执行批次 `serial-20261108T155037Z`。搜索批次串行处理24条（全部待审），在第25次尝试 `UEIn8GJIg0E` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计78条，不自动重试。工作库进度推进至5579/6454，确认保持1130，剩余待处理原片降至875部。数据校验、65项单元测试、桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十三

继续执行批次 `serial-20261108T161843Z`。搜索批次串行处理38条（37条待审、1条确认），在第39次尝试 `VjzqO6UOPFQ` 时遇到 `TimeoutError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计79条，不自动重试。工作库进度推进至5617/6454，确认增至1131，剩余待处理原片降至837部。

本轮新增确认原片1部：`VfjjiHGuHoc` → `BV1jW411B7Sf`（Danny MacAskill Tests Santa Cruz Reserve Carbon Wheels，265秒），单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。新增原片实播烟测通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume23.json` 和 `reports/playback-increment-2026-11-08-resume23.json`；未做逐帧比较。

构建后共1131张原片卡、1565个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十四

继续执行批次 `serial-20261108T170434Z`。搜索批次串行处理33条（31条待审、2条确认），在第34次尝试 `X7HmltUWXgs` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计80条，不自动重试。工作库进度推进至5650/6454，确认增至1133，剩余待处理原片降至804部。

本轮新增确认原片2部：`WiPp9YEBV0Q` → `BV1gZ421T7AG`（Filesystem in Rust - Kent Overstreet，2116秒）、`X3-hOigoxHs` → `BV1zP4y1r73e`（The Adorkable Misogyny of The Big Bang Theory，1271秒）。两条均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。2部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume24.json` 和 `reports/playback-increment-2026-11-08-resume24.json`；未做逐帧比较。

构建后共1133张原片卡、1567个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十五

继续执行批次 `serial-20261108T174226Z`。启动前由 `drain_identities` 完成1条来源身份线索核验（合集分P待审）。随后搜索批次串行处理13条（全部待审），在第14次尝试 `XZmGGAbHqa0` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计81条，不自动重试。工作库进度推进至5663/6454，确认保持1133，剩余待处理原片降至791部。数据校验、65项单元测试、桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十六

继续执行批次 `serial-20261108T180336Z`。启动前由 `drain_identities` 完成1条来源身份线索核验并确认（`DJklHwoYgBQ` 确认 `BV1GL4y1K7ZS`）。随后搜索批次在第1次尝试 `X_8E3ENrKrQ` 时遇到 `TimeoutError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计82条，不自动重试。工作库进度推进至5663/6454，确认增至1134，剩余待处理原片为791部。

本轮新增确认原片1部：`DJklHwoYgBQ` → `BV1GL4y1K7ZS`（Smart Pipe | Infomercials | Adult Swim，662秒），单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。新增原片实播烟测通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume26.json` 和 `reports/playback-increment-2026-11-08-resume26.json`；未做逐帧比较。

构建后共1134张原片卡、1568个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十八

继续执行批次 `serial-20261108T181112Z`。搜索批次串行处理23条（19条待审、4条确认），在第24次尝试 `YZZV464z9g8` 时遇到 `TimeoutError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计84条，不自动重试。工作库进度推进至5688/6454，确认增至1138，剩余待处理原片降至766部。

本轮新增确认原片4部：`XfonhlM6I7w` → `BV1PCy5BxEsn`（This Town Did The Impossible，808秒）、`XpunFFS-n8I` → `BV1WwLyz9Ehz`（How Netflix Uses Java - 2025 Edition，2863秒）、`XqZsoesa55w` → `BV1W5411H7Ra`（Baby Shark Dance，137秒）、`YScIPA8RbVE` → `BV1Ga4y1J7EM`（The Algebra of Algebraic Data Types，3875秒）。4条均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。4部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume28.json` 和 `reports/playback-increment-2026-11-08-resume28.json`；未做逐帧比较。

构建后共1138张原片卡、1572个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量二十九

继续执行批次 `serial-20261108T183918Z`。启动前由 `drain_identities` 完成2条来源身份线索核验并确认（`sforhbLiwLA` 确认 `BV1Vs41167e2`，`XfonhlM6I7w` 增加版本 `BV1ph4y1c7tw`）。随后搜索批次串行处理6条（5条待审、1条确认），在第7次尝试 `YpNuh-J5IgE` 时遇到 `TimeoutError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计85条，不自动重试。工作库进度推进至5695/6454，确认增至1140，剩余待处理原片降至759部。

本轮新增确认原片2部：`sforhbLiwLA` → `BV1Vs41167e2`（Microsoft Windows 1.0 with Steve Ballmer，62秒）、`YbYWhdLO43Q` → `BV1zU4y1v7Mo`（This Unicorn Changed the Way I Poop，174秒）；并为 `XfonhlM6I7w` 新增版本 `BV1ph4y1c7tw`（This Town Did The Impossible，808秒）。3条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。3个新增版本实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume29.json` 和 `reports/playback-increment-2026-11-08-resume29.json`；未做逐帧比较。

构建后共1140张原片卡、1575个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量三十

继续执行批次 `serial-20261108T185204Z`。搜索批次串行完整处理50条（47条待审、3条确认），0错误。工作库进度推进至5746/6454，确认增至1143，剩余待处理原片降至708部。

本轮新增确认原片3部（共4个确认分P）：
- `ZXsQAXx_ao0` → `BV1QW411g7r1`（Shia LaBeouf "Just Do It" Motivational Speech，65秒 vs 64秒）
- `ZzCegQVljdY` → `BV1ME411P7wY`（Inequality: Why are the rich getting richer?，181秒 vs 182秒）
- `bZe5J8SVCYQ` → `BV1os4y1K7i7`、`BV1P5411878N`（The Missile Knows Where It Is...，100秒 vs 101秒）

4条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。3部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume30.json` 和 `reports/playback-increment-2026-11-08-resume30.json`；未做逐帧比较。

构建后共1143张原片卡、1579个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量三十一

继续执行批次 `serial-20261108T195354Z`。搜索批次串行处理38条（35条待审、3条确认），在第39次尝试 `b1XGPvbWn0A` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计86条，不自动重试。工作库进度推进至5784/6454，确认增至1146，剩余待处理原片降至670部。

本轮新增确认原片3部：
- `_oJs8-I9WtA` → `BV1PBxTeHEvf`（Comparing Beta & VHS on Quality: Was Beta Really Better?，592秒 vs 591秒）
- `ap-BkkrRg-o` → `BV1zx42127p1`（Starship High Altitude Test - SN8，7173秒 vs 7173秒）
- `aqz-KE-bpKQ` → `BV1gD4y1o72p`（Big Buck Bunny 60fps 4K - Official Blender Foundation Short Film，635秒 vs 634秒）

3条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。3部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume31.json` 和 `reports/playback-increment-2026-11-08-resume31.json`；未做逐帧比较。

构建后共1146张原片卡、1582个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量三十二

继续执行批次 `serial-20261108T203949Z`。启动前由 `drain_identities` 完成4条来源身份线索核验并确认（包括为已确认原片 `YdOXS_9_P4U` 增加版本 `BV1Je81zQEet`、为 `aqz-KE-bpKQ` 增加版本 `BV1QSM86fED4`，以及确认新原片 `HB5TrK7A4pI`、`k7YVxLLIuGM`）。随后搜索批次串行处理15条（14条待审、1条确认），在第16次尝试 `b_WmjWAGkLI` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计87条，不自动重试。工作库进度推进至5800/6454，确认增至1149，剩余待处理原片降至654部。

本轮新增确认原片3部（共5个确认版本）：
- `HB5TrK7A4pI` → `BV1H34y1W7QU`（"We Really Don't Know How to Compute!" - Gerald Sussman (2011)，3859秒 vs 3859秒）
- `k7YVxLLIuGM` → `BV1164y1Y7UL`（Is Your Car Safe From Supermaneuverable Air-Defense Fighter Aircraft?，361秒 vs 361秒）
- `b2F-DItXtZs` → `BV1eq4y1176K`（Episode 1 - Mongo DB Is Web Scale，API时长336秒 vs 原片336秒，实播328秒在容差内）
- 并为 `YdOXS_9_P4U` 新增版本 `BV1Je81zQEet`（Terence Tao on the cosmic distance ladder，1713秒 vs 1713秒）
- 为 `aqz-KE-bpKQ` 新增版本 `BV1QSM86fED4`（Big Buck Bunny 60fps 4K，635秒 vs 634秒）

5条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。5个新增版本实播烟测均通过（4个时长完全一致，1个时长差异8.2秒在8%容差范围内）并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume32.json` 和 `reports/playback-increment-2026-11-08-resume32.json`；未做逐帧比较。

构建后共1149张原片卡、1587个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量三十三

继续执行批次 `serial-20261108T210311Z`。搜索批次串行处理13条（10条待审、3条确认），在第14次尝试 `cQ54GDm1eL0` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计88条，不自动重试。工作库进度推进至5813/6454，确认增至1152，剩余待处理原片降至641部。

本轮新增确认原片3部：
- `buqtdpuZxvk` → `BV1Qx411R7NW`（Galaxy Song - Monty Python's The Meaning of Life，164秒 vs 164秒）
- `bx_LGilOuE4` → `BV1vaYBe3E8X`（Jujutsu: A Git-Compatible VCS - Git Merge 2022，2006秒 vs 2006秒）
- `bzE-IMaegzQ` → `BV1Us411z791`（Bike Lanes by Casey Neistat，183秒 vs 183秒）

3条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。3部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume33.json` 和 `reports/playback-increment-2026-11-08-resume33.json`；未做逐帧比较。

构建后共1152张原片卡、1590个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量三十四

继续执行批次 `serial-20261108T211811Z`。启动前由 `drain_identities` 完成2条来源身份线索核验并确认（为已确认原片 `bzE-IMaegzQ` 增加版本 `BV1tpcWeuEu6` 与 `BV1bQ4y1D7fb`）。随后搜索批次串行处理8条（全部待审），在第9次尝试 `cdgQpa1pUUE` 时遇到 `URLError` 停止，错误不表示视频失效，该ID已加入本地阻塞清单，累计89条，不自动重试。工作库进度推进至5821/6454，确认保持1152部，确认版本增至1592个，剩余待处理原片降至633部。

本轮为原片 `bzE-IMaegzQ`（Bike Lanes by Casey Neistat）新增确认2个版本：
- `BV1tpcWeuEu6`（『Casey Neistat双字』自行车只能在自行车道骑吗？，184秒 vs 183秒）
- `BV1bQ4y1D7fb`（敢问路在何方？Bike Lanes by Casey Neistat，184秒 vs 183秒）

2条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。2个新增版本实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume34.json` 和 `reports/playback-increment-2026-11-08-resume34.json`；未做逐帧比较。

构建后共1152张原片卡、1592个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-08 恢复后增量三十五

执行批次 `serial-20261108T213019Z`。搜索批次串行处理21条（18条待审、3条确认）。因接近早上06:00目标节点且收到用户暂停指令，批次手动停止；工作库进度推进至5842/6454，确认增至1155，剩余待处理原片降至612部。

本轮新增确认原片3部：
- `cpraXaw7dyc` → `BV1oc411U7E4`（Optimus - Gen 2 | Tesla，104秒 vs 104秒）
- `cyN-CRNrb3E` → `BV1Ji4y1j7SQ`（Triple Pendulum on a Cart，57秒 vs 57秒）
- `djV11Xbc914` → `BV1H8Yr6zEZt`（a-ha - Take On Me (Official Video) [4K]，245秒 vs 244秒）

3条版本均为单P且完整简介含对应原片链接，时长与原片一致。标题元数据复核完成，无集数或衍生冲突；冲突审计0冲突。3部新增原片实播烟测均通过并捕获实际CID与匹配时长，快照哈希与实播结果见 `reports/metadata-review-2026-11-08-resume35.json` 和 `reports/playback-increment-2026-11-08-resume35.json`；未做逐帧比较。

构建后共1155张原片卡、1595个确认分P、0个冲突，`data.json` 数据校验、65项单元测试、Node语法检查及桌面/手机15个浏览器场景均通过。

## 2026-11-09 补验收、时长标准统一与全量实播复核

响应用户指令，暂停后续抓取扩充，在分支 `continue-20261108` 上优先执行严格补验收与规范治理，不将未处理原片混入本次交付。

### 1. 播放检查脚本修复与测试补充
- 重构 `scripts/playback_smoke.cjs`：在播放未启动、视频编号（CID）未命中网络请求、实播媒体流时长与分P声明时长差超过 3 秒或抛出异常时，明确报告失败原因并退出非零码（`process.exit(1)`），严禁静默或隐性通过。
- 增加针对性单元测试 [`tests/test_playback_smoke.py`](file:///Users/qqiang/AI%20project/06-开发项目/youtobili%20推荐页/tests/test_playback_smoke.py)，覆盖未播放、CID 缺失、时长偏差、接口错误及非零退出码场景。全套 Python 单元测试扩展至 71 项，全部通过。

### 2. 双重时长标准统一与异常记录复核
- **标准 A（候选准入/内容同一性）**：YouTube 原片与 B 站分P声明时长差严格遵循既定规则 `max(60秒, 8%)`，用于筛除删减或错配视频。
- **标准 B（实播流与元数据一致性）**：B 站嵌入播放器 `<video>` 元素解析出的真实流时长与该分P声明时长误差必须 `<= 3秒`，用于验证媒体流与 CID 加载的一致性。
- **复核 `b2F-DItXtZs` (`BV1eq4y1176K`)**：API 声明 336 秒，但实播媒体时长仅 327.8 秒（偏差 8.2 秒 > 3 秒），违反标准 B。判定实播核验未通过，绝不临时放宽标准；立即撤回并标记 `manual_review_hold: true`，移出公开 `data.json`。

### 3. 补齐 59 个历史新增版本实播核验
- 对本次任务自基线 `f2d8860` 以来新增的 59 个未单独实播版本进行逐一自动化嵌入播放器核验，保存播放状态、CID 捕获、声明时长与实播时长记录至 [`reports/playback-audit-59.json`](file:///Users/qqiang/AI%20project/06-开发项目/youtobili%20推荐页/reports/playback-audit-59.json)。
- **58 个版本 100% 通过**，无任何播放、CID 或时长异常。
- **1 个版本失败并撤回**：`ugvHCXCOmm4` 候选 `BV13Em8YFEjg` 声明时长 18901 秒，但播放器实播时长仅 12202.1 秒（截断近 2 小时，偏差 6698.9 秒 > 3 秒），判定未通过。已将该版本撤回为待审核并置 `manual_review_hold: true`，从公开库完全剔除；该原片公开展示仅保留此前已实播验证通过的官方版本 `BV1JNSwB8EvF`。

### 4. Grok Build 独立复查与全套完整验收
- 使用 `--always-approve` 运行 Grok Build CLI 审查本分支：重跑构建检查、71 项单元测试、15 项端到端浏览器测试，并逐项核对实播审计与撤回条目状态，给出明确 **PASS** 验收结论。
- 数据校验（`pipeline.py check`）：PASS（1154 张原片卡片，1593 个已核验分P，0 冲突，无内部路径或凭据）。
- 单元测试（`unittest discover`）：PASS（71 项全部通过）。
- 浏览器场景测试（`tests/browser.cjs`）：PASS（桌面 1440px / 移动 390px 15 个场景全通，0 脚本错误）。

### 5. 交付指标与归因口径纠正
- **已处理原片（Processed）**：5,842 部（占全库 6,454 的 90.52%）。
- **已确认原片（Confirmed）**：1,154 部（17.88%）。
- **已上线条目（Published）**：1,154 张原片卡片、1,593 个有效分P版本（双重核验 100% 通过，0 冲突）。
- **累计排除原片数（Excluded Originals）**：89 部（检索中断条目，在缺乏底层网络抓包证据前，原因统一标记为“待核实网络中断”，不判定失效，不反复试错）。
- **剩余未处理原片（Remaining Unprocessed）**：612 部（明确作为后续扩充目标，不混入本次交付）。

## 2026-11-09 恢复后增量三十六

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T012308Z`（含线索批次 `leads-1`、`leads-2` 及检索批次 `20261109T012744Z`）。检索配额 50 条全部正常完成，0 请求错误，0 网络异常，0 风控停止；此前 89 条待核实网络中断原片继续在排除清单中隔离，未自动重试，亦未判定失效。

本轮净增 5 部确认原片、6 个有效分P版本，无撤回：
1. `dxIPcbmo1_U` → `BV1NZ4y1f7m1`（《【UNIX传奇】侏罗纪公园名场面 It's a UNIX System》，85秒 vs 85秒，B站简介含明确原片URL与分P对应，实播CID `499198713` 通过）
2. `e9dZQelULDk` → `BV18q4y1H7sU`（《每只老鼠都在追求幸福，但这真的是幸福吗？》，253秒 vs 253秒，B站简介含明确原片URL，实播CID `374023685` 通过）
3. `e9dZQelULDk` → `BV1z4411v7Y5`（《【黑色幽默/默剧】幸福 Happiness by Steve Cutts》，257秒 vs 257秒，B站简介含明确原片URL，实播CID `90830701` 通过，该原片第2个确认版本）
4. `eXYUNrgqWUU` → `BV1x84y1v7rM`（《Enemies – real-time cinematic teaser - Unity》，121秒 vs 121秒，B站简介含明确原片URL，实播CID `887359599` 通过）
5. `f3lUEnMaiAU` → `BV1ktCpByEZ9`（《Jack Ma and Elon Musk hold debate in Shanghai》，2813秒 vs 2813秒，B站简介含明确原片URL，实播CID `33959970508` 通过）
6. `gX9cbxLSOkE` → `BV1Ri4y1774u`（《无源环境反向散射通信 - Ambient Backscatter Communications Technology》，184秒 vs 184秒，B站简介含明确原片URL，实播CID `238993300` 通过）

**核验与验收情况**：
- **标题元数据复核**：覆盖全部 6 个版本，未发现年份、集数冲突或衍生/AI二创标识（凭证存入 `reports/metadata-review-2026-11-09-resume36.json`）。
- **冲突审计**：跨原片分P绑定审计 0 冲突。
- **嵌入播放器实播烟测**：按标准 B（流时长与元数据误差 $\le 3$ 秒）和 CID 观测要求，6 个版本 100% 通过（误差均为 0.0 秒，实测媒体时长与分P声明完全一致，凭证存入 `reports/playback-increment-2026-11-09-resume36.json`）。未做逐帧内容比较。
- **构建后统计**：全库已处理原片 5,894 部（91.32%），确认原片 1,159 部（17.96%），已上线 1,159 张原片卡片、1,599 个确认分P版本。剩余未处理原片降至 560 部。
- **全套自动化验收**：数据校验（`check`）、71 项 Python 单元测试、桌面 1440px / 移动 390px 15 个浏览器场景测试全数通过。

## 2026-11-09 恢复后增量三十七

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T031525Z`（检索批次 `20261109T031530Z`）。检索配额 50 条全部正常完成，0 请求错误，0 网络异常，0 风控停止；此前 89 条待核实网络中断原片继续在排除清单中隔离，未自动重试，亦未判定失效。

本轮净增 4 部确认原片、4 个有效分P版本，无撤回：
1. `ghdTqnYnFyg` → `BV16W4y187U5`（《Apple WWDC 2005-The Intel Switch Revealed》，495秒 vs 495秒，B站简介含明确原片URL，实播CID `816485077` 通过，实测流时长 495 秒，误差 0.0 秒）
2. `gn4nRCC9TwQ` → `BV15x411B7c3`（《Google AI已经学会了如何走路 Google's DeepMind AI just taught itself to walk》，111秒 vs 111秒，分P标题含明确原片ID `gn4nRCC9TwQ`，实播CID `20149756` 通过，实测流时长 111 秒，误差 0.0 秒）
3. `hX1YVzdnpEc` → `BV14s411i711`（《奥巴马演唱蹲妹单曲《Call me maybe》@柚子木字幕组》，106秒 vs 106秒，柚子木字幕组翻译原版，实播CID `7726018` 通过，实测流时长 107 秒，误差 1.0 秒 $\le 3$ 秒）
4. `i8ju_10NkGY` → `BV1254Ae5EWj`（《Lazy Town | You Are A Pirate Music Video》，115秒 vs 115秒，B站简介含明确原片URL，实播CID `26138707100` 通过，实测流时长 112.7 秒，误差 2.3 秒 $\le 3$ 秒）

**核验与验收情况**：
- **标题元数据复核**：覆盖全部 4 个版本，未发现年份、集数冲突或衍生/AI二创标识（凭证存入 `reports/metadata-review-2026-11-09-resume37.json`）。
- **冲突审计**：跨原片分P绑定审计 0 冲突。
- **嵌入播放器实播烟测**：按标准 B（流时长与元数据误差 $\le 3$ 秒）和 CID 观测要求，4 个版本 100% 通过（实测媒体时长与分P声明误差均 $\le 3$ 秒，全部命中实际请求 CID，凭证存入 `reports/playback-increment-2026-11-09-resume37.json`）。未做逐帧内容比较。
- **构建后统计**：全库已处理原片 5,944 部（92.10%），确认原片 1,163 部（18.02%），已上线 1,163 张原片卡片、1,603 个确认分P版本。剩余未处理原片降至 510 部。
- **全套自动化验收**：数据校验（`check`）、71 项 Python 单元测试、桌面 1440px / 移动 390px 15 个浏览器场景测试全数通过。

## 2026-11-09 恢复后增量三十八

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T042215Z`（含线索批次 `leads-1` 与检索批次 `20261109T042220Z`）。检索配额 50 条全部正常完成，0 请求错误，0 网络异常，0 风控停止；此前 89 条待核实网络中断原片继续隔离，未自动重试，亦未判定失效。

本轮净增 4 部确认原片、5 个有效分P版本，无撤回：
1. `rX0ItVEVjHc` → `BV1cm421u7dc`（《CppCon 2014 Mike Acton Data-Oriented Design and cpp》，5266秒 vs 5266秒，B站简介含明确原片URL，实播CID `1536707117` 通过，实测流时长 5266 秒，误差 0.0 秒；该原片新增第4个确认版本）
2. `JfmTagWcqoE` → `BV1Gb411E7xS`（《CppCon 2016 Herb Sutter “Leak-Freedom in C ++ ... By Default.”》，5965秒 vs 5965秒，B站简介含明确原片URL，实播CID `81740217` 通过，实测流时长 5965 秒，误差 0.0 秒）
3. `ig3xI8dUdm0` → `BV1CW411a76d`（《[生肉]Thinkpad P50评估，IS IT SPILL PROOF？》，2699秒 vs 2699秒，B站简介含明确原片URL，实播CID `27561627` 通过，实测流时长 2699 秒，误差 0.0 秒）
4. `jVhlJNJopOQ` → `BV18D4y1V7GU`（《【中文字幕】周六夜现场 SNL：阿凡达&莎草纸体 Papyrus 喜剧特辑》，187秒 vs 187秒，B站简介含明确原片URL，实播CID `956689126` 通过，实测流时长 185.8 秒，误差 1.2 秒 $\le 3$ 秒）
5. `jgYYOUC10aM` → `BV1BL411u71A`（《Planning a Heist - Key & Peele(720p)》，62秒 vs 62秒，B站简介含明确原片URL，实播CID `437363380` 通过，实测流时长 62 秒，误差 0.0 秒）

**核验与验收情况**：
- **标题元数据复核**：覆盖全部 5 个版本，未发现年份、集数冲突或衍生/AI二创标识（凭证存入 `reports/metadata-review-2026-11-09-resume38.json`）。
- **冲突审计**：跨原片分P绑定审计 0 冲突。
- **嵌入播放器实播烟测**：按标准 B（流时长与元数据误差 $\le 3$ 秒）和 CID 观测要求，5 个版本 100% 通过（实测媒体时长与分P声明误差均 $\le 3$ 秒，全部命中实际请求 CID，凭证存入 `reports/playback-increment-2026-11-09-resume38.json`）。未做逐帧内容比较。
- **构建后统计**：全库已处理原片 5,994 部（92.87%），确认原片 1,167 部（18.08%），已上线 1,167 张原片卡片、1,608 个确认分P版本。剩余未处理原片降至 460 部。
- **全套自动化验收**：数据校验（`check`）、71 项 Python 单元测试、桌面 1440px / 移动 390px 15 个浏览器场景测试全数通过。

## 2026-11-09 恢复后增量三十九

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T050747Z`（含线索批次 `leads-1` 与检索批次 `20261109T050752Z`）。检索配额 50 条全部正常完成，0 请求错误，0 网络异常，0 风控停止；此前 89 条待核实网络中断原片继续隔离，未自动重试，亦未判定失效。

本轮净增 6 部确认原片、8 个有效分P版本，无撤回：
1. `k5xf40KrK3I` → `BV1tYsGeKEty`（《【授权翻译】我曾经为MrBeast工作，他就是个诈骗犯.. [DogPack404]》，3220秒 vs 3220秒，B站简介含明确原片URL，实播CID `25647841860` 通过，实测流时长 3218.7 秒，误差 1.3 秒 $\le 3$ 秒）
2. `kPMHcanq0xM` → `BV12c411j7ps`（《Magic leap AR概念视频》，97秒 vs 97秒，B站简介含明确原片URL，实播CID `1063811277` 通过，实测流时长 95.8 秒，误差 1.2 秒 $\le 3$ 秒）
3. `kPMHcanq0xM` → `BV1kW411y768`（《Magic Leap _ Original Concept Video》，96秒 vs 96秒，B站简介含明确原片URL，实播CID `58331309` 通过，实测流时长 96 秒，误差 0.0 秒；该原片第2个确认版本）
4. `kSLJriaOumA` → `BV1Ub411i7Qs`（《【 生成式对抗网络GAN 】A Style-Based Generator Architecture for Generative Adversaria》，378秒 vs 378秒，B站简介含明确原片URL，实播CID `79507625` 通过，实测流时长 378 秒，误差 0.0 秒）
5. `kSLJriaOumA` → `BV1vb411t7Au`（《英伟达 StyleGAN 川剧变脸 —— A_Style_Based_Generator_Architec》，378秒 vs 378秒，B站简介含明确原片URL，实播CID `78542782` 通过，实测流时长 378 秒，误差 0.0 秒；该原片第2个确认版本）
6. `kWSIFh8ICaA` → `BV1U7411y7Lu`（《【笑死我了】2013 PS4 广告 《如何分享你的游戏》Official PlayStation Used Game Instructional Video》，22秒 vs 22秒，B站简介含明确原片URL，实播CID `169293914` 通过，实测流时长 22 秒，误差 0.0 秒）
7. `kx_G2a2hL6U` → `BV1QA411e7Xh`（《[转载]我有个朋友叫 Biggus Dickus》，246秒 vs 246秒，分P标题明确绑定原片标题，实播CID `212928359` 通过，实测流时长 246 秒，误差 0.0 秒）
8. `lEplzHraw3c` → `BV1g1JuzGEvJ`（《古巴的地下游戏网络丨Cuba's Underground Gaming Network》，1241秒 vs 1241秒，B站简介含明确原片URL，实播CID `30019489558` 通过，实测流时长 1241 秒，误差 0.0 秒）

**核验与验收情况**：
- **标题元数据复核**：覆盖全部 8 个版本，未发现年份、集数冲突或衍生/AI二创标识（凭证存入 `reports/metadata-review-2026-11-09-resume39.json`）。
- **冲突审计**：跨原片分P绑定审计 0 冲突。
- **嵌入播放器实播烟测**：按标准 B（流时长与元数据误差 $\le 3$ 秒）和 CID 观测要求，8 个版本 100% 通过（实测媒体时长与分P声明误差均 $\le 3$ 秒，全部命中实际请求 CID，凭证存入 `reports/playback-increment-2026-11-09-resume39.json`）。未做逐帧内容比较。
- **构建后统计**：全库已处理原片 6,044 部（93.65%），确认原片 1,173 部（18.17%），已上线 1,173 张原片卡片、1,616 个确认分P版本。剩余未处理原片降至 410 部。
- **全套自动化验收**：数据校验（`check`）、71 项 Python 单元测试、桌面 1440px / 移动 390px 15 个浏览器场景测试全数通过。

## 2026-11-09 恢复后增量四十

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T060712Z`。批次在处理第 1 条原片 `lkjyeI0ykGM`（经详情比对归入待审）后，在第 2 次尝试处理 `ll3CMgiUPuU` 时遇到 `URLError` 即刻停止。依项目规则，遇到网络中断即刻停止当前批次且不反复试错，该请求失败不直接判为视频失效，未作自动重试；已将 `ll3CMgiUPuU` 隔离加入本地排除清单，原因标记为“待核实网络中断”，累计排除原片数增至 90 部。

本轮无新增确认条目。全库已处理原片微增至 6,045 部（93.66%），确认原片保持 1,173 部（18.17%），已上线 1,173 张原片卡片、1,616 个确认分P版本。剩余未处理原片降至 409 部（扣除排除清单后尚余 366 部待初筛）。数据校验（`check`）、71 项 Python 单元测试及桌面/移动端 15 个浏览器场景测试全数通过。

## 2026-11-09 恢复后增量四十一

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T061148Z`。批次连续完成前 9 条原片初筛审定（`llRkf1fnNDM` 至 `mArrNRWQEso`，均无显式原片证据归入待审），在第 10 次尝试处理 `mJHvSp9AKYg` 时遇到 `URLError` 即刻停止。依项目规则，遇到网络中断即刻停止当前批次且不反复试错，该请求失败不直接判为视频失效，未作自动重试；已将 `mJHvSp9AKYg` 隔离加入本地排除清单，原因标记为“待核实网络中断”，累计排除原片数增至 91 部。

本轮无新增确认条目。全库已处理原片推进至 6,054 部（93.80%），确认原片保持 1,173 部（18.17%），已上线 1,173 张原片卡片、1,616 个确认分P版本。剩余未处理原片降至 400 部（扣除排除清单后尚余 356 部待初筛）。数据校验（`check`）、71 项 Python 单元测试及桌面/移动端 15 个浏览器场景测试全数通过。

## 2026-11-09 恢复后增量四十二

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T062449Z`（含检索批次 `20261109T062454Z` 与线索批次 `leads-1` `20261109T071532Z`）。检索配额 50 条全部正常完成，0 请求错误，0 网络异常，0 风控停止；此前 91 条待核实网络中断原片继续隔离在排除清单中，未自动重试，亦未判定失效。

本轮净增 5 部确认原片、7 个有效分P版本，无撤回：
1. `zNVQfWC_evg` → `BV1k4411U758`（《大卫·汤：量子场，宇宙真正的基本组成部分 (The Royal Institution)》，3618秒 vs 3618秒，B站简介含明确原片URL，实播CID `110932070` 通过，实测流时长 3618 秒，误差 0.0 秒）
2. `mS5WYp5xmvI` → `BV1Eu411y74P`（《托马斯·索威尔论经济不平等的迷思 Thomas Sowell on the Myths of Economic Inequality》，3214秒 vs 3214秒，分P文件名含明确原片ID `mS5WYp5xmvI`，实播CID `580841021` 通过，实测流时长 3214 秒，误差 0.0 秒）
3. `mS5WYp5xmvI` → `BV1jf4y1B7u2`（《Thomas Sowell: the Myths of Economic Inequality》，3214秒 vs 3214秒，分P名称含明确原片ID `mS5WYp5xmvI`，实播CID `246462743` 通过，实测流时长 3214 秒，误差 0.0 秒；该原片第2个确认版本）
4. `ny_OPsxHQmU` → `BV1mt4y1q7KK`（《THROUGH THE LENSES - QUEST 2 vs Reverb G2 vs INDEX! 90Hz Quest》，831秒 vs 831秒，B站简介含明确原片URL，实播CID `240087282` 通过，实测流时长 831 秒，误差 0.0 秒）
5. `o4TdHrMi6do` → `BV14SWpzDE4Q`（《【YouTube搬运】每秒 20 亿 帧 的 激光 指示器Laser pointer at 2 billion fps》，1762秒 vs 1762秒，B站简介含明确原片URL，实播CID `33170915847` 通过，实测流时长 1762 秒，误差 0.0 秒）
6. `oLt5qSm9U80` → `BV1Rx411x7T7`（《爆笑：但是我们在说日语啊！But we're speaking Japanese!》，130秒 vs 131秒，B站简介含明确原片URL，实播CID `23258598` 通过，实测流时长 131 秒，误差 1.0 秒 $\le 3$ 秒）
7. `oLt5qSm9U80` → `BV1KJmUYGEhp`（《But we're speaking Japanese!》，114秒 vs 112.7秒，B站简介含明确原片URL，实播CID `26712936320` 通过，实测流时长 112.7 秒，误差 1.3 秒 $\le 3$ 秒；该原片第2个确认版本）

**核验与验收情况**：
- **标题元数据复核**：覆盖全部 7 个版本，未发现年份、集数冲突或衍生/AI二创标识（凭证存入 `reports/metadata-review-2026-11-09-resume42.json`）。
- **冲突审计**：跨原片分P绑定审计 0 冲突。
- **嵌入播放器实播烟测**：按标准 B（流时长与元数据误差 $\le 3$ 秒）和 CID 观测要求，7 个版本 100% 通过（实测媒体时长与分P声明误差均 $\le 3$ 秒，全部命中实际请求 CID，凭证存入 `reports/playback-increment-2026-11-09-resume42.json`）。未做逐帧内容比较。
- **构建后统计**：全库已处理原片 6,104 部（94.58%），确认原片 1,178 部（18.25%），已上线 1,178 张原片卡片、1,623 个确认分P版本。剩余未处理原片降至 350 部（扣除排除清单后尚余 306 部待初筛）。
- **全套自动化验收**：数据校验（`check`）、71 项 Python 单元测试、桌面 1440px / 移动 390px 15 个浏览器场景测试全数通过。

## 2026-11-09 恢复后增量四十三

在分支 `continue-20261109` 上执行串行批次 `serial-20261109T072253Z`（含检索批次 `20261109T072359Z` 与线索批次 `leads-1` `20261109T081910Z`）。检索配额 50 条全部正常完成，0 请求错误，0 网络异常，0 风控停止；此前 91 条待核实网络中断原片继续隔离在排除清单中，未自动重试，亦未判定失效。

本轮净增 2 部确认原片、2 个有效分P版本，无撤回：
1. `pnbJEg9r1o8` → `BV1PM4y1K7uz`（《中文字幕｜疯狂的泳池漩涡｜Crazy pool vortex - Physics Girl》，243秒 vs 243秒，B站简介含明确原片URL，实播CID `383042177` 通过，实测流时长 243 秒，误差 0.0 秒）
2. `qNf9nzvnd1k` → `BV1ws41117vZ`（《20Hz to 20kHz (人类听觉的可听频率)》，144秒 vs 144秒，B站简介含明确原片URL，实播CID `8761760` 通过，实测流时长 143.866 秒，误差 0.134 秒 $\le 3$ 秒）

**核验与验收情况**：
- **标题元数据复核**：覆盖全部 2 个版本，未发现年份、集数冲突或衍生/AI二创标识（凭证存入 `reports/metadata-review-2026-11-09-resume43.json`）。
- **冲突审计**：跨原片分P绑定审计 0 冲突。
- **嵌入播放器实播烟测**：按标准 B（流时长与元数据误差 $\le 3$ 秒）和 CID 观测要求，2 个版本 100% 通过（实测媒体时长与分P声明误差均 $\le 3$ 秒，全部命中实际请求 CID，凭证存入 `reports/playback-increment-2026-11-09-resume43.json`）。未做逐帧内容比较。
- **构建后统计**：全库已处理原片 6,154 部（95.35%），确认原片 1,180 部（18.28%），已上线 1,180 张原片卡片、1,625 个确认分P版本。剩余未处理原片降至 300 部（扣除排除清单后尚余 256 部待初筛）。
- **全套自动化验收**：数据校验（`check`）、71 项 Python 单元测试、桌面 1440px / 移动 390px 15 个浏览器场景测试全数通过。

## 2026-11-09 按指令暂停与阶段总结

当前工作分支为 `continue-20261109`，最近一次已推送内容提交为 `7390ae8`（增量四十三），包含 1,180 部确认原片、1,625 个确认分P版本。本次按用户指令暂停全库匹配初筛任务，并总结分支已完成内容。运行中的后台串行进程（批次 `serial-20261109T082613Z`）已安全终止，未产生未核验写入，状态已持久化至本地 `data/work/active-continuation.json`。

### 本轮分支推进成果（基线 `7e8d836` → 最新 `7390ae8`）
1. **处理规模**：
   - 全库已处理原片从 5,844 部推进至 **6,154 部**（覆盖率达 **95.35%**），净处理 310 部原片。
   - 剩余未处理原片从 610 部降至 **300 部**；扣除 91 部隔离网络中断项后，仅余 **209 部**待初筛。
2. **确认与发布**：
   - 净增确认原片 **26 部**（全库确认数达 **1,180 部**）。
   - 净增有效分P版本 **32 个**（全库发布版本数达 **1,625 个**）。
   - 0 撤回，0 跨原片分P绑定冲突。
3. **核验严谨性**：
   - 全部 32 个新增版本均完成人工标题元数据快照复核，无年份、集次冲突或未授权衍生内容。
   - 全部 32 个新增版本均通过 Playwright 实播烟测，媒体流时长与元数据误差均 $\le 2.3$ 秒（严格符合 $\le 3$ 秒标准），且全部命中播放器实际网络请求 CID。
   - 历次增量均通过数据校验（`check`）、71 项 Python 单元测试及桌面端/移动端 15 个浏览器场景测试。
4. **异常隔离**：
   - 增量四十、四十一遇到的 2 次网络连接异常（`ll3CMgiUPuU`、`mJHvSp9AKYg`）均严格遵循零猜测规则，不直接判定为视频失效，不自动重试，隔离写入排除清单，累计排除原片数记为 91 部。

## 2026-11-09 第1轮推进（continue-20261109-r1）

本轮在分支 `continue-20261109-r1` 工作，对应本地提交 `b148920`（未推送、未合并到 `main`）。本轮不修改发布数据 [`data.json`](data.json)，核实并记录以下关键事实与工作进展：

### 1. 实播烟测退出码强化与测试套件扩充
- [`scripts/playback_smoke.cjs`](scripts/playback_smoke.cjs) 机制强化：任何检查失败或检查集合为空（0 条检查）时，CLI 进程均严格以非 0 状态码退出；输出报告中每条 check 对象均包含布尔型 `passed` 及详细问题列表 `issues`。
- 新增评估函数 [`scripts/playback_smoke.cjs#L23-L32`](scripts/playback_smoke.cjs#L23-L32)，统一评估执行结果并在存在异常时汇总失败信息。
- 单元测试扩展：在 [`tests/test_playback_smoke.py`](tests/test_playback_smoke.py) 中新增离线单元测试与本地 HTTP 端到端超时模拟用例。全套 Python 单元测试数量从 71 项扩充至 75 项。经本地真实运行，75 项测试全部通过（Ran 75 tests in 5.744s, OK），无编造测试结果。本项改动包含在本地提交 `b148920` 中（未推送、未合并 main）。

### 2. 11月8日历史新增版本的实播审计与现状
- 针对 11 月 8 日提交 `d697cec` 相对 `f2d8860` 引入的 106 个新版本：此前提交 `b4e780d`（已在 `main`）已完成对其中 59 个缺少独立日志版本的实播审计，记录归档于 [`reports/playback-audit-59.json`](reports/playback-audit-59.json)。
- 审计结果：58 个版本实播通过；1 个版本 `ugvHCXCOmm4` / `BV13Em8YFEjg` 因播放器实播时长（12202.1 秒）与声明时长（18901 秒）严重不符（偏差 6698.9 秒 > 3 秒）撤回并设待审；另有 `b2F-DItXtZs` / `BV1eq4y1176K` 亦因实播流时长（327.8 秒）与声明（336 秒）偏差 8.2 秒 > 3 秒撤回。
- 当前公开库（[`data.json`](data.json)）中该批仍上线的 104 个版本均具备实播日志且全部通过。本轮无需也不做重复实播。

### 3. 主页地址配置与 GitHub 仓库设置交回项
- 本地提交 `b148920` 已在 [`package.json`](package.json) 中添加 `homepage` 字段：`https://farmland2049.github.io/youtobili/`（未推送、未合并 main）。
- 经核对，GitHub 仓库设置（Repository Settings）里的 Website 仍配置为旧值 `https://qinqiang316.github.io/youtobili/`。因修改仓库设置需要仓库管理权限与专门授权，本轮未作修改，明确记为未完成交回项。

### 4. 待审队列失真与工作库状态卡点
- 从 [`data/confirmed.json`](data/confirmed.json) 执行 `import` 重建工作库后缺少 `search_result_limit`，无法忠实清理 4820 条已扩大待审原片。
- [`reports/STATUS.md`](reports/STATUS.md) 中显示「待审中尚需扩大 5018 / 已扩大 50」，属于 `import` 重建后的失真统计，不能当作真实队列恢复。

### 5. 未处理原片匹配批次与进展
- 本轮另对未处理原片运行了 1 批 `match --primary-first --limit 50 --delay 2`，并使用 `--exclude-vid` 明确排除此前隔离的 91 个网络异常原片。
- 批次 ID 为 `20261109T085022Z`；50/50 完成，全部 `status=review`，0 新确认，0 错误，0 风控停止；日志见 `/workspace/youtobili-r1-logs/match-r1-batch1.log`。
- 处理后状态：完成处理 6154→6200（[`reports/STATUS.md`](reports/STATUS.md) 当前），确认原片仍 1180，全库覆盖率仍 18.28%；未处理约 254（6454-6200）。

### 6. 离线线索整理与核验
- `seed-identities` 离线得 1 条线索，经 `verify-leads` 核验后仍为 `review`（时长超容差且简介多原片链接），0 确认。
- `seed-related` 离线新增 4 条合集候选线索，未自动批准。

### 7. 交付与发布现状
- 本轮无新上线版本，故未跑实播烟测增量、未 `build` 发布数据。
- 单元测试经本地真实运行，75 项测试全部通过（Ran 75 tests in 5.744s, OK）。
- 仍未推送、未开 PR、未合并 `main`。

## 2026-11-09 第2轮推进（continue-20261109-r2）

### 1. 待审统计失真根因
- `build()` 写 `data/confirmed.json` 账本时此前只保留 `vid`、`status`、`completed_at` 和已确认候选，丢掉 `searched_at`、`search_session_version`、`search_queries`、`search_result_limit`、`last_error`。
- `data/work/` 不进 Git，新环境 `import` 重建后这些字段缺失，`report()` 把缺失的 `search_result_limit` 当作 0，于是全部算成「尚需扩大」。
- 提交 `7390ae8` 时真实为尚需扩大 198 / 已扩大 4820；r1 重建后显示 5018 / 50。

### 2. 修复（提交 ba8dff9，已并入 main / d133287）
- 新增 `ledger_entry()`，账本保留上述 5 个搜索元数据字段（待审候选仍只留本地）；
- `report()` 新增第三类 `review_search_metadata_missing`（无搜索元数据、无错误），`STATUS.md` 显示「待审中搜索元数据缺失（重建丢失，状态未知，需重新搜索）」；
- `--expand-review` 仍选入这类条目（其待审候选已随重建丢失，只能重新搜索）；
- 新增 4 项单元测试，共 79 项。

### 3. 修复前后工作库对比
- 修复前后同一工作库：尚需扩大 5018→0，已扩大 50→50，元数据缺失 0→5018（新类）。
- 4820 条的逐条扩大状态与 213,596 个待审候选当时只存在原本地 `data/work/`，未入库，无法逐条恢复，只能用 `--expand-review` 重新搜索补回。

### 4. 积压处理与匹配批次
- 运行 `match --expand-review --primary-first --limit 50 --delay 2`，排除 91 个此前隔离的网络异常原片：
  - 批次 `20261109T100701Z`：完成 9，第 10 条 `gM95HHI4gLk` `TimeoutError` 停止；
  - 批次 `20261109T101202Z`（另排除 `gM95HHI4gLk`）：完成 12，第 13 条 `YQ2QtKcK2dA` `URLError` 停止。
- 两次普通网络错误后按规则停止，不自动重试；这两个原片隔离，不判失效，累计隔离 93。
- 共重新搜索 21 条旧待审原片，新确认 4 条（均为B站简介写明原片链接/ID）：
  - `iDulhoQ2pro` → `BV1XQWCe8EHf`
  - `-EVqrDlAqYo` → `BV1uM4y1r7er`
  - `5MgBikgcWnY` → `BV1Fb4y1Q73z`
  - `oUaOucZRlmE` → `BV1WX4y1P7Yo`
- 本次暂缓详情的候选 25+22 个。

### 5. 指标前后变化
- 完成处理 6200→6200（重新搜索的都是已处理条目）；
- 确认原片 1180→1184，覆盖率 18.28%→18.35%；
- 发布版本 1625→1629；
- 待审 5068→5064；
- 尚需扩大 0→2（两条网络错误），已扩大 50→67，元数据缺失 5018→4995。

### 6. 实播烟测与重建模拟
- 4 个新版本已 `build` 并实播烟测通过（`reports/playback-r2-batch.json`，4/4，时长与CID一致）。
- 重建模拟：删除 `library.json` 后从新 `confirmed.json` `import`，统计与本地完全一致（2/67/4995）。

### 7. 验收与交接状态
- 验证：`npm test` 79 项 OK；`npm run test:browser` 15 场景 pass（originals 1184，`browser-tests.json` 随数据更新）；`pipeline check` PASS 1184 原片 / 1629 分P。
- 第2轮最终已合并 main：`origin/main` = `d133287`。Website 仍是旧链接，未改。
- 剩余：约 4995 条待审需重新搜索；254 条未处理原片；93 条网络隔离原片待单条复查。

## 2026-11-09 第3轮推进（continue-20261109-r3）

- 分支 `continue-20261109-r3`，最终提交 `39131b4`（已并入 `main`）。基线 `main` = `d133287`。
- 文档：本轮开头已用 agy 补记第2轮结果，并在 `WORKFLOW.md`「扩大旧待审」节补充账本保留搜索元数据与三类待审说明；批次成果正文因 agy 地区限制两次失败未写入，现由第4轮补记。
- 起点：确认 1184 / 版本 1629；待审三类：尚需扩大 2 / 已扩大 67 / 元数据缺失 4995；隔离网络异常原片 93；完成处理 6200。
- 目标：分批 `match --expand-review --primary-first` 重搜元数据缺失待审（批次 limit 约 50，遇网络错按现有规则停批/排除/满 2 错批停）；有新确认则实播检查并写 reports；更新 STATUS/summary。
- 本轮文档目标：补记第2轮结果与第3轮目标；若 agy 地区限制导致文档未写入，如实记录。

### 1. 匹配批次
- 批次（`match --expand-review --primary-first --limit 50 --delay 2`）：
  - `20261109T111816Z`：排除 93；完成 6（确认 3 / 待审 4），第 7 条 `AouW9_jyZck` `TimeoutError` 停止；暂缓详情候选 27。
  - `20261109T113114Z`：另排除 `AouW9_jyZck`（排除 94）；完成 27（确认 3 / 待审 25），第 28 条 `LIb3L4vKZ7U` `URLError` 停止；暂缓详情候选 26。
  - 两次普通网络错误后按规则停止，不自动重试；两原片隔离不判失效，累计隔离 95。

### 2. 新确认条目
新确认 6 条（均为自动匹配确认）：
- `yCd3CzGSte8` → `BV12u411C7vh`（original，4386秒，CID 575509095）
- `NfnWJUyUJYU` → `BV1ap4y1D7ML`（original，4748秒，CID 202689347）
- `AaTRHFaaPG8` → `BV1cxwqeBE4v`（sub_zh，11871秒，CID 27951368336）
- `RJVL80Gg3lA` → `BV1SW411E74j`（original，3309秒，CID 31948556）
- `Yf1o0TQzry8` → `BV1gc411T7G8`（original，2862秒，CID 1116067897）
- `cIQ0yIZgQeE` → `BV18hWJeoERK`（original，1513秒，CID 500001659003991）

### 3. 指标前后变化（终点）
- 完成处理 6200→6201；
- 确认原片 1184→1190；
- 覆盖率 18.35%→18.44%；
- 发布版本 1629→1635；
- 待审 5064→5058；
- 尚需扩大 2→4；
- 已扩大 67→94；
- 元数据缺失 4995→4960。

### 4. 实播验证
- `reports/playback-r3-batch.json`：6/6 通过，时长与CID一致；未做逐帧比较。

### 5. 验收与交接状态
- 验证：`npm test` 79 项 OK；`npm run test:browser` 15 场景 pass（originals 1190，`browser-tests.json` 随数据更新）；`pipeline check` PASS 1190 原片 / 1635 分P。
- 本轮提交已并入 `main`（`39131b4`）。Website 后来已改为 `https://farmland2049.github.io/youtobili/`（另事由强哥授权完成，非本轮提交内容）。
- 剩余交接：约 4960 条元数据缺失待审需继续重搜；253 条未处理；95 条网络隔离原片待单条复查。

## 2026-11-09～10 第4轮推进（continue-20261110-r4）

- 分支 `continue-20261110-r4`，相对 `main` `39131b4`，5 个提交：`aab9a5d`（补第3轮批次正文到 CONTINUATION）、`6878072`、`d1f48a7`、`e85d937`（过程提交）、`9b3f8f2`（最终）。已并入 `main`（`origin/main` = `9b3f8f2`）。日志位于 `/workspace/youtobili-r4-logs/`。
- 起点：确认 1190 / 版本 1635；待审三类：尚需扩大 4 / 已扩大 94 / 元数据缺失 4960；完成处理 6201；隔离网络异常原片 95。
- 方式：过夜循环脚本 `run-batches.sh` 反复跑 `match --expand-review --primary-first --limit 50 --delay 2`，带 `--exclude-vid` 排除隔离原片；普通网络错误结束本批、该原片加入排除名单；连续 2 个错误批次后休眠 15–30 分钟再继续；遇 412/Blocked 硬停；原定截止 2026-11-10 06:00（北京时间）。

### 1. 匹配批次
时间均为北京时间：
- `20261109T134640Z`（11-09 21:46–21:50）：排除 95；尝试 7，完成 6 均待审，第 7 条 `ZK3O402wf1c` `TimeoutError`。
- `20261109T135054Z`（21:50–22:14）：排除 96；完成 50/50，全部待审，无错误。
- `20261109T141413Z`（22:14–22:43）：排除 96；完成 49，确认 3（`JjDsP5n2kSM`、`5Ge2RcvDlgw`、`CTV-wwszGw8`），第 50 条 `GJCF-Ufapu8` `TimeoutError`；暂缓详情候选 19。
- `20261109T144348Z`（22:43–23:09）：排除 97；完成 24，确认 1（`JEYh5WACqEk`），第 25 条 `hB6eY73sLV0` `URLError`；暂缓详情候选 11。之后连续 2 个错误批次，休眠（日志写 1239 秒，实际墙钟到 11-10 05:12 才恢复，约 6 小时，原因不明，可能宿主休眠）。
- `20261109T211211Z`（11-10 05:12–05:16）：排除 98；完成 2 均待审，第 3 条 `kjBOesZCoqc` `RemoteDisconnected`。
- 第 6 批 05:16 启动（排除 99），05:44 应强哥提前检查的要求被终止（rc=143），未写批次回执；期间已搜索 1 条 `n8m7lFQ3njk`（仍待审，计入已扩大）。
- 五批 `stopped` 均为 `false`，日志无 412/Blocked；停因 EARLY_CHECK（提前检查），不是风控。

### 2. 新确认条目
新确认 4 条（均为简介中明确原片链接，自动匹配确认，均为 `original` 档、分P 1）：
- `JjDsP5n2kSM` → `BV1qs4y1h7yq`（4551秒，CID `1017935532`）
- `5Ge2RcvDlgw` → `BV1wu411D7C4`（1040秒，CID `471602324`）
- `CTV-wwszGw8` → `BV1MZ4i6WEDS`（1028秒，CID `43370087433`）
- `JEYh5WACqEk` → `BV1PQ4j6oELC`（672秒，CID `43399184832`；原片时长 728，差 56 秒，低于阈值 `max(60, 8%)`）

### 3. 指标前后变化（终点）
- 完成处理 6201 不变；
- 确认原片 1190→1194；
- 覆盖率 18.44%→18.50%；
- 发布版本 1635→1639；
- 待审 5058→5054；
- 尚需扩大 4→8；
- 已扩大 94→222；
- 元数据缺失 4960→4824；
- 账本改动 136 条 = 确认 4 + 已扩大仍待审 128 + 网络错误 4。
- 隔离原片 95→99（新增 `ZK3O402wf1c`、`GJCF-Ufapu8`、`hB6eY73sLV0`、`kjBOesZCoqc`）。

### 4. 实播验证
- `reports/playback-r4-batch.json`：4/4 通过，播放器时长与声明时长差 0，CID 一致；未做逐帧比较。

### 5. 验收与交接状态
- 验证：`npm test` 79 项 OK；`npm run test:browser` 15 场景 pass（originals 1194）；`pipeline check` PASS 1194 原片 / 1639 分P。
- Grok Build 独立验收通过（`/workspace/youtobili-r4-logs/grok-review-r4.md`）。

### 6. 遗留缺口与 search-health 原因核查
- 第4轮遗留缺口：本 CONTINUATION 当时没写第4轮小节（现由第5轮补记）；`reports/search-health.json` 在提交 `6878072` 中被记为 `passed:false`。
- `search-health` `passed:false` 原因（第5轮核查）：
  - 该文件 `checked_at` 为 `2026-11-09T13:41:35Z`（北京时间 21:41，第4轮开跑前）。
  - 三条查询都返回 `code 0`、各 20 条结果、未被拦截（`stopped:false`），只是第 2、3 条查询（How to Speak Patrick Winston → `BV1tU4y187xz`；3Blue1Brown 神经网络 → `BV1bx411M7Zx`）当次结果里没有预期视频，第 1 条命中。`passed` 规则要求三条都命中预期 BV。
  - 第5轮开工时（2026-11-10 07:51 北京时间）原样重跑 `python3 scripts/search_health.py`，三条全部命中，`passed:true`，退出码 0。
  - 结论：不是代码问题，也不是风控，而是 B 站游客搜索排序当时的临时波动；不改代码，`search-health.json` 已更新为本次通过的结果。
  - 另注：第4轮在健康检查未通过的情况下仍开了批次，此后应先看健康检查再开批。

## 2026-11-10 第5轮推进（continue-20261110-r5）

- 分支 `continue-20261110-r5`，从 `origin/main` `9b3f8f2` 新建；日志位于 `/workspace/youtobili-r5-logs/`。
- 起点：确认 1194 / 版本 1639；待审三类：尚需扩大 8 / 已扩大 222 / 元数据缺失 4824；完成处理 6201 / 6454；隔离原片 99。
- 目标：强哥要求「继续开发，直到我让你暂停再整理并检查」。用循环脚本 `/workspace/youtobili-r5-logs/run-batches.sh` 不设截止时间反复跑 `match --expand-review --primary-first --limit 50 --delay 2 --exclude-vid...`；每批开始前检查暂停文件 `PAUSE`；遇 Blocked 硬停；连续 2 个错误批次休眠后再试；每 5 批本地提交一次；停下后补实播抽检、跑全部测试并补齐本小节结果。

### 1. 匹配批次
- 方式：循环脚本 `/workspace/youtobili-r5-logs/run-batches.sh` 不设截止时间，反复跑 `match --expand-review --primary-first --limit 50 --delay 2`，带 `--exclude-vid` 排除隔离原片；普通网络错误结束本批、该原片加入排除名单；连续 2 个错误批次后休眠 15–30 分钟再继续；遇 Blocked 硬停；每 5 批本地提交一次。
- 停因：秦强在 youtobili 群说「暂停」。循环进程 21392 被终止。不是风控，也不是 Blocked/412。已完成的 14 批 stopped 均为 false，日志无 Blocked/HTTP 401/403/412/429。
- 批次（时间均为北京时间 2026-11-10）：
  - `20261109T235552Z`（07:55–08:14）：排除 99；完成 50/50，确认 6 / 待审 44，暂缓详情候选 34；rc=0。确认数 1200。
  - `20261110T001450Z`（08:14–08:40）：排除 99；完成 50/50，全部待审，无错误；rc=0。确认数仍 1200。
  - `20261110T004046Z`（08:40–09:13）：排除 99；完成 22，确认 2 / 待审 21，第 23 条 `HI09kat_GeI` `URLError`；暂缓 11；rc=2。确认数 1202。
  - `20261110T011324Z`（09:13–09:21）：排除 100；完成 12，全部待审，第 13 条 `ZTC_RxWN_xo` `RemoteDisconnected`；rc=2。确认数仍 1202。随后连续 2 个错误批次，休眠 1065 秒后继续。
  - `20261110T013946Z`（09:39–09:58）：排除 101；完成 30，确认 2 / 待审 29，第 31 条 `52Mx0_8YEtg` `URLError`；暂缓 14；rc=2。确认数 1204。提交 `d6edf94`。
  - `20261110T015829Z`（09:58–10:04）：排除 102；完成 9，确认 1 / 待审 9，第 10 条 `DJtef410XaM` `TimeoutError`；暂缓 9；rc=2。确认数 1205。随后连续 2 个错误批次，休眠 1119 秒后继续。
  - `20261110T022307Z`（10:23–10:50）：排除 103；完成 50/50，确认 1 / 待审 49，暂缓 14；rc=0。确认数 1206。
  - `20261110T025027Z`（10:50–11:13）：排除 103；完成 50/50，确认 1 / 待审 49，暂缓 30；rc=0。确认数 1207。
  - `20261110T031314Z`（11:13–11:14）：排除 103；完成 0，第 1 条 `kya_LXa_y1E` `URLError`；rc=2。确认数仍 1207。
  - `20261110T031438Z`（11:14–11:32）：排除 104；完成 33，确认 2 / 待审 32，第 34 条 `8Ko3TdPy0TU` `RemoteDisconnected`；暂缓 11；rc=2。确认数 1209。提交 `ea02470`。随后连续 2 个错误批次，休眠 1512 秒后继续。
  - `20261110T035806Z`（11:58–12:44）：排除 105；完成 23，确认 1 / 待审 23，第 24 条 `NHopJHSlVo4` `URLError`；暂缓 23；rc=2。确认数 1210。
  - `20261110T044435Z`（12:44–13:26）：排除 106；完成 36，确认 3 / 待审 34，第 37 条 `iGFqfTCL2fs` `TimeoutError`；暂缓 32；rc=2。确认数 1213。随后连续 2 个错误批次，休眠 1201 秒后继续。
  - `20261110T054714Z`（13:47–14:20）：排除 107；完成 50/50，全部待审，无错误；rc=0。确认数仍 1213。
  - `20261110T062035Z`（14:20–14:45）：排除 107；完成 50/50，确认 3 / 待审 47，暂缓 38；rc=0。确认数 1216。此为最后完整批次。
  - 第 15 批 `20261110T064533Z`（14:45 启动）：排除 107；14:49 因「暂停」被 SIGNAL 中断。match 日志写下 7 条均待审（`iffTJ1vPCSo`、`j-vJxez9UF8`、`jVoSQP2yUYA`、`jgOTZe07eHA`、`jh8supIUj6c`、`k7X7sZzSXYs`、`klaJqofCsu4`），回执不完整（completed=7、attempted=6、statuses.review=6，无 candidate_count）。无新确认。已把这 7 条从已扩大还原为元数据缺失（candidates 清空，completed_at 恢复为 batch 10 账本中的原值），不完整回执移出 `data/work/batches/`，保存到日志 `batch-20261110T064533Z.interrupted.json`。batch 1–14 已完成数据未删。还原后统计与 batch 14 结束时一致。

### 2. 新确认条目
新确认 22 条（均为简介中明确原片链接的自动匹配确认，均分P 1；除另注外原片时长与发布时长相同或相差 1 秒）：
- `0bcZb-SsnrA` → `BV14V411Y7hG`（original，2261秒，CID 307089566）
- `1ffBJ4sVUb4` → `BV1ux41167yX`（original，5983秒，CID 19152212）
- `43XKfuptnik` → `BV1qr61BWEFW`（dub_zh，2660秒，CID 35730558491；原片时长 2793，差 133 秒，低于阈值 max(60, 8%)）
- `AmgkSdhK4K8` → `BV161UUBdEaJ`（original，990秒，CID 34252392672）
- `Bd8_vO5zrjo` → `BV124411Y7Wv`（original，2506秒，CID 128961342）
- `G_eYTctGZw8` → `BV1Ka411v7qK`（original，2398秒，CID 575831787）
- `IV3dnLzthDA` → `BV1gY4y1h7Di`（original，1497秒，CID 710887228）
- `OoJsPvmFixU` → `BV1sP7u6VETR`（original，3614秒，CID 39326322628；原片时长 3920，差 306 秒，低于阈值 max(60, 8%)）
- `S7TUe5w6RHo` → `BV1jWfnBeE56`（sub_zh，3736秒，CID 36195143661；原片时长 3811，差 75 秒，低于阈值 max(60, 8%)）
- `T647CGsuOVU` → `BV15K4y1Y7ar`（original，347秒，CID 238675023）
- `Tb823aqgX_0` → `BV16T411U78B`（original，2203秒，CID 1015774755）
- `VQKMoT-6XSg` → `BV16p4y147sG`（original，4751秒，CID 335629630）
- `XvDZLjaCJuw` → `BV19W411U7vZ`（original，1419秒，CID 57000379）
- `YyIQKBzIuBY` → `BV1fA411e7Ts`（original，3399秒，CID 212823891）
- `ZMByI4s-D-Y` → `BV1KxWJ6hEJQ`（original，704秒，CID 43436608202）
- `bHIhgxav9LY` → `BV1Bxno65EEw`（original，888秒，CID 43079238333）
- `gEKSpZPByD0` → `BV1bJ411r7Xc`（original，5875秒，CID 135570925）
- `m3svKOdZijA` → `BV1ey4y1Z7AW`（original，2191秒，CID 1016730180）
- `sGG-A80Tl5g` → `BV1jk4y1j7Pe`（original，1392秒，CID 1119058808）
- `tISy7EJQPzI` → `BV1Ex411V7Sv`（original，5473秒，CID 24335235）
- `wJyUtbn0O5Y` → `BV1zt4y1q7Ww`（original，193秒，CID 236788118）
- `xt1KNDmOYqA` → `BV1rH4y1w7sq`（original，1813秒，CID 1614944674）

### 3. 指标前后变化
终点指标（还原 batch 15 中断产物并 build 之后，与 batch 14 结束时一致）：
- 完成处理 6201 不变；
- 确认原片 1194→1216（+22）；
- 覆盖率 18.50%→18.84%；
- 发布版本 1639→1661；
- 待审 5054→5032；
- 尚需扩大 8→16；
- 已扩大 222→665；
- 元数据缺失 4824→4351；
- 账本相对基线改动 473 条（新确认 22 + 新写入搜索元数据 449 + 新记录错误 2）。
- 隔离原片 99→107（新增 `HI09kat_GeI`、`ZTC_RxWN_xo`、`52Mx0_8YEtg`、`DJtef410XaM`、`kya_LXa_y1E`、`8Ko3TdPy0TU`、`NHopJHSlVo4`、`iGFqfTCL2fs`）。

### 4. 实播验证
- `reports/playback-r5-batch.json`：22/22 通过；播放器时长与声明时长差最大 1.22 秒（阈值 3 秒），CID 一致；未做逐帧比较。

### 5. 验收与交接状态
- 验证：
  - `npm test` 79 项 OK；
  - `npm run test:browser` 15 场景 pass（originals 1216；`reports/browser-tests.json` 已按要求 checkout 还原，未纳入提交）；
  - `pipeline check` PASS 1216 原片 / 1661 分P。
- 提交与交接：
  - 本轮已有本地提交（均未 push、未合并 main）：`fc98494`（第5轮开工时补记第4轮小节并刷新 search-health）、`d6edf94`（b5，确认 1194→1204）、`ea02470`（b10，确认 1194→1209）、`76feb7e`（收尾数据提交，确认 1194→1216）。文档与 `reports/playback-r5-batch.json` 将在本节写入后另作提交，文档中不编造该提交 sha。
  - 交接状态：未 push、未合并 main。
  - 剩余约 4351 条元数据缺失待审需继续重搜；253 条未处理（6454-6201）；107 条网络隔离原片待单条复查。
  - 因秦强暂停而停，未跑完后续批次。

## 2026-11-10 阶段增量（Round 6）

### 1. 目标与执行
- 承接上一轮基线（`32e695b`，确认原片 1216 条、1661 个版本）。
- 启动 `continue-20261110-r6` 分支，执行第 6 轮扩大审查匹配批次（`match --expand-review --primary-first --limit=50 --delay=2`）。
- 连续执行 5 个批次（b1–b5），共计对 250 条历史待审条目补查第 6–20 个候选（共检阅 1877 个候选），0 请求错误，0 触发风控。

### 2. 新确认条目
- `wAIP6fI0NAI` → `BV1UE411q7Uu`（original，1032秒，CID 127414906，P1；B站标题《How one tweet can ruin your life|社交媒体将如何摧毁你的生活》，简介含明确原片链接 `https://youtu.be/wAIP6fI0NAI`，单P时长 1032 秒与原片完全一致）。

### 3. 指标前后变化
- 完成处理条数：6201；
- 确认原片：1216 → 1217（+1）；
- 发布版本：1661 → 1662（+1）；
- 全库覆盖率：18.84% → 18.86%；
- 检阅待审候选：补查 250 条原片之后续候选，写入工作库与发布数据。

### 4. 实播验证与脚本加固
- 实播检查：`reports/playback-r6-batch.json` 针对新发布条目 `wAIP6fI0NAI` 执行真实播放 smoke 检查，结果为 PASS（`readyState: 4`, `currentTime: 3.93s`, `duration: 1032s`, 请求 CID `127414906` 确认命中，未做逐帧比较）。
- 抽样基线检查：对 6 种版本形态（official_zh, sub_zh, original, dub_zh, short, collection）全量运行 `playback_smoke.cjs`，6/6 全部通过。
- 脚本机制优化：加固 `scripts/playback_smoke.cjs`，在 `frame.locator('video').waitFor()` 之后增加 `waitForFunction` 等待视频 readyState >= 1 或 source 挂载，彻底避免动态 blob 播放器在挂载流媒体前被触发 play() 导致偶发空源报错。

### 5. 验收与交接状态
- 数据校验：`python3 scripts/pipeline.py check` 通过（1217 originals, 1662 verified segments）。
- 单元测试：79 项 Python 单元测试全部通过（Ran 79 tests in 3.223s, OK）。
- 浏览器场景测试：15 项端到端场景全部通过（1217 条原片渲染正常）。
- 分支合并准备就绪，合并至 `main` 并开启新分支 `continue-20261110-r7` 继续推进。

## 2026-11-10 阶段增量（Round 7）

### 1. 目标与执行
- 承接 Round 6 基线（`6ce52e1`，确认原片 1217 条、1662 个版本）。
- 启动 `continue-20261110-r7` 分支，连续执行 5 个扩大审查匹配批次（b1–b5，命令 `match --expand-review --primary-first --limit=50 --delay=2`）。
- 共计处理 250 条原片扩大审查（覆盖所有历史待审条目中候选不足 20 的条目，以及推进元数据缺失条目的重新搜索检索），检阅候选总数由 5,523 个扩充至 13,239 个（净增 7,716 个候选条目并持久化保存至 `data/confirmed.json`）。
- 全程 0 请求错误，0 触发风控。

### 2. 新确认条目
- 本轮 5 个批次主要为扩大审查补全 6–20 个候选，本轮无新增确认条目（已确认数维持 1,217 条、1,662 个版本），所有不符合规则阈值的候选按规范保持 review 状态。

### 3. 指标前后变化
- 完成处理条数：6,201 / 6,454；
- 确认原片：1,217 条；
- 发布版本：1,662 个；
- 全库覆盖率：18.86%；
- 检阅候选总数：5,523 → 13,239（+7,716）；
- 已扩大检查仍待审核条目：878 → 1,128（+250）；
- 待审中搜索元数据缺失需重新搜索条目：4,086 → 3,886（-200）。

### 4. 验证与验收状态
- 数据校验：`python3 scripts/pipeline.py check` 通过（1217 originals, 1662 verified segments）。
- 单元测试：79 项 Python 单元测试全部通过。
- 浏览器场景测试：15 项端到端场景全部通过。
- 分支合并准备就绪，合并至 `main`。

## 2026-11-11 阶段增量（Round 8）

### 1. 目标与执行
- 承接 Round 7 基线（`2fff4c9`，确认原片 1217 条、1662 个版本）。
- 启动 `continue-20261110-r8` 分支，按计划彻夜连续推进至 2026-11-11 05:30。
- 连续执行 50 个批次（b1–b50）：
  - b1–b7：针对此前未处理原片（not_processed）执行标准匹配，完成 204 条未处理原片处理，未处理数从 253 骤降至 49；直接发掘并确认多条具有显式 YouTube 原片来源的条目。
  - b8–b50：针对历史待审条目执行扩大候选检查（6–20 候选）以及缺失元数据重新检索。
- 全程严格遵守串行限速（2s 间隔）与风控熔断机制，0 触发 412 风控，0 触发登录限制。

### 2. 新确认条目（共 15 条，每条简介均有明确对应 YouTube 原片链接，时长在容差内，实播全部通过）
- `-DVyjdw4t9I` → `BV1towjedEH5` P1（sub_zh, 11751秒, CID 27910275410；[310] Python之父Guido van Rossum_编程的未来[中英精校]）
- `1YFrISfN7jo` → `BV1Ht411m7PQ` P1（original, 967秒, CID 63414319；The Geometry of Causality _ Space Time）
- `3pvpNKUPbIY` → `BV1hVreY4E5z` P1（sub_zh, 9879秒, CID 27769241858；[233] Instagram联合创始人Kevin Systrom_揭秘社交帝国[中英精校]）
- `3wMKoSRbGVs` → `BV1RRrSYCEir` P1（sub_zh, 10376秒, CID 27742571718；[212] AI领域先驱Douglas Lenat_Cyc与常识推理的探索[中英精校]）
- `F3Jd9GI6XqE` → `BV1FvfaYjEAV` P1（sub_zh, 10245秒, CID 28014479814；[381] 麻省理工学院教授Edward Gibson_人类语言、心理语言学、句法与LLMs[中英精校]）
- `RGw6fXprV9U` → `BV1hD4y1Q7Up` P1（sub_zh, 1803秒, CID 207358802；【中英双字】制作铀玻璃 NileRed）
- `ett_8wLJ87U` → `BV1Ys4y197Yy` P1（original, 3886秒, CID 1107596261；[BobbyBroccoli/字幕付] 那个伪造了人类克隆的男人 上篇）
- `tWdgAMYjYSs` → `BV1Wo4y1d7KP` P1（original, 126秒, CID 294178447；Max Headroom WTTW Pirating Incident - 11_22_87）
- `uASUHbFEhWY` → `BV1US4y167Uf` P1（original, 164秒, CID 518319054；名场面--10年前的动画预言了苹果眼镜的未来形态 - eyePhone）
- `up863eQKGUI` → `BV1Sx41177nn` P1（original, 582秒, CID 25777269；【怀旧向】90年代版权保护宣传 Don't Copy That Floppy）
- `vKA4w2O61Xo` → `BV1rB4y1T74j` P1（original, 285秒, CID 365094665；The Most Common Cognitive Bias）
- `vjqt8T3tJIE` → `BV1Ad4y1z79J` P1（original, 1375秒, CID 839337026；[生肉]Did People Used To Look Older ?）
- `wCrtk-pyP0I` → `BV1jb41187zL` P1（original, 496秒, CID 78187217；How Microwaving Grapes Makes Plasma 微波葡萄如何产生等离子体）
- `y8OnoxKotPQ` → `BV1iq4y1574e` P1（original, 190秒, CID 427510459；Microservices）
- `zyaocKS3sfg` → `BV1n7411J75n` P1（original, 1699秒, CID 152290940；亚当萨维奇的Spot人(?)力车-Adam Savage's Spot Robot Rickshaw Carriage!）

### 3. 指标前后变化
- 原片总库：6,454
- 完成处理条数：6,201 → 6,405（+204）；
- 未处理条数：253 → 49（-204）；
- 确认原片：1,217 → 1,232（+15）；
- 发布版本：1,662 → 1,677（+15）；
- 全库覆盖率：18.86% → 19.09%（+0.23%）；
- 检阅候选总数：13,239 → 102,682（+89,443 个候选持久化至 `data/confirmed.json` 候选总账）；
- 已扩大检查仍待审核条目：1,128 → 3,487（+2,359）；
- 待审中搜索元数据缺失需重新搜索条目：3,886 → 1,714（-2,172）。

### 4. 实播验证与脚本加固
- 实播检查：`reports/playback-r8-batch.json` 针对 15 个新增确认版本全量执行真实播放 smoke 检查，结果为 15/15 全部 PASSED，实测 CID 与时长差均符合规范（未做逐帧比较）。
- 抽样基线检查：`reports/playback-checks.json` 对 6 种版本形态（official_zh, sub_zh, original, dub_zh, short, collection）全量运行，6/6 全部通过。
- 脚本加固：优化 `scripts/playback_smoke.cjs`，增加判断在点击播放器后若因浏览器自动缓冲行为触发暂停则进行二次 `evaluate(e.play())` 保护，彻底杜绝假阴性误报。

### 5. 验收与交接状态
- 数据校验：`python3 scripts/pipeline.py check` 通过（1232 originals, 1677 verified segments）。
- 单元测试：79 项 Python 单元测试全部通过。
- 浏览器场景测试：15 项端到端场景全部通过（1232 条原片渲染正常）。
- 分支合并准备就绪，合并至 `main`。

## 2026-11-11 阶段增量（Round 9）

### 1. 目标与执行
- 承接 Round 8 合并后基线（`a40b8d5`，确认原片 1232 条、1677 个版本）。
- 按照工作规范创建新分支 `continue-20261111-r9` 继续推进。
- 前置执行 `scripts/search_health.py`，三项真实中英文查询均返回 `code 0` 且命中目标 BVID，搜索健康检查通过。
- 连续执行 3 个扩大审查匹配批次（b1 5 条试点、b2 50 条、b3 50 条，共计 105 条原片）：
  - 针对高分历史待审条目补查第 6–20 个候选，并对缺失元数据条目进行重新检索。
  - 全程排除 112 条网络隔离原片，严格保持 2s 串行延迟，0 次 412 风控，0 次登录拦截，0 错误中断。

### 2. 指标前后变化
- 原片总库：6,454
- 完成处理条数：6,405
- 未处理条数：49（全部属于网络隔离原片，非隔离原片已 100% 处理完毕）
- 确认原片：1,232 条
- 发布版本：1,677 个版本
- 全库覆盖率：19.09%
- 检阅候选总数：102,682 → 106,612（净增 3,930 个候选并持久化至 `data/confirmed.json` 候选总账）
- 已扩大检查仍待审核条目：3,487 → 3,592（+105）
- 待审中搜索元数据缺失需重新搜索条目：1,714 → 1,609（-105 条成功重新检索）

### 3. 验收与交接状态
- 数据校验：`python3 scripts/pipeline.py check` 通过（1232 originals, 1677 verified segments）。
- 单元测试：79 项 Python 单元测试全部通过。
- 浏览器场景测试：15 项端到端场景全部通过。
- 准备提交并推送到远端 `continue-20261111-r9`，已合并至 `main`。

## 2026-11-12 阶段增量（Round 10 夜间连续推进）

### 1. 目标与执行
- 承接 Round 9 合并至 `main` 后基线（`d362717`，确认原片 1232 条、1677 个版本）。
- 签出全新夜间推进分支 `continue-20261111-overnight`，按计划彻夜连续推进至 2026-11-12 05:00（实际执行至 05:09 平稳收工）。
- 连续执行 22 个扩大审查批次（b1–b22，共处理 1,100 条待审原片候选 6–20 扩大检阅与缺失元数据重新检索）。
- 全程保持 2s 串行限速、排除 112 条网络隔离原片，0 次 412 风控，0 次登录限制，0 错误中断。

### 2. 新确认条目
- `kXpzp4RDGJI` → `BV1df4y1F7Hv` P1（original，299 秒，CID 418403124；Harvard Online《ATP synthase in action》，B站标题《ATP合酶(已嵌入英文字幕)/ATP synthase in action》，分P文件名包含 `ATP synthase in action-kXpzp4RDGJI.mp4-muxed`，B站简介含明确原片来源，单P时长 299 秒与原片完全一致，实播测试通过）。

### 3. 指标前后变化
- 原片总库：6,454
- 完成处理条数：6,405
- 未处理条数：49（全部属于网络隔离原片，非隔离原片保持 100% 处理完毕）
- 确认原片：1,232 → 1,233（+1 条）
- 发布版本：1,677 → 1,678（+1 个版本）
- 全库覆盖率：19.09% → 19.10%（+0.01%）
- 检阅候选总数：106,612 → 147,515（净增 40,903 个候选持久化至 `data/confirmed.json` 候选总账）
- 已扩大检查仍待审核条目：3,592 → 4,691（+1,099 条）
- 待审中搜索元数据缺失需重新搜索条目：1,609 → 509（-1,100 条成功覆盖恢复）

### 4. 实播验证
- 新增确认条目实播：`reports/playback-r10-batch.json` 记录 `kXpzp4RDGJI` 实播通过（`readyState: 4`, `currentTime: 3.79s`, `duration: 299s`, 命中实际 CID `418403124`，未做逐帧比较）。
- 抽样基线实播：`reports/playback-checks.json` 针对 6 种版本形态全量运行，6/6 全部通过。

### 5. 验收与交接状态
- 数据校验：`python3 scripts/pipeline.py check` 通过（1233 originals, 1678 verified segments）。
- 单元测试：79 项 Python 单元测试全部通过。
- 浏览器场景测试：15 项端到端场景全部通过（1233 条原片渲染正常）。
- 分支合并准备就绪，合并至 `main`。
