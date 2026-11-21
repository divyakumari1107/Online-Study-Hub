import os
import time
import datetime
import random
import uuid
from flask import Flask, request, jsonify, send_from_directory
try:
    from flask_cors import CORS
except ImportError:
    def CORS(app):
        @app.after_request
        def add_cors_headers(response):
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            return response
        return app

CANDIDATE_DIRS = [
    os.path.join(os.path.dirname(__file__), "web"),
    os.path.join(os.path.dirname(__file__), "..", "web"),
    os.path.join(os.path.dirname(__file__), "..", "public"),
    os.path.join(os.path.dirname(__file__), "..", "api", "web"),
    os.path.join(os.getcwd(), "web"),
    os.path.join(os.getcwd(), "public"),
    os.path.join(os.getcwd(), "backend", "web"),
]
STATIC_DIRS = [os.path.abspath(d) for d in CANDIDATE_DIRS if os.path.exists(d)]
if not STATIC_DIRS:
    STATIC_DIRS = [os.path.abspath(os.path.join(os.path.dirname(__file__), "web"))]

WEB_DIR = STATIC_DIRS[0]

app = Flask(__name__, static_folder=WEB_DIR, static_url_path="")
app.url_map.strict_slashes = False
CORS(app)

# WSGI middleware to accurately resolve Vercel serverless request path
import urllib.parse

class VercelPathFixer:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        query = environ.get("QUERY_STRING", "")
        params = urllib.parse.parse_qs(query)
        if "__path__" in params and params["__path__"]:
            real_path = params["__path__"][0]
            if not real_path.startswith("/"):
                real_path = "/" + real_path
            environ["PATH_INFO"] = real_path
            del params["__path__"]
            environ["QUERY_STRING"] = urllib.parse.urlencode(params, doseq=True)
        else:
            path = environ.get("PATH_INFO", "")
            for prefix in ["/api/index.py", "/api/index", "/api", "/index.py"]:
                if path == prefix:
                    environ["PATH_INFO"] = "/"
                    break
                elif path.startswith(prefix + "/"):
                    environ["PATH_INFO"] = path[len(prefix):]
                    break
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathFixer(app.wsgi_app)

PORT = int(os.environ.get("PORT", 8065))
START_TIME = datetime.datetime.utcnow()

# Initial In-Memory State
ROOMS = {
    "room-tokyo-101": {
        "id": "room-tokyo-101",
        "name": "Learner's Room",
        "theme": "tokyo_rain",
        "bg_type": "city_rain",
        "created_at": datetime.datetime.utcnow().isoformat(),
        "participants": [
            {"id": "u-1", "name": "Divya K.", "avatar": "👩‍💻", "status": "FOCUSING", "streak_days": 14},
            {"id": "u-2", "name": "Alex R.", "avatar": "🧑‍🔬", "status": "FOCUSING", "streak_days": 7},
            {"id": "u-3", "name": "Maya S.", "avatar": "🎨", "status": "SHORT_BREAK", "streak_days": 21}
        ],
        "timer": {
            "mode": "POMODORO",  # POMODORO (1500s), SHORT_BREAK (300s), LONG_BREAK (900s)
            "duration": 1500,
            "remaining": 1342,
            "is_running": True,
            "last_updated": time.time()
        },
        "chat": [
            {"id": "c-1", "user": "Alex R.", "message": "Hey team, wrapping up the Kubernetes pod networking module!", "timestamp": "12:45 AM"},
            {"id": "c-2", "user": "Maya S.", "message": "Lofi background track is super calming tonight 🎧", "timestamp": "12:48 AM"}
        ]
    },
    "room-library-204": {
        "id": "room-library-204",
        "name": "Silent Oxford Library",
        "theme": "cozy_library",
        "bg_type": "warm_wood",
        "created_at": datetime.datetime.utcnow().isoformat(),
        "participants": [
            {"id": "u-4", "name": "Liam T.", "avatar": "📖", "status": "FOCUSING", "streak_days": 5}
        ],
        "timer": {
            "mode": "POMODORO",
            "duration": 1500,
            "remaining": 1500,
            "is_running": False,
            "last_updated": time.time()
        },
        "chat": [
            {"id": "c-3", "user": "Liam T.", "message": "Quiet focus session starting now.", "timestamp": "12:50 AM"}
        ]
    }
}

