## 2024-05-24 - Optimizing Leaderboard Queries

**Learning:** When querying Firebase Realtime Database on the client-side for ranked data (e.g., leaderboards), avoid full-node downloads. Full-node downloads scale poorly O(N) as the user base grows and create significant bandwidth bottlenecks. Adding an index (`.indexOn`) in `database.rules.json` enables performant queries combined with `limitToLast` on the client. Also, avoid computing global rank for a single user if it requires an O(N) full node download.

**Action:** Always check `database.rules.json` to ensure indices exist for ordered properties. Replace `.once('value')` full node fetches on large nodes with `.orderByChild(property).limitToLast(N)` queries or point queries when possible.
