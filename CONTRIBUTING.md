# Contributing

Thanks for helping keep the tracker accurate. Accuracy matters more than tool count.

## Add a new tool

1. Copy an existing file in `tools/`.
2. Use the vendor's canonical product name and URL.
3. Add at least one official source.
4. Separate recurring free access from trials/promotions.
5. Run validation and regenerate the index.
6. Open a PR with the source links and the date you verified them.

## Update a quota

A quota-change PR must state:

- old value
- new value
- official source URL
- relevant source wording in your own short paraphrase
- verification date

Do not paste large sections of vendor pages into this repository.

## Confidence values

- `official_exact`: official source publishes the exact relevant value.
- `official_undisclosed`: official source confirms the free tier but not the number.
- `mixed`: some fields are official and others are secondary/community.
- `community_only`: allowed only outside the verified main dataset.

## Pull request checklist

- [ ] I used an official source for every new numerical quota.
- [ ] I did not add a fake cross-vendor “total credits” metric.
- [ ] I separated trials/promotions from recurring tiers.
- [ ] I set `last_verified` to the date I personally checked the source.
- [ ] `python scripts/validate_data.py` passes.
- [ ] `python scripts/build_index.py` produces no unexpected diff.
