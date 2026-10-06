# Contributing

Thanks for considering a contribution to AI Career Agent. This is a young project, so small, focused changes are the easiest to review.

## Good First Contributions

- Improve setup docs.
- Add tests for retrieval or agent workflow behavior.
- Improve fallback-mode examples.
- Add screenshots that match the current English UI.
- Propose roadmap items through issues.

## Local Development

Backend:

```powershell
cd backend
python -m pip install -r requirements.txt
python -m pytest
```

Frontend:

```powershell
cd frontend
npm ci
npm run build
```

## Pull Request Expectations

- Keep changes focused.
- Explain the user-visible behavior change.
- Include tests or explain why tests are not needed.
- Do not commit `.env`, API keys, uploaded profile files, generated reports, `node_modules`, or build output.
- Keep public-facing text in English.

## Reporting Issues

When filing an issue, include:

- expected behavior
- actual behavior
- steps to reproduce
- relevant environment details
- whether fallback or vector retrieval mode was used

Security-sensitive reports should not include secrets, API keys, or private profile data.
