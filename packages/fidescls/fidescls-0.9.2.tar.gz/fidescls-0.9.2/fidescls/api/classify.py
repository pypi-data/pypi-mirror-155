"""
Classifier API Endpoint
"""
import logging
from typing import cast, List, Dict, Union

from fastapi import APIRouter

from fidescls.api import config as _aconf, models as _api_models
from fidescls.cls import (
    models as _cls_models,
    aggregation as _cls_agg,
    context,
    content,
)

logger = logging.getLogger(_aconf.LOGGER_NAME)

# pylint: disable=invalid-name

RESPONSE = Union[
    Dict[
        str,
        Union[
            List,
            Dict[str, List],
        ],
    ],
    _cls_models.AggregatedSystemClassification,
]
RESPONSE_LIST = List[RESPONSE]

routers = []
for resource_type in _aconf.RESOURCES:
    router = APIRouter(tags=["Classify", resource_type], prefix=f"/{resource_type}")

    @router.post(f"/{_aconf.CLASSIFY_ENDPOINT}")
    async def classify(
        payload: _api_models.RequestPayload,
    ) -> RESPONSE_LIST:
        """
        Perform PII classification
        Args:
            payload: request payload containing fields described in the ClassifyPayload data model

        Returns:
            The result of the classification

        Raises:
            HTTPException of status code
        """
        responses: RESPONSE_LIST = []

        if payload.data:
            for input_data in payload.data:
                response: RESPONSE = {}

                if input_data.context:
                    if input_data.context.method == "similarity":
                        logger.debug(
                            f"Similarity Request Payload:\n{input_data.context.dict()}"
                        )
                        context_labels = context.classify(
                            input_data.context.data,
                            method_name="similarity",
                            method_params={
                                "possible_targets": input_data.context.method_params.possible_targets,
                                "top_n": input_data.context.method_params.top_n,
                                "remove_stop_words": input_data.context.method_params.remove_stop_words,
                                "pii_threshold": input_data.context.method_params.pii_threshold,
                            },
                        )
                        response["context"] = context_labels  # type: ignore
                if input_data.content:
                    if input_data.content.method == "default":
                        logger.debug(
                            f"Content Request Payload:\n{input_data.content.dict()}"
                        )
                        content_labels = content.classify(
                            input_data.content.data,
                            language=input_data.content.method_params.language,
                            model=input_data.content.method_params.model,
                            decision_method=input_data.content.method_params.decision_method,
                            aggregation_method=input_data.content.method_params.aggregation_method,
                            infer_not_pii=input_data.content.method_params.infer_not_pii,
                        )
                        response["content"] = content_labels  # type: ignore
                if payload.data_aggregation:
                    response = _cls_agg.aggregate_system(
                        context_classification=cast(List, response["context"]),  # type: ignore
                        content_classification=cast(List, response["content"]),  # type: ignore
                        aggregation_method=payload.data_aggregation.method,
                        aggregation_params=payload.data_aggregation.method_params,
                    )
                responses.append(response)
        else:
            raise ValueError("No input data provided for classification!")
        return responses

    routers.append(router)
