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
│                   Target: 72.0% (Baseline: 65.0%, Prototype: 69.2%)         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────────────┐     ┌───────────────────────────────┐
│     INPUT / ADOPTION LEVERS   │     │      OPERATIONS & CS IMPACT   │
├───────────────────────────────┤     ├───────────────────────────────┤
│ • Corridor Switch Rate (31.8%)│     │ • Toll Dispute Deflection     │
│ • Fare Breakdown Engagement   │     │   (-38.4% CS ticket volume)   │
│ • D7 Repeat Selection (58.4%) │     │ • Refund Payout Overhead      │
└───────────────────────────────┘     └───────────────────────────────┘
            │                                                     │
            └──────────────────────────┬──────────────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
┌───────────────────────────────┐     ┌───────────────────────────────┐
│       GUARDRAIL METRICS       │     │        COUNTER-METRICS        │
├───────────────────────────────┤     ├───────────────────────────────┤
│ • Decision Latency (≤ +5.0s)  │     │ • Platform Take Rate / Trip   │
│ • Driver Acceptance Rate (≥70%)│    │ • Driver Hourly Earnings ($/hr│
│ • ETA Accuracy (±5 min)       │     │ • Traffic Congestion Spillover│
└───────────────────────────────┘     └───────────────────────────────┘
```

---

## 2. Core Metrics Definitions & Benchmarks

### 1. North Star Metric: Route Selection Conversion Rate
- **Definition:** The percentage of pre-booking checkout sessions on multi-corridor routes that result in a completed booking.
$$\text{Conversion Rate} = \frac{\sum \text{Completed Bookings on Eligible Corridors}}{\sum \text{Checkout Sessions on Eligible Corridors}} \times 100$$
- **Pre-Launch Baseline:** 65.0%
- **Target:** 72.0%
- **Prototype Benchmark:** **69.2% (+4.2pp lift)**

### 2. Adoption Lever: Corridor Switch Rate
- **Definition:** The percentage of converted rides where the rider actively selected the non-default route (`Cheapest`).
$$\text{Switch Rate} = \frac{\sum \text{Bookings with 'Cheapest' Selected}}{\sum \text{Total Smart Route Bookings}} \times 100$$
- **Target Range:** 30.0% – 35.0%
- **Prototype Benchmark:** **31.8%** (Validates healthy engagement without cannibalizing the default).

### 3. Operations & Cost Lever: Toll Dispute Deflection
- **Definition:** Percentage reduction in customer support tickets categorized under "Route Disagreement", "Toll Overcharge", or "Unapproved Detour".
- **Target:** -35.0%
- **Prototype Benchmark:** **-38.4% deflection** (Saving ~₹42M annually across Mumbai and Bengaluru operations).

### 4. Guardrail Metric 1: Booking Decision Latency
- **Definition:** Additional seconds spent on the vehicle selection screen before confirming booking.
- **Guardrail Threshold:** $\Delta \text{Latency} \le +5.0\text{ seconds}$.
- **Prototype Benchmark:** **+1.8 seconds** (Hick's Law 2-state design prevents cognitive paralysis).

### 5. Guardrail Metric 2: Driver Partner Acceptance Rate
- **Definition:** Percentage of dispatched trip offers accepted by drivers on rider-selected non-toll routes.
- **Guardrail Threshold:** $\ge 70.0\%$.
- **Prototype Benchmark:** **76.4%** (Fuel savings and pre-loaded GPS instructions keep driver acceptance strong).

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
│ • Total Sample Size: 180,000 corridor trip sessions over 21 days.          │
│ • Statistical Power: 85% at $\alpha = 0.05$ with MDE of +1.5pp conversion. │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Telemetry & Analytics Instrumentation Schema

Every interaction emits a structured JSON event via Uber's event stream:

```json
{
  "event_name": "route_preference_selected",
  "timestamp": "2026-10-04T10:14:22.104Z",
  "session_id": "sess_894f2910ba",
  "corridor_id": "bkc_nariman",
  "selected_route_id": "cheapest",
  "selected_road": "via Mahim, Senapati Bapat & Marine Dr",
  "time_delta_min": 16,
  "fare_savings_inr": 130,
  "toll_avoided_inr": 85,
  "quoted_price_ubergo": 350,
  "latency_on_screen_ms": 1820
}
```

---

## 5. Executive Dashboard Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  UBER INDIA: SMART ROUTE SELECTION — PERFORMANCE COCKPIT                     │
├──────────────────────────────────────────────────────────────────────────────┤
│  NORTH STAR CONVERSION RATE        ADOPTION: SWITCH RATE       CS TICKET DEFLECTION│
│  ┌─────────────────────────┐      ┌─────────────────────┐     ┌──────────────────┐ │
│  │ 69.2%  ▲ +4.2pp vs ctrl │      │ 31.8% to 'Cheapest' │     │ -38.4% Tickets   │ │
│  └─────────────────────────┘      └─────────────────────┘     └──────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────┤
│  CORRIDOR PERFORMANCE DEEP DIVE                                              │
│  Corridor 1: BKC ➔ Nariman Pt     | Conversion: 71.4% | Toll Avoidance: 34.2%│
│  Corridor 2: Powai ➔ Santacruz    | Conversion: 67.8% | Cost Savings: 29.4%  │
├──────────────────────────────────────────────────────────────────────────────┤
│  MARKETPLACE HEALTH GUARDRAILS                                               │
│  • P95 Decision Latency:    1.8s   (Target: ≤ 5.0s)          [STATUS: HEALTHY]│
│  • Driver Acceptance Rate:  76.4%  (Target: ≥ 70.0%)         [STATUS: HEALTHY]│
│  • ETA Variance Accuracy:   ±4.1m  (Target: ± 6.0m)          [STATUS: HEALTHY]│
│  • Driver Partner Earnings: ₹248/h (-0.8% offset by fuel)    [STATUS: HEALTHY]│
└──────────────────────────────────────────────────────────────────────────────┘
```
