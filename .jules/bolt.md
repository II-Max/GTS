## 2026-08-17 - Iterating over Firebase RTDB snapshot results
**Learning:** When iterating over Firebase RTDB snapshot results ordered via `orderByChild`, you must use `snap.forEach()` instead of retrieving raw values (e.g., via `Object.entries(snap.val())`) because standard JavaScript objects do not guarantee order preservation.
**Action:** Always use `snap.forEach()` when iterating over ordered Firebase query results on the client-side.
