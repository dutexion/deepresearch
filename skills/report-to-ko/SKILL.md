---
name: report-to-ko
description: >
  Translate a large markdown research report (5000+ lines) into Korean.
  Use when the user says "translate report", "report to korean", "한글화",
  "보고서 번역", or wants to convert an English research report to Korean.
argument-hint: "[report-file-path]"
allowed-tools: Bash, Read, Write, Glob, Agent, AskUserQuestion
---

# Report to Korean - Large Report Translation

## Trigger
`/deep-research:report-to-ko [path]`

## Workflow

### Step 1: Locate Report File
- If `$ARGUMENTS` is provided, use it as the report file path
- Otherwise, find `*/report.md` in current working directory using Glob
- If multiple found, use AskUserQuestion to let user choose
- Read the file and count total lines

### Step 2: Build Terminology Glossary (CRITICAL for consistency)
Before any translation, scan the entire report to build a unified glossary.

**2a. Extract key terms**:
Scan the full report and extract:
- Technical terms (e.g., "context window", "fine-tuning", "retrieval-augmented generation")
- Product/company names (e.g., "OpenAI", "Claude", "GPT-4")
- Domain-specific jargon recurring 2+ times
- Abbreviated terms and their full forms (e.g., "RAG", "RLHF")
- Section/category names used as headings
- **Field key names** used in the report (e.g., "name", "company", "release_date", "open_source", "pricing", "benchmark_scores", etc.) — these MUST be included with their Korean translations to ensure all chunks translate field keys identically

**2b. Generate glossary with Korean translations**:
Create a glossary mapping of ~50-200 terms:

```
| English Term | Korean Translation | Note |
|---|---|---|
| context window | 컨텍스트 윈도우 | 음차 사용 |
| fine-tuning | 미세조정(Fine-tuning) | 첫 등장 시 병기 |
| retrieval-augmented generation | 검색 증강 생성(RAG) | 약어도 병기 |
| benchmark | 벤치마크 | 음차 |
| open-source | 오픈소스 | 붙여쓰기 |
```

**Field key translations** (MUST include in glossary):
```
| Field Key | Korean Translation |
|---|---|
| name | 명칭 |
| company | 회사 |
| release_date | 출시일 |
| latest_version | 최신 버전 |
| category | 카테고리 |
| open_source | 오픈소스 |
| license | 라이선스 |
| pricing | 가격 정책 |
| underlying_model | 기반 모델 |
| agent_pattern | 에이전트 패턴 |
| tool_integration | 도구 통합 |
| memory_system | 메모리 시스템 |
| benchmark_scores | 벤치마크 점수 |
| deployment_options | 배포 옵션 |
| ... | (report에서 사용된 모든 필드 키를 포함) |
```
Scan the report's `fields.yaml` (if available) or the report itself to build the complete field key mapping.

**2c. Confirm with user**:
Use AskUserQuestion to show glossary and ask:
- Any terms to add/modify?
- Preferred translation style? (formal 격식체 vs conversational 비격식체)

Save glossary to `{directory}/glossary_ko.md`

### Step 3: Build Section Map
Generate a structural overview of the entire report:
- List all `##` and `###` headings with line numbers
- Summarize each section in 1 line (topic + key entities mentioned)
- This section map is passed to every translation agent for global context

Save to `{directory}/section_map.txt`

### Step 4: Chunking (Python script)
Run the chunking script to split the report and generate a manifest:

```bash
python3 ${CLAUDE_SKILL_DIR}/chunk_report.py {report_path} -o {directory}/chunks
```

This produces:
- `chunks/chunk_00.md`, `chunk_01.md`, ... (individual chunk files)
- `chunks/manifest.json` (chunk metadata with pre-computed context)

Read `chunks/manifest.json` to get the chunk list. Display chunk plan to user.

### Step 5: Batch Execution
- Batch by batch_size (default 5)
- Each agent translates 1 chunk
- Launch agents (background parallel, disable task output)
- Need user approval before launching next batch

**For each chunk in manifest.json**, read these fields:
- `chunk["index"]`: chunk number
- `chunk["file"]`: path to raw English chunk
- `chunk["output"]`: path to write Korean translation
- `chunk["context_before"]`: pre-computed previous chunk context (raw English)
- `chunk["context_after"]`: pre-computed next chunk context (raw English)

