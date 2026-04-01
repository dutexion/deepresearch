[한국어](README.ko.md)

# Deep Research Plugin for Claude Code

> Forked from [Weizhena/deep-research-skills](https://github.com/Weizhena/deep-research-skills) and restructured as a Claude Code plugin.
>
> Inspired by [RhinoInsight: Improving Deep Research through Control Mechanisms for Model Behavior and Context](https://arxiv.org/abs/2511.18743)

A structured research workflow plugin for Claude Code, supporting two-phase research: outline generation (extensible) and deep investigation with parallel agents. Human-in-the-loop design ensures precise control at every stage.

### What's different from the original?
- Restructured as a proper **Claude Code plugin** (`.claude-plugin/plugin.json`)
- No manual `cp` installation — use `/plugin install` or `--plugin-dir`
- Hardcoded `~/.claude/` paths replaced with `${CLAUDE_SKILL_DIR}`
- Added `/deep-research:report-to-ko` skill for Korean translation of large reports
- Removed Codex/OpenCode support (Claude Code only)

## Use Cases

- **Academic Research**: Paper surveys, benchmark reviews, literature analysis
- **Technical Research**: Technology comparison, framework evaluation, tool selection
- **Market Research**: Competitor analysis, industry trends, product comparison
- **Due Diligence**: Company research, investment analysis, risk assessment

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3 with `pyyaml` package:
  ```bash
  pip install pyyaml
  ```

## Installation

### Option A: Marketplace Plugin Install (Recommended)

```
/plugin marketplace add https://github.com/dutexion/deepresearch
/plugin install deep-research
```

### Option B: Development / Local Testing

```bash
git clone https://github.com/dutexion/deepresearch.git
claude --plugin-dir ./deepresearch
```

## Commands

| Command | Description |
|---------|-------------|
| `/deep-research:research <topic>` | Generate research outline with items and fields |
| `/deep-research:research-add-items` | Add more research items to existing outline |
| `/deep-research:research-add-fields` | Add more field definitions to existing outline |
| `/deep-research:research-deep` | Deep research each item with parallel agents |
| `/deep-research:research-report` | Generate markdown report from JSON results |
| `/deep-research:report-to-ko [path]` | Translate a large markdown report to Korean |

## Workflow

### Phase 1: Generate Outline

```
/deep-research:research AI Agent Demo 2025
```

Tell it your topic and it creates a structured research list. You get a list of items to research + what info to collect for each.

### (Optional) Expand the Outline

```
/deep-research:research-add-items
/deep-research:research-add-fields
```

Add more research items or field definitions to refine your outline.

### Phase 2: Deep Research

```
/deep-research:research-deep
```

AI automatically searches the web for each item using parallel agents. Each item gets detailed structured JSON output with validation.

### Phase 3: Generate Report

```
/deep-research:research-report
```

All data is compiled into one organized markdown report with table of contents, ready to read or share.

### Phase 4: Translate Report (Optional)

```
/deep-research:report-to-ko
```

Translates the full report to Korean using parallel agents. Builds a terminology glossary first for consistency, then chunks the report and translates in batches of 5. Supports resume from partial completion.

## Output Structure

```
{topic_slug}/
  ├── outline.yaml         # Research items + execution config
  ├── fields.yaml          # Field definitions
  ├── results/             # Individual JSON results per item
  │   ├── Item_One.json
  │   └── Item_Two.json
  ├── generate_report.py   # Auto-generated report script
  ├── report.md            # Final markdown report
  ├── report_ko.md         # Korean translation (optional)
  └── glossary_ko.md       # Terminology glossary (optional)
```

## Plugin Structure

```
deepresearch/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── research/            # Outline generation
│   ├── research-deep/       # Parallel deep investigation
│   ├── research-add-items/  # Expand items
│   ├── research-add-fields/ # Expand fields
│   ├── research-report/     # Report generation
│   └── report-to-ko/       # Korean translation with chunking
├── agents/
│   └── web-search-agent.md  # Web research specialist
├── hooks/
│   └── hooks.json           # Dependency check
├── LICENSE
└── README.md
```

## References

- [RhinoInsight: Improving Deep Research through Control Mechanisms for Model Behavior and Context](https://arxiv.org/abs/2511.18743)

## License

MIT
