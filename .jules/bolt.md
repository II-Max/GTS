
## 2024-05-24 - Avoiding O(N) client-side Firebase downloads for Leaderboards
**Learning:** In Firebase Realtime Database, when a client fetches an entire node (like `public_leaderboard`) just to compute a rank or display the top users, the bandwidth scales linearly O(N) with the number of users, which becomes a major bottleneck as the userbase grows.
**Action:** Configure `.indexOn` in `database.rules.json` for the field being sorted. Then on the client side, strictly fetch only what is needed using queries like `.orderByChild('score').limitToLast(50)` for top lists, or `.startAt(queryScore)` to compute an individual's relative rank without downloading the whole node. Iterate using `snap.forEach()` to preserve the Firebase query order before any client-side tie-breaker sorting.