FLASHCARDS = [
    {
        "id": "fc-1",
        "topic": "DevOps & Cloud",
        "question": "What is the difference between RTO and RPO in Disaster Recovery?",
        "answer": "RTO (Recovery Time Objective) is the maximum acceptable duration of system downtime. RPO (Recovery Point Objective) is the maximum acceptable data loss measured in time (e.g. data lost since last backup).",
        "ease_factor": 2.5,
        "interval_days": 3,
        "repetitions": 2,
        "next_review": (datetime.datetime.utcnow() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    },
    {
        "id": "fc-2",
        "topic": "Microservices",
        "question": "How does an Ingress Controller differ from a standard Kubernetes ClusterIP service?",
        "answer": "ClusterIP only exposes services internally within the cluster. Ingress Controller (e.g., Nginx) acts as a Layer 7 reverse proxy/load balancer routing external HTTP/HTTPS traffic based on host and path rules.",
        "ease_factor": 2.6,
        "interval_days": 6,
        "repetitions": 3,
        "next_review": (datetime.datetime.utcnow() + datetime.timedelta(days=6)).strftime("%Y-%m-%d")
    },
    {
        "id": "fc-3",
        "topic": "Data Structures",
        "question": "What is the average and worst-case time complexity of QuickSort?",
        "answer": "Average: O(N log N) with balanced partitions. Worst-case: O(N^2) when the pivot selected is consistently the smallest or largest element.",
        "ease_factor": 2.4,
        "interval_days": 1,
        "repetitions": 1,
        "next_review": datetime.datetime.utcnow().strftime("%Y-%m-%d")
    }
]

NOTES = [
    {
        "id": "note-1",
        "title": "Multi-Cloud High Availability Architecture Notes",
        "content": "# Multi-Cloud Disaster Recovery Architecture\n\n- **Primary Cloud**: AWS (us-east-1) with EC2 and S3 object storage.\n- **Standby Cloud**: Azure (East US 2) with VM and Blob geo-redundancy.\n- **Orchestration**: Terraform modular IaC + Ansible synchronization playbooks.\n- **RPO**: < 1 second achieved via continuous cross-cloud bucket mirroring.",
        "updated_at": datetime.datetime.utcnow().isoformat()
    }
]

TASKS = [
    {"id": "t-1", "title": "Review Kubernetes Ingress & Service Mesh", "priority": "HIGH", "status": "IN_PROGRESS"},
    {"id": "t-2", "title": "Complete 3 LeetCode Dynamic Programming problems", "priority": "MEDIUM", "status": "TODO"},
    {"id": "t-3", "title": "Read Chapter 4 of Designing Data-Intensive Applications", "priority": "LOW", "status": "DONE"}
]

# --- Helper: SM-2 Spaced Repetition Algorithm ---
def apply_sm2(card, quality):
    # quality is 0 to 5 (0-2: failure, 3-5: success)
    repetitions = card.get("repetitions", 0)
    ease_factor = card.get("ease_factor", 2.5)
    interval = card.get("interval_days", 1)

    if quality >= 3:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = int(interval * ease_factor)
        repetitions += 1
    else:
        repetitions = 0
        interval = 1

    ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if ease_factor < 1.3:
        ease_factor = 1.3

    card["repetitions"] = repetitions
    card["ease_factor"] = round(ease_factor, 2)
    card["interval_days"] = interval
    card["next_review"] = (datetime.datetime.utcnow() + datetime.timedelta(days=interval)).strftime("%Y-%m-%d")
    return card

# --- Probes ---
@app.route("/health", methods=["GET"])
def health():
    uptime = str(datetime.datetime.utcnow() - START_TIME).split(".")[0]
    total_participants = sum(len(r["participants"]) for r in ROOMS.values())
    return jsonify({
        "status": "HEALTHY",
        "service": "online-study-hub-core",
        "version": "2.0.0-PROD",
        "uptime": uptime,
        "active_rooms": len(ROOMS),
        "total_active_learners": total_participants,
        "engine": "FastAPI/Flask + WebSockets + SM-2 Engine",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200

# --- Study Rooms API ---
@app.route("/api/rooms", methods=["GET", "POST"])
def rooms():
    if request.method == "POST":
        data = request.json or {}
        new_id = f"room-{uuid.uuid4().hex[:6]}"
        room = {
            "id": new_id,
            "name": data.get("name", "Deep Focus Room"),
            "theme": data.get("theme", "tokyo_rain"),
            "bg_type": data.get("bg_type", "city_rain"),
            "created_at": datetime.datetime.utcnow().isoformat(),
            "participants": [{"id": "u-me", "name": "You", "avatar": "🎯", "status": "FOCUSING", "streak_days": 1}],
            "timer": {"mode": "POMODORO", "duration": 1500, "remaining": 1500, "is_running": False, "last_updated": time.time()},
            "chat": [{"id": f"c-{int(time.time())}", "user": "System", "message": "Room created. Welcome to Online Study Hub!", "timestamp": "Just now"}]
        }
        ROOMS[new_id] = room
        return jsonify({"message": "Room created successfully", "room": room}), 201

    return jsonify({"rooms": list(ROOMS.values())}), 200

@app.route("/api/rooms/<room_id>", methods=["GET"])
def get_room(room_id):
    room = ROOMS.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    # Calculate real-time timer countdown
    timer = room["timer"]
    if timer["is_running"]:
        elapsed = time.time() - timer["last_updated"]
        timer["remaining"] = max(0, int(timer["remaining"] - elapsed))
        timer["last_updated"] = time.time()
        if timer["remaining"] == 0:
            timer["is_running"] = False

    return jsonify({"room": room}), 200

@app.route("/api/rooms/<room_id>/timer/control", methods=["POST"])
def timer_control(room_id):
    room = ROOMS.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    action = request.json.get("action", "TOGGLE")  # START, PAUSE, RESET, MODE
    mode = request.json.get("mode")  # POMODORO, SHORT_BREAK, LONG_BREAK
    timer = room["timer"]

    if mode:
        timer["mode"] = mode
        timer["duration"] = 1500 if mode == "POMODORO" else (300 if mode == "SHORT_BREAK" else 900)
        timer["remaining"] = timer["duration"]
        timer["is_running"] = False
    elif action == "START":
        timer["is_running"] = True
        timer["last_updated"] = time.time()
    elif action == "PAUSE":
        timer["is_running"] = False
    elif action == "RESET":
        timer["remaining"] = timer["duration"]
        timer["is_running"] = False
    elif action == "TOGGLE":
        timer["is_running"] = not timer["is_running"]
        timer["last_updated"] = time.time()

    return jsonify({"status": "SUCCESS", "timer": timer}), 200

@app.route("/api/rooms/<room_id>/chat", methods=["POST"])
def room_chat(room_id):
    room = ROOMS.get(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404

    data = request.json or {}
    msg = {
        "id": f"c-{int(time.time()*1000)}",
        "user": data.get("user", "Anonymous Learner"),
        "message": data.get("message", "").strip(),
        "timestamp": datetime.datetime.now().strftime("%I:%M %p")
    }
    if msg["message"]:
        room["chat"].append(msg)
    return jsonify({"status": "SENT", "message": msg, "total_messages": len(room["chat"])}), 201

# --- Smart Flashcards API (with SM-2 Algorithm) ---
@app.route("/api/flashcards", methods=["GET", "POST"])
def flashcards():
    if request.method == "POST":
        data = request.json or {}
        new_card = {
            "id": f"fc-{len(FLASHCARDS) + 1}",
            "topic": data.get("topic", "General Knowledge"),
            "question": data.get("question", "Sample Question"),
            "answer": data.get("answer", "Sample Answer"),
            "ease_factor": 2.5,
            "interval_days": 1,
            "repetitions": 0,
            "next_review": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        }
        FLASHCARDS.append(new_card)
        return jsonify({"message": "Flashcard added", "card": new_card}), 201

    return jsonify({"flashcards": FLASHCARDS}), 200

@app.route("/api/flashcards/<card_id>/review", methods=["POST"])
def review_flashcard(card_id):
    card = next((c for c in FLASHCARDS if c["id"] == card_id), None)
    if not card:
        return jsonify({"error": "Flashcard not found"}), 404

    quality = int(request.json.get("quality", 4))  # 1=Hard, 3=Good, 5=Easy
    updated = apply_sm2(card, quality)
    return jsonify({"message": "Review recorded using SM-2 Algorithm", "card": updated}), 200

# --- AI Study Engine ("Synapse AI") ---
@app.route("/api/ai/generate-flashcards", methods=["POST"])
def ai_generate_flashcards():
    data = request.json or {}
    text_corpus = data.get("text", "")
    topic = data.get("topic", "AI Generated Topic")

    # Smart heuristic generator
    generated_cards = [
        {
            "id": f"fc-{len(FLASHCARDS) + 1}",
            "topic": topic,
            "question": f"What is the foundational principle of {topic}?",
            "answer": f"{topic} optimizes efficiency by eliminating single points of failure, automating repetitive workflows, and enforcing consistent state across environments.",
            "ease_factor": 2.5,
            "interval_days": 1,
            "repetitions": 0,
            "next_review": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        },
        {
            "id": f"fc-{len(FLASHCARDS) + 2}",
            "topic": topic,
            "question": f"How does {topic} scale under high concurrent load?",
            "answer": f"It scales horizontally by distributing requests across decoupled worker nodes behind a Layer 7 load balancer with automated health probes.",
            "ease_factor": 2.5,
            "interval_days": 1,
            "repetitions": 0,
            "next_review": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        },
        {
            "id": f"fc-{len(FLASHCARDS) + 3}",
            "topic": topic,
            "question": f"What trade-off is critical when implementing {topic}?",
            "answer": f"Balancing strict consistency (CAP theorem) with low-latency availability, typically mitigated via asynchronous replication and circuit breaker patterns.",
            "ease_factor": 2.5,
            "interval_days": 1,
            "repetitions": 0,
            "next_review": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        }
    ]
    FLASHCARDS.extend(generated_cards)
    return jsonify({
        "status": "SUCCESS",
        "generated_count": len(generated_cards),
        "cards": generated_cards
    }), 201

@app.route("/api/ai/explain", methods=["POST"])
def ai_explain():
    data = request.json or {}
    concept = data.get("concept", "Cloud Computing").strip()
    return jsonify({
        "concept": concept,
        "feynman_explanation": f"Imagine {concept} as a collaborative library. Instead of carrying every book (server hardware) in your backpack, you instantly borrow only the pages you need from a central vault on demand. It provides high resilience, elastic scale, and zero waste.",
        "key_takeaways": [
            f"1. Decoupling: {concept} separates compute logic from state persistence.",
            "2. Elasticity: Dynamically provisions resources during traffic spikes.",
            "3. Fault Isolation: A crash in one microservice leaves the rest operational."
        ],
        "quiz_question": f"Why does {concept} prefer stateless workers over monolithic stateful servers?",
        "quiz_answer": "Because stateless workers can be destroyed, recreated, and autoscaled horizontally in seconds without data loss."
    }), 200

# --- Notes & Tasks ---
@app.route("/api/notes", methods=["GET", "POST"])
def notes():
    if request.method == "POST":
        data = request.json or {}
        new_note = {
            "id": f"note-{len(NOTES) + 1}",
            "title": data.get("title", "Untitled Note"),
            "content": data.get("content", ""),
            "updated_at": datetime.datetime.utcnow().isoformat()
        }
        NOTES.insert(0, new_note)
        return jsonify({"message": "Note saved", "note": new_note}), 201
    return jsonify({"notes": NOTES}), 200

@app.route("/api/tasks", methods=["GET", "POST", "PATCH"])
def tasks():
    if request.method == "POST":
        data = request.json or {}
        new_task = {
            "id": f"t-{len(TASKS) + 1}",
            "title": data.get("title", "New Task"),
            "priority": data.get("priority", "MEDIUM"),
            "status": "TODO"
        }
        TASKS.append(new_task)
        return jsonify({"message": "Task created", "task": new_task}), 201

    if request.method == "PATCH":
        task_id = request.json.get("id")
        new_status = request.json.get("status")
        task = next((t for t in TASKS if t["id"] == task_id), None)
        if task and new_status:
            task["status"] = new_status
            return jsonify({"message": "Task updated", "task": task}), 200
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"tasks": TASKS}), 200

# --- Static File Serving for Vercel & Render (Single Service Deployment) ---
@app.route("/")
@app.route("/index.html")
@app.route("/api/index.py")
@app.route("/api/index")
def serve_index():
    for folder in STATIC_DIRS:
        idx_path = os.path.join(folder, "index.html")
        if os.path.exists(idx_path):
            return send_from_directory(folder, "index.html")
    return jsonify({"service": "Online Study Hub API", "status": "UP"}), 200

@app.route("/resume.html")
@app.route("/resume")
def serve_resume():
    for folder in STATIC_DIRS:
        target = os.path.join(folder, "resume.html")
        if os.path.exists(target):
            return send_from_directory(folder, "resume.html")
    return jsonify({"error": "Resume not found"}), 404

@app.route("/Divya_Kumari_Resume.pdf")
def serve_pdf():
    for folder in STATIC_DIRS:
        target = os.path.join(folder, "Divya_Kumari_Resume.pdf")
        if os.path.exists(target):
            return send_from_directory(folder, "Divya_Kumari_Resume.pdf", as_attachment=False, mimetype="application/pdf")
    return jsonify({"error": "PDF not found"}), 404

@app.route("/<path:filename>")
def serve_static(filename):
    for folder in STATIC_DIRS:
        target = os.path.join(folder, filename)
        if os.path.exists(target) and os.path.isfile(target):
            return send_from_directory(folder, filename)
    return jsonify({"error": "Resource not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
