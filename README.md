# youtobili

从 HackerTube 发现好视频，在 B 站接着看。面向国内用户，只展示经过对应关系核验的 B 站版本；未匹配、存疑和失效条目隐藏。

**[访问网站](https://qinqiang316.github.io/youtobili/)** · [批次与覆盖率](reports/STATUS.md) · [操作说明](docs/WORKFLOW.md)

## 本地预览

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

浏览器打开 `http://127.0.0.1:8765/`。页面从相对路径加载 `data.json`，请通过 HTTP 预览。

## 更新流程

Python 3 标准库即可运行数据流程，无付费 API、个人账号或服务端依赖。

```sh
python3 scripts/fetch_source.py
python3 scripts/pipeline.py import
python3 scripts/pipeline.py match --limit 50
python3 scripts/pipeline.py export-review
python3 scripts/pipeline.py build
python3 scripts/pipeline.py check
python3 -m unittest discover -s tests -v
```

匹配批次遇到412、登录要求或限流立即停止并保留进度。先检查 `reports/STATUS.md`，不要连续重试。详细的合集定位、人工审核与发布步骤见[操作说明](docs/WORKFLOW.md)。

## 内容与版本规则

- 全量原片候选库，沿用原站16个领域、150个分类ID；分类中文化且隐藏没有确认视频的分类。
- 不设10分钟门槛。一条原片一张卡片；同一原片可以选择不同的确认版本。
- 内容完整、一致时，优先官方中文、中文字幕、中文配音、官方原语、其他原语；同档按播放量排序。
- 原片链接、内容身份、分P和时长共同用于检查。旧可信度、相似标题和相近时长不能直接作为审核通过依据。
- 喜欢、稍后再看和历史记录存储在本机浏览器；旧BV记录迁移为原片ID，不上传个人记录。
- 自动核验不代替观看内容的逐帧比对；覆盖率、处理量与播放抽查的边界见验收报告。

## 目录

| 位置 | 用途 |
| --- | --- |
| `web/` | 网页模板、脚本、样式、中文分类名称 |
| `scripts/` | 来源更新、匹配、审核、构建与校验 |
| `data/source/` | 原站公开导出快照、数据说明与来源哈希 |
| `data/confirmed.json` | 可重建的最小确认清单，不含完整接口响应 |
| `data/work/` | 本地候选、接口缓存、批次断点和待审队列，不进入 Git |
| `reports/` | 覆盖率、批次进展、发布与验收依据 |
| 根目录网页与 `data.json` | GitHub Pages 发布产物 |

## 来源与署名

数据来自 [HackerTube](https://hackertube.org) 与 [open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news)，遵循 [ODC-By 1.0](https://opendatacommons.org/licenses/by/1-0/)。完整来源说明保留在 [DATA.md](data/source/DATA.md)。原站分类与摘要可能存在误差；视频、标题及频道名称属于各自作者。本项目与 B 站、YouTube、HackerTube 无隶属关系，不下载或重新托管视频。
