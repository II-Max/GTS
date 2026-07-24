## 2024-05-24 - Database Egress in Stats Endpoint
**Learning:** Found a Firebase architecture bottleneck in `/api/stats`. Fetching length of Firebase tables downloads entire database nodes, consuming large amounts of bandwidth and memory for large nodes.
**Action:** Always implement a caching mechanism when retrieving statistical aggregation from large data nodes, especially if Firebase Realtime Database is used, since it doesn't natively support querying table lengths efficiently.
