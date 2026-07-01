<!-- markdownlint-disable MD036 MD041 MD033 -->

<p align="center">
    <img src="../assets/readme-banner-small.png" width="512" height="141" alt="cpp-linter brand logo" />
</p>

<p align="center">
    <strong>Automated C/C++ linting and formatting for your CI/CD pipelines and local workflows.</strong>
</p>

<p align="center">
    <a href="https://cpp-linter.github.io/"><img src="https://img.shields.io/static/v1?label=Website&message=cpp-linter.github.io&color=blue" alt="Documentation" /></a>
    <a href="https://github.com/cpp-linter/.github/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" /></a>
    <a href="https://github.com/cpp-linter/cpp-linter-action"><img src="https://img.shields.io/github/stars/cpp-linter/cpp-linter-action?style=social" alt="GitHub stars" /></a>
</p>

---

## 📖 About

**cpp-linter** bundles the power of `clang-format`, `clang-tidy`, and other LLVM tools into packages that are easy to install, integrate, and maintain. Whether you’re linting a single file locally or enforcing code quality across dozens of repos in CI, cpp-linter has you covered.

We target C/C++ developers and DevOps engineers who want **reliable clang tooling without the build-from-source headache**.

---

## 🧭 Which one should I use?

Not sure where to start? Pick the entry point that matches your workflow:

| Your goal | Use this | How |
|-----------|----------|-----|
| Lint & format on **GitHub PRs / pushes** | [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) | Add the action to your workflow |
| Catch issues **locally before committing** | [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) | Add to your `.pre-commit-config.yaml` |
| Install the clang tools as a **cross-platform CLI** *(most people)* | [pip: `clang-tools`](https://github.com/cpp-linter/clang-tools-pip) | `pip install clang-tools` |
| Install on **macOS** the native way | [Homebrew tap](https://github.com/cpp-linter/homebrew-tap) | `brew tap cpp-linter/tap && brew install clang-tools` |
| Manage tool **versions across a polyglot team** | [asdf](https://github.com/cpp-linter/asdf-clang-tools) | `asdf plugin add clang-tools <url>` |
| Run inside **containers / custom CI images** | [clang-tools-docker](https://github.com/cpp-linter/clang-tools-docker) | Pull the image |
| Just grab the **raw static binary** | [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries) | Download from releases |

> 💡 **New here?** For CI, start with **cpp-linter-action**. For local development, use **cpp-linter-hooks**. To install the underlying clang tools directly, `pip install clang-tools` works on every platform.

---

## 🚀 Get Started

Integrate cpp-linter into your workflow in minutes:

- **[cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action)** — GitHub Action that runs `clang-format` and `clang-tidy` on PRs and pushes, posting inline annotations.
- **[cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks)** — [pre-commit](https://pre-commit.com/) hooks for local development — catch issues before they hit CI.

---

## 🔧 Clang Tools — Simplified

We provide ready-to-use **binaries**, **Docker images**, and **Python wheels** of key clang tools:

| Package | Description |
|---------|-------------|
| [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries) | Statically-linked `clang-format`, `clang-tidy`, `clang-query`, `clang-apply-replacements`, and `clang-include-cleaner` binaries |
| [clang-tools-docker](https://github.com/cpp-linter/clang-tools-docker) | Docker images with pre-installed `clang-format` and `clang-tidy` |
| [clang-tools-wheel](https://github.com/cpp-linter/clang-tools-wheel) | Redistribute `clang-format` and `clang-tidy` Python wheels |
| [clang-apply-replacements](https://github.com/cpp-linter/clang-apply-replacements) | Standalone Python wheel for `clang-apply-replacements` |
| [clang-include-cleaner](https://github.com/cpp-linter/clang-include-cleaner) | Standalone Python wheel for `clang-include-cleaner` — detects unused `#include` directives |

---

## 📦 Easy Installation

Prefer modern package managers? Install `clang-format`, `clang-tidy`, `clang-query`, and more via:

- **[pip](https://github.com/cpp-linter/clang-tools-pip)** — `pip install clang-tools` — installs static binaries or Python wheels for `clang-format`, `clang-tidy`, `clang-query`, `clang-apply-replacements`, and `clang-include-cleaner`
- **[asdf](https://github.com/cpp-linter/asdf-clang-tools)** — `asdf plugin add clang-tools https://github.com/cpp-linter/asdf-clang-tools`
- **[Homebrew Tap](https://github.com/cpp-linter/homebrew-tap)** — `brew tap cpp-linter/tap && brew install clang-tools` — installs pre-built static binaries for `clang-format`, `clang-tidy`, `clang-query`, `clang-apply-replacements`, and `clang-include-cleaner`

---

## 👥 Maintainers

<table>
  <tr>
    <td>
      <a href="https://github.com/shenxianpeng">
        <img src="https://github.com/shenxianpeng.png" width="100" alt="shenxianpeng" /><br />
        <b>shenxianpeng</b>
      </a>
    </td>
    <td>
      <a href="https://github.com/2bndy5">
        <img src="https://github.com/2bndy5.png" width="100" alt="2bndy5" /><br />
        <b>2bndy5</b>
      </a>
    </td>
  </tr>
</table>

---

## 🤝 Contributing

We welcome contributions of all kinds — bug reports, feature requests, documentation improvements, and code.

- 📋 Read our [Code of Conduct](https://github.com/cpp-linter/.github/blob/main/CODE_OF_CONDUCT.md)
- 🔧 Check individual repos for their `CONTRIBUTING.md` guides
- 💬 Join the discussion on [GitHub Discussions](https://github.com/orgs/cpp-linter/discussions)

---

<p align="center">
    <sub>Made with ❤️ by the cpp-linter community</sub>
</p>