**Resume support**: Skip chunks where `chunk["output"]` file already exists.

**Hard Constraint**: The following prompt must be strictly reproduced, only replacing variables in {xxx}, do not modify structure or wording.

**Prompt Template**:
```python
prompt = f"""## Task
Translate the following markdown content from English to Korean.
This is chunk {chunk_index + 1} of {total_chunks}.

## Terminology Glossary (MUST follow exactly)
{glossary}

You MUST use the exact Korean translations from this glossary. Do not deviate.
If a term appears in the glossary, use the glossary translation — no exceptions.

## Full Report Structure (for global context)
{section_map}

## Translation Rules
1. Translate ALL text content to natural, fluent Korean
2. DO NOT translate:
   - Code blocks (``` ... ```)
   - URLs and links
   - Proper nouns listed in glossary as-is (company names, product names, person names)
   - JSON keys and values inside code blocks
3. Preserve ALL markdown formatting exactly:
   - Headings (#, ##, ###)
   - Tables (alignment, columns)
   - Bold, italic, links
   - Lists (numbered and bulleted)
   - Blockquotes
4. For technical terms on first occurrence within THIS chunk, use: 한국어(English) format
   On subsequent occurrences within the same chunk, use 한국어 only
5. Maintain the same tone and style throughout — formal/informational (격식체)
6. Numbers, dates, and metrics: keep original format (do not convert units)
7. REMOVE the "Uncertain Fields" section entirely — any block matching this pattern must be deleted, not translated:
   **Uncertain Fields** / **불확실한 필드**
   - field_name1
   - field_name2
   Delete the heading AND the bullet list below it. Do not include any trace of it in the output.
8. Field keys (bold items like **name**, **company**, **release_date**) MUST be translated to Korean using the glossary field key mapping. Every chunk must use the same Korean field keys — no English field keys allowed in the output.

## Context: Previous Chunk Ending (raw English, for flow continuity)
{context_before}

## Context: Next Chunk Beginning (raw English, for transition)
{context_after}

Use the above context to ensure smooth transitions between sections.

## Content to Translate
{chunk_content}

## Output
Write the translated content to {output_path}
Write ONLY the translated markdown content, no explanations or wrappers.
"""
```

### Step 6: Wait and Monitor
- Wait for current batch to complete
- Display progress: "Batch {n}/{total_batches} complete ({chunks_done}/{total_chunks} chunks)"
- Use AskUserQuestion to ask user approval before launching next batch
- Launch next batch after approval

### Step 7: Merge (Python script)
After all chunks translated, run the merge script:

```bash
python3 ${CLAUDE_SKILL_DIR}/merge_chunks.py -d {directory}/chunks -o {directory}/report_ko.md
```

The script:
- Reads all chunk_XX_ko.md files in order
- Validates no chunks are missing
- Checks line ratio is within 0.5x-2.0x of original
- Concatenates into final report

### Step 8: Cleanup
- Remove `{directory}/chunks/` directory
- Remove `{directory}/section_map.txt`
- Keep `{directory}/glossary_ko.md` (reusable for future updates)
- Report: "Translation complete: {output_path} ({total_lines} lines)"

## Agent Config
- Background execution: Yes
- Task Output: Disabled (agent has explicit output file when complete)
- Resume support: Yes (skip chunks where output file already exists)
- Model: sonnet (MUST pass `model: "sonnet"` when launching each translation Agent — translation is rule-following work, not reasoning-heavy)
- Permission mode: bypassPermissions (MUST pass `mode: "bypassPermissions"` when launching each Agent, otherwise subagents default to restricted mode and Write will fail)

## Output
- `{directory}/report_ko.md` - Translated Korean report
- `{directory}/glossary_ko.md` - Terminology glossary (preserved)

## Notes
- For reports under 500 lines, skip chunking and translate in a single pass (still build glossary)
- If a chunk translation fails, retry that specific chunk once before reporting error
- The glossary is the single source of truth for terminology — consistency depends on it
- Glossary + section map + raw English context ensures consistency without inter-chunk dependencies
