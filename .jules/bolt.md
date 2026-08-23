## 2024-08-23 - Optimize Leaderboard Query
**Learning:** Avoid full-node downloads for ranked data (e.g., leaderboards) by setting `.indexOn` in `database.rules.json` and using `orderByChild` combined with `limitToLast` (or `startAt`). This reduces payload size and prevents O(N) bandwidth bottlenecks.
**Action:** Always check if a query downloads an entire collection. If so, add indices to Firebase rules and apply server-side filtering via limit or range queries, then process the results client-side using `snap.forEach()`.
