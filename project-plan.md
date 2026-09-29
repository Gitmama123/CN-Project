
# Computer Networks Project: Distributed Network Monitoring with SDN

## Problem Statement

> Develop a distributed network-monitoring system where hosts transmit telemetry through UDP sockets. The SDN controller should combine application telemetry with network-flow statistics to identify abnormal conditions.

## Team and Roles

| Person | Name | Responsibility |
|---|---|---|
| A | Sai | Mininet topology, host telemetry agents, fault injection |
| B | Chinmayi | Ryu controller: UDP collector, flow stats polling, anomaly detection |
| C | Navaneeth | Report, architecture diagram, README, test logs, slides and demo |

## System Overview

```
+-----------+   UDP telemetry (JSON)   +-----------------------+
|  Host h1  | -----------------------> |                       |
|  (agent)  |                          |     Ryu SDN           |
+-----------+                          |     Controller        |
+-----------+   UDP telemetry (JSON)   |                       |
|  Host h2  | -----------------------> |  1. UDP collector     |
|  (agent)  |                          |  2. Flow stats poller |
+-----------+                          |  3. Correlator        |
     ...                               |  4. Anomaly detector  |
      |                                +-----------+-----------+
      |        OpenFlow 1.3                        |
      +------------- Switches (Mininet) -----------+
                  (flow / port stats replies)
```

**Data sources the controller combines**
1. **Application telemetry** from hosts over UDP (latency, request rate, errors, CPU, memory).
2. **Network-flow statistics** from switches over OpenFlow (bytes, packets, rates per flow and port).

## Tools

- Mininet (network emulation)
- Ryu controller, OpenFlow 1.3
- Python 3 (`socket`, `json`, `psutil`)
- `iperf` and `tc netem` (fault injection)
- matplotlib or a terminal log (visualization of results)

## Telemetry Message Format (agreed interface between A and B)

Each host sends one UDP datagram per interval (default 1 second):

```json
{
  "host_id": "h1",
  "seq": 42,
  "timestamp": 1700000000.123,
  "metrics": {
    "app_latency_ms": 12.4,
    "req_per_sec": 85,
    "error_count": 0,
    "cpu_percent": 23.1,
    "mem_percent": 41.7
  }
}
```

Controller listens on a fixed UDP port (proposed: `9999`). Any change to this format must be agreed by A and B.

## Anomaly Detection Logic (starting rules)

| App telemetry | Flow stats | Likely condition |
|---|---|---|
| Latency high | Throughput very high | Congestion or flood |
| Latency high | Throughput normal | Host or application problem |
| Telemetry missing | Flows still active | Agent crash or UDP loss |
| Telemetry missing | No flows | Host or link down |

Start with fixed thresholds. If time permits, upgrade to a rolling mean with a z-score.

## Fault Injection Scenarios (for testing)

1. UDP flood between two hosts using `iperf`.
2. Added delay on a link using `tc netem`.
3. Packet loss on a link using `tc netem`.
4. Host agent killed.
5. Link brought down in Mininet.

## Task Breakdown

### Person A: Sai
- [ ] Create Mininet topology (1 to 2 switches, 4 to 6 hosts)
- [ ] Write the host telemetry agent script
- [ ] Write scripts for each fault injection scenario
- [ ] Share the topology and agent scripts with the team

### Person B: Chinmayi
- [ ] Set up Ryu with a basic learning switch
- [ ] Implement the UDP telemetry collector
- [ ] Implement periodic flow and port stats polling
- [ ] Implement correlation and anomaly detection rules
- [ ] Log detected anomalies with timestamps

### Person C: Navaneeth
- [ ] Draw the architecture diagram
- [ ] Draft the report: introduction, background (SDN, OpenFlow, UDP telemetry), references
- [ ] Write the README with install and run steps
- [ ] After A and B's code works: run each fault scenario, save logs and screenshots, fill in the results table
- [ ] Build presentation slides and record a demo video

## Milestones

| # | Milestone | Owner(s) | Target date |
|---|---|---|---|
| 1 | Mininet + Ryu running, basic switching works | A, B | ____ |
| 2 | One host sends telemetry, controller prints it | A, B | ____ |
| 3 | Flow stats polling working | B | ____ |
| 4 | Detection rules working | B | ____ |
| 5 | All fault scenarios tested | A, C | ____ |
| 6 | Report, slides and demo complete | C (all review) | ____ |

## Results Table (to be filled by Person C)

| Fault injected | Expected detection | Actual detection | Time to detect |
|---|---|---|---|
| UDP flood | Congestion or flood | | |
| Added delay | Latency anomaly | | |
| Packet loss | Loss or missing telemetry | | |
| Agent killed | Agent crash | | |
| Link down | Host or link down | | |

## Ground Rules

- Agree on the telemetry format before writing code, and keep it updated in this file.
- Push code to a shared GitHub repo, with small and frequent commits.
- Post blockers in the group chat early instead of waiting.
