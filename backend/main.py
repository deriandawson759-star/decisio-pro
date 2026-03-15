"""
DECISIO PRO - Backend API
Flask server pour la generation de PDF premium
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pdf_generator import generate_pdf
from io import BytesIO
import os

app = Flask(__name__)

# CORS - autoriser le frontend Vercel + dev local
CORS(app, origins=[
    "https://decisio-pro.vercel.app",
    "https://decisio.pro",
    "https://www.decisio.pro",
    "http://localhost:5173",
    "http://localhost:3000",
])


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "DECISIO PRO PDF API", "version": "1.0"})


@app.route("/generate-pdf", methods=["POST"])
def gen_pdf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnee recue"}), 400

        report_text = data.get("report", "")
        nom = data.get("nom", "Client")
        secteur = data.get("secteur", "")
        mode = data.get("mode", "premium")
        date_str = data.get("date", None)

        if not report_text:
            return jsonify({"error": "Texte du rapport manquant"}), 400

        pdf_bytes = generate_pdf(report_text, nom, secteur, mode, date_str)

        slug = nom.replace(" ", "_")[:20]
        filename = f"DECISIO_Audit_{slug}.pdf"

        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
