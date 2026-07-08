<!-- markdownlint-disable MD036 MD041 MD033 -->

<div align="center">

  <img src="../assets/readme-banner-small.png" width="512" height="141" alt="cpp-linter brand logo" />

  # cpp-linter

  ### Automated C/C++ linting and formatting for your CI/CD pipelines and local workflows.

  [![Docs](https://img.shields.io/badge/Docs-cpp--linter.github.io-blue?logo=readthedocs&logoColor=white)](https://cpp-linter.github.io/)
  [![CLI](https://img.shields.io/badge/CLI-cpp--linter-00ADD8?logo=python&logoColor=white)](https://github.com/cpp-linter/cpp-linter)
  [![GitHub Action](https://img.shields.io/badge/GitHub_Action-cpp--linter--action-2088FF?logo=githubactions&logoColor=white)](https://github.com/cpp-linter/cpp-linter-action)
  [![pre-commit](https://img.shields.io/badge/pre‑commit-cpp--linter--hooks-F7B93E?logo=pre-commit&logoColor=white)](https://github.com/cpp-linter/cpp-linter-hooks)
  [![License](https://img.shields.io/badge/License-MIT-green.svg?logo=opensourceinitiative&logoColor=white)](https://github.com/cpp-linter/.github/blob/main/LICENSE)

</div>

---

## 📖 About

**cpp-linter** provides `clang-format`, `clang-tidy`, and other LLVM tools as ready-to-use packages — no building from source.

---

## 🧭 Which one should I use?

| Your goal | Start here | One-liner |
|-----------|------------|-----------|
| **CI/CD** linting | [cpp-linter-action](https://github.com/cpp-linter/cpp-linter-action) | Add to `.github/workflows/` |
| **Pre-commit** linting | [cpp-linter-hooks](https://github.com/cpp-linter/cpp-linter-hooks) | Add to `.pre-commit-config.yaml` |
| **Cross-platform** CLI | [clang-tools-pip](https://github.com/cpp-linter/clang-tools-pip) | `pip install clang-tools` |
| **macOS** native | [homebrew-tap](https://github.com/cpp-linter/homebrew-tap) | `brew tap cpp-linter/tap && brew install clang-tools` |
| **Version** management | [asdf-clang-tools](https://github.com/cpp-linter/asdf-clang-tools) | `asdf plugin add clang-format ...` |
| **Docker** images | [clang-tools-docker](https://github.com/cpp-linter/clang-tools-docker) | `docker pull ...` |
| **Static** binaries | [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries) | Download from releases |

<details>
<summary>📦 <strong>More packages</strong> — lower-level & specialized builds</summary>

<br />

The tools above are built on a few underlying distributions you can also use directly:

| Project | What it does |
|---------|--------------|
| [clang-tools-static-binaries](https://github.com/cpp-linter/clang-tools-static-binaries) | The upstream source: statically-linked binaries for Linux, macOS, and Windows that every other distribution builds on. |
| [clang-tools-wheel](https://github.com/cpp-linter/clang-tools-wheel) | Python wheels that redistribute `clang-format` and `clang-tidy`. |
| [clang-apply-replacements](https://github.com/cpp-linter/clang-apply-replacements) | Standalone Python wheel for `clang-apply-replacements`. |
| [clang-include-cleaner](https://github.com/cpp-linter/clang-include-cleaner) | Standalone Python wheel for `clang-include-cleaner` — detects unused `#include` directives. |

Browse every repository on the [organization page](https://github.com/cpp-linter).

</details>

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
