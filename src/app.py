import base64
import copy
import json
import jsonpatch

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/mutate", methods=["POST"])
def mutate():
    spec = request.json["request"]["object"]
    modified_spec = copy.deepcopy(spec)

    try:
        modified_spec["spec"]["schedulerName"] = "custom-scheduler"
    except KeyError:
        pass
    patch = jsonpatch.JsonPatch.from_diff(spec, modified_spec)
    return jsonify({
        "response": {
            "allowed": True,
            "uid": request.json["request"]["uid"],
            "patch": base64.b64encode(str(patch).encode()).decode(),
            "patchtype": "JSONPatch",
        }
    })


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"response": {"status": "OK"}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, ssl_context=('cert.pem', 'key.pem'))
