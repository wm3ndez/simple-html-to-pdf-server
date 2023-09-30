import io

from flask import Flask, send_file, request

from html_to_pdf import to_pdf

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello World!</h1>"


@app.route("/pdf", methods=["POST"])
def pdf():
    html_content = request.get_data().decode("utf-8")
    content = to_pdf(html_content)

    # Convert binary data to a file-like object using BytesIO
    pdf_io = io.BytesIO(content)

    # Use send_file to send the data as an attachment
    return send_file(
        pdf_io,
        download_name="downloaded.pdf",
        mimetype="application/pdf",
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
