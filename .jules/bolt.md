## 2024-05-24 - [Firebase RTDB Pagination Bottleneck]
**Learning:** Client-side sorting and limiting of Firebase Realtime Database nodes (like `public_leaderboard`) requires downloading the entire node. For leaderboards with potentially many users, this causes an O(N) bandwidth bottleneck.
**Action:** Always add `.indexOn` rules in `database.rules.json` and use `.orderByChild().limitToLast()` in the client to drastically reduce payload sizes and prevent full-node downloads.
