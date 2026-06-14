# LLVM Version Support Policy

This document defines cpp-linter's policy for supporting LLVM / Clang versions across all
projects in the organization. It covers pre-built binary availability, CI testing, issue triage,
and paths for users who need help with versions outside our default support window.

---

## 1. Background: LLVM Upstream Release Cycle

LLVM releases a new major version roughly every 6 months (typically March and September). Each
major branch receives patch releases for about 6 months — until the next major release stabilizes.
After that, upstream **does not provide long-term support** for older branches. Bug fixes and
security patches land only on the current release branch (and `main`).

This policy extends support well beyond upstream's window so that projects with older toolchains
can still rely on cpp-linter.

---

## 2. cpp-linter Support Tiers

| Tier | Description | Pre-built Binaries | CI Testing | Issue Triage |
|------|-------------|:---:|:---:|:---:|
| **Tier 1 — Full Support** | Latest 3 major versions | ✅ All platforms | ✅ Full CI matrix | Bug fixes prioritized |
| **Tier 2 — Standard Support** | Versions from the **support floor** up to Tier 1 | ✅ All platforms | ⚠️ Spot-check only | Best-effort bug fixes |
| **Tier 3 — Legacy** | Versions below the support floor | ❌ Not provided | ❌ Not tested | Community best-effort |

### Tier 1 — Full Support

The latest **3 major LLVM versions** receive full support:

- Pre-built static binaries for all 5 platforms (linux-amd64, linux-arm64, macos-amd64, macos-arm64, windows-amd64).
- Docker images (normal + alpine variants).
- Python wheels (where upstream publishes them on PyPI).
- Full CI testing on every change.
- Bug fixes and regressions are prioritized.
- The default `version` in `cpp-linter-action` tracks the middle Tier-1 version.

### Tier 2 — Standard Support

Versions from the **support floor** (the oldest major version we maintain) up to but not
including Tier 1 receive standard support:

- Pre-built binaries continue to be published (via the same build pipeline).
- Docker images remain available.
- CI testing is limited to spot-checks (a representative platform per version).
- Issues are triaged and fixed on a best-effort basis. Community contributions are welcome.

**As new LLVM releases enter Tier 1, the support floor moves forward.** When the floor advances,
the version that falls below it transitions to Tier 3 after a **6-month grace period**.

### Tier 3 — Legacy

Versions below the support floor are considered **legacy**. By default:

