from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample news data
articles = [
    {"id": 1, "title": "AI Technology News",
     "topic": "Technology"},
    {"id": 2, "title": "Sports Latest Updates",
     "topic": "Sports"},
    {"id": 3, "title": "Artificial Intelligence News",
     "topic": "Artificial Intelligence"}
]

users = {}
cache = {}

# Home page
@app.route("/")
def home():
    return """
    <h1>Personalized News Platform</h1>
    <p>Server is running successfully!</p>
    <ul>
      <li><a href="/api/news/search?q=AI">Search News</a></li>
      <li><a href="/api/articles/1">Article Details</a></li>
      <li><a href="/api/news/trending">Trending News</a></li>
      <li><a href="/api/users/1/feed">Personalized Feed</a></li>
    </ul>
    <p>Use Postman to follow a topic using POST.</p>
    """

# 1. Search News
@app.route("/api/news/search", methods=["GET"])
def search_news():
    q = request.args.get("q", "").lower()
    results = [
        a for a in articles
        if q in a["title"].lower()
        or q in a["topic"].lower()
    ]
    return jsonify(results), 200

# 2. Get Article Details
@app.route("/api/articles/<int:aid>", methods=["GET"])
def article_details(aid):
    for a in articles:
        if a["id"] == aid:
            return jsonify(a), 200
    return jsonify({"error": "Article not found"}), 404

# 3. Follow Topic
@app.route("/api/users/<int:uid>/topics", methods=["POST"])
def follow_topic(uid):
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    topics = users.setdefault(uid, [])

    if topic in topics:
        return jsonify({"error": "Already following topic"}), 409

    topics.append(topic)
    cache.pop(uid, None)

    return jsonify({
        "message": "Topic followed successfully",
        "userId": uid,
        "topic": topic
    }), 201

# 4. Personalized Feed
@app.route("/api/users/<int:uid>/feed", methods=["GET"])
def personalized_feed(uid):
    topics = users.get(uid, [])
    feed = [
        a for a in articles
        if a["topic"] in topics
    ]
    return jsonify(feed), 200

# 5. Trending News
@app.route("/api/news/trending", methods=["GET"])
def trending_news():
    return jsonify(articles[:5]), 200

if __name__ == "__main__":
    app.run(debug=False, port=5000)