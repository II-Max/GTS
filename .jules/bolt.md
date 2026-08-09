## 2024-05-24 - Firebase Realtime Database Query Optimization
**Learning:** Querying a node without `limitToLast` or `startAt` will download the entire node, resulting in O(N) bandwidth usage which is extremely slow for large datasets like a public leaderboard.
**Action:** Always define `.indexOn` in `database.rules.json` and use `orderByChild` combined with `limitToLast` for operations requiring sorted, paginated results to ensure O(K) complexity on client data retrieval.
