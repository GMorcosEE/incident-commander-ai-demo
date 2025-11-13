# Incident Commander AI - MTTR Reduction Demo

A demonstration repository showcasing AI-driven incident response and resolution using Ona (formerly Gitpod) workspaces. This repo contains a FastAPI checkout service with an intentional bug designed to simulate a production incident.

## 🎯 Purpose

This demo illustrates how an AI agent can:
1. Investigate application logs to identify errors
2. Determine the root cause of incidents
3. Propose and apply fixes
4. Run tests to verify the solution
5. Open pull requests with proper documentation
6. Generate Root Cause Analysis (RCA) reports

## 🏗️ Architecture

```
incident-commander-ai-demo/
├── app/
│   ├── main.py              # FastAPI application with intentional bug
│   ├── config.py            # Configuration settings
│   └── requirements.txt     # Python dependencies
├── logs/
│   └── app.log             # Generated at runtime
├── scripts/
│   └── simulate_incident.py # Script to trigger the bug
├── tests/
│   └── test_checkout.py    # Test suite
├── rca/
│   └── README.md           # RCA reports directory
├── .gitpod.yml             # Ona workspace configuration
└── README.md               # This file
```

## 🐛 The Bug

The application contains a **division by zero error** in the discount calculation logic:

- **Location**: `app/main.py`, function `calculate_discount()`
- **Trigger**: Using discount code `WELCOME10`
- **Cause**: Incorrect calculation `1 / (rate * 10 - 1)` where `rate = 0.10`, resulting in `1 / 0`
- **Impact**: 500 Internal Server Error, checkout process fails

## 🚀 Quick Start

### Option 1: Using Ona Workspace (Recommended)

1. Open this repository in Ona
2. Wait for automatic setup (dependencies install, API starts)
3. Run the incident simulation:
   ```bash
   python scripts/simulate_incident.py
   ```
4. Check logs:
   ```bash
   cat logs/app.log
   ```

### Option 2: Local Setup

```bash
# Install dependencies
pip install -r app/requirements.txt

# Start the API
cd app
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal, simulate the incident
python scripts/simulate_incident.py
```

## 🧪 Running Tests

```bash
# Run all tests
pytest -q

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_checkout.py::test_health_endpoint
```

**Note**: Tests will pass for working discount codes (SAVE20, FLASH50) but the WELCOME10 code will cause failures until the bug is fixed.

## 🤖 AI Agent Workflow

The AI agent should follow this 6-step process:

### 1. Analyze Logs
```bash
cat logs/app.log | grep -A 10 "CRITICAL ERROR"
```
Look for stack traces, error messages, and context around the failure.

### 2. Identify Root Cause
- Review the error: `ZeroDivisionError` in `calculate_discount()`
- Examine the code in `app/main.py` around line 70-75
- Identify the faulty calculation: `multiplier = 1 / (rate * 10 - 1)`

### 3. Propose Fix
Replace the buggy calculation with the correct discount logic:
```python
# Before (buggy):
if discount_code == 'WELCOME10':
    multiplier = 1 / (rate * 10 - 1)  # Division by zero!
    discount = subtotal * multiplier

# After (fixed):
discount = subtotal * rate
```

### 4. Apply Fix
Edit `app/main.py` to remove the special case for WELCOME10 and use the standard discount calculation.

### 5. Run Tests
```bash
pytest -q
```
Verify all tests pass, including checkouts with WELCOME10 code.

### 6. Open PR & Generate RCA
- Create a new branch: `git checkout -b fix/welcome10-discount-bug`
- Commit changes with descriptive message
- Push and open PR
- Generate RCA report in `rca/incident-YYYY-MM-DD.md`

## 📊 Expected Behavior

### Before Fix
```bash
$ python scripts/simulate_incident.py

TEST 2: Triggering WELCOME10 bug (INCIDENT)
Status Code: 500
❌ INCIDENT TRIGGERED: Server returned 500 error
```

### After Fix
```bash
$ python scripts/simulate_incident.py

TEST 2: Triggering WELCOME10 bug (INCIDENT)
Status Code: 200
✅ Checkout completed successfully
```

## 📝 RCA Template

When generating the RCA report, include:

```markdown
# Incident Report: WELCOME10 Discount Bug

**Date**: YYYY-MM-DD
**Severity**: High
**MTTR**: X minutes
**Status**: Resolved

## Summary
Division by zero error in discount calculation for WELCOME10 code.

## Root Cause
Incorrect mathematical formula in calculate_discount() function...

## Impact
- All checkouts with WELCOME10 code failed
- Estimated X failed transactions

## Resolution
Removed special case logic and applied standard discount calculation.

## Prevention
- Add unit tests for all discount codes
- Implement input validation
- Add monitoring alerts for 500 errors
```

## 🔧 Troubleshooting

**API won't start:**
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill the process if needed
kill -9 <PID>
```

**Tests failing:**
```bash
# Ensure you're in the repo root
cd /workspace/incident-commander-ai-demo
# Run tests with full output
pytest -v
```

**No logs generated:**
```bash
# Ensure logs directory exists
mkdir -p logs
# Check API is running
curl http://localhost:8000/health
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Ona Documentation](https://www.gitpod.io/docs)
- [Pytest Documentation](https://docs.pytest.org/)

## 🤝 Contributing

This is a demo repository. Feel free to:
- Add more test cases
- Introduce additional bugs for practice
- Improve the RCA template
- Enhance logging and monitoring

## 📄 License

MIT License - feel free to use this for training and demonstrations.
