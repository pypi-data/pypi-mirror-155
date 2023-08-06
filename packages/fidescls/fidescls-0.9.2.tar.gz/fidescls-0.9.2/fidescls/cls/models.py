"""
Classification related data models
"""
from typing import Dict, List, Optional, Union
from enum import Enum

from pydantic import BaseModel


class ClassificationParadigm(str, Enum):
    """Classification paradigm options"""

    CONTEXT = "context"
    CONTENT = "content"
    INFERRED = "inferred"


class MethodLabel(BaseModel):
    """Classification method output data model"""

    label: Optional[Union[str, List]]
    score: Optional[float]
    aggregated_score: Optional[float]
    position_start: Optional[Union[int, None]] = None
    position_end: Optional[Union[int, None]] = None


class AggregatedMethodLabel(BaseModel):
    """Aggregated classification output data model"""

    label: Optional[str]
    score: Optional[float]
    aggregated_score: Optional[float]
    classification_paradigm: Optional[ClassificationParadigm]

    class Config:
        """Set custom model configuration parameters"""

        use_enum_values = True


class MethodClassification(BaseModel):
    """Classification output data model"""

    input: Union[str, List]
    labels: List


class AggregatedMethodClassification(BaseModel):
    """Aggregated classification output data model"""

    input: Union[str, List]
    labels: List
    aggregation_method: str


class AggregatedSystemClassification(BaseModel):
    """System level classification aggregation"""

    content_input: Optional[List]
    context_input: Optional[List]
    aggregation_method: str = "weighted"
    aggregation_params: Optional[Dict]
    aggregated_labels: List = []
