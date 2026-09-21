# How Jevmax Studio Tested an AirPods Category Without Guessing

## The business problem

A small brand can waste money in two opposite ways:

1. copy competitors without understanding what is actually running
2. generate a large batch of AI videos without a market signal or cost gate

Jevmax Studio's internal dogfood run tested a third route:

```text
bounded market signal
read-only account audit
locked fictional identity
ranked concepts
controlled V6 motion tests
QA and measured spend
```

This was not a live performance experiment. It was a production-system test
designed to answer: can the studio produce an evidence-controlled ad test
package before a client spends money?

## What we inspected

The internal run used the public AirPods-accessory category as the test
market.

| Measure | Result |
|---|---:|
| Estimated active ads found by the bounded search | 6,792 |
| Ads returned by the top-50 search | 50 |
| Current-only IDs versus the prior bounded sample | 29 |
| Overlap with the prior bounded sample | 21 |
| Unique IDs retained in the longitudinal snapshot | 103 |

The search was bounded and newest-first. It was not a whole-library census.

The bounded sample showed a simple competitive pattern among the ads already
connected to the tagged baseline:

- direct offer: 14
- curiosity claim: 5
- untagged: 2
- other-product offers: 19

That does not prove which ad will win. It does give the creative team a
concrete starting point: most visible tagged competitors led with direct
product offers, so a test brand needs either sharper specificity or a stronger
pattern interrupt.

## What the account audit found

The read-only audit of the internal test account found three pre-launch
blockers:

1. a pixel existed but had never fired
2. no Instagram account was linked
3. lead-gen terms had not been accepted

Both old campaigns were already paused. The audit made no live campaign
changes.

The practical result was immediate: paid launch should wait until measurement
and placement blockers are fixed. This is the exact kind of finding that
prevents creative spend from flying blind.

## How the creative system worked

Jevmax Studio did not start by generating random videos.

It used four layers:

1. **Lost Future style family**
   - selected: 1986–1992 Local Sponsor Bumper
   - effect: a specific historical visual register, not generic "retro"

2. **Eyecandy technique**
   - selected: Central Framing
   - effect: keep the subject and product visually dominant

3. **Frozen identity system**
   - fictional character Ava
   - approved seed image
   - no real-person likeness
   - product legibility required

4. **Concept gate**
   - concepts were scored before rendering
   - top score: 6.34
   - winning concept: Sponsored Minute

Only after those layers passed did the studio render motion.

## What the render tests measured

The current default route is:

```text
GPT Image 2.5 Sunburst board
V6 720p five-second no-audio video
```

Measured results:

| Route | Output | Measured cost | Practical result |
|---|---|---:|---|
| GPT Image 2.5 Flare | product image | 0 credits | clean image, but drifted from towel to sand |
| GPT Image 2.5 Sunburst | product image | 0 credits | closest to brief; no text |
| V6 720p | 5s vertical video | 40 credits | identity held; product legible; no text card |
| MiniMax H3 768p | 5s vertical video | 150 credits | stronger output but drifted composition |
| Seedance 2.5 1080p | 5s vertical video | 850 credits | technically strong but generated unwanted text card |

The default commercial route is therefore V6 720p. It is not the most cinematic
option, but it produced the best measured balance of identity control, prompt
obedience, and cost.

An eight-video V6 sprint projects to:

```text
8 x 40 credits = 320 credits
```

The earlier nine-video audio-enabled batch cost 475 credits. The current route
removes generated audio, reduces cost, and avoids unpredictable native audio.

## QA and claim discipline

The V6 hero test passed:

- local file delivery
- 720×1280 resolution
- 9:16 aspect ratio
- 5.0417-second duration
- stable subject identity
- legible earbud product
- no text card
- no extra people
- no live ad changes

No ROAS, conversion lift, or production performance improvement is claimed.
Those results require an approved live test, defined baseline, and measured
spend.

## What the studio now sells

The internal dogfood became five products:

1. Category Signal Audit
2. Brand Identity System
3. Creative Test Sprint
4. Paid Launch Kit
5. Growth Loop

The flagship offer is the Category Signal Sprint:

- bounded category scan
- account audit
- Lost Future concept directions
- Eyecandy technique mapping
- ranked concepts
- controlled identity
- free image boards
- eight V6 videos
- QA report
- top-two recommendation
- launch checklist

## The takeaway

AI video does not make advertising cheaper by itself. The cost saving comes
from the order of operations:

```text
look at the market
audit the account
freeze the identity
rank the concepts
render one test
QA the output
then batch
```

That is the difference between a studio and a content slot machine.
