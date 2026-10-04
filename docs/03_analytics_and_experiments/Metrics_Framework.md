# 📊 Metrics Framework & Experimentation Protocol
## North Star Hierarchy, A/B Testing Design & Telemetry Instrumentation
**Project:** Uber India Product Improvement Case Study  
**Author:** Jaivik Chauhan (Aspiring Product Manager)  

---

## 1. Metrics Hierarchy: The 4-Layer Taxonomy

To validate feature efficacy and safeguard marketplace balance, this framework establishes a 4-layer metrics architecture:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       NORTH STAR: CONVERSION LIQUIDITY                      │
│                Route Selection Quote-to-Book Conversion Rate                │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────────────┐     ┌───────────────────────────────┐
│     INPUT / ADOPTION LEVERS   │     │      OPERATIONS & CS IMPACT   │
├───────────────────────────────┤     ├───────────────────────────────┤
│ • Corridor Switch Rate        │     │ • Toll Dispute Deflection     │
│ • Fare Breakdown Engagement   │     │ • Refund Payout Overhead      │
│ • D7 Repeat Route Selection   │     │ • CS Ticket Volume            │
└───────────────────────────────┘     └───────────────────────────────┘
            │                                                     │
            └──────────────────────────┬──────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────────────┐     ┌───────────────────────────────┐
