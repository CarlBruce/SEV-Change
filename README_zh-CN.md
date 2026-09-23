# SEV-Change 数据发布包（草案）

本目录已将 RSRCC 与 DisasterM3 的语义等价问题变体整理为统一的 GitHub 发布结构。每条任务记录包含原始问题 `raw` 和七个受控变体 `t1`–`t7`，并保留视觉输入路径、标准答案及任务相关元数据。

> 当前是已公开的候选版，不是经过完整审核的最终 benchmark。明确的再使用许可证、人工语义等价审查、生成规则冻结和正式引用信息仍待完成。

GitHub 仓库为 [CarlBruce/SEV-Change](https://github.com/CarlBruce/SEV-Change)，候选版本为 `v0.1.0-rc1`。尚无数据集 DOI 或 GitHub Release 标签；准确状态见 `RELEASE_METADATA.md`。

## 获取完整数据

11 个原始 JSON 文件未改写，保存在同一个 ZIP 中。因当前上传通道对大文件超时，ZIP 分成 `release/` 下的七个编号分包。下载全部七个分包及 `release/parts.json`，运行：

```bash
python scripts/archive_parts.py assemble release/parts.json SEV-Change-v0.1.0-rc1-git.zip
```

脚本会校验每个分包及合并后的 ZIP 的 SHA-256。解压后可获得 `data/rsrcc/` 与 `data/disasterm3/`。ZIP 内的 `manifest.json` 记录上传前冻结状态；仓库根目录的 `RELEASE_METADATA.md` 记录当前发布状态。数据包不含影像和掩膜。

## 数据规模

| 来源 | 文件数 | 任务级记录 | 问题表述 |
|---|---:|---:|---:|
| RSRCC test | 1 | 21,999 | 175,992 |
| DisasterM3 十灾种 | 10 | 29,024 | 232,192 |
| 合计 | 11 | 51,023 | 408,184 |

DisasterM3 原始变体文件共有 30,042 条，其中 1,018 条是只有单张 `image_path` 的关系推理记录，不满足双时相输入定义，因此按可复现规则排除。具体分类数量见 `EXCLUSIONS.md`。

## 目录结构

```text
data/rsrcc/                 RSRCC 测试集变体
data/disasterm3/            DisasterM3 十灾种变体
scripts/                    过滤与校验脚本
manifest.json               文件统计、SHA-256 与校验结果
DATA_DICTIONARY.md          文件格式与字段字典
DATASET_CARD.md             数据卡草案
EXCLUSIONS.md               排除规则与数量
LICENSE_STATUS.md           来源许可与衍生标注授权状态
RELEASE_METADATA.md         仓库名、版本、访问地址和 DOI 状态
SOURCES.md                  RSRCC 与 DisasterM3 官方仓库和引用
RELEASE_CHECKLIST.md        正式上传前检查清单
```

本数据包衍生自 [RSRCC 官方数据页](https://huggingface.co/datasets/google/RSRCC) 和 [DisasterM3 官方仓库](https://github.com/Junjue-Wang/DisasterM3)。使用对应子集时应同时引用原始数据集；来源链接与已核实的引用信息见 `SOURCES.md`。

## 校验命令

```bash
python scripts/validate_dataset.py --write-manifest
```

脚本不依赖第三方 Python 包。当前全部 JSON 均通过结构校验；唯一警告是 RSRCC 中 `test_003550` 与 `test_009075` 共享相同的原始任务身份，但七类生成变体并不相同，因此暂时保留，等待回查源数据。

## 上传建议

- 直接建 GitHub 仓库时，单个最大文件约 60 MiB，未超过 GitHub 100 MB 单文件限制。
- 若计划频繁更新大 JSON，建议在正式建库前决定使用 Git LFS 还是 GitHub Release 附件，避免仓库历史持续膨胀。
- 不要把本地实验日志、模型权重、API 密钥或未授权影像一起上传。
