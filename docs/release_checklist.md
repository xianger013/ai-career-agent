# Release Checklist

Use this checklist before tagging a public release or submitting the project for review.

## Required Checks

- [ ] `python -m pytest` passes in `backend`.
- [ ] `npm run build` passes in `frontend`.
- [ ] CI is green on the release branch.
- [ ] README quick-start commands still work.
- [ ] Screenshots match the current English UI.
- [ ] No public docs or display files contain Chinese text.
- [ ] `.env.example` contains no real secrets.
- [ ] Generated outputs and uploaded user files are not committed.

## Documentation

- [ ] README includes status, setup, demo flow, limitations, and roadmap links.
- [ ] `CONTRIBUTING.md` explains how to report issues and test changes.
- [ ] `docs/roadmap.md` reflects the next planned work.
- [ ] `docs/codex_for_oss_application.md` is current if used for an application.

## Maintainer Review

- [ ] Adoption metrics are stated honestly.
- [ ] Known limitations are visible.
- [ ] PR description includes tests run.
- [ ] Any external API use is optional or clearly documented.
