## 2024-05-24 - Firebase RTDB O(N) Bandwidth Bottleneck
**Learning:** Querying a full node (like `public_leaderboard`) on the client side without limits downloads the entire dataset, creating an O(N) bandwidth bottleneck as the user base grows.
**Action:** Always use `.indexOn` in `database.rules.json` and query with `orderByChild().limitToLast(N)` to drastically reduce payload sizes. Iterate using `snap.forEach()` to maintain order, and handle tie-breakers on the client side.
