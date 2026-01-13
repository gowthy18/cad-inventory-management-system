import os
from flask import Flask, render_template, request, send_from_directory

from src.integrated_search import integrated_search  # 👈 IMPORTANT

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DATABASE_FOLDER = "data/database"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["cad_file"]
        filename = file.filename

        upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(upload_path)

        # 🔥 RUN YOUR REAL ENGINE HERE
        results = integrated_search(upload_path)

        # results assumed sorted best → worst
        best_match = results[0]["name"]
        similar_models = results[1:4]  # next top 3

        return render_template(
            "index.html",
            uploaded_model_name=filename,
            best_match=best_match,
            best_match_download=f"/download/{best_match}",
            similar_models=[
                {
                    "name": r["name"],
                    "download": f"/download/{r['name']}"
                }
                for r in similar_models
            ],
        )

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(DATABASE_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
