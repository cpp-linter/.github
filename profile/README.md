<!-- markdownlint-disable MD036 MD041 MD033 -->

<div align="center">

  <img src="../assets/readme-banner-small.png" width="683" height="188" alt="cpp-linter brand logo" />

  # cpp-linter

  ### C/C++ linting and formatting — for CI, CLI, and local development.

  <a href="https://cpp-linter.github.io/">
    <img src="https://img.shields.io/badge/Docs-cpp--linter.github.io-1E88E5?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Docs" />
  </a>
  <a href="https://github.com/cpp-linter/cpp-linter">
    <img src="https://img.shields.io/badge/CLI-cpp--linter-00ADD8?style=for-the-badge&logo=python&logoColor=white" alt="CLI" />
  </a>
  <a href="https://github.com/marketplace/actions/cpp-linter-action">
    <img src="https://img.shields.io/badge/GitHub_Action-cpp--linter-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="Action" />
  </a>
  <a href="https://github.com/cpp-linter/cpp-linter-hooks">
    <img src="https://img.shields.io/badge/pre‑commit-cpp--linter--hooks-F9A825?style=for-the-badge&logo=pre-commit&logoColor=white" alt="pre-commit" />
  </a>
  <a href="https://github.com/cpp-linter/.github/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-43A047?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License" />
  </a>

  <br />

  <table>
    <tr>
      <td align="center">
        <code>⬢ Linux</code>
      </td>
      <td align="center">
        <code>🍎 macOS</code>
      </td>
      <td align="center">
        <code>⊞ Windows</code>
      </td>
      <td align="center">
        <code>📦 x86_64</code>
      </td>
      <td align="center">
        <code>📱 arm64</code>
      </td>
    </tr>
  </table>

</div>

---

## 🎯 What is cpp-linter?

**cpp-linter** packages `clang-format`, `clang-tidy`, and other LLVM tools into distributions that work across local machines, CI pipelines, containers, and package managers — so you don't need to build LLVM from source or manage platform-specific paths.

Use **pip**, **brew**, **asdf**, **Docker**, or a **GitHub Action** — whichever fits your workflow.

---

## 🧭 Pick your entry point

Not sure where to begin? Follow the decision flow below:

```mermaid
flowchart LR
    CI[GitHub PR/Push] --> Action
    Action["⚡ cpp-linter-action"]
    Local[Local Pre-commit] --> Hooks
    Hooks["🔗 cpp-linter-hooks"]
    CLI[CLI Tool] --> Pip
    Pip["🐍 pip install clang-tools"]
    Pip --> Brew["🍺 brew tap"]
    Pip --> Asdf["🔧 asdf plugin"]
    Pip --> Docker["🐳 Docker image"]
    Pip --> Binary["📦 static binary"]
```

