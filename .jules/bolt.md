## 2024-05-24 - Firebase RTDB O(N) Bandwidth Bottleneck
**Learning:** Querying a full node (like `public_leaderboard`) on the client side without limits downloads the entire dataset, creating an O(N) bandwidth bottleneck as the user base grows.
**Action:** Always use `.indexOn` in `database.rules.json` and query with `orderByChild().limitToLast(N)` to drastically reduce payload sizes. Iterate using `snap.forEach()` to maintain order, and handle tie-breakers on the client side.

## 2024-05-24 - Firebase RTDB Single User Rank Calculation
**Learning:** Calculating a single user's global rank in `problems.html` by downloading the full leaderboard (`public_leaderboard`) is an O(N) bandwidth trap.
**Action:** Always fetch the user's current score first, then query for users with equal or higher scores using `orderByChild('score').startAt(myScore)`. This drastically limits the payload payload. Use `snap.forEach()` locally to handle client-side tie-breakers securely and performantly.
