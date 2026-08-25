## 2024-05-24 - O(N) Bandwidth bottleneck in leaderboard
**Learning:** Fetching an entire Firebase node (e.g., `public_leaderboard`) just to display the top N users causes an O(N) download payload, which degrades client performance and increases bandwidth as the user base grows.
**Action:** Always add an `.indexOn` rule for the sort key and use `orderByChild().limitToLast(N)` when fetching leaderboards. Additionally, use `snap.forEach()` to iterate over results to preserve Firebase's ordering before applying any secondary sorting client-side.
