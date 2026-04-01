---
name: research-add-items
description: >
  Add more research items (objects) to an existing research outline.
  Use after /deep-research:research when the user wants to expand the items list
  with additional research subjects.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Agent, AskUserQuestion
---

# Research Add Items - Supplement Research Objects

## Trigger
`/research-add-items`

## Workflow

### Step 1: Auto-locate Outline
Find `*/outline.yaml` file in current working directory, auto-read.

### Step 2: Get Supplement Sources in Parallel
Simultaneously:
- **A. Ask user**: What items to supplement? Any specific names?
- **B. Ask if Web Search needed**: Launch agent to search for more items?

### Step 3: Merge and Update
- Append new items to outline.yaml
- Display to user for confirmation
- Avoid duplicates
- Save updated outline

## Output
Updated `{topic}/outline.yaml` file (in-place modification)
