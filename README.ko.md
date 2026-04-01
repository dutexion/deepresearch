[English](README.md)

# Deep Research Plugin for Claude Code

> [Weizhena/deep-research-skills](https://github.com/Weizhena/deep-research-skills)에서 포크하여 Claude Code 플러그인으로 재구성했습니다.
>
> [RhinoInsight: Improving Deep Research through Control Mechanisms for Model Behavior and Context](https://arxiv.org/abs/2511.18743)에서 영감을 받았습니다.

Claude Code용 구조화된 리서치 워크플로우 플러그인입니다. 아웃라인 생성(확장 가능)과 병렬 에이전트를 활용한 딥 리서치의 2단계 리서치를 지원합니다. 휴먼 인 더 루프 설계로 모든 단계에서 정밀한 제어가 가능합니다.

### 원본과의 차이점
- **Claude Code 플러그인** 형태로 재구성 (`.claude-plugin/plugin.json`)
- 수동 `cp` 설치 불필요 — `/plugin install` 또는 `--plugin-dir` 사용
- 하드코딩된 `~/.claude/` 경로를 `${CLAUDE_SKILL_DIR}`로 대체
- 대용량 보고서 한국어 번역을 위한 `/deep-research:report-to-ko` 스킬 추가
- Codex/OpenCode 지원 제거 (Claude Code 전용)

## 활용 사례

- **학술 리서치**: 논문 서베이, 벤치마크 리뷰, 문헌 분석
- **기술 리서치**: 기술 비교, 프레임워크 평가, 도구 선정
- **시장 리서치**: 경쟁사 분석, 산업 트렌드, 제품 비교
- **실사(Due Diligence)**: 기업 조사, 투자 분석, 리스크 평가

## 사전 요구사항

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 설치
- Python 3 및 `pyyaml` 패키지:
  ```bash
  pip install pyyaml
  ```

## 설치

### 옵션 A: 마켓플레이스 플러그인 설치 (권장)

```
/plugin marketplace add https://github.com/dutexion/deepresearch
/plugin install deep-research
```

### 옵션 B: 개발 / 로컬 테스트

```bash
git clone https://github.com/dutexion/deepresearch.git
claude --plugin-dir ./deepresearch
```

## 명령어

| 명령어 | 설명 |
|--------|------|
| `/deep-research:research <주제>` | 리서치 항목 및 필드로 구성된 아웃라인 생성 |
| `/deep-research:research-add-items` | 기존 아웃라인에 리서치 항목 추가 |
| `/deep-research:research-add-fields` | 기존 아웃라인에 필드 정의 추가 |
| `/deep-research:research-deep` | 병렬 에이전트로 각 항목 딥 리서치 수행 |
| `/deep-research:research-report` | JSON 결과에서 마크다운 보고서 생성 |
| `/deep-research:report-to-ko [경로]` | 대용량 마크다운 보고서를 한국어로 번역 |

## 워크플로우

### 1단계: 아웃라인 생성

```
/deep-research:research AI Agent Demo 2025
```

주제를 입력하면 구조화된 리서치 목록을 생성합니다. 리서치할 항목 목록과 각 항목에서 수집할 정보가 제공됩니다.

### (선택) 아웃라인 확장

```
/deep-research:research-add-items
/deep-research:research-add-fields
```

리서치 항목이나 필드 정의를 추가하여 아웃라인을 세분화합니다.

### 2단계: 딥 리서치

```
/deep-research:research-deep
```

AI가 병렬 에이전트를 사용하여 각 항목을 자동으로 웹 검색합니다. 각 항목은 검증된 상세 구조화 JSON 출력을 생성합니다.

### 3단계: 보고서 생성

```
/deep-research:research-report
```

모든 데이터를 목차가 포함된 하나의 정리된 마크다운 보고서로 컴파일합니다. 바로 읽거나 공유할 수 있습니다.

### 4단계: 보고서 번역 (선택)

```
/deep-research:report-to-ko
```

전체 보고서를 병렬 에이전트를 사용하여 한국어로 번역합니다. 일관성을 위해 먼저 용어 사전을 구축한 후, 보고서를 청크로 분할하여 5개씩 배치 번역합니다. 부분 완료 상태에서 이어하기를 지원합니다.

## 출력 구조

```
{topic_slug}/
  ├── outline.yaml         # 리서치 항목 + 실행 설정
  ├── fields.yaml          # 필드 정의
  ├── results/             # 항목별 JSON 결과
  │   ├── Item_One.json
  │   └── Item_Two.json
  ├── generate_report.py   # 자동 생성된 보고서 스크립트
  ├── report.md            # 최종 마크다운 보고서
  ├── report_ko.md         # 한국어 번역 (선택)
  └── glossary_ko.md       # 용어 사전 (선택)
```

## 플러그인 구조

```
deepresearch/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── research/            # 아웃라인 생성
│   ├── research-deep/       # 병렬 딥 리서치
│   ├── research-add-items/  # 항목 확장
│   ├── research-add-fields/ # 필드 확장
│   ├── research-report/     # 보고서 생성
│   └── report-to-ko/       # 청킹 기반 한국어 번역
├── agents/
│   └── web-search-agent.md  # 웹 리서치 전문 에이전트
├── hooks/
│   └── hooks.json           # 의존성 검사
├── LICENSE
└── README.md
```

## 참고 자료

- [RhinoInsight: Improving Deep Research through Control Mechanisms for Model Behavior and Context](https://arxiv.org/abs/2511.18743)

## 라이선스

MIT
