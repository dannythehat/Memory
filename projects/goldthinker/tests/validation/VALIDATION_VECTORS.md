# Validation golden vectors (GVV-0.1)

For `VALIDATION_RULES.md` v0.3. Deterministic pure-function vectors (multiplicity procedures, block construction, signal-day assignment, stress denominators, p-value formula). The seeded resampling itself cannot be tested here; it is tested through given draws. Expected values were derived by hand and matched by a scratch script.

#### `GV-VAL-01`
> Holm at family-wise alpha 0.05, m = 5: sorted p 0.001, 0.011, 0.012, 0.03, 0.20 against 0.05/5, 0.05/4, 0.05/3, 0.05/2 = 0.01, 0.0125, 0.01667, 0.025: the first three pass, 0.03 fails and stops the procedure.

Input: `{"p": ["1/1000", "3/250", "11/1000", "1/5", "3/100"], "alpha": "0.05"}`

Expected: `{"rejected_indices": [0, 1, 2]}`

#### `GV-VAL-02`
> An untestable strategy carries p = 1 and stays in m: m = 4 (one p = 1). 0.004 <= 0.05/4 = 0.0125 passes; 0.02 > 0.05/3 = 0.01667 fails. Only one rejection.

Input: `{"p": ["1/250", "1/50", "9/10", "1"], "alpha": "0.05"}`

Expected: `{"rejected_indices": [0]}`

#### `GV-VAL-03`
> Holm at the interim alpha 0.01 and the final alpha 0.04 (m = 4, p = 0.002, 0.009, 0.03, 0.5). Interim: 0.002 <= 0.0025 passes, 0.009 > 0.01/3 fails. Final: 0.002 <= 0.01, 0.009 <= 0.0133, 0.03 > 0.02 stops.

Input: `{"p": ["0.002", "0.009", "0.03", "0.5"], "alpha_interim": "0.01", "alpha_final": "0.04"}`

Expected: `{"interim_rejected": [0], "final_rejected": [0, 1]}`

#### `GV-VAL-04`
> Benjamini-Yekutieli q = 0.10, m = 5: c(5) = 1 + 1/2 + 1/3 + 1/4 + 1/5 = 137/60, so the thresholds are i x 0.10 / (5 x 137/60) = i x 0.0087591 (0.00876, 0.01752, 0.02628, 0.03504, 0.0438). The largest i with p_(i) <= threshold is 4 (0.02 <= 0.03504); 0.5 fails. Four rejections.

Input: `{"p": ["1/1000", "1/125", "3/250", "1/50", "1/2"], "q": "0.10"}`

Expected: `{"c_m": "137/60", "rejected_indices": [0, 1, 2, 3]}`

#### `GV-VAL-05`
> BY is a step-up procedure: m = 4, c = 25/12, thresholds i x 0.10 / (4 x 25/12) = i x 0.03: 0.03, 0.06, 0.09, 0.12. Sorted p 0.01, 0.02, 0.5, 0.5: 0.02 <= 0.06 so i = 2 is the largest passing index; both of the two smallest are rejected.

Input: `{"p": ["1/50", "1/100", "1/2", "1/2"], "q": "0.10"}`

Expected: `{"c_m": "25/12", "rejected_indices": [0, 1]}`

#### `GV-VAL-06`
> Circular 5-day block bootstrap. Day series of N = 12 days (indices 0-11); block starts 10, 3, 7 give blocks [10,11,0,1,2], [3,4,5,6,7], [7,8,9,10,11]; concatenated they hold 15 days and are truncated to exactly 12: 10,11,0,1,2,3,4,5,6,7,7,8.

Input: `{"N_days": 12, "block_length": 5, "starts": [10, 3, 7]}`

Expected: `{"days": [10, 11, 0, 1, 2, 3, 4, 5, 6, 7, 7, 8]}`

