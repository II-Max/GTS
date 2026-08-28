
## 2024-XX-XX - [Optimize Leaderboard Query]
**Learning:** Firebase RTDB clients download the entire JSON tree at a path if you don't use query parameters (like orderByChild + limitToLast). Downloading the entire 'public_leaderboard' node is O(N) where N is number of users, which becomes a major bottleneck as the userbase grows. Also, Realtime Database indices need to be defined in rules.
**Action:** Adding an index on '.indexOn': ['score'] in database.rules.json for public_leaderboard and modifying the frontend code in rank.html to use orderByChild('score') and limitToLast(50) prevents full download of the entire leaderboard data. Then, iterating using forEach preserves the sorting.
