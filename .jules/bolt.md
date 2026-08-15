## 2024-05-19 - Firebase Leaderboard Query Optimization
**Learning:** Querying a large node like `public_leaderboard` entirely on the client side using `.once('value')` causes an O(N) payload size download. For ranked data, this is a significant bandwidth and performance bottleneck.
**Action:** Always set `.indexOn` in `database.rules.json` for fields used in ordering (e.g., `score`), and use `orderByChild('field').limitToLast(N)` on the client side to restrict the downloaded payload to only the necessary nodes.