| Your goal | Start here | One-liner |
|-----------|------------|-----------|
| <img src="https://img.shields.io/badge/-GitHub_Actions-2088FF?logo=githubactions&logoColor=white" height="22" /> Lint & format **PRs / pushes in CI** | [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) | Add to `.github/workflows/` |
| <img src="https://img.shields.io/badge/-pre--commit-F7B93E?logo=pre-commit&logoColor=white" height="22" /> Catch issues **before you commit** | [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) | Add to `.pre-commit-config.yaml` |
| <img src="https://img.shields.io/badge/-pip-3776AB?logo=pypi&logoColor=white" height="22" /> Install **cross-platform CLI** | [clang-tools-pip](https://github.com/cpp-linter/clang-tools-pip) | `pip install clang-tools` |
| <img src="https://img.shields.io/badge/-Homebrew-FBB040?logo=homebrew&logoColor=white" height="22" /> Install natively on **macOS** | [homebrew-tap](https://github.com/cpp-linter/homebrew-tap) | `brew tap cpp-linter/tap && brew install clang-tools` |
| <img src="https://img.shields.io/badge/-asdf-4B8BBE?logo=&logoColor=white" height="22" /> Manage versions in a **polyglot team** | [asdf-clang-tools](https://github.com/cpp-linter/asdf-clang-tools) | `asdf plugin add clang-tools` |
| <img src="https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white" height="22" /> Use **containers / custom CI images** | [clang-tools-docker](https://github.com/cpp-linter/clang-tools-docker) | `docker pull ...` |
| <img src="https://img.shields.io/badge/-Binary-555555?logo=files&logoColor=white" height="22" /> Grab the **raw static binary** | [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries) | Download from releases |

> 💡 **New here?** Start with [**cpp-linter-action**](https://github.com/cpp-linter/cpp-linter-action) for CI, or [**cpp-linter-hooks**](https://github.com/cpp-linter/cpp-linter-hooks) for local pre-commit. To install the underlying clang tools directly: `pip install clang-tools`.

---

## ⚡ See it in action

### CI — Lint pull requests automatically

```yaml
# .github/workflows/cpp-linter.yml
name: cpp-linter
on: pull_request

jobs:
  cpp-linter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cpp-linter/cpp-linter-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          style: file          # format against your .clang-format
          tidy-checks: ''      # analyze against your .clang-tidy
```

The action posts **inline annotations**, a **step summary**, and optionally **PR review suggestions** — no extra config needed. → [Full docs](https://github.com/cpp-linter/cpp-linter-action)

### Local — Lint and format from the command line

```bash
# Install anywhere
pip install clang-tools

# Lint a single file
clang-format -n src/main.cpp
clang-tidy src/main.cpp -- -std=c++20

# Fix formatting in-place
clang-format -i src/*.cpp
```

→ [CLI docs](https://github.com/cpp-linter/cpp-linter)

---

## 📦 All packages

<details>
<summary><strong>Lower-level and specialized packages</strong></summary>

<br />

| Package | Description |
|---------|-------------|
| [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries) | 🧱 **Foundation** — Statically-linked binaries for Linux, macOS, Windows. Everything else builds on this. |
| [clang-tools-wheel](https://github.com/cpp-linter/clang-tools-wheel) | 🐍 Python wheels redistributing `clang-format` & `clang-tidy`. |
| [clang-apply-replacements](https://github.com/cpp-linter/clang-apply-replacements) | 🔧 Standalone wheel for `clang-apply-replacements`. |
| [clang-include-cleaner](https://github.com/cpp-linter/clang-include-cleaner) | 🧹 Detect unused `#include` directives. |

Browse **all repos** on the [organization page →](https://github.com/cpp-linter)

</details>

---

## Why cpp-linter?

| | Problem | How cpp-linter helps |
|---|---|---|
| ⏱️ | Building LLVM from source is time-consuming | Pre‑built binaries, ready to use |
| 📦 | clang tools may not be in your distro's package manager | Available via **pip, brew, asdf, Docker** |
| 🔄 | Paths and behavior differ across macOS, Linux, Windows | **Consistent interface** across OS and architectures |
| 📐 | Need to pin tool versions across a team | Version management via **asdf** or **pip** |

---

## 👥 Maintainers

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/shenxianpeng">
        <img src="https://github.com/shenxianpeng.png" width="100" height="100" style="border-radius:50%" alt="shenxianpeng" /><br />
        <b>shenxianpeng</b>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/2bndy5">
        <img src="https://github.com/2bndy5.png" width="100" height="100" style="border-radius:50%" alt="2bndy5" /><br />
        <b>2bndy5</b>
      </a>
    </td>
  </tr>
</table>

---

## 🤝 Contributing

We welcome all contributions — bugs, feature requests, docs, and code.

- 📋 Read our [Code of Conduct](https://github.com/cpp-linter/.github/blob/main/CODE_OF_CONDUCT.md)
- 🔧 Check individual repos for their `CONTRIBUTING.md`
- 💬 Join the discussion on [GitHub Discussions](https://github.com/orgs/cpp-linter/discussions)

---

<p align="center">
  <sub>Made with ❤️ by the cpp-linter community &nbsp;·&nbsp; Powered by <a href="https://clang.llvm.org/extra/clang-tidy/">clang-tidy</a> & <a href="https://clang.llvm.org/docs/ClangFormat.html">clang-format</a></sub>
</p>
