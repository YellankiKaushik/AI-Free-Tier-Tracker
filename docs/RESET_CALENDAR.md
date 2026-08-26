# Reset Calendar

`data/reset-calendar.json` is generated from `tools/*.yaml` by `scripts/build_reset_calendar.py`.

It describes theoretical reset schedules from documented plan rules. It does not know any user's live remaining usage.

Reset values are intentionally explicit:

- `daily`, `weekly`, `monthly`, and `billing_cycle` mean the vendor publishes that cadence.
- `dynamic` means the vendor controls the limit in a way that is not a simple calendar reset.
- `undisclosed` means the reset time or cadence was not published.
- `not_applicable` means the record is open-source/BYOK, discontinued, or otherwise has no vendor-hosted free quota.

Known exact reset times include the timezone. Unknown reset times stay `undisclosed`; the project never guesses.
