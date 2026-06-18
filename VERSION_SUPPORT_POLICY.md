# Version Alignment Policy

> **Disclaimer:** cpp-linter does **not** develop or maintain LLVM / Clang tools. We only
> pre-build and repackage upstream LLVM releases for easier installation. We do **not** fix
> bugs, add features, or backport patches to any LLVM version — those are the responsibility
> of the [LLVM project](https://github.com/llvm/llvm-project).

We provide pre-built static binaries, Docker images, and Python wheels for **LLVM 11 through
the latest stable release**. The latest 3 major versions receive full CI testing coverage.

Older versions may be dropped over time as they become difficult to build on current platforms.
Version-specific issues in dropped versions will be closed as `wontfix`.

---

## FAQ

**Q: Do you fix bugs in clang-tidy or clang-format?**

No. Please report tool bugs to the [LLVM project](https://github.com/llvm/llvm-project/issues).
If a download is broken or a binary is missing, report that to us.

**Q: Which default version does `cpp-linter-action` use?**

Currently **LLVM 20** (the middle of the latest 3 major versions).

**Q: Need a version we no longer package?**

You can fork our build repositories and build it yourself. Start a
[discussion](https://github.com/orgs/cpp-linter/discussions) if you think others need it too.
