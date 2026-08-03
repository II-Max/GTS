## 2024-05-14 - Firebase Shallow Reads for Counts
**Learning:** In Firebase Realtime Database, counting top-level nodes by fetching the entire path (e.g. `problems`, `users`) can download a massive payload of nested data, causing a performance bottleneck. The `firebase_admin` Python SDK supports a `shallow=True` argument that returns only the top-level keys.
**Action:** Use `db.reference(path).get(shallow=True)` whenever we only need to count items or fetch a list of keys, avoiding unnecessary download of nested child data.
