# Issues found in `digital_wallet.py`

Tools: Pylint (5.69/10 before, 10.00/10 after), Bandit (4 issues before, 0 after), Flake8 (4 issues before, 0 after).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak SHA-1 hash (B324) | Security (High) | 14 | `hashlib.sha1` is broken for security use and was used to hash the wallet PIN. | Switched to `hashlib.sha256`; PIN compared with `hmac.compare_digest`. |
| Insecure `tempfile.mktemp` (B306) | Security (Medium) | 60 | `mktemp` only returns a name, so another process can create that file first (race condition). | Used `tempfile.mkstemp`, which creates the file atomically; closed the descriptor. |
| Hardcoded secret (B105) | Security (Low) | 6 | Gateway secret `sk_demo_wallet_0000` was committed in source code. | Read from the `GATEWAY_SECRET` environment variable; `check_gateway` returns False if unset and uses `hmac.compare_digest`. |
| Weak random for OTP (B311) | Security (Low) | 64 | `random.randint` is predictable, not suitable for one-time passwords. | Used `secrets.randbelow(900000) + 100000` (still 6 digits). |
| Mutable default argument (W0102) | Bug | 17 | `log=[]` is created once and shared across every call to `addMoney`. | Default is `None`; a new list is created inside the function. |
| Global statement (W0603) | Design | 28 | `setDailyLimit` rebinds a module global. | Stored the limit in the `wallet` dict (`wallet["daily_limit"]`) and updated it directly. |
| Unused argument (W0613) | Code quality | 50 | `merchantType` is never used in `cashbackFor`. | Renamed to `_merchant_type` (documented as reserved); cashback rate moved to `CASHBACK_RATE`. |
| Naming (C0103) | Style | 9, 13, 17, 27, 32, 45, 50, 54, 58, 78 | camelCase functions/variables and a lowercase module constant break PEP 8. | Renamed to snake_case (`add_money`, `pay_merchant`, `credit_amounts`, ...); removed the global `daily_limit`. |
| Missing docstrings (C0114, C0116) | Documentation | 1, 13-63 | Module and all functions had no docstrings. | Added a module docstring and one for every function. |
| E261 | Style (Flake8) | 76 | Only one space before inline comment. | Two spaces before `#`. |
| E225 / E231 | Style (Flake8) | 78, 79 | Missing space around `=` and after `,`. | Added the spaces. |
| E305 | Style (Flake8) | 80 | `main()` called straight after a function with no blank lines. | Added two blank lines and wrapped the call in `if __name__ == "__main__":`. |

## Verification

- Program output is identical before and after (apart from the random OTP).
- Reports: `reports/before/` and `reports/after/`.
- Commits: one for Bandit fixes, one for Flake8 fixes, one for Pylint fixes.
