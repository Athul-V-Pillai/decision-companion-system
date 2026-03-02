# Decision Companion System - Build Process & Development Journey

## 1. How Development Started

When I first approached this project, the problem seemed straightforward: help users make better decisions by comparing multiple options against multiple criteria. But I quickly realized that "better" could mean many things.

My initial instinct was to build something that would rank options automatically—almost like a recommendation engine. I considered using machine learning to learn user preferences from their past decisions. However, after thinking through the implications, I realized this approach had a critical flaw: **users didn't want a black box telling them what to do. They wanted to understand the logic.**

This realization changed everything. Instead of building an AI-driven system, I decided on a deterministic, rule-based approach. The algorithm would be transparent—users could see exactly how the scoring worked and why one option ranked higher than another. I chose the **Weighted Sum Model (WSM)** because it's mathematically simple, fully explainable, and widely used in decision-making contexts.

The initial design was intentionally lean: a form for inputs, a backend calculation, and results display. I used Flask because it allowed rapid prototyping without the overhead of larger frameworks, and vanilla JavaScript for the frontend to keep dependencies minimal.

## 2. Evolution of Thinking

As I built the first working version, requirements became clearer through actually using the system. Initially, I thought displaying a simple ranked list would be sufficient. But when I tested it, the results felt incomplete.

**Early problem:** Users asked, "Why is this option ranked higher? What if I change the weights?" This pushed me toward adding explanations alongside scores. I realized the ranking alone wasn't enough—I needed to provide reasoning.

**Second realization:** Raw scores (0-100) didn't tell the full story. An option with a score of 67 could be genuinely good or barely acceptable depending on context. This led me to introduce **confidence scoring** (High/Medium/Low)—a more intuitive way to communicate decision quality.

**Architectural shift:** Initially, all logic lived in a single file. As features grew, I found myself rewriting validation logic, score calculations, and explanations in different places. I made the decision to **split the decision engine into modular components:**
- `validator.py` - Input validation
- `evaluator.py` - Scoring and ranking
- `explainer.py` - Human-readable explanations
- `__init__.py` - Module interface and history management

This modular approach meant I could test each component independently and reuse logic across the application.

## 3. Alternative Approaches Considered

### AI-Based Recommendation System
**What I considered:** Train a model on user decisions to predict future preferences.

**Why rejected:** The concept conflicted with our core goal—transparency. Users needed to *understand* why an option was recommended. An ML model would introduce unexplainability, and for a decision support tool, that's a fundamental weakness. Additionally, with limited historical data early on, a model wouldn't be reliable.

### Hardcoded Comparison Tables
**What I considered:** Pre-built decision matrices for common scenarios (buying a phone, choosing a job, etc.).

**Why rejected:** This severely limited flexibility. Every new decision scenario would require me to hardcode a new template. The system needed to handle arbitrary options and criteria—hardcoding wasn't scalable.

### Full MERN Stack vs. Flask + Vanilla JS
**What I considered:** Using React for the frontend to handle complex state management and visualization.

**Why rejected:** Early on, the UI requirements didn't justify the complexity overhead. Vanilla JavaScript handled the form generation, API calls, and chart rendering sufficiently. MERN would have added a build step, node_modules bloat, and unnecessary abstraction layers for what was fundamentally a single-page application with modest interactivity.

## 4. Refactoring Decisions

The most important refactoring happened when I realized the evaluator was doing too much. The original `evaluator.py` had validation logic, scoring, confidence calculation, and explanation templating all mixed together.

**First refactor:** Extracted validation into a separate module. This made the code clearer and allowed me to validate inputs before processing them, reducing bugs.

**Second refactor:** Introduced normalization as a reusable function. I noticed I was manually handling score ranges inconsistently. Creating a dedicated normalization function (min-max scaling to 0-1 range) solved this and made the weighting calculation more reliable.

**Third refactor:** Separated explanation generation from scoring. This made the code easier to test and allowed me to modify how explanations were worded without touching the core algorithm.

**Readability improvement:** Early code used abbreviated variable names and nested loops. During refactoring, I expanded variable names (`w` → `weight`, `s` → `score`) and extracted nested logic into helper functions. It made the codebase more maintainable.

## 5. Mistakes and Corrections

### Validation Assumption Failure
**What went wrong:** I initially assumed weights would always sum to 100. Some users entered weights that summed to 80 or 120, thinking the system would normalize them. Instead, the algorithm broke silently, producing nonsensical scores.

**Fix:** Added explicit validation that weights sum to 100 (with a small tolerance) and returned detailed error messages explaining what went wrong. Now users get feedback immediately.

### Score Range Inconsistency
**What went wrong:** I accepted scores on a scale of 0-10 but didn't normalize them when mixing with other criteria that used 0-100 scales. This caused the algorithm to weight high-scale criteria unfairly.

**Fix:** Implemented min-max normalization to convert all scores to a 0-1 range before applying weights. This ensures fair comparison regardless of input scale.

### Frontend-Backend Data Mismatch
**What went wrong:** When implementing PDF export, the frontend was sending form input data to the backend, but the backend expected processed evaluation results. This caused a 500 error because the export function couldn't find the scores.

**Fix:** Modified the frontend to capture and store the evaluation results in a variable, then include that in the export request. Now the backend receives all necessary data in the expected format.

## 6. Changes During Development and Why

### Adding Explainability Outputs
**Why:** Early feedback showed users wanted to understand the logic. A simple ranked list wasn't enough. Adding natural language explanations ("Option A ranks highest because it excels in criteria X and Y") made decisions feel legitimate rather than arbitrary.

### Introducing Confidence Scoring
**Why:** Users needed quick visual feedback on decision quality before diving into details. Confidence scores (High/Medium/Low) provide immediate context—a High confidence ranking at an 85 score is more meaningful than a Low confidence ranking at the same score.

### Adding Chart Visualization
**Why:** Numbers alone were hard to parse. A bar chart showing score comparison and a radar chart showing multi-criteria performance made patterns instantly visible. Users understood their data better through visualization.

### Saving Decision History
**Why:** Users wanted to revisit past decisions, compare different analyses, and track how their criteria had evolved. History tracking transformed the tool from single-use to ongoing reference material. I used JSON file storage initially—simple, sufficient for MVP scope, and easy to upgrade to a database later if needed.

### Exporting Reports to PDF
**Why:** Users needed to share decisions with stakeholders or reference them offline. PDF export with professional formatting (tables, styling, recommendations) made the tool practical for business contexts. This single feature shifted perception from "experimental tool" to "usable decision assistant."

## Lessons Learned

1. **Transparency beats sophistication:** A simple, explainable algorithm builds more trust than complex AI that users don't understand.

2. **User feedback drives priorities:** History tracking and PDF export weren't in my original plan—they emerged from how users actually wanted to interact with the tool.

3. **Modular design pays off early:** Splitting the decision_engine into separate modules saved debugging time and made testing individual components straightforward.

4. **Validation is foundational:** Many early issues stemmed from assuming valid input. Explicit validation prevented cascading errors.

5. **Normalization matters:** Handling different scales properly from the start would have prevented the score range bug entirely.

6. **Keep it simple until you need it not to be:** Vanilla JavaScript was sufficient; MERN would have been premature optimization.

The Decision Companion System evolved from a simple scoring tool into a practical decision support system because I stayed focused on what users actually needed: transparency, correctness, and usability.