- **No pre-built binaries are published.**
- No Docker images are maintained.
- No CI testing.
- Issues specific to these versions are closed as `wontfix` unless there is community interest
  or a sponsorship arrangement (see [Special Support](#5-special-support)).

---

## 3. Support Lifecycle Table

> **Current as of: June 2026**
>
> Support floor: **LLVM 11**
> Tier 1: **22, 21, 20**

| LLVM Version | Release Date | Tier (as of 2026-06) | Notes |
|:---:|:---|:---|:---|
| **22** | Mar 2026 | 🟢 Tier 1 | Latest stable |
| **21** | Sep 2025 | 🟢 Tier 1 | |
| **20** | Mar 2025 | 🟢 Tier 1 | Current `cpp-linter-action` default |
| **19** | Sep 2024 | 🔵 Tier 2 | |
| 18 | Mar 2024 | 🔵 Tier 2 | |
| 17 | Sep 2023 | 🔵 Tier 2 | |
| 16 | Mar 2023 | 🔵 Tier 2 | |
| 15 | Sep 2022 | 🔵 Tier 2 | |
| 14 | Mar 2022 | 🔵 Tier 2 | |
| 13 | Sep 2021 | 🔵 Tier 2 | |
| 12 | Apr 2021 | 🔵 Tier 2 | |
| **11** | Oct 2020 | 🔵 Tier 2 | Current support floor |
| 10 | Mar 2020 | ⚫ Tier 3 | No default support |
| 9 | Sep 2019 | ⚫ Tier 3 | No default support |
| 8 | Mar 2019 | ⚫ Tier 3 | No default support |
| 7 | Sep 2018 | ⚫ Tier 3 | No default support |

### How the Support Floor Moves

When a new LLVM major version is released (e.g., LLVM 23 in September 2026):

1. The new version enters Tier 1. The oldest Tier 1 version (20) exits to Tier 2.
2. The support floor *may* advance. We evaluate this on a case-by-case basis, considering:
   - Build complexity for the oldest Tier 2 version (toolchain availability, platform compatibility).
   - Community usage (download counts, issue reports, survey).
   - Whether staying on the current floor adds unreasonable maintenance burden.
3. If the floor advances, the version that falls below it gets a **6-month grace period** in Tier 2 before moving to Tier 3.

---

## 4. Why a Long Support Window?

cpp-linter's mission is to make C++ linting accessible across diverse environments. Many teams work
with older toolchains due to:

- Embedded systems and long-term-support (LTS) distributions.
- Corporate environments with slow upgrade cycles.
- Legacy codebases that cannot easily adopt newer Clang versions.

By maintaining a **~6-year support window** (currently 11→22), we aim to cover the vast majority
of real-world C++ projects while keeping the maintenance burden manageable.

---

## 5. Special Support

If you need a version that is outside our default support window — whether it's a Tier 3 version
or a version that has not yet been released — you have several options:

### 5.1 Community / Free Support

For any LLVM version, you can:

- **Open a discussion** in [GitHub Discussions](https://github.com/cpp-linter/.github/discussions)
  to gauge community interest. If enough users need the same version, we may consider extending support.
- **Submit a PR** that adds support for the version. Our build infrastructure is open-source and
  designed to be extended.
- **Build from source** using the instructions below.

### 5.2 Sponsored Support

For organizations that need guaranteed support for a specific Tier 3 version (pre-built binaries,
CI testing, bug fixes), we offer **sponsored support arrangements**. This can include:

- Adding a specific version back to the build matrix.
- Docker image publication for that version.
- Prioritized bug fixes.
- Custom build configurations (e.g., specific platform, specific tools).

👉 **Contact us** at [cpp-linter@googlegroups.com](mailto:cpp-linter@googlegroups.com) or open a
private discussion to discuss terms.

### 5.3 Paid Build Services

If you need pre-built binaries for a legacy version but don't want to set up the build
infrastructure yourself, we can produce and sign them for you as a one-time paid service. This
includes SHA-512 checksums and optionally GPG-signed artifacts.

---

## 6. Building from Source

Our build infrastructure is fully open-source. You can reproduce any build on your own machine
or fork our repositories and run CI on your own GitHub account.

### Static Binaries

```bash
git clone https://github.com/cpp-linter/clang-tools-static-binaries
cd clang-tools-static-binaries
python build.py --version 15 --platform linux-amd64
```

See [`clang-tools-static-binaries/README.md`](https://github.com/cpp-linter/clang-tools-static-binaries#building-locally)
for detailed requirements per platform.

### Docker Images

```bash
git clone https://github.com/cpp-linter/clang-tools-docker
cd clang-tools-docker
docker build -f Dockerfile --build-arg LLVM_VER=15 -t clang-tools:15 .
```

### Contributing Back

If you successfully build a version we no longer publish, consider submitting a PR to add it back
to our build matrix. We welcome contributions that expand the ecosystem!

---

## 7. Frequently Asked Questions

**Q: Why is the `cpp-linter-action` default version not the latest?**

We default to the middle Tier-1 version (currently 20) to balance stability and freshness. The
latest version is always available — just set `version: '22'` in your workflow.

**Q: What happens when my version reaches Tier 3?**

Existing releases and artifacts remain available indefinitely on GitHub Releases, PyPI, and
Docker Hub. We don't delete anything. What changes is that we stop producing *new* builds for
that version.

**Q: Can I still use a Tier 3 version with `cpp-linter-action`?**

If you already have the binaries locally (or installed via your system package manager), you can
point `version` to their path. See the
[action documentation](https://github.com/cpp-linter/cpp-linter-action#version) for details.

**Q: How do I request a version be added to the support floor?**

Open a [GitHub Discussion](https://github.com/cpp-linter/.github/discussions) with your use case.
We evaluate requests based on community demand and maintenance cost.

**Q: Does this policy apply to all cpp-linter projects?**

Yes. All projects under the `cpp-linter` organization (`clang-tools-static-binaries`,
`clang-tools-docker`, `clang-tools-pip`, `clang-tools-wheel`, `cpp-linter-action`,
`cpp-linter-hooks`, `asdf-clang-tools`) follow this version support policy.

---

## 8. Changelog

| Date | Change |
|:---|:---|
| 2026-06-14 | Initial policy published. Support floor: LLVM 11. Tier 1: 22, 21, 20. |
