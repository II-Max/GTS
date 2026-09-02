## 2024-05-24 - Firebase RTDB O(N) Bandwidth Bottleneck
**Learning:** Querying a full node (like `public_leaderboard`) on the client side without limits downloads the entire dataset, creating an O(N) bandwidth bottleneck as the user base grows.
**Action:** Always use `.indexOn` in `database.rules.json` and query with `orderByChild().limitToLast(N)` to drastically reduce payload sizes. Iterate using `snap.forEach()` to maintain order, and handle tie-breakers on the client side.
## 2026-09-02 - Uncached O(N) Database Reads in Stats API
**Learning:** The `/api/stats` endpoint retrieves the entire "problems", "users", and "submissions" nodes from Firebase Realtime Database (which does not support shallow counts natively). This causes an O(N) bandwidth bottleneck every time a user visits the homepage.
**Action:** Implement short-lived in-memory caching for aggregated global stats APIs to prevent massive redundant data transfers on frequently accessed public endpoints.
