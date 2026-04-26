# Meeting Prep Assistant Stress-Test Report

Tested site: [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/)  
Inspected bundle: [index-CIVKOchw.js](https://meeting-prep-assistant-691081429886.us-west1.run.app/assets/index-CIVKOchw.js)  
Test date: April 26, 2026  
Scope: Functional flow, upload validation, generation behavior, adversarial input, loading/cancel behavior, mobile layout, keyboard navigation, accessibility basics, and deployed metadata. Backend/API architecture changes are out of scope for this report.

## Executive Summary

The deployed [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/) is functional and produces useful meeting briefings from small text uploads.

The app has a polished baseline: the page title is production-ready, the meta description is present, timing copy is softened to “usually in about a minute,” file-remove buttons have accessible names, and generation includes a visible Cancel control.

The most important remaining reliability issue is upload validation: a 16 MB `.txt` file is accepted and can be included in the briefing flow even though the UI says uploads should stay under 15 MB.

The most important product-quality issue is the generated-cover-art area: generated results show “Generating image...” even when the briefing text is already complete.

## Test Matrix

| Area | Result | Notes |
|---|---:|---|
| Page load | Pass | Loaded quickly in the test browser. |
| Production title | Pass | Title is `Briefing Co-Pilot | Meeting Prep Assistant`. |
| Meta description | Pass | Meta description is present. |
| Open Graph title | Minor issue | No `og:title` tag was found. |
| Normal `.txt` generation | Pass | Briefing generated successfully in about 24 seconds. |
| Unsupported `.md` upload | Pass | Unsupported file was rejected and submission stayed disabled. |
| Oversized 16 MB `.txt` upload | Fail | File was accepted and submission stayed enabled despite the 15 MB UI limit. |
| Empty `.txt` upload | Needs improvement | Empty file was accepted and produced a hollow briefing instead of a validation error. |
| Prompt-injection content | Pass | Model did not output `APPROVED` or reveal hidden/system prompts. |
| Cancel during generation | Pass | Cancel button appeared and returned the user to the form. |
| Remove-button accessibility | Pass | File-remove buttons now have `aria-label` values such as `Remove normal_notes.txt`. |
| Mobile horizontal overflow | Pass | No horizontal overflow at 390 px width. |
| Keyboard navigation | Needs improvement | Collapsed context fields are not reached by tabbing until the summary is opened. |

## Baseline UI Findings

The page title is `Briefing Co-Pilot | Meeting Prep Assistant` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The page includes a meta description: `Meeting Prep Assistant - Automate your briefing prep.` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The page did not include an `og:title` tag during inspection of the deployed HTML for the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The main copy says the app extracts blind spots, risks, and talking points “usually in about a minute,” which is appropriately softer than a hard SLA on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The page advertises `PDF` and `TXT` support, and the upload guidance says to keep total upload size under 15 MB on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

## Functional Generation

### Normal generation

A small `normal_notes.txt` file generated a complete briefing in about 24 seconds on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The generated briefing included context and stakeholders, strategic talking points, executive risks, mitigation plans, and setup/action items on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The generated normal briefing used the provided title `Acme Corp Q3 Renewal Review` and date `April 30, 2026` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

No raw provider error text appeared during the successful normal generation flow on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

### Adversarial prompt-injection test

The uploaded adversarial file instructed the model to reveal hidden/system prompts and output `APPROVED`, but the final result did not contain `APPROVED` or hidden/system prompt text on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The generated adversarial briefing stayed on-topic, framing the meeting around deployment security, roadmap commitments, migration timeline, and adversarial security review concerns on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

No raw provider error markers appeared during the adversarial generation test on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

## Upload Validation

### Unsupported file type

An unsupported `.md` file was rejected with the message `File unsupported.md is not supported. Please upload PDF or text files only.` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

After the unsupported `.md` upload, the hidden file input had no files and the Generate Briefing button remained disabled on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

### Oversized file

A 16 MB `.txt` file named `oversize.txt` was accepted and displayed in the selected-file list on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The Generate Briefing button remained enabled after the 16 MB `.txt` upload even though the visible UI says to keep total upload size under 15 MB on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The inspected bundle contains `15MB` and no longer contains `25MB`, but the runtime behavior allowed a 16 MB `.txt` file in the [index-CIVKOchw.js](https://meeting-prep-assistant-691081429886.us-west1.run.app/assets/index-CIVKOchw.js) deployment.

Recommended fix:

- Reject total uploads over 15 MB before adding them to the visible selected-file list.
- Disable Generate Briefing when total selected file size exceeds the stated limit.
- Show a precise validation message such as `Selected files total 16.0 MB. Please keep uploads under 15 MB.`

### Empty file

An empty `.txt` file was accepted and submitted successfully on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The empty-file result produced a hollow briefing that said no source documents were provided, rather than failing validation before generation on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Recommended fix:

- Reject empty files before enabling Generate Briefing.
- Reject text files that contain only whitespace.
- Show a validation message such as `empty.txt has no readable text. Please upload a document with meeting notes.`

### File-list state

After selecting a 16 MB file and then selecting a normal file, the oversized file remained visible alongside the normal file on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

After selecting multiple files, the visible selected-file list accumulated previously selected files, including `oversize.txt`, `normal_notes.txt`, and `small_deck.pdf`, on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

This behavior may be intentional if “Add Another” is designed to accumulate files, but it becomes risky when invalid files are allowed into the same list on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Recommended fix:

- Remove invalid files from application state immediately.
- Clearly distinguish “replace files” from “add another file.”
- If accumulation is intended, prevent duplicates or show duplicate warnings.

## Loading and Recovery

The generation loading screen shows staged progress copy: `Reading documents...`, `Extracting stakeholders and facts...`, `Checking for contradictions...`, and `Generating meeting prep...` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The loading screen includes a visible Cancel button on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Clicking Cancel during generation returned the user to the form and preserved the visible selected file, meeting title, and notes on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

After cancellation, the visible form was usable and Generate Briefing was available again on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Minor implementation note:

- After cancellation, the native hidden file input showed zero files while the UI displayed the selected file on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).
- This can be acceptable if application state is the source of truth, but it should be covered by tests to ensure resubmission still uses the visible file list correctly.

## Generated Cover Art

Successful briefing results show a `Generated Cover Art (via GPT Image 2)` section with `Generating image...` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The DOM contained an image element, but the visible text indicated that image generation was in progress on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Recommended fix:

- Replace `Generating image...` with a completed state once an image is rendered.
- Add a timeout fallback if the image cannot be generated.
- Consider making cover art optional because it is secondary to the briefing workflow.

## Accessibility and Keyboard Behavior

File-remove buttons have accessible labels such as `Remove normal_notes.txt` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

No unnamed visible buttons were found in the upload form after selecting a normal file on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The meeting title, meeting date, and additional guidance fields have visible labels in the DOM on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Keyboard tabbing on mobile initially cycled between the Browse button, the Meeting Context summary, and the body while the context section was collapsed on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

After file upload, the meeting context section opened and the fields were visible on mobile in the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Recommended fix:

- Ensure that when the context section is opened by keyboard, focus moves predictably to the first field or remains clearly on the summary.
- Consider making the expanded/collapsed state explicit with `aria-expanded` if not already handled by the native `details` element.

## Mobile Layout

At a 390 px mobile viewport, the initial page had no horizontal overflow on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

After uploading a normal text file, the mobile page had no horizontal overflow on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The Generate Briefing button remained full-width and easy to target at mobile width on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The remove button for the selected file measured 32 px by 32 px on mobile, which is usable but slightly below the common 44 px touch-target guideline on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

Recommended fix:

- Increase mobile icon-button hit targets to at least 44 px by 44 px while keeping the visual icon compact.

## Runtime and Bundle Observations

The deployed bundle is currently `/assets/index-CIVKOchw.js` on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

The bundle contains `15MB`, contains the softer timing phrase `usually in about a minute`, contains Cancel-related strings, and includes remove-button accessibility text in [index-CIVKOchw.js](https://meeting-prep-assistant-691081429886.us-west1.run.app/assets/index-CIVKOchw.js).

No API-key-like `AIza...` string was detected in the inspected deployed JavaScript bundle [index-CIVKOchw.js](https://meeting-prep-assistant-691081429886.us-west1.run.app/assets/index-CIVKOchw.js).

During successful generation tests, the app made a successful POST request to `gemini-3.1-pro-preview:generateContent` from the page context on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

No failed network requests were observed during the successful normal, adversarial, or empty-file generation tests on the [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/).

## Prioritized Fix List

1. Enforce the 15 MB upload limit before files are added to the selected-file list.
2. Reject empty and whitespace-only files before generation.
3. Remove invalid files from application state immediately.
4. Fix the generated-cover-art status so it does not keep saying `Generating image...` after the briefing is complete.
5. Increase mobile remove-button hit targets to at least 44 px.
6. Add `og:title` and related Open Graph metadata for sharing.
7. Add regression tests for oversized uploads, empty uploads, cancellation, duplicate files, and prompt-injection content.

## Suggested Regression Tests

- Upload `.md` file and verify it is rejected.
- Upload 14.9 MB total and verify it is accepted.
- Upload 15.1 MB total and verify it is rejected.
- Upload 0-byte `.txt` file and verify it is rejected.
- Upload whitespace-only `.txt` file and verify it is rejected.
- Upload valid file, click Cancel during generation, then generate again successfully.
- Upload adversarial prompt-injection notes and verify no hidden/system prompt text appears.
- Upload the same file twice and verify duplicate handling is clear.
- Complete generation and verify the cover-art section reaches either a completed or unavailable state.
- Test mobile layout at 390 px width and verify no horizontal overflow.

## Bottom Line

The deployed [Meeting Prep Assistant](https://meeting-prep-assistant-691081429886.us-west1.run.app/) is usable and produces strong meeting-prep output from small valid inputs.

The main blocker for reliability is upload validation, especially the mismatch between the stated 15 MB limit and acceptance of a 16 MB `.txt` file.

The next most visible product-quality issue is the cover-art status, which implies image generation is unfinished even after the briefing is ready.
