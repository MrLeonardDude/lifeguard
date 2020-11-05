import json
import traceback

from flask import Flask, make_response

from lifeguard.logger import lifeguard_logger as logger
from lifeguard.validations import VALIDATIONS, load_validations

APP = Flask(__name__)

load_validations()


@APP.route("/lifeguard/validations/<validation>/execute", methods=["POST"])
def execute_validation(validation):
    try:
        result = VALIDATIONS[validation]["ref"]()
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json"

        return response
    except Exception:
        logger.error(
            "error on execute validation %s",
            validation,
            extra={"traceback": traceback.format_exc()},
        )
        return json.dumps({"error": traceback.format_exc()})
