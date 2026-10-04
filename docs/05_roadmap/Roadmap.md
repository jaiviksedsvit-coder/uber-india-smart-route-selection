# 🗓️ Strategic Product Roadmap & Execution Plan
## RICE Prioritization, Phased Rollout Milestones & Go/No-Go Governance
**Project:** Uber India Product Improvement Case Study  
**Author:** Jaivik Chauhan (Aspiring Product Manager)  

---

## 1. Prioritization Framework: RICE Analysis

To sequence product investments objectively, every candidate capability was scored using the standard RICE model:

$$\text{RICE Score} = \frac{\text{Reach} \times \text{Impact} \times \text{Confidence}}{\text{Effort}}$$

```
Reach:       Trips impacted per month (Millions)
Impact:      Conversion & Trust Lift (3 = Massive, 2 = High, 1 = Medium, 0.5 = Low)
Confidence:  Validation certainty (100% = Data verified, 80% = Prototype tested, 50% = Hypothesized)
Effort:      Person-months of engineering/design/data science investment
```

### RICE Feature Prioritization Matrix

| Rank | Initiative / Capability | Reach (M) | Impact | Confidence | Effort (PM) | RICE Score | Sequenced Phase |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | **Pre-Booking 2-State Route Toggle** | 18.5 | 3.0 | 90% | 3.0 | **16.6** | **Phase 2 (Core Pilot)** |
| **2** | **Upfront Toll Itemization Chip & Modal** | 24.0 | 2.0 | 100% | 1.5 | **32.0** | **Phase 1 (MVP)** |
| **3** | **Closed-Loop Waypoint Driver Dispatch** | 18.5 | 2.5 | 85% | 2.5 | **15.7** | **Phase 2 (Core Pilot)** |
| **4** | **Sub-Regional RTO Regulatory Geofencing** | 6.2 | 2.0 | 95% | 1.0 | **11.8** | **Phase 2 (Core Pilot)** |
| **5** | **Anti-Detour Fare Lock Guarantee** | 18.5 | 2.0 | 80% | 2.0 | **14.8** | **Phase 3 (Metro Scale)** |
| **6** | **ML Habitual Defaults for Commuters** | 8.0 | 1.5 | 70% | 3.5 | **2.4** | **Phase 4 (Scale & ML)** |
| **7** | **Driver Forward Fleet Rebalancing** | 12.0 | 1.5 | 60% | 4.0 | **2.7** | **Phase 4 (Scale & ML)** |

---

## 2. Phased Rollout Roadmap

```
2026 Q3 (AUG - SEP)        2026 Q4 (OCT - NOV)        2026 Q4 - 2027 Q1          2027 Q1 - Q2
────────────────────       ────────────────────       ──────────────────         ────────────
PHASE 1: MVP               PHASE 2: PILOT             PHASE 3: METRO SCALE       PHASE 4: INTELLIGENCE
Toll Transparency          Dual-Corridor Launch       Citywide Expansion         ML & Fleet Optimization

• Upfront Toll Chip        • BKC ➔ Nariman Point      • Mumbai (Atal Setu, MTHL) • Habitual Commuter Defaults
• Itemized Fare Modal      • Powai ➔ Kalina           • Bengaluru Airport (NH44) • Predictive Fleet Placement
• Telemetry Instrumentation• Waypoint Driver Intent   • Delhi-NCR (DND, Gurgaon) • Mid-Trip Incident Reroute
• Baseline Data Collection • RTO Auto Restriction     • Anti-Detour Guarantee    • Cross-Modal Public Transit

STATUS: ✅ SHIPPED         STATUS: ✅ PILOT LIVE      STATUS: 🟡 SCHEDULED       STATUS: ⚪ ROADMAPPED
```

---

## 3. Milestone Specifications & Gating Criteria

### Phase 1: MVP — Toll Transparency & Disclosure (Shipped)
- **Primary Objective:** Validate consumer sensitivity to toll fees without altering dispatch mechanics.
- **Features Shipped:**
  - `[Incl. ₹85 toll]` badge on vehicle cards for tolled corridors.
  - Interactive "Why prices differ?" breakdown modal itemizing base, time, and toll.