│       GUARDRAIL METRICS       │     │        COUNTER-METRICS        │
├───────────────────────────────┤     ├───────────────────────────────┤
│ • Booking Decision Latency    │     │ • Platform Take Rate / Trip   │
│ • Driver Acceptance Rate      │     │ • Driver Hourly Earnings      │
│ • ETA Accuracy                │     │ • Traffic Congestion Spillover│
└───────────────────────────────┘     └───────────────────────────────┘
```

---

## 2. Core Metrics Definitions & Rationale

### 1. North Star Metric: Route Selection Conversion Rate
- **Definition:** The percentage of pre-booking checkout sessions on multi-corridor routes that result in a completed booking.
$$\text{Conversion Rate} = \frac{\sum \text{Completed Bookings on Eligible Corridors}}{\sum \text{Checkout Sessions on Eligible Corridors}} \times 100$$
- **Why This Metric:** This is the most direct measure of whether presenting route choice resolves the price shock that currently causes riders to abandon checkout. A meaningful lift here indicates the feature is recapturing sessions that previously dropped off due to opaque toll pricing.

### 2. Adoption Lever: Corridor Switch Rate
- **Definition:** The percentage of converted rides where the rider actively selected the non-default route (`Cheapest`).
$$\text{Switch Rate} = \frac{\sum \text{Bookings with 'Cheapest' Selected}}{\sum \text{Total Smart Route Bookings}} \times 100$$
- **Why This Metric:** A healthy switch rate validates that riders find the cheapest option genuinely valuable and that the feature is not purely cosmetic. However, an excessively high switch rate (e.g., >80%) would indicate the default route is failing most riders, which is a product signal of its own. The goal is a balanced distribution that reflects genuine rider preference.

### 3. Operations & Cost Lever: Toll Dispute Deflection
- **Definition:** Percentage reduction in customer support tickets categorized under "Route Disagreement", "Toll Overcharge", or "Unapproved Detour" after feature launch vs. control group.
- **Why This Metric:** The core hypothesis is that pre-booking route transparency eliminates the information asymmetry that generates post-trip disputes. If riders consciously select a toll route (or explicitly choose to avoid it), there is no grounds for a post-trip dispute. This metric directly measures resolution of the operational cost driver identified in the problem framing.

### 4. Guardrail Metric 1: Booking Decision Latency
- **Definition:** Additional time (in seconds) a rider spends on the vehicle selection screen before confirming a booking, compared to the current single-route flow.
- **Why This Metric:** Adding a choice always risks increasing cognitive load and decision time (Hick's Law). If presenting two routes causes riders to freeze or overthink, it could worsen checkout abandonment rather than improve it. A binary (Fastest vs. Cheapest) design is specifically chosen to minimize this risk — this metric measures whether that design constraint holds in practice.

### 5. Guardrail Metric 2: Driver Partner Acceptance Rate
- **Definition:** Percentage of dispatched trip offers accepted by drivers on rider-selected non-toll routes (Cheapest corridor).
- **Why This Metric:** The feature's success depends on driver cooperation. If drivers systematically reject non-toll routes (e.g., fearing lower earnings on longer surface-road trips), the feature creates a new supply-side problem. Monitoring acceptance rate ensures marketplace health is not degraded on one side to fix a problem on the other.

### 6. Counter-Metric: Driver Hourly Earnings
- **Definition:** Average earnings per active driver-hour on corridors where Smart Route Selection is enabled, compared to control corridors.
- **Why This Metric:** A well-intentioned rider feature should not structurally harm driver-partners. Non-toll routes are longer in time (e.g., 42 min vs. 26 min for BKC ➔ Nariman Point). If drivers spend more time on cheaper routes without proportional fare compensation, their effective hourly rate drops. This counter-metric acts as a fairness guardrail for the driver side of the two-sided marketplace.

---

## 3. A/B Testing & Experimentation Protocol

### Experiment Design: Cluster-Randomized Switchback Experiment

Because two-sided ride-hailing marketplaces suffer from **network interference and SUTVA violations** (a rider choosing a non-toll route consumes driver supply that affects other riders), standard user-level A/B randomization is invalid.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXPERIMENT RANDOMIZATION STRATEGY                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Randomization Unit: Geospatial Corridor & 2-Hour Time Block (Switchback). │
│ • Geo Units: Mumbai H3 Hexagonal Clusters (BKC, Bandra, Lower Parel, Fort).│
│ • Allocation: 50% Treatment (Smart Route Enabled) / 50% Control (Status Quo)│
│ • Actual sample size, power, and MDE to be determined based on              │
│   production traffic volume during pilot instrumentation.                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Why Switchback Design?**
- Standard A/B at the user-level creates **marketplace interference**: a rider in the control group may fail to book because treatment-group riders absorbed the available driver supply on a non-toll corridor.
- Geo-temporal switchback randomization isolates the treatment effect by corridor and time block, preserving SUTVA (Stable Unit Treatment Value Assumption) and generating cleaner causal estimates.

---

## 4. Telemetry & Analytics Instrumentation Schema

Every interaction emits a structured JSON event via Uber's event stream. The schema below defines the data contract needed to compute all metrics above:

```json
{
  "event_name": "route_preference_selected",
  "timestamp": "<ISO 8601 UTC>",
  "session_id": "<unique session identifier>",
  "corridor_id": "<e.g. bkc_nariman | powai_santacruz>",
  "selected_route_id": "<fastest | cheapest>",
  "selected_road": "<road description string>",
  "fare_savings_inr": "<delta vs default route fare>",
  "toll_avoided_inr": "<toll component of fare delta>",
  "quoted_price_vehicle": "<upfront fare for selected vehicle>",
  "latency_on_screen_ms": "<time from sheet open to confirm tap>"
}
```

**Key Design Decisions in the Telemetry Schema:**
- `corridor_id` enables per-corridor deep-dives without joining against a separate route table.
- `latency_on_screen_ms` directly feeds Guardrail Metric 1 (Decision Latency) without any post-hoc inference.
- `toll_avoided_inr` is tracked separately from `fare_savings_inr` to distinguish toll avoidance from general congestion-based savings.

---

## 5. Executive Dashboard: Metric Categories

The post-launch monitoring dashboard should surface metrics across four panels:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  UBER INDIA: SMART ROUTE SELECTION — PERFORMANCE COCKPIT                     │
├──────────────────────────────────────────────────────────────────────────────┤
│  [NORTH STAR]              [ADOPTION]               [OPERATIONS]             │
│  Quote-to-Book             Corridor Switch Rate      CS Ticket Deflection    │
│  Conversion Rate           (% selecting Cheapest)    (Route Dispute Volume)  │
├──────────────────────────────────────────────────────────────────────────────┤
│  CORRIDOR PERFORMANCE DEEP DIVE                                              │
│  • Breakdown by: Corridor ID, Time of Day, Vehicle Type, Day of Week        │
│  • Key Dimensions: Conversion Rate, Switch Rate, Avg Fare Delta              │
├──────────────────────────────────────────────────────────────────────────────┤
│  MARKETPLACE HEALTH GUARDRAILS                                               │
│  • Booking Decision Latency       (vs. pre-feature baseline)                 │
│  • Driver Acceptance Rate         (on Cheapest corridor assignments)         │
│  • ETA Prediction Accuracy        (variance: predicted vs. actual trip time) │
│  • Driver Partner Hourly Earnings (vs. control corridor benchmark)           │
└──────────────────────────────────────────────────────────────────────────────┘
```
