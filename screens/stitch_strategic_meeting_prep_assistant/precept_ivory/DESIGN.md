# Design System Document: The Executive Brief

## 1. Overview & Creative North Star
**Creative North Star: The Silent Partner**
This design system is built to evoke the feeling of a high-end, physical executive dossier. In the world of high-stakes B2B meetings, clarity is the ultimate luxury. We move beyond the "standard SaaS" look by embracing a **High-End Editorial** aesthetic. This is not just a tool; it is a calm, authoritative presence that organizes chaos.

To achieve this, we reject the rigid, "boxed-in" grid. Instead, we use **Intentional Asymmetry** and **Tonal Layering**. By utilizing expansive white space (the "generous breathe") and a hierarchy based on surface depth rather than lines, we create an environment that feels expensive, curated, and trustworthy.

---

## 2. Colors: Tonal Depth & Meaning
Our palette is rooted in the reliability of Navy and the prestige of Gold, set against a warm, architectural neutral.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders for sectioning or containment. 
Boundaries must be defined through:
1.  **Background Color Shifts:** A `surface-container-low` section sitting on a `surface` background.
2.  **Tonal Transitions:** Using the hierarchy of `surface-container-lowest` to `surface-container-highest` to define "nested" importance.

### Signature Textures
*   **The "Executive Gradient":** For primary CTAs and high-level Hero backgrounds, use a subtle linear gradient from `primary` (#06104c) to `primary_container` (#1e2761). This prevents the UI from feeling "flat" or "cheap."
*   **Glassmorphism:** For floating menus or "Quick Action" overlays, use semi-transparent `surface_bright` with a `backdrop-blur` of 12px-20px.

| Token Name | Hex | Role |
| :--- | :--- | :--- |
| `primary` | #06104c | Anchor brand color, high-authority text. |
| `tertiary_fixed_dim` | #f3bf53 | Accent Gold. Used for "Premium" status and key highlights. |
| `background` | #fbf9f5 | The warm, cream canvas. Provides the "Paper" feel. |
| `secondary` | #565e70 | Slate grey for metadata and non-critical UI elements. |
| `error` | #ba1a1a | High severity alerts and critical errors. |

---

## 3. Typography: Editorial Authority
We pair **Manrope** for display elements and **Inter** for functional reading. This creates a bridge between modern tech and traditional high-end publishing.

*   **Display & Headlines (Manrope):** These are our "anchors." Use `display-lg` (3.5rem) for center-aligned hero sections to establish immediate confidence.
*   **Body & Labels (Inter):** Chosen for its exceptional legibility at high densities. 
*   **The Hierarchy Rule:** Never use two different weights of the same size next to each other. Create contrast through scale (e.g., a `headline-sm` title paired with `body-md` secondary text).

---

## 4. Elevation & Depth: Tonal Layering
In this design system, shadows are a secondary thought; **Layering** is the primary driver of depth.

*   **The Layering Principle:** Stack containers to create hierarchy. 
    *   *Example:* A `surface-container-lowest` card (#ffffff) placed on a `surface-container` (#efeeea) background creates a soft, natural lift that mimics fine stationery.
*   **Ambient Shadows:** If an element must "float" (like a Modal), use a shadow with a 40px-60px blur at 6% opacity. Use a tint of `on_surface` (#1b1c1a) rather than pure black to ensure the shadow feels like a part of the warm environment.
*   **The "Ghost Border":** If accessibility requires a border, use `outline_variant` at 15% opacity. Never use 100% opaque borders.

---

## 5. Components: Precision & Clarity

### High-Density Cards
Cards must never have a border. 
*   **Status Indicators:** Use a 4px vertical "Left-Edge Status Bar" using the `tertiary` (Gold) or `primary` (Navy) tokens to indicate meeting priority.
*   **Severity Pills:** Use `error_container` with `on_error_container` text for high-severity prep items. The corner radius must be `full` for a soft, "pill" aesthetic.

### Large File Upload Zones
*   **Styling:** Use `surface_container_low` with a dashed `outline` at 20% opacity. 
*   **Interaction:** On drag-over, transition the background to `primary_fixed` to provide a calm, "magnetic" feel.

### Buttons
*   **Primary:** `primary` background with `on_primary` text. Use `lg` (0.5rem) roundedness. 
*   **Secondary:** `secondary_container` background. No border.
*   **Tertiary:** Text-only with an underline that appears on hover using the `tertiary` (Gold) token.

### Progress Indicators
*   Avoid standard "loading spinners." Use a thin, linear progress bar at the very top of a container or page, transitioning from `primary_container` to `tertiary_fixed_dim`.

### Cards & Lists (The "No-Divider" Rule)
Forbid the use of 1px horizontal lines between list items. Use **Vertical Whitespace** (at least 16px) or a alternating subtle background shift (`surface` to `surface_container_low`) to separate content.

---

## 6. Do’s and Don’ts

### Do:
*   **DO** use center-aligned hero sections for "Entry" pages (like the Dashboard landing) to create a sense of focus.
*   **DO** use `tertiary_fixed_dim` (Gold) sparingly. It is a highlighter, not a primary color.
*   **DO** leave more whitespace than you think you need. "Breathing room" is a functional requirement for high-level preparation.

### Don't:
*   **DON'T** use pure black (#000000). Use `on_surface` (#1b1c1a) for all high-contrast text to keep the "warmth."
*   **DON'T** use "Standard Blue" for links. Use the `primary` Navy for an authoritative, custom feel.
*   **DON'T** use heavy drop shadows. If an element looks like it's "hovering" too much, pull the shadow back. We want "stacked paper," not "flying boxes."
*   **DON'T** use 100% opaque lines to separate content. Let the background colors do the work.