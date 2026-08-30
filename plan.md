1. **Add Firebase Database Index for Performance:**
   - In `database.rules.json`, add `.indexOn: ["score"]` to the `public_leaderboard` node. This allows the Realtime Database to efficiently filter and sort by the `score` field, saving server processing time and avoiding unindexed query warnings.

2. **Optimize `rank.html` Data Fetching:**
   - In `frontend/rank.html`, change the query `db.ref('public_leaderboard').once('value')` to `db.ref('public_leaderboard').orderByChild('score').limitToLast(50).once('value')`.
   - This ensures we only download the top 50 users based on their scores, preventing an O(N) data download where N is the total number of users in the system. The payload will be drastically reduced.
   - Refactor the mapping and sorting to use `.forEach()` on the snapshot (to preserve the Firebase sort order, and then reverse it since `limitToLast` returns ascending order) instead of `Object.entries(snap.val())` and `.sort()`.

3. **Verify Functionality & Performance:**
   - Use `frontend_verification_instructions` to ensure visual parity of the `rank.html` page.
   - Use Playwright/python local server to confirm the top 50 items load properly and the UI retains identical functionality and highlight styling (top 1-3).
   - Ensure the `.jules/bolt.md` journal has a critical learning about this indexing/querying bottleneck.

4. **Complete pre-commit steps:**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

5. **Submit the Pull Request:**
   - Create PR with title "⚡ Bolt: [performance improvement]".
   - Document the *What*, *Why*, *Impact*, and *Measurement* in the description as per instructions.
