# Fi-Dog

自主推理链股票分析 Agent。基于 Claude Code 运行，通过 9 步分析链对股票市场事件进行深度分析，输出结构化 markdown 报告。

## 功能

给定一个股票代码和市场事件，自动执行：

1. **市场冲击检测** — 价格、技术指标、成交量分析
2. **基本面完整性检查** — P/E、EPS、FCF、利润率
3. **叙事验证** — 媒体报道 vs 事实对比
4. **情绪极端性分析** — 期权市场恐慌指标
5. **同业对标 + 误分类检测** — 个股 vs 行业整体表现
6. **抛售归因分解** — Beta放大、ETF被动卖出、叙事恐慌、基本面重定价
7. **收入风险分解** — 量化实际受威胁收入占比
8. **历史先例分析** — 类似事件的恢复模式
9. **反向论证构建** — 构建看多论点
10. **最终综合** — 公允价值、置信度、投资建议

报告输出到 `./reports/YYYY-MM-DD-{ticker}-{事件关键词}.md`

## 前置条件

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 包管理器
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI

## 安装

```bash
uv sync
```

可选：复制 `.env.example` 并设置 [Finnhub](https://finnhub.io/register) API key 获取更丰富的新闻数据：

```bash
cp .env.example .env
# 编辑 .env 填入你的 FINNHUB_API_KEY
```

## 使用

在项目目录下启动 Claude Code，然后输入分析请求：

```
claude

> 分析 IBM，事件：Anthropic 发布 Claude Code 展示 COBOL 编写能力导致 IBM 股价暴跌 13%
```

或者英文：

```
> Analyze AAPL, event: Apple announces major AI partnership causing stock volatility
```

Claude 会自动：
1. 运行 `tools/` 下的脚本获取市场数据
2. 执行 10 步分析链
3. 将报告写入 `./reports/`

## 项目结构

```
fi-dog/
├── CLAUDE.md           # Claude Code 的操作指南
├── README.md           # 本文件
├── pyproject.toml      # 项目配置 & 依赖 (uv)
├── tools/              # 数据获取脚本
│   ├── price.py        # 价格、成交量
│   ├── technicals.py   # RSI、SMA、MACD、布林带
│   ├── fundamentals.py # P/E、EPS、财务报表
│   ├── options.py      # 期权数据、看跌/看涨比
│   ├── news.py         # 新闻、情绪分析
│   └── peers.py        # 行业同行对比
├── reports/            # 分析报告输出目录
└── .claude/
    ├── settings.json   # Claude Code 权限配置
    └── skills/         # 分析框架 (Claude Code custom skills)
        ├── narrative-validation/    # 叙事验证问卷
        ├── options-divergence/      # 期权背离检测
        ├── selloff-attribution/     # 抛售归因分解
        ├── overreaction-multiple/   # 过度反应倍数计算
        └── historical-precedent/    # 历史先例匹配
```

## 数据源

| 数据 | 来源 | API Key |
|------|------|---------|
| 价格、基本面、期权、同行 | Yahoo Finance (yfinance) | 不需要 |
| 技术指标 | pandas-ta | 不需要 |
| 新闻 | Finnhub / Google News RSS | Finnhub 可选 |

## 自定义

- **添加数据获取工具**: 在 `tools/` 下新建 `.py` 脚本，接受 ticker 作为第一个参数，输出 JSON 到 stdout，然后在 `CLAUDE.md` 中注册
- **添加分析框架**: 在 `.claude/skills/` 下新建目录，包含 `SKILL.md`（需含 YAML frontmatter），然后在 `CLAUDE.md` 对应步骤中引用
- **修改分析步骤**: 编辑 `CLAUDE.md` 中对应步骤的描述
