"""
Problems in Entity Authentication - Educational Demonstration
Run: python main.py

This program uses dummy credentials and simplified demonstrations for learning.
It is NOT a production authentication system.
"""

import hashlib
import hmac
import secrets
import time

# Demo-only account. Never hard-code real user credentials in an application.
DEMO_USERNAME = "jyothi"
DEMO_PASSWORD = "Demo@123"
DEMO_OTP = "123456"

# Password hash is generated from a random salt when this demo starts.
_PASSWORD_SALT = secrets.token_bytes(16)
_PASSWORD_HASH = hashlib.pbkdf2_hmac(
    "sha256", DEMO_PASSWORD.encode("utf-8"), _PASSWORD_SALT, 200_000
)

# Demonstration secret for HMAC challenge-response.
# In a real system, secrets/keys must be securely provisioned and stored.
_DEMO_SHARED_SECRET = b"entity-authentication-demo-secret"

MAX_ATTEMPTS = 3
used_nonces = set()
used_otps = set()


def verify_password(username: str, password: str) -> bool:
    """Verify the username and password against the demo credential record."""
    if username != DEMO_USERNAME:
        return False

    candidate_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), _PASSWORD_SALT, 200_000
    )
    return hmac.compare_digest(candidate_hash, _PASSWORD_HASH)


def verify_otp(otp: str) -> bool:
    """Verify the sample OTP and prevent reuse during this program run."""
    if otp != DEMO_OTP or otp in used_otps:
        return False
    used_otps.add(otp)
    return True


def challenge_response_demo() -> bool:
    """Create a fresh nonce and verify an HMAC response for that nonce."""
    nonce = secrets.token_hex(16)
    message = f"login:{DEMO_USERNAME}:{nonce}".encode("utf-8")

    # Claimant creates a response using the demo shared secret.
    response = hmac.new(
        _DEMO_SHARED_SECRET, message, hashlib.sha256
    ).hexdigest()

    # Verifier independently calculates and compares the expected response.
    expected = hmac.new(
        _DEMO_SHARED_SECRET, message, hashlib.sha256
    ).hexdigest()

    if nonce in used_nonces:
        return False

    valid = hmac.compare_digest(response, expected)
    if valid:
        used_nonces.add(nonce)
    return valid


def login_demo() -> None:
    """Run the login workflow with a three-attempt limit and two factors."""
    print("\n--- Entity Authentication Login Demo ---")
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        username = input("Enter demo username (jyothi): ").strip()
        password = input("Enter demo password (Demo@123): ")

        if verify_password(username, password):
            print("First-factor verification: PASS")
            break

        attempts += 1
        print("Authentication failed.")
        print(f"Attempts remaining: {MAX_ATTEMPTS - attempts}")

    if attempts >= MAX_ATTEMPTS:
        print("Access BLOCKED: maximum failed attempts reached.")
        return

    otp = input("Enter demo OTP (123456): ").strip()
    if not verify_otp(otp):
        print("Second-factor verification: FAIL. Access denied.")
        return

    print("Second-factor verification: PASS")

    if challenge_response_demo():
        print("Challenge-response verification: PASS")
        print("RESULT: Authentication successful. Demo session established.")
    else:
        print("Challenge-response verification: FAIL. Access denied.")


def run_test_scenarios() -> None:
    """Show basic repeatable checks without asking for interactive input."""
    print("\n--- Sample Demonstration Results ---")
    print("TC01 Valid demo password:", "PASS" if verify_password("jyothi", "Demo@123") else "FAIL")
    print("TC02 Incorrect password:", "PASS" if not verify_password("jyothi", "wrong") else "FAIL")
    print("TC03 Unknown account:", "PASS" if not verify_password("unknown", "Demo@123") else "FAIL")

    otp_ok = verify_otp(DEMO_OTP)
    otp_reuse_rejected = not verify_otp(DEMO_OTP)
    print("TC04 Valid OTP (first use):", "PASS" if otp_ok else "FAIL")
    print("TC05 Reused OTP rejected:", "PASS" if otp_reuse_rejected else "FAIL")

    challenge_ok = challenge_response_demo()
    print("TC06 Fresh challenge-response:", "PASS" if challenge_ok else "FAIL")


def main() -> None:
    while True:
        print("\n========================================")
        print(" PROBLEMS IN ENTITY AUTHENTICATION")
        print("========================================")
        print("1. Run login demonstration")
        print("2. Run sample test scenarios")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            login_demo()
        elif choice == "2":
            run_test_scenarios()
        elif choice == "3":
            print("Exiting demonstration.")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
