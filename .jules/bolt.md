## 2024-05-18 - [Firebase RTDB Leaderboard Optimization]
**Learning:** [Querying Firebase RTDB for ranked data (like leaderboards) without using `.indexOn` and `.orderByChild` combined with `limitToLast` or `startAt` results in full-node downloads. This causes O(N) bandwidth bottlenecks and performance degradation as the user base grows.]
**Action:** [Set `.indexOn` in `database.rules.json` and use query constraints (`limitToLast`, `startAt`, etc.) to drastically reduce payload sizes for leaderboard queries.]
