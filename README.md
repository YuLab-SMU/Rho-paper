# Rho-paper

Rho 的方法提案与论文稿作为一个独立项目维护。

论文需要的一手材料——读了哪些工作、读的是哪个版本、哪些判断已被既有研究覆盖、哪部分仍未验证——与实现仓库的日常推进不是同一套节奏和判据。因此这份工作单独成项目；[Rho](https://github.com/YuLab-SMU/Rho)、[Rho-core](https://github.com/YuLab-SMU/Rho-core) 和 [Rho-plugins](https://github.com/YuLab-SMU/Rho-plugins) 继续拥有各自的实现事实。

## 两份文档的分工

| 文档 | 是什么 | 读者 |
| --- | --- | --- |
| [论文稿](docs/MANUSCRIPT.md) | 论文体裁成稿：摘要、相关工作、方法、场景走查、使主张不成立的判据、局限与参考文献 | 想了解主张本身及其边界的人 |
| [论证与取舍记录](docs/PAPER.md) | 定位记录：每条来源标注了核查位置与“不能据此声称什么”，并保留逐次修改的历史 | 维护这套论证的人 |

两者不互相替代。论文稿去掉工作笔记，供独立阅读；定位记录保留证据层次的区分，是论文中每句限定语的来源。

## 现在有什么

- 候选贡献：依据当前科学目的和实际接入的能力，从持续分析中选择或取得材料、组织它们的关系并组合可操作的视图；这份组织同时是人理解分析的界面和 Agent 继续工作的共享上下文。
- 单细胞场景：判断差异在供者间是否一致、理解修正分析为何尚无新结果、为同一结果准备学术说明；以及本地可计算、远程排队、只有已有结果三种接入条件下的差别。
- 正面对照：InsightLens、WaitGPT、Mycelium、SEMV、DashChat、DynaVis、Data Formulator 2、生成式界面、Galaxy、JupyterLab，以及本文不认领的部分。

不含实验与用户观察。文中数据、运行与版本标识是说明机制的假设；远程单细胞接入是方法示例，不是已验收连接器清单。候选贡献的新颖性与人的收益都尚未被 Rho 已有检查证明。

## 与实现仓库的关系

| 项目 | 拥有的内容 |
| --- | --- |
| [Rho](https://github.com/YuLab-SMU/Rho) | 应用的选择、组装、窗口、布局与共享交互 |
| [Rho-core](https://github.com/YuLab-SMU/Rho-core) | 受管执行、请求身份与保留事实 |
| [Rho-plugins](https://github.com/YuLab-SMU/Rho-plugins) | 功能组件及可选的 CLI、Skills、MCP 与 UI 入口 |

对上述仓库记录的引用使用绝对公开路径，便于在实现推进后仍能追到依据；这些引用不把实现事实转成本项目的结论。

## 检查

```
python3 scripts/check_docs.py
```

检查本地链接、锚点、表格列数与路径包含关系，并在 `work/render/` 下生成可直接阅读的 HTML；退出码非零表示存在错误。依赖 `markdown` 与 `beautifulsoup4`。外部链接只列出，不联网验证。

## 维护方式

见 [AGENTS.md](AGENTS.md)。
