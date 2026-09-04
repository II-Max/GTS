## 2024-05-24 - Firebase RTDB O(N) Bandwidth Bottleneck
**Learning:** Querying a full node (like `public_leaderboard`) on the client side without limits downloads the entire dataset, creating an O(N) bandwidth bottleneck as the user base grows.
**Action:** Always use `.indexOn` in `database.rules.json` and query with `orderByChild().limitToLast(N)` to drastically reduce payload sizes. Iterate using `snap.forEach()` to maintain order, and handle tie-breakers on the client side.
## 2024-05-25 - Firebase Client-Side Order and Count Bottleneck
**Learning:** In `frontend/problems.html`, the client calculates the user rank by fetching the entire `public_leaderboard` node (`db.ref("public_leaderboard").once("value")`) and sorting it. This creates an O(N) bandwidth and memory bottleneck on the client, violating the learning in `.jules/bolt.md`.
**Action:** Do not download the entire leaderboard to find a rank. Since Firebase RTDB lacks count queries, we can fetch the user`s current score first, and then count how many users have a score greater than or equal to that score using `.orderByChild("score").startAt(myScore)`.
