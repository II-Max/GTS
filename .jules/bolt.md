## 2023-10-27 - Shallow reads for counting top-level keys
**Learning:** Firebase Realtime Database natively supports `shallow=True` via `firebase_admin.db.Reference.get(shallow=True)`. Previously, fetching `problems`, `users`, and `submissions` to count their length was downloading the entire nested data, creating a significant network and memory bottleneck as data grows.
**Action:** Always check if we only need top-level keys (e.g. for `len()`). If so, use `shallow=True` to fetch only the keys without downloading child nodes.
