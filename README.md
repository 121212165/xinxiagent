# Self-Evolving Knowledge Base

A multi-agent system for automated knowledge management running locally on Windows.

## Architecture

```
├── Agents (7 specialized agents)
│   ├── Coordinator - Orchestrates workflows
│   ├── Collector - Gathers external content via Firecrawl
│   ├── Evaluator - Calculates information density
│   ├── Storage - Writes to Obsidian vault
│   ├── Explorer - Health checks
│   ├── Planner - Generates improvements
│   └── Executor - Implements fixes
│
├── Local Services
│   ├── Firecrawl (localhost:3002) - Web scraping
│   └── Obsidian Vault - Knowledge storage
│
└── Runtime
    ├── queue/ - Message queues
    ├── cache/ - Content cache
    └── logs/ - Activity logs
```

## Features

- **Auto Collection**: Scrape from web via local Firecrawl
- **Density Assessment**: 7-dimension scoring algorithm
- **Health Explorer**: Scan vault for issues
- **Self-Evolution**: Auto-improve based on findings
- **Bidirectional Convert**: Project ↔ Knowledge

## Quick Start

```bash
# Start Firecrawl (local)
cd firecrawl
docker compose up -d

# Use via Claude Code
"采集 https://example.com"
"检查知识库健康"
```

## Agent Definitions

Located in `.claude/agents/`:
- `self-evolving-kb-collector.md`
- `self-evolving-kb-evaluator.md`
- `self-evolving-kb-storage.md`
- `self-evolving-kb-explorer.md`
- `self-evolving-kb-planner.md`
- `self-evolving-kb-executor.md`
- `self-evolving-kb-coordinator.md`

## Density Algorithm

| Dimension | Weight |
|-----------|--------|
| Bidirectional Links | 25% |
| Original Insight | 25% |
| Sections | 10% |
| References | 10% |
| Depth | 10% |
| Frontmatter | 10% |
| Length | 10% |

## Configuration

- `config/format-standards.json` - Format thresholds
- `config/health-indicators.json` - Health metrics

## License

MIT