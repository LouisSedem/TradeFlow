# TradeFlow + FreeWave Worklog

---
Task ID: pay-1
Agent: Main Agent
Task: Competitive audit of TradeFlow Phase 1 against 11 African payment competitors

Work Log:
- Audited current TradeFlow Phase 1 codebase (FX calculator, engine, currencies, API, schema)
- Researched 11 competitors: Wise, SendWave, Chipper Cash, AZA Finance, Fonbnk, Remitly, Monito, Flutterwave, Paystack, Africa's Talking, Pfegha
- Built feature-by-feature scoring matrix across 6 dimensions
- Identified 3 critical gaps, 3 important gaps, 3 nice-to-have gaps
- Confirmed TradeFlow's uncontested white space: 0/11 competitors mention PAPSS
- Generated 13-page competitive audit PDF with cover, TOC, and 8 chapters

Stage Summary:
- Key finding: PAPSS-aware multi-rail comparison is a completely uncontested niche
- Critical gaps: live FX rates, production database, user auth
- Closest benchmarks: Monito (comparison model), Wise (transparency standard), AZA Finance (African FX depth)
- Deliverable: /home/z/my-project/download/TradeFlow-Competitive-Audit.pdf

---
Task ID: 3
Agent: Main Agent
Task: Fix 30-second playback - client-side CORS proxy approach

Work Log:
- Tested all 5 Invidious instances - all dead/timing out
- Tested 4 Piped API instances - all down
- Tested allorigins, corsproxy.io, cors.sh, proxyfx - all fail from production
- corsproxy.io returns 403 on vercel.app domains ("Free usage is limited to localhost")
- Tested YouTube innertube API - works locally but blocked on Vercel IPs
- Tested ytInitialData HTML parsing - works locally but Vercel IPs get empty results
- Discovered corsproxy.io DOES work from browser (returns YouTube HTML with 257 videoIds)
- Moved YouTube search to client-side via CORS proxy
- Implemented ytInitialData parsing in browser (proven to extract videoIds + metadata)
- corsproxy.io blocks production - need self-hosted proxy
- Created Cloudflare Worker (worker/youtube-proxy-worker.js) as the solution
- Cloudflare Workers run on edge, not blocked by YouTube, free 100K requests/day
- App reads NEXT_PUBLIC_YT_PROXY_URL env var to find the proxy

Stage Summary:
- Root cause: YouTube blocks ALL datacenter IPs (Vercel, AWS, GCP) + all public CORS proxies block production domains
- Solution: Self-hosted Cloudflare Worker as CORS proxy (2 min setup, free, permanent)
- Code is ready, just needs NEXT_PUBLIC_YT_PROXY_URL env var on Vercel
