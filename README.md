# Problems in Entity Authentication

An educational Python demonstration for the Information and Network Security mini project.

## Features
- Dummy username and password verification
- Password hashing with PBKDF2-HMAC-SHA256
- Three-attempt limit in the interactive login
- One-time sample OTP with reuse prevention during one program run
- Fresh nonce and HMAC challenge-response demonstration
- Sample test scenarios

## Requirements
- Python 3.8 or later
- No third-party packages are required

## Run the program
Open a terminal in this folder and run:

```bash
python main.py
```

On some Windows systems, use:

```bash
py main.py
```

## Demo credentials
- Username: `jyothi`
- Password: `Demo@123`
- OTP: `123456`

The OTP can be used once per program run. Restart the program to reset the in-memory demonstration state.

## Menu
1. Run login demonstration
2. Run sample test scenarios
3. Exit

## Project team
- H K Jyothi
- Chan Dana R
- Bindu V Gowda
- Amrutha G

Don Bosco Institute of Technology, Department of Information Science and Engineering  
Academic Year: 2026-27

## Important limitations
This is a classroom demonstration only, not a production authentication service. The OTP is a fixed sample value, the challenge-response uses a shared HMAC demo secret, state is stored only in memory, and there is no database, TLS server, real MFA provider, or asymmetric digital signature. Do not use real passwords or personal information.
