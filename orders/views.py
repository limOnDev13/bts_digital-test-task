import json
from logging import getLogger
from typing import Any, Dict, List

from django.http import HttpRequest, JsonResponse
from pydantic import ValidationError

from .business.main import create_new_order
from .business.models import OrderInfo
from .schemas import OrderSchema

logger = getLogger("view")


def create_order(request: HttpRequest) -> JsonResponse:
    """
    Create a record about a new order.

    :param request: HttpRequest
    :return: The endpoint will return {"status": False, "message": <errors>}
    with code 400 in case of error,
    {"status": True, "message": OK} with code 201 if the request is valid
    and the robot of the selected series is in stock,
    {"status": True, "message": "The product is out of stock"} with code 201
    if the request is valid and the robot of the selected series is not in stock yet.
    In the latter case, the client is added to the queue for this model.
    As soon as the goods appear in the warehouse and the customer reaches the queue,
    a notification letter will be sent to him by mail.
    """
    if request.method == "POST":
        json_data: str = request.body.decode(encoding="utf-8")

        try:
            logger.debug("json_data:\n%s", json.loads(json_data))
            schema: OrderSchema = OrderSchema.model_validate_json(json_data)
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
            order_info: OrderInfo = OrderInfo(
                customer_id=schema.customer_id, robot_serial=schema.robot_serial
            )
            order, in_stock = create_new_order(order_info)

            logger.debug("New order created, order.pk=%d", order.pk)
            if in_stock:
                return JsonResponse(
                    {"status": True, "message": "OK"},
                    status=201,
                )
            else:
                return JsonResponse(
                    {"status": True, "message": "The product is out of stock"},
                    status=201,
                )
