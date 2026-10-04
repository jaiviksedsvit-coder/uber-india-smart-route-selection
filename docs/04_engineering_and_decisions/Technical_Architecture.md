# ⚙️ Technical Architecture & Systems Engineering
## Routing Microservices, Latency Budgets, Waypoint Dispatch & Reliability
**Project:** Uber India Product Improvement Case Study  
**Author:** Jaivik Chauhan (Aspiring Product Manager)  

---

## 1. System Architecture: End-to-End Topology

The Smart Route Selection feature integrates across Uber's microservices stack to deliver pre-booking route choices without introducing client latency or driver disruption:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    END-TO-END SMART ROUTE ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────────────┘

 [RIDER APP (iOS/Android)]
        │
        ├─ 1. POST /v2/rides/quotes (origin_coords, dest_coords, user_id)
        ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      API GATEWAY & ROUTING ORCHESTRATOR                │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 2. Parallel Evaluation Pipeline:                                       │
 │    ├─ Service A: OSRM Multi-Corridor Engine (Computes Top 2 Polylines) │
 │    ├─ Service B: Toll Tariff Engine (Evaluates FASTag / BWSL Fees)     │
 │    └─ Service C: Dynamic Pricing Engine (Computes Multi-Modal Fares)   │
 │                                                                        │
 │ 3. Bundles Dual-Corridor Payload: {fastest: {...}, cheapest: {...}}    │
 └────────────────────────────────────────────────────────────────────────┘
        │
        ├─ 4. Returns JSON Bundle in <350ms (P95)
        ▼
 [RIDER APP: CLIENT-SIDE RE-INDEXING ENGINE]
        │
        ├─ 5. Evaluates Corridor Eligibility: (ΔTime ≥ 3m, ΔPrice ≥ ₹15)
        ├─ 6. Renders Binary Segmented Control (Fastest / Cheapest)
        ├─ 7. Synchronous DOM re-indexing on toggle click (<50ms, zero network)
        ├─ 8. Rider confirms: POST /v2/rides/book {corridor_id, waypoints}
        ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                   DISPATCH & DRIVER WAYPOINT INJECTION ENGINE          │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 9. Locks rider upfront quote (Anti-Detour Guarantee)                   │
 │ 10. Constructs Driver Partner Navigation Payload:                      │
 │     `google.navigation:q=dest&waypoints=wp1|wp2&mode=d`               │
 └────────────────────────────────────────────────────────────────────────┘
        │
        ▼
 [DRIVER PARTNER APP] ──> Launches Google Maps / Native SDK with locked waypoints
```

---

## 2. Latency Budgets & Engineering SLAs

To maintain Uber's checkout performance thresholds, strict latency budgets are enforced across the pipeline:

| Pipeline Stage | P50 SLA | P95 SLA | P99 SLA | Architectural Enforcement Mechanism |
|---|---|---|---|---|
| **OSRM Route Generation** | 45ms | 85ms | 140ms | Pre-computed contraction hierarchies (CH) cached in RAM |
| **Toll Matrix Evaluation** | 12ms | 25ms | 50ms | In-memory lookup table of Indian national & municipal toll plazas |
| **Multi-Vehicle Pricing** | 60ms | 110ms | 190ms | Vectorized rate calculation across 5 vehicle tiers simultaneously |
| **Total API Response** | **180ms** | **320ms** | **450ms** | Single bundled network roundtrip (`/v2/rides/quotes`) |
| **Client Toggle Transition**| **<10ms** | **25ms** | **50ms** | **100% Client-side synchronous DOM swap; zero network call** |

---

## 3. Data Schemas & API Payloads

### 1. Pre-Booking Multi-Corridor Quote Payload (`/v2/rides/quotes`)
```json
{
  "corridor_evaluation": {
    "has_alternatives": true,
    "primary_theme": "Toll Avoidance (Bandra-Worli Sea Link)",
    "rto_restrictions": {
      "auto_restricted": true,
      "notice": "By municipal RTO regulations, autos cannot operate south of Bandra/Sion."
    }
  },
  "routes": [
    {
      "id": "fastest",
      "name": "Fastest",
      "road_summary": "via Bandra-Worli Sea Link (BWSL)",
      "distance_km": 21.2,
      "duration_min": 26,
      "has_tolls": true,
      "toll_amount_inr": 85,
      "waypoints": [[19.0658, 72.8686], [19.0340, 72.7960], [18.9260, 72.8230]],
      "fares": {
        "ubergo": 480,
        "premier": 640,
        "auto": null,
        "moto": 160,
        "uberxl": 790
      },
      "fare_breakdown": {
        "base_fare": 295,
        "time_fare": 100,
        "toll_fee": 85,
        "total": 480
      }
    },
    {
      "id": "cheapest",
      "name": "Cheapest",
      "road_summary": "via Mahim, Senapati Bapat & Marine Dr",
      "distance_km": 16.4,
      "duration_min": 42,
      "has_tolls": false,
      "toll_amount_inr": 0,
      "waypoints": [[19.0658, 72.8686], [19.0412, 72.8409], [18.9780, 72.8540], [18.9260, 72.8230]],
      "fares": {
        "ubergo": 350,
        "premier": 490,
        "auto": null,
        "moto": 160,
        "uberxl": 590
      },
      "fare_breakdown": {
        "base_fare": 225,
        "time_fare": 125,
        "toll_fee": 0,
        "total": 350
      }
    }
  ]
}
```

### 2. Driver Dispatch Intent Construction (`/v2/dispatch/match`)
```json
{
  "trip_id": "trip_bkc_np_8829104",
  "rider_selected_corridor": "cheapest",
  "locked_upfront_fare": 350,
  "navigation_payload": {
    "intent_uri": "google.navigation:q=18.9260,72.8230&waypoints=19.0412,72.8409|18.9780,72.8540&mode=d",
    "fallback_polyline_geojson": "...",
    "deviation_threshold_meters": 250
  }
}
```

---

## 4. Resilience, Caching & Failover Engineering

### 1. Redis Spatial Caching (H3 Hexagonal Bucketing)
To avoid overloading OSRM engines during peak rush hour, polylines for high-traffic metro commuter corridors are cached in Redis using H3 Hexagonal indices (resolution 8, ~460m edge length):
- **Cache Key:** `corridor:h3_origin:h3_dest:time_bucket`
- **Cache TTL:** 180 seconds (refreshes dynamically with live traffic delta updates).

### 2. Defensive Single-Corridor Fallback
If the routing engine fails to find a secondary route within 150ms, or if the corridor has zero topological divergence:
1. The API returns `has_alternatives: false`.
2. The client silently suppresses the toggle container (`display: none; height: 0;`).
3. Standard single-price Uber checkout renders instantly without error modals.

### 3. Tunnel Map-Matching & GPS Degradation Handling
For coastal infrastructure with prolonged cellular blind spots (e.g., Mumbai Coastal Road 2km undersea tunnel):
- Mobile client switches to **dead-reckoning inertial navigation** using device accelerometer and gyroscope data.
- Snaps location marker along the pre-loaded polyline until GPS satellite lock is re-acquired at the tunnel exit portal.
