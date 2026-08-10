## 2024-05-19 - Firebase Leaderboard Pagination

**Learning:** In Firebase Realtime Database, a common anti-pattern is doing full-node downloads on the client side (e.g. `db.ref('public_leaderboard').once('value')`) for data like leaderboards and then slicing the array locally (`rankArray.slice(0, 50)`). This is a hidden O(N) bandwidth bottleneck that scales linearly as the user base grows, negatively affecting both client load times and server bandwidth.
**Action:** When querying ranked data from Firebase RTDB on the client-side, set `.indexOn` in `database.rules.json` and combine `orderByChild` with `limitToLast` (or `startAt`/`endAt`) to download a fixed payload (e.g., `db.ref('...').orderByChild('score').limitToLast(50)`).
