# .github

Organization-wide files for [cpp-linter](https://github.com/cpp-linter): the
[profile README](https://github.com/cpp-linter/.github/blob/main/profile/README.md), the default
contributing guide, code of conduct, security policy, support page, issue and pull request templates,
reusable workflows and the brand assets.

[Website](https://cpp-linter.github.io/) ·
[Get started](https://cpp-linter.github.io/getting-started/) ·
[Discussions](https://github.com/orgs/cpp-linter/discussions)

## Reusable workflows

The other cpp-linter repositories call the workflows in
[`.github/workflows/`](https://github.com/cpp-linter/.github/tree/main/.github/workflows) with
`uses: cpp-linter/.github/.github/workflows/<file>.yml@main`, so a change to one of them reaches
every repository that calls it on its next run. `main.yml` only runs this repository's own checks.

## Brand assets

[`branding/`](https://github.com/cpp-linter/.github/tree/main/branding) holds the logos, the social
preview images and the profile banner generator; its
[README](https://github.com/cpp-linter/.github/blob/main/branding/README.md) lists them. The profile
banners in `assets/` come from `uv run branding/profile-banner/generate.py`.

## License

[MIT](https://github.com/cpp-linter/.github/blob/main/LICENSE)
