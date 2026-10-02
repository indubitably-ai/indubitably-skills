# Functional Programming

A functional-programming plugin for ChatGPT and Codex, built from the repository's [functional-programming skill](https://github.com/indubitably-ai/indubitably-skills/tree/master/functional-programming).

Learn and apply functional programming in JavaScript and TypeScript: refactor code into pure functions, review mutation and side effects, and understand composition and algebraic data types through concrete examples. It follows the project's existing tools and conventions. Repository access and code execution depend on the host session's available tools.

Try:

- “Refactor this JavaScript into pure functions without changing its behavior.”
- “Review this TypeScript for mutation, side effects, and error-handling pitfalls.”
- “Teach me map versus flatMap with a small JavaScript example.”

## Package

The release ZIP includes a portable `plugin.json`, a compatible `.codex-plugin/plugin.json`, one complete skill under `skills/functional-programming/`, icons, and attribution. It has no MCP server, connector, lifecycle hook, account requirement, or plugin-operated service.

The skill remains maintained in the repository's top-level `functional-programming/` directory. Packaging copies the canonical files into the ZIP; there is no second checked-in skill copy to keep synchronized.

## Build from source

From the repository root, with Python 3.10 or later:

```sh
python3 plugins/functional-programming/build.py
```

This creates `dist/functional-programming-1.0.2.zip` and its SHA-256 checksum. Use `--output-dir <directory>` to change the destination. The builder requires only the Python standard library and includes an explicit file list so unrelated repository files are excluded. Add new skill resources to `SKILL_FILES` when needed.

Edit the version and listing metadata in `.codex-plugin/plugin.json` before a new release. The portable manifest is generated from that same metadata. Extract the ZIP into a directory named `functional-programming` for local plugin validation or installation; the source folder here is a package template, not a complete installed plugin.

## Public distribution

Downloadable packages are published under this repository's [GitHub Releases](https://github.com/indubitably-ai/indubitably-skills/releases). A GitHub release makes the package available to download; availability in the shared ChatGPT and Codex directory is established separately through OpenAI's review process.

Upload the ZIP to the [OpenAI Plugins dashboard](https://platform.openai.com/plugins) using the intended verified developer identity. Resolve its automated findings, submit the draft for review, and publish the approved version. See the [official submission instructions](https://developers.openai.com/plugins/deploy/submission) for current requirements. Local and personal marketplaces are useful for authoring and testing but do not publish a plugin to the public directory.

## Privacy and support

See the [privacy policy](PRIVACY.md) for the plugin's data handling. For questions or bug reports, use the repository's [issue tracker](https://github.com/indubitably-ai/indubitably-skills/issues).

## Attribution and license

This is an independent adaptation of *Professor Frisby's Mostly Adequate Guide to Functional Programming*, by the Mostly Adequate Core Team and contributors. The plugin and bundled skill are distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The full source map and adaptation notice travel with the skill. No endorsement by the original authors is implied.
