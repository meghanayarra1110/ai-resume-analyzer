from flask import Flask, request, render_template_string
from pypdf import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Resume Analyzer</title>
</head>
<body>
    <h1>AI Resume Analyzer 🚀</h1>

    <p>Upload your resume PDF below:</p>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="resume" accept=".pdf" required>
        <button type="submit">Analyze Resume</button>
    </form>

    {% if text %}
        <hr>
        <h2>Extracted Resume Text</h2>
        <pre>{{ text }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    text = ""

    if request.method == "POST":
        file = request.files.get("resume")

        if file and file.filename.endswith(".pdf"):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            reader = PdfReader(filepath)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    return render_template_string(HTML, text=text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
