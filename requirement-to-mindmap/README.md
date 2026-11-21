# requirement-to-mindmap

Turns **one requirement** into a **test-coverage mindmap** in markmap-compatible Markdown: Feature → scenario groups → checkbox test cases, with inferred cases clearly flagged.

Vietnamese version: [README.vi.md](README.vi.md). The AI agent follows `SKILL.md`.

## Skill structure

```
requirement-to-mindmap/
  ├── SKILL.md      ← instructions for the AI agent
  ├── README.md     ← this file
  └── README.vi.md  ← Vietnamese user guide
```

## When to use

- You want a visual test tree of a requirement, to review coverage or tick off cases during execution.
- Only when you explicitly ask for a **mindmap / mind map / markmap / coverage tree**.

Not for: a general "analyze this requirement" (use `requirement-clarifier`), a whole-product feature map (use `product-feature-overview`), or test case tables (use `write-quick-test-cases`).

## Installation

Copy the `requirement-to-mindmap` folder into the skills folder of your AI tool:
- **Claude Code:** `~/.claude/skills/` (all projects) or `<your-project>/.claude/skills/` (one project).
- **Other tools** that support [Agent Skills](https://agentskills.io) (`SKILL.md`): see your tool's documentation for its skills folder.

Restart the tool or start a new session. No extra dependencies.

## How to use

```
Draw a test coverage mindmap for this feature: <paste requirement>
Turn this requirement into a mind map
Vẽ mindmap test coverage cho requirement này
```

## Output

A Markdown file `mindmap/yyyy-mm-dd_hh-mm-ss-feature-name.md`. Open it with [markmap](https://markmap.js.org) (VS Code extension or web) to see it as an interactive mindmap.

```
# <System / requirement>
## <Feature>
### Happy path
- [ ] <test case with expected result>
### Negative
### Boundary / Edge
### UI/UX
(+ Security / Performance / Compatibility when relevant)
```

- Exactly 4 levels (root → feature → scenario group → test case), so it stays readable.
- Test data and boundary values in `inline code`.
- Cases the requirement does not state are marked `❓(assumed)` (`❓(giả định)` in Vietnamese).
- The output is only the mindmap — no introduction or explanation.

## Language

Written in the language you use (Vietnamese or English). Markmap syntax, scenario group names (Happy path, Negative, Boundary / Edge, UI/UX…) and technical terms stay in English.

## Author

tuyenvo224