#### `GV-VAL-07`
> Days are SIGNAL days on the server clock (UTC+1, day starts 23:00 UTC), not close days. Signals at 22:30Z 5 Oct and 23:00Z 5 Oct are on server days 5 Oct and 6 Oct; 22:59:59Z 6 Oct is still 6 Oct. Trade c closes on 9 Oct but belongs to 6 Oct; e closes on 12 Oct but belongs to 8 Oct. The 7-day window 5-11 Oct keeps zero-trade days. Expectancy = 2/5 = 0.4. The best single signal day is 5 Oct (+2R, one trade); removing it leaves (1 - 1)/4 = 0.

Input: `{"window_start": "2026-10-05", "window_days": 7, "trades": [{"id": "a", "signal_time": "2026-10-05T22:30:00Z", "close_time": "2026-10-07T10:00:00Z", "R": "2"}, {"id": "b", "signal_time": "2026-10-05T23:00:00Z", "close_time": "2026-10-05T23:30:00Z", "R": "-1"}, {"id": "c", "signal_time": "2026-10-06T10:00:00Z", "close_time": "2026-10-09T10:00:00Z", "R": "3"}, {"id": "d", "signal_time": "2026-10-06T22:59:59Z", "close_time": "2026-10-06T23:30:00Z", "R": "-1"}, {"id": "e", "signal_time": "2026-10-08T12:00:00Z", "close_time": "2026-10-12T12:00:00Z", "R": "-1"}]}`

Expected: `{"day_series": [["2026-10-05", "2", 1], ["2026-10-06", "1", 3], ["2026-10-07", "0", 0], ["2026-10-08", "-1", 1], ["2026-10-09", "0", 0], ["2026-10-10", "0", 0], ["2026-10-11", "0", 0]], "expectancy": "0.4", "best_day": "2026-10-05", "expectancy_without_best_day": "0"}`

#### `GV-VAL-08`
> Stress replay keeps unexecutable signals in the denominator at 0R. Ten trades, stressed R 1.5, -1, (unexecutable), 2, -1, (unexecutable), -1, 1.5, -1, -1: the sum is 0.0 over 10 trades (not over 8), so the stressed expectancy is 0; two of ten = 20% are unexecutable, above the 5% cap, so V5 FAILS although the expectancy is not negative.

Input: `{"stressed_R": ["1.5", "-1", null, "2", "-1", null, "-1", "1.5", "-1", "-1"], "cap": "0.05"}`

Expected: `{"stressed_expectancy": "0", "stress_unexecutable_count": 2, "unexecutable_share": "0.2", "V5_pass": false}`

#### `GV-VAL-09`
> 5% cap boundary: 20 trades, one unexecutable (exactly 5%) -> allowed; stressed R of the other 19 is +1.5 each, so the stressed expectancy is 28.5/20 = 1.425 (the excluded trade counts as 0R, not removed).

Input: `{"stressed_R": ["1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", "1.5", null], "cap": "0.05"}`

Expected: `{"stressed_expectancy": "1.425", "stress_unexecutable_count": 1, "unexecutable_share": "1/20", "V5_pass": true}`

#### `GV-VAL-10`
> Bootstrap p-value formula p = (1 + #{E* >= E_hat}) / (B + 1) on given centred replicates: E_hat = 0.05, B = 9 replicates [-0.4, -0.1, 0.0, 0.05, 0.2, 0.3, 0.05, 0.5, -0.2]; those >= 0.05 are 0.05, 0.2, 0.3, 0.05, 0.5 = 5, so p = 6/10 = 0.6. Two bootstraps: the verdict p is the larger of the 1-day p and the 5-day p.

Input: `{"E_hat": "0.05", "replicates": ["-2/5", "-1/10", "0", "1/20", "1/5", "3/10", "1/20", "1/2", "-1/5"], "p_1day_alt": "0.03", "p_5day_alt": "0.06"}`

Expected: `{"p": "0.6", "verdict_p_for_alts": "0.06"}`
