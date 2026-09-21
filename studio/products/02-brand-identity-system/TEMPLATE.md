# Brand Identity System Template

## 1. Client brief

- Client: `{{CLIENT_NAME}}`
- Product or offer: `{{PRODUCT_OR_OFFER}}`
- Category and market: `{{CATEGORY_AND_MARKET}}`
 - Primary channel and format: `{{CHANNEL_AND_FORMAT}}`
- Brand attributes: `{{THREE_TO_FIVE_BRAND_ATTRIBUTES}}`
- Must-avoid attributes: `{{MUST_AVOID_ATTRIBUTES}}`
- Identity budget and approval owner: `{{BUDGET_AND_APPROVER}}`
- AI-disclosure requirement: `{{PLATFORM_DISCLOSURE_REQUIREMENT}}`

## 2. Product promise

The Brand Identity System turns a campaign character from a visual accident into
a controlled commercial asset. It defines one reusable fictional identity, locks
the approved reference, records the visual grammar, and creates the QA contract
needed to reproduce that identity across image and video variants without
re-deriving it for every ad.

## 3. Scope

### Included

1. Identity discovery summary and competitive context.
2. One reusable fictional character contract.
3. One approved identity seed and its immutable SHA-256 record.
4. A controlled visual grammar covering camera, wardrobe, scene, grade, motion,
   and prohibited directions.
5. A product-legibility and disclosure checklist.
6. One downstream validation reference using an already-generated V6 sample.
7. Client-facing portfolio summary and delivery manifest.

### Excluded

1. Living-person or celebrity likeness work.
2. Trademark, copyright, talent, or legal clearance.
3. Paid media deployment.
4. Voice cloning or synthetic reproduction of a real person.
5. Unlimited character revisions or new seed generation without explicit
   approval.
6. Claims about live performance, ROAS, or longitudinal survival without the
   required snapshots.

## 4. Required inputs

| Input | Client artifact | Gate |
|---|---|---|
| Product truth | Product photo or factual product sheet | Unbranded test object is acceptable for dogfood |
| Audience and category | Category Signal Audit or client brief | Names the tension the character must express |
| Brand palette and tone | Existing brand guide or proposed attributes | Must resolve conflicts before seed approval |
| Format plan | Primary aspect ratios and channels | Seed must cover the first paid format |
| Disclosure rule | Platform/client policy | Written into every deliverable |
| Rights posture | Client confirmation that no real-person likeness is requested | Must pass before generation |

## 5. Identity production workflow

### Stage A: Discover

1. Convert the brief into a character job: who speaks, who they remind the buyer
   of, what they must never seem like, and why they make the product easier to
   notice.
2. Select a fictional archetype. Record age band, appearance, expression,
   wardrobe range, voice/tone, and the first product interaction.
3. Check category samples for repeated visual cliches and write at least three
   explicit avoid rules.

### Stage B: Lock the identity contract

1. Freeze the character description verbatim.
2. Keep scene, wardrobe, pose, camera, product interaction, motion, and grade in
   separate variable sections.
3. Add these mandatory constraints:
   - `render_fictional_model_only: true`
   - `no_real_person_likeness: true`
   - `disclose_as_ai: true`
   - `product_must_be_legible: true`
4. Store the contract as JSON so downstream render kits consume the same fields.

### Stage C: Approve the seed

1. Generate or reuse one identity seed under the active approval policy.
2. Review at full resolution against the frozen character block.
3. Record model, task ID, cost, resolution, local path, reviewer, date, QA
   issues, and SHA-256.
4. On approval, make the local seed the only permitted identity reference.
5. Never edit the approved seed. Replace it only through a new dated approval
   record.

### Stage D: Build the visual grammar

Define one dominant visual technique per execution, not a crowded style mixture:

| Layer | Decision | Reuse rule |
|---|---|---|
| Camera | Framing, distance, angle, lens feeling | Stable while identity and product are being tested |
| Scene | Location, time, atmosphere, background | Vary only after the seed is approved |
| Wardrobe | Palette and fit rules | Must not obscure product or identity |
| Product interaction | How the product is held, worn, or used | Product remains second-most-prominent after the face |
| Grade | Color, texture, imperfection, retouching | Preserve enough period or format wrongness to remain distinctive |
| Motion | Subject, camera, and world movement | One dominant motion idea per variant |
| Prohibitions | Text, logos, extra people, style drift, real likeness | Applied by render and QA prompts |

### Stage E: Validate and deliver

1. Validate identity consistency against the seed.
2. Validate product legibility, composition, no-readable-text, hand logic,
   disclosure, and prohibited-likeness rules.
3. Record limitations and failed alternatives without masking them.
4. Package the approved identity contract, seed, grammar, evidence, and next
   route into the Creative Test Sprint intake.

## 6. Client-facing QA gates

| Gate | Evidence required | Pass condition |
|---|---|---|
| G-ID01 Fictional identity | Identity JSON | Character is fictional and not based on a real person |
| G-ID02 Frozen contract | Character block and change log | Approved wording is byte-stable across render variants |
| G-ID03 Seed integrity | Local seed plus SHA-256 | File exists and hash matches the approved record |
| G-ID04 Product legibility | Human review frames | Product is identifiable and not obscured |
| G-ID05 Identity hold | Human review against seed | Face, hair, skin, wardrobe family, and expression remain recognizable |
| G-ID06 Text and logo safety | Human review | No invented readable text, fake UI, or brand logo |
| G-ID07 Disclosure | Identity JSON and delivery notes | AI-generated status is disclosed |
| G-ID08 Rights posture | Client confirmation | No real-person likeness requested or used |
| G-ID09 Cost control | Render ledger | Cost and approval policy are recorded before scaling |
| G-ID10 Reusability | Downstream variant JSON | One seed and one grammar drive multiple executions |

## 7. Delivery package and delivery checklist

| Deliverable | Format | Owner | Acceptance |
|---|---|---|---|
| Identity contract | JSON | Studio | Mandatory safety constraints are true |
| Approved seed | PNG plus hash record | Studio | Client approves and hash is recorded |
| Visual grammar | Markdown plus JSON mappings | Studio | Each technique maps to render fields |
| QA evidence | Markdown | Studio | Every failed and passed gate is dated |
| Reuse brief | Markdown | Studio | Creative Test Sprint can consume without clarification |
| Portfolio summary | Markdown | Client | Client understands outcome, exclusions, cost, and next step |

## 8. Cost policy

| Work item | Default route | Approval |
|---|---|---|
| Package assembly and QA | Existing artifacts only | No new generation |
| Product-only image boards | Current free GPT Image 2.5 route when promotion is active | Follow current account evidence |
| Identity seed | Reuse approved seed | New seed requires explicit approval |
| Downstream motion check | Existing V6 sample where possible | New V6 720p five-second render is 40 measured credits |
| Other image/video models | Not routine | Explicit operator approval required |

Record actual credits, task IDs, model, quality, duration, output path, and QA
result. Never infer cost from a price list when an observed account result is
available.

## 9. Final checklist

- [ ] Client question and category tension are stated.
- [ ] No real-person likeness is requested.
- [ ] Character block is frozen verbatim.
- [ ] Mandatory AI, fiction, product, and safety constraints are true.
- [ ] Seed is approved, local, and hash-recorded.
- [ ] Visual grammar names one dominant technique and explicit prohibitions.
- [ ] Product legibility and no-readable-text checks passed.
- [ ] Identity hold is validated on at least one downstream image or video.
- [ ] Cost, task IDs, limitations, and QA evidence are recorded.
- [ ] Client approved the identity or the open approval issue is explicit.
- [ ] Creative Test Sprint intake is complete.
- [ ] No unapproved paid generation occurred.
