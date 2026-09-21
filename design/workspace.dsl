workspace "Jevmax Studio Product Portfolio" "Validated commercial routing and product packages over the existing Jevmax intelligence and creative repository." {
  model {
    sys = softwareSystem "Jevmax Studio Portfolio" "Routes clients to commercial products and verifies reusable deliverables." {
      validator = container "Portfolio Validator" "Deterministically checks package shape, manifests, paths, routes, policy, and claim discipline." "Python"
      packages = container "Product Packages" "Five product directories containing templates, manifests, evidence, and portfolio summaries." "Markdown/JSON"
      comedy = container "Comedy Test Sprint Pipeline" "Generates premises, applies deterministic filters, runs recorded Jev tournaments, mutates survivors, and prepares bounded rendering." "Python"
      gtm = container "Go-To-Market Assets" "Public-safe case study, sales kit, outreach playbook, tracker schema, and measured-fact manifest." "Markdown/JSON"
      index = container "Studio Index" "Client-facing routing map and production policy." "Markdown"
      artifacts = container "Artifact Store" "Existing repository outputs: scans, audits, snapshots, prompts, images, videos, QA, and cost reports." "Repository filesystem"
    }

    meta = softwareSystem "Meta Ads MCP" "Official read-only or explicitly approved ad-account and Ad Library interface." "External"
    typesafe = softwareSystem "TypeSafe System One" "Judgment and concept-gating API." "External"
    pixverse = container "PixVerse CLI" "Controlled image and video generation provider." "External"

    index -> packages "Routes to a product package"
    validator -> packages "Reads manifests, templates, evidence, and summaries"
    validator -> comedy "Reads comedy premise, tournament, board, render, and QA evidence"
    validator -> gtm "Reads public-safe claims and measured facts"
    validator -> artifacts "Resolves every referenced artifact path"
    gtm -> artifacts "Cites measured source artifacts"
    packages -> artifacts "Cites concrete dogfood artifacts"
    comedy -> artifacts "Writes and cites comedy sprint artifacts"
    comedy -> typesafe "Runs recorded premise judgment tournaments"
    comedy -> pixverse "Creates free boards and at most two V6 videos"
    packages -> meta "Records the provenance of market and account intelligence"
    packages -> typesafe "Records judgment-gate provenance"
    packages -> pixverse "Records measured render cost and QA provenance"
  }
}
