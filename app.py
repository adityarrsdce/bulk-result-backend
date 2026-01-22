from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/bulk-results", methods=["POST"])
def bulk_results():
    data = request.json

    start_reg = int(data["startReg"])
    end_reg = int(data["endReg"])

    name = data["name"]
    semester = data["semester"]      # Roman: III, IV, V...
    session = data["session"]
    exam_held = data["exam_held"]

    results = []

    for reg in range(start_reg, end_reg + 1):
        url = (
            "https://beu-bih.ac.in/result-three"
            f"?name={name}"
            f"&semester={semester}"
            f"&session={session}"
            f"&regNo={reg}"
            f"&exam_held={exam_held}"
        )

        try:
            # Light check if page exists
            r = requests.get(url, timeout=5)

            if r.status_code == 200 and "Result" in r.text:
                results.append({
                    "regNo": reg,
                    "url": url,
                    "success": True
                })
            else:
                results.append({
                    "regNo": reg,
                    "url": url,
                    "success": False
                })

        except Exception:
            results.append({
                "regNo": reg,
                "url": url,
                "success": False
            })

    return jsonify({
        "count": len(results),
        "results": results
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
