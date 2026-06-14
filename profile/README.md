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

## 🚀 Get Started

Integrate cpp-linter into your workflow in minutes:

- **[cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action)** — GitHub Action that runs `clang-format` and `clang-tidy` on PRs and pushes, posting inline annotations.
- **[cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks)** — [pre-commit](https://pre-commit.com/) hooks for local development — catch issues before they hit CI.

---

## 🔧 Clang Tools — Simplified

We provide ready-to-use **binaries**, **Docker images**, and **Python wheels** of key clang tools:

| Package | Description |
|---------|-------------|
| [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries) | Statically-linked `clang-format`, `clang-tidy`, `clang-query`, and `clang-apply-replacements` binaries |
| [clang-tools-docker](https://github.com/cpp-linter/clang-tools-docker) | Docker images with pre-installed `clang-format` and `clang-tidy` |
| [clang-tools-wheel](https://github.com/cpp-linter/clang-tools-wheel) | Redistribute `clang-format` and `clang-tidy` Python wheels |

---

## 📦 Easy Installation

Prefer modern package managers? Install `clang-format`, `clang-tidy`, `clang-query`, and more via:

- **[pip](https://github.com/cpp-linter/clang-tools-pip)** — `pip install clang-tools`
- **[asdf](https://github.com/cpp-linter/asdf-clang-tools)** — `asdf plugin add clang-tools https://github.com/cpp-linter/asdf-clang-tools`

---

## 👥 Maintainers

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/shenxianpeng">
        <img src="https://github.com/shenxianpeng.png" width="100px;" alt="shenxianpeng" /><br />
        <sub><b>shenxianpeng</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/2bndy5">
        <img src="https://github.com/2bndy5.png" width="100px;" alt="2bndy5" /><br />
        <sub><b>2bndy5</b></sub>
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
