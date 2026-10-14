# Reflection

**1. Which issues were the easiest and which the hardest to fix?**
The Flake8 issues and the Pylint naming and docstring warnings were easiest because they are mechanical (add a space, rename, write a line). The hardest were the security ones, mainly the hardcoded secret. Removing the string is easy, but the code then has to cope with the secret being missing: an empty secret must never make `check_gateway("")` return True. Removing the `global` also needed a small redesign, since the limit had to live somewhere else.

**2. Did the tools report any false positives?**
Mostly no, but some findings need judgement. Bandit flagged the demo gateway secret as a hardcoded password (it was a placeholder, but the pattern is still bad practice). It also flagged `random` for the OTP; for a game this is fine, but for an OTP it is a real weakness. The Pylint unused-argument warning was also a design choice: the parameter was meant for later, so I kept it with a leading underscore instead of deleting it.

**3. How would you integrate static analysis into a real workflow?**
Run Flake8 and Pylint in a pre-commit hook so style problems never reach the repo, and run all three tools in CI (for example GitHub Actions) on every pull request, failing the build on Bandit High/Medium findings or a Pylint score below a threshold. Keep the reports as build artifacts, and use `# nosec` or disable comments only with a written reason.

**4. What tangible improvements did you see after the fixes?**
Pylint went from 5.69 to 10.00, and Bandit and Flake8 went from 4 issues each to 0. The code is more secure (SHA-256 with constant-time compare, no hardcoded secret, atomic temp files, cryptographically secure OTP), fixes a real bug (the shared `log` list), reads consistently in PEP 8 style, and every function is documented. Behaviour stays the same, and importing the file no longer runs the demo.
