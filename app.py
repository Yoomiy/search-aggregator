from flask import Flask, request, jsonify, render_template
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID
from search_logic import logic

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    # sources = request.form.get("sources").split(",")
    sources = [source.strip() for source in request.form.getlist("sources")]
    # print(request.form.getlist("sources"), sources)

    if not sources:
        return jsonify({"error": "No valid search engine selected"})
        
    aggregated_results = logic(query, sources)

    if aggregated_results:
        return jsonify(aggregated_results)
    else:
        return jsonify({"error": "No results found"})
    
if __name__ == "__main__":
    app.run(debug=True)