"""Digital wallet and payment tracker demo.

Sends a one-time password, tops up the balance, pays merchants after a PIN
check and a daily limit, prints a mini statement, works out cashback and
verifies a payment-gateway key.
"""
import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

# Secrets come from the environment, not from source code.
GATEWAY_SECRET = os.environ.get("GATEWAY_SECRET", "")
# "4321" is only a fallback so the demo runs without setup.
WALLET_PIN = os.environ.get("WALLET_PIN", "4321")
CASHBACK_RATE = 0.02
wallet = {"balance": 0.0, "daily_limit": 1000}
transactions = []


def hash_pin(pin):
    """Return the SHA-256 hex digest of a PIN."""
    return hashlib.sha256(pin.encode()).hexdigest()


def add_money(amount, source="UPI", log=None):
    """Credit the wallet; return False if the amount is not positive."""
    if amount <= 0:
        return False
    if log is None:
        log = []
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set the maximum amount allowed for a single payment."""
    wallet["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Pay a merchant after checking the PIN, balance and daily limit."""
    if not hmac.compare_digest(hash_pin(pin), hash_pin(WALLET_PIN)):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > wallet["daily_limit"]:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def mini_statement(count=3):
    """Print the most recent transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, _merchant_type):
    """Return cashback for a payment (flat rate; type reserved for later)."""
    return round(amount * CASHBACK_RATE, 2)


def check_gateway(secret):
    """Return True if the given key matches the gateway secret."""
    if not GATEWAY_SECRET:
        return False
    return hmac.compare_digest(secret.encode(), GATEWAY_SECRET.encode())


def receipt_path():
    """Create a unique temporary receipt file and return its path."""
    file_descriptor, path = tempfile.mkstemp(suffix=".pdf")
    os.close(file_descriptor)
    return path


def main():
    """Run a short demonstration of the wallet."""
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [
        t["amount"] for t in transactions if t["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