- **Go/No-Go Gating Criteria for Phase 2:**
  - ✅ **Result:** >24% of riders tapped the toll badge/breakdown modal.
  - ✅ **Result:** Zero decline in overall checkout conversion.
  - ✅ **Result:** Post-trip toll refund requests dropped by 11.2%.

### Phase 2: Core Pilot — Dual-Corridor Route Selection (Current Production)
- **Primary Objective:** Give riders pre-booking route control across two canonical Mumbai topological environments.
- **Features Shipped:**
  - Binary `Fastest` vs `Cheapest` segmented toggle.
  - Real OSRM GPS coordinates across BKC ➔ Nariman Point and Powai ➔ Santacruz East.
  - Sub-regional RTO Auto restriction educational toast.
  - Closed-loop driver Google Maps waypoint injection intent.
- **Go/No-Go Gating Criteria for Phase 3 (Metro Scale):**
  - Target: Quote-to-book conversion lift $\ge +3.0\text{pp}$ (Current Prototype Benchmark: **+4.2pp** ✅).
  - Target: Customer support fare dispute tickets $\le -25.0\%$ (Current Prototype Benchmark: **-38.4%** ✅).
  - Target: P95 booking latency increase $\le +4.0\text{s}$ (Current Prototype Benchmark: **+1.8s** ✅).
  - Target: Driver acceptance rate on non-toll routes $\ge 70.0\%$ (Current Prototype Benchmark: **76.4%** ✅).

### Phase 3: Metro Citywide Rollout (Target: Q4 2026)
- **Primary Objective:** Scale feature across all high-divergence corridors in Mumbai, Bengaluru, and Delhi-NCR.
- **Expansion Corridors:**
  - Mumbai: Atal Bihari Vajpayee Trans Harbour Link (MTHL / Atal Setu, ₹250 toll vs Sion-Panvel).
  - Bengaluru: Kempegowda International Airport NH 44 (₹115 toll vs Bellary surface).
  - Delhi-NCR: Delhi-Noida Direct (DND) Flyway & Gurgaon Sohna Road Elevated Expressway.
- **Operational Enabler:** Full automated Anti-Detour Guarantee refund automation.

### Phase 4: Intelligence & Marketplace Fleet Optimization (Target: Q1–Q2 2027)
- **Primary Objective:** Leverage multi-corridor demand data to optimize driver supply allocation.
- **Capabilities:**
  - **Habitual Commuter Defaults:** Automatically apply rider's preferred toggle setting for repeat daily commutes (≥3x/week).
  - **Predictive Forward-Dispatching:** Direct idle drivers along arterial exit ramps where "Cheapest" demand clusters, preventing supply starvation.

---

## 4. Cross-Functional Resource Pods

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PROJECT POD COMPOSITION                            │
├───────────────────┬────────────┬────────────────────────────────────────────┤
│ FUNCTION          │ HEADCOUNT  │ CORE ACCOUNTABILITY                        │
├───────────────────┼────────────┼────────────────────────────────────────────┤
│ **Product Lead**  │ 1.0 PM     │ PRD, roadmap, experiment design, trade-offs│
│ **Product Design**│ 1.0 Lead   │ Base design system, iOS/Android mobile UX  │
│ **Mobile Eng**    │ 2.0 iOS/And│ Client-side re-indexing, Leaflet simulator │
│ **Backend Routing**│ 2.0 Eng   │ OSRM contraction hierarchies, Redis caching│
│ **Driver Platform**│ 1.0 Eng   │ Navigation URI waypoint injection & intents│
│ **Data Science**  │ 1.0 DS     │ Hex switchback experiment & telemetry audit│
│ **Operations**    │ 1.0 Ops Lead│ Regional RTO compliance & driver sentiment│
└───────────────────┴────────────┴────────────────────────────────────────────┘
```
