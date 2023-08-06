"""
API related data models
"""
from typing import Dict, List, Iterable, Optional, Union
from pydantic import BaseModel
from fidescls.api import config as _api_conf


class SimilarityParams(BaseModel):
    """Data model for the similarity method params"""

    possible_targets: Iterable
    top_n: Optional[Union[int, None]] = 1
    remove_stop_words: bool = False
    pii_threshold: Optional[Union[float, None]] = _api_conf.PII_DEFAULT_THRESHOLD


class ContentParams(BaseModel):
    """Data model for the content paradigm options"""

    language: str = "en"
    model: Optional[Union[str, None]] = None
    decision_method: str = "direct-mapping"
    aggregation_method: str = "mean"
    infer_not_pii: bool = True


class AggregationPayload(BaseModel):
    """Data model for classification aggregation"""

    method: str
    method_params: Dict


class ContentPayload(BaseModel):
    """Data model for the content paradigm"""

    data: Union[List, Dict]
    method: str = "default"
    method_params: ContentParams
    aggregation: Optional[AggregationPayload]


class ContextPayload(BaseModel):
    """Data model for the context paradigm"""

    data: Union[str, List]
    method: str = "similarity"
    method_params: SimilarityParams
    aggregation: Optional[AggregationPayload]


class ClassifyPayload(BaseModel):
    """Data model for classification request payloads"""

    context: Optional[ContextPayload]
    content: Optional[ContentPayload]


class RequestPayload(BaseModel):
    """Input Data Payload"""

    data: List[ClassifyPayload]
    data_aggregation: Optional[AggregationPayload]
