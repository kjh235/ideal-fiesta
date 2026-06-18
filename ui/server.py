import os
import re
import json
from pathlib import Path

import yaml
import jsonschema
from flask import Flask, jsonify, request, send_from_directory, abort

app = Flask(__name__)

BASE_DIR = Path(__file__).parent.parent.resolve()

DOMAINS = {
    "capabilities":  "capabilities",
    "organization":  "organization",
    "value-streams": "value-streams",
    "information":   "information",
}

SCHEMA_FILES = {
    "capabilities":  "capability.schema.json",
    "organization":  "organization.schema.json",
    "value-streams": "valuestream.schema.json",
    "information":   "information.schema.json",
}


def domain_path(domain: str) -> Path:
    return BASE_DIR / DOMAINS[domain]


def load_schema(domain: str) -> dict:
    with open(BASE_DIR / "schemas" / SCHEMA_FILES[domain]) as f:
        return json.load(f)


def validate_filename(filename: str) -> None:
    if not re.match(r"^[a-zA-Z0-9_\-]+\.yaml$", filename):
        abort(400)


def id_to_filename(artifact_id: str) -> str:
    return artifact_id.lower().replace("-", "_") + ".yaml"


@app.route("/")
def index():
    return send_from_directory(Path(__file__).parent, "index.html")


@app.route("/api/schemas")
def get_schemas():
    return jsonify({d: load_schema(d) for d in DOMAINS})


@app.route("/api/<domain>", methods=["GET"])
def list_artifacts(domain):
    if domain not in DOMAINS:
        abort(404)
    result = []
    for path in sorted(domain_path(domain).glob("*.yaml")):
        with open(path) as f:
            data = yaml.safe_load(f)
        if data:
            data["_filename"] = path.name
            result.append(data)
    return jsonify(result)


@app.route("/api/<domain>", methods=["POST"])
def create_artifact(domain):
    if domain not in DOMAINS:
        abort(404)
    payload = request.get_json(force=True)
    payload.pop("_filename", None)

    try:
        jsonschema.validate(payload, load_schema(domain))
    except jsonschema.ValidationError as e:
        return jsonify({"error": e.message}), 422

    filename = id_to_filename(payload.get("id", ""))
    filepath = domain_path(domain) / filename
    if filepath.exists():
        return jsonify({"error": f"Artifact {payload.get('id')} already exists. Use Edit to update it."}), 409

    with open(filepath, "w") as f:
        yaml.dump(payload, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return jsonify({"_filename": filename, **payload}), 201


@app.route("/api/<domain>/<filename>", methods=["PUT"])
def update_artifact(domain, filename):
    if domain not in DOMAINS:
        abort(404)
    validate_filename(filename)
    filepath = domain_path(domain) / filename
    if not filepath.exists():
        abort(404)

    payload = request.get_json(force=True)
    payload.pop("_filename", None)

    try:
        jsonschema.validate(payload, load_schema(domain))
    except jsonschema.ValidationError as e:
        return jsonify({"error": e.message}), 422

    with open(filepath, "w") as f:
        yaml.dump(payload, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    return jsonify({"_filename": filename, **payload})


@app.route("/api/<domain>/<filename>", methods=["DELETE"])
def delete_artifact(domain, filename):
    if domain not in DOMAINS:
        abort(404)
    validate_filename(filename)
    filepath = domain_path(domain) / filename
    if not filepath.exists():
        abort(404)
    os.remove(filepath)
    return "", 204


if __name__ == "__main__":
    print("\n  Business Architecture Repository UI")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(debug=True, port=5000)
