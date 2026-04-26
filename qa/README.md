# qa/

Stress test reports against the live Cloud Run deployment. Used as evidence for the productionisation discussion in `assignment.md` section 6.

- [`stress_test_2026-04-19.md`](stress_test_2026-04-19.md) — second-pass retest after a first round of fixes. Tested the live app at https://meeting-prep-assistant-691081429886.us-west1.run.app/. Scope was user-facing fixes only; backend/API architecture was held out of scope. Result: core generation flow works (~27s for a small `.txt` upload), prompt-injection resistance held, mobile layout passed. Eight client-side issues remain — the priority list at the bottom of the report is the productionisation roadmap drawn on in the Reflection.
