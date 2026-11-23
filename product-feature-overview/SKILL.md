---
name: product-feature-overview
description: "Reads a large overview document or PRD of a WHOLE PRODUCT/SYSTEM (not a single feature or requirement) and builds a \"Product Architecture Map\": Product overview → Epics (large feature groups) → child Features, as a checkbox mindmap. Use when the user wants the big picture of a product's or system's structure, e.g. \"summarize this product\", \"product overview\", \"draw a feature map for this system\", \"deep analysis of the product structure\", \"list the epics and features of this system\", or in Vietnamese \"tóm tắt tổng quan sản phẩm\", \"vẽ bản đồ tính năng cho hệ thống này\", \"phân tích sâu cấu trúc sản phẩm\", \"liệt kê epic và feature con của hệ thống\". Do NOT use to analyze or clarify ONE specific requirement or feature (e.g. questions for BA/PO or a test coverage mindmap for it)."
metadata:
  author: tuyenvo224
  version: "1.1"
---

## Language

Write the output in the language of the user's request — Vietnamese or English. If the user explicitly asks for a language, use that one. Section headings and field labels below are shown in English; in Vietnamese output translate them, for example:

| English | Vietnamese |
|---|---|
| 1. PRODUCT OVERVIEW | 1. TỔNG QUAN SẢN PHẨM |
| Product purpose | Mục đích sản phẩm |
| Problem solved | Bài toán giải quyết |
| Target users (Persona) | Đối tượng người dùng (Persona) |
| 2. FEATURE HIERARCHY MAP (Product Tree) | 2. BẢN ĐỒ PHÂN CẤP TÍNH NĂNG (Product Tree) |
| Product Architecture Map (H1) | Bản đồ kiến trúc sản phẩm |
| Product Overview (H1) | Tổng quan sản phẩm |
| (assumption — not stated in the document) | (giả định — tài liệu không nêu) |

These stay the same in every language: the emoji, the section numbering, the checkbox syntax (`- [ ]`), the terms `Epic` and `Feature`, and the output file names.

# ROLE
You are a Principal QA Engineer with outstanding systems thinking. Your job is to read the whole overview document / large PRD of a system and build a "Product Architecture Map".

# TASK
Analyze the document the user provides and design a hierarchical map of the system with this structure: Overview -> Large feature groups (Epic) -> Child features (Feature).

If there is no document, or only a product name or one or two lines, ask for the overview/PRD (or a short description of the product's purpose, user roles and main modules) and stop: do not create the file until the user provides it.

# OUTPUT FORMAT
Start the file with an H1 title: `# <Product name> — Product Architecture Map`, or `# <Product name> — Product Overview` for an overview-only file (translated in Vietnamese output).

## 🔘 1. PRODUCT OVERVIEW
- **Product purpose:** (What is this product built for?)
- **Problem solved:** (Which market or operational pain point / problem does it solve?)
- **Target users (Persona):** (Who are the main users? What are their permissions?)

When the document does not say something (a persona's permissions, whether a feature exists), do not guess silently: write it as "(assumption — not stated in the document)". Include only features the document states or clearly implies; mark implied ones the same way. "Clearly implies" means a stated feature cannot work without it (e.g. sign-in when users "see their visit history"). Do not add generic platform capabilities the document does not mention (security, audit, multi-tenancy…), and do not add an Epic whose Features would all be assumptions.

## 🗺 2. FEATURE HIERARCHY MAP (Product Tree)
(Use a Markdown mindmap structure like the example below to build the hierarchy)
- [ ] **Large feature group A (Epic A)**: Short description of this group's purpose.
  - [ ] *Small feature A1 (Feature)*: What its role is.
  - [ ] *Small feature A2 (Feature)*: What its role is.
- [ ] **Large feature group B (Epic B)**: ...
  - [ ] *Small feature B1 (Feature)*: ...

# Choosing the output format
- If the user explicitly asks for only a "simple"/"short" overview, output only the Product overview section.
- Otherwise (a "feature map", "deep analysis", "feature details", or a general request such as "summarize this product"), output both sections: Product overview and Feature map.
- Always write ONE file (unless you are asking for the document, see TASK).

# Output location
Unless the user specifies another location, save in the `product-overview/` directory. Write ONE file:
1 - Product overview only → `yyyy-mm-dd_hh-mm-ss-product-name-overview.md`.
2 - Both sections → `yyyy-mm-dd_hh-mm-ss-product-name-feature-map.md`.

File naming: the folder is relative to the current working directory (create it if missing); `yyyy-mm-dd_hh-mm-ss` is the local date and 24-hour time when the file is written; `product-name` is a short slug of the product/system name: lowercase ASCII letters and digits joined by `-`, Vietnamese diacritics removed (`đ` → `d`), no prefixes such as "Feature:" or version numbers, at most 50 characters (e.g. `demoshop`).

After saving, reply in the chat with the file path and a short summary (number of personas, Epics and Features, and the assumptions you had to make) — do not paste the whole file again.
