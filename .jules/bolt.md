## 2024-05-24 - Firebase RTDB O(N) Bandwidth Bottleneck
**Learning:** Querying a full node (like `public_leaderboard`) on the client side without limits downloads the entire dataset, creating an O(N) bandwidth bottleneck as the user base grows.
**Action:** Always use `.indexOn` in `database.rules.json` and query with `orderByChild().limitToLast(N)` to drastically reduce payload sizes. Iterate using `snap.forEach()` to maintain order, and handle tie-breakers on the client side.
## 2024-05-24 - Avoiding Client-Side O(N) Bandwidth for User Ranking
**Learning:** Querying the entire leaderboard on the client to find a single user's rank downloads the whole dataset, causing O(N) bandwidth explosion as the app scales.
**Action:** Always fetch the current user's score first, then query the dataset with `orderByChild('score').startAt(myScore)` to count higher-ranked users, resolving tie-breakers purely on the client side over a much smaller snapshot.
