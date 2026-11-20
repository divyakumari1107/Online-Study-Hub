import urllib.request
import urllib.error
import json
import time
import sys

BASE_URL = "http://localhost:3030"

def log_test(name, passed, details=""):
    symbol = "[PASS]" if passed else "[FAIL]"
    print(f"{symbol} {name}")
    if details:
        print(f"       -> {details}")

def test_nginx_ui():
    try:
        req = urllib.request.Request(f"{BASE_URL}/")
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode("utf-8")
            passed = resp.status == 200 and "StudyVerse" in content
            log_test("Nginx Static Glassmorphism UI (Port 3030)", passed, f"Status: {resp.status}, Title: StudyVerse detected")
            return passed
    except Exception as e:
        log_test("Nginx Static Glassmorphism UI (Port 3030)", False, str(e))
        return False

def test_health():
    try:
        req = urllib.request.Request(f"{BASE_URL}/health")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            passed = resp.status == 200 and data.get("status") == "HEALTHY"
            log_test("Core Backend Health Probe (/health)", passed, f"Status: {data.get('status')}, Active Rooms: {data.get('active_rooms')}")
            return passed
    except Exception as e:
        log_test("Core Backend Health Probe (/health)", False, str(e))
        return False

def test_study_rooms():
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/rooms")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            rooms = data.get("rooms", [])
            passed = resp.status == 200 and len(rooms) >= 2
            log_test("Multiplayer Study Rooms API (/api/rooms)", passed, f"Found {len(rooms)} active study rooms")
            return passed
    except Exception as e:
        log_test("Multiplayer Study Rooms API (/api/rooms)", False, str(e))
        return False

def test_synced_pomodoro():
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/rooms/room-tokyo-101/timer/control", method="POST")
        req.add_header("Content-Type", "application/json")
        payload = json.dumps({"action": "START"}).encode("utf-8")
        with urllib.request.urlopen(req, data=payload, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            timer = data.get("timer", {})
            passed = resp.status == 200 and timer.get("is_running") is True
            log_test("Synced Pomodoro Timer Engine", passed, f"Status: RUNNING, Remaining: {timer.get('remaining')}s, Mode: {timer.get('mode')}")
            return passed
    except Exception as e:
        log_test("Synced Pomodoro Timer Engine", False, str(e))
        return False

def test_sm2_spaced_repetition():
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/flashcards/fc-1/review", method="POST")
        req.add_header("Content-Type", "application/json")
        payload = json.dumps({"quality": 5}).encode("utf-8")
        with urllib.request.urlopen(req, data=payload, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            card = data.get("card", {})
            passed = resp.status == 200 and card.get("repetitions") > 0
            log_test("SuperMemo-2 (SM-2) Spaced Repetition Algorithm", passed, 
                     f"Ease Factor: {card.get('ease_factor')}, Next Interval: {card.get('interval_days')} days, Review: {card.get('next_review')}")
            return passed
    except Exception as e:
        log_test("SuperMemo-2 (SM-2) Spaced Repetition Algorithm", False, str(e))
        return False

def test_ai_generator():
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/ai/generate-flashcards", method="POST")
        req.add_header("Content-Type", "application/json")
        payload = json.dumps({"topic": "Kubernetes Orchestration"}).encode("utf-8")
        with urllib.request.urlopen(req, data=payload, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            count = data.get("generated_count", 0)
            passed = resp.status == 201 and count == 3
            log_test("Synapse AI Flashcard Generator Engine", passed, f"Generated {count} smart flashcards with answers")
            return passed
    except Exception as e:
        log_test("Synapse AI Flashcard Generator Engine", False, str(e))
        return False

def main():
    print("=" * 70)
    print("StudyVerse AI Virtual Study Metaverse - Automated Test Suite")
    print("Target Ingress: " + BASE_URL)
    print("=" * 70)

    tests = [
        test_nginx_ui,
        test_health,
        test_study_rooms,
        test_synced_pomodoro,
        test_sm2_spaced_repetition,
        test_ai_generator
    ]

    results = [t() for t in tests]
    passed_count = sum(results)
    total_count = len(results)

    print("=" * 70)
    print(f"Summary: {passed_count}/{total_count} tests passed ({passed_count/total_count*100:.1f}%)")
    print("=" * 70)

    if passed_count == total_count:
        print("[SUCCESS] All StudyVerse AI platform tests passed successfully!")
        sys.exit(0)
    else:
        print("[ERROR] Some tests failed. Please inspect container logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
