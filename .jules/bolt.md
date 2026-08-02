## 2024-08-02 - Fast Stats with Shallow Firebase Queries
**Learning:** Firebase Realtime Database reads nested data by default. In `/api/stats`, we were downloading the entire `problems`, `users`, and `submissions` datasets just to compute their lengths (`len(data)`).
**Action:** Use the `shallow=True` argument in `firebase_admin.db.Reference.get()` to only fetch the top-level keys. This drastically reduces bandwidth and latency for counting operations without sacrificing accuracy. Always check if only keys are needed before fetching full datasets from Firebase.
