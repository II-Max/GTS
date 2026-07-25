## 2024-05-24 - Firebase Realtime Database O(N) Query Bottleneck

**Learning:** When fetching rankings or leaderboards in Firebase Realtime Database, both the backend (`get_all_users()`) and frontend (`db.ref('public_leaderboard').once('value')`) were previously downloading the entire node and sorting the data in memory/client-side. This is a common O(N) anti-pattern in Firebase that wastes bandwidth and memory as the user base grows.
**Action:** Always add indexes (e.g. `".indexOn": ["score"]`) in `database.rules.json` and utilize indexed queries (`orderByChild('score').limitToLast(limit)`) to shift the sorting and limiting workload to the Firebase server, turning an O(N) operation into an O(1) payload size.
