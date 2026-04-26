# qa/

Evidence for the productionisation discussion in `assignment.md` section 6 — the live Cloud Run deployment plus how it got there.

- [`stress_test_2026-04-19.md`](stress_test_2026-04-19.md) — second-pass retest after a first round of fixes. Tested the live app at https://meeting-prep-assistant-691081429886.us-west1.run.app/. Scope was user-facing fixes only; backend/API architecture was held out of scope. Result: core generation flow works (~27s for a small `.txt` upload), prompt-injection resistance held, mobile layout passed. Eight client-side issues remain — the priority list at the bottom of the report is the productionisation roadmap drawn on in the Reflection.
- [`ai_studio_build_log.md`](ai_studio_build_log.md) — unedited transcript of the Google AI Studio Build-mode session that produced the deployed app. Companion to the stress test: the stress test reports the issues, this log shows which were fixed in-loop, which were correctly flagged as needing approval (browser-side → backend rewrite was the one Build-mode self-bounded on), and how it iterated. The "what to extract" section at the top of the file is the navigation aid; the raw transcript follows.
