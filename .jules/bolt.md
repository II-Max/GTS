## 2023-08-16 - [Firebase Query Optimization]
**Learning:** Avoid full-node downloads on client side.
**Action:** When querying Firebase RTDB on the client-side for ranked data (e.g., leaderboards), avoid full-node downloads by setting `.indexOn` in `database.rules.json` and using `orderByChild` combined with `limitToLast` or `startAt` to drastically reduce payload sizes and prevent O(N) bandwidth bottlenecks.
