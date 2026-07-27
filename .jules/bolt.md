## 2024-05-24 - Optimize Firebase Count Queries
**Learning:** Firebase Realtime Database `get()` pulls the entire nested JSON tree into memory and over the network, which is highly inefficient if we only need the top-level keys (e.g., to count the number of problems, users, or submissions).
**Action:** Use `get(shallow=True)` when fetching large lists just to count items, preventing unnecessary data transfer and memory usage.
