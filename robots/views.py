import json
from logging import getLogger
from typing import Any, Dict, List

from django.http import HttpRequest, JsonResponse
from pydantic import ValidationError

from .models import Robot
from .schemas import RobotSchema

logger = getLogger("view")


def create_robot(request: HttpRequest) -> JsonResponse:
    """
    Create a record about a new robot.

    :param request: HttpRequest
    :return: The endpoint will return {"status": False, "message": <errors>}
    with code 400 in case of error, and {"status": True, "message": "OK"}
    with code 201 in case of success.
    """
    if request.method == "POST":
        json_data: str = request.body.decode(encoding="utf-8")

        try:
            logger.debug("json_data:\n%s", json.loads(json_data))
            schema: RobotSchema = RobotSchema.model_validate_json(json_data)
        except ValidationError as exc:
            errors: List[Dict[str, Any]] = list()
            for error in exc.errors():
                errors.append({"type": error["type"], "msg": error["msg"]})
            logger.warning("Validation error\n%s", json.dumps(errors))

            return JsonResponse(
                {
                    "status": False,
                    "message": str(errors),
                },
                status=400,
            )
        else:
            validated_data: Dict[str, Any] = schema.model_dump()
            validated_data["serial"] = "-".join(
                (validated_data["model"], validated_data["version"])
            )
            robot: Robot = Robot.objects.create(**validated_data)

            logger.debug("New robot created. Robot.pk=%d", robot.pk)
            return JsonResponse(
                {"status": True, "message": "OK"},
                status=201,
            )
