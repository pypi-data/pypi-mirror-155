"""
Base text classification functionality
"""
import logging
from typing import cast, Iterable, Union, List, Dict

from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_analyzer.nlp_engine import NlpEngineProvider

from fidescls.cls import config as _cconf, models as _cls_models
from fidescls.utils import fides_nlp as _nlp

logger = logging.getLogger(__name__)


class BatchAnalyzerEngine(AnalyzerEngine):
    """
    Class inheriting from AnalyzerEngine and adds the functionality
    to analyze lists or dictionaries.
    https://microsoft.github.io/presidio/samples/python/batch_processing/#set-up-classes-for-batch-processing
    """

    def __init__(self, small_model: bool = True):
        """
        Use the small english model instead of the default large one for speed
        TODO: make this configurable
        """
        configuration = {
            "nlp_engine_name": "spacy",
            "models": [
                {
                    "lang_code": "en",
                    "model_name": "en_core_web_sm" if small_model else "en_core_web_lg",
                }
            ],
        }
        provider = NlpEngineProvider(nlp_configuration=configuration)
        super().__init__(nlp_engine=provider.create_engine())

    def analyze_list(
        self,
        list_of_texts: List[str],
        language: str = _cconf.LANGUAGE,
        **kwargs: List[str],
    ) -> List[List[RecognizerResult]]:
        """
        Analyze a list of strings

        Args:
            list_of_texts: A list containing strings to be analyzed
            language: language string
            **kwargs: Additional parameters for the `AnalyzerEngine.analyze` method

        Returns:

        """

        list_results = []
        for text in list_of_texts:
            results = (
                self.analyze(text, language, **kwargs) if isinstance(text, str) else []
            )
            list_results.append(results)
        return list_results

    def analyze_dict(
        self,
        input_dict: Dict[str, Union[object, List[object]]],
        language: str = _cconf.LANGUAGE,
        **kwargs: List[str],
    ) -> List[Dict[str, Union[str, List, RecognizerResult]]]:
        """
        Analyze a dictionary of keys (strings) and values (either object or List[object]).
        Non-string values are returned as is.

        Args:
            input_dict: The input dictionary for analysis
            language: language string
            **kwargs: Additional keyword arguments for the `AnalyzerEngine.analyze` method

        Returns:

        """
        results = []
        for key, values in input_dict.items():
            item_result: Union[
                List[None], List[RecognizerResult], List[List[RecognizerResult]]
            ]
            if not values:
                item_result = []
            else:
                if isinstance(values, str):
                    item_result = self.analyze(values, language, **kwargs)
                elif isinstance(values, List):
                    item_result = self.analyze_list(
                        list_of_texts=cast(List[str], values),
                        language=language,
                        **kwargs,
                    )
                else:
                    item_result: List[None] = []  # type: ignore
            results.append(
                {"key": key, "value": values, "recognizer_results": item_result}
            )
        return results


class BaseTextClassifier(BatchAnalyzerEngine):
    """
    Presidio based text PII classifier/analyzer
    """

    def classify(
        self,
        raw_text: Union[str, List[str], Dict[str, List]],
        language: str = _cconf.LANGUAGE,
        **kwargs: List[str],
    ) -> Union[
        List[Union[List[RecognizerResult], Dict[str, List[RecognizerResult]]]],
        List[RecognizerResult],
    ]:
        """
        High level, standardized function call for text classification
        Args:
            raw_text: input data to be classified
            language: language string
            **kwargs: keyword arguments that get passed onto the `AnalyzerEngine.analyze` method

        Returns:

        """
        classify_result: Union[
            List[Union[List[RecognizerResult], Dict[str, List[RecognizerResult]]]],
            List[RecognizerResult],
        ]
        logger.debug(
            f"BaseTextClassifier classify inputs: {raw_text}, {language}, {kwargs}"
        )
        if isinstance(raw_text, list):
            logger.debug("Classifying a list")
            classify_result = self.analyze_list(raw_text, language, **kwargs)
        elif isinstance(raw_text, dict):
            logger.debug("Classifying a dict")
            raw_dict = cast(Dict[str, Union[object, List[object]]], raw_text)
            classify_result = self.analyze_dict(raw_dict, language, **kwargs)
        else:
            logger.debug("Classifying a string")
            classify_result = self.analyze(raw_text, language, **kwargs)

        logger.debug(f"Classify result: {classify_result}")
        return classify_result


def similarity_classifier(
    input_text: Union[str, Iterable],
    possible_targets: Iterable = (),
    top_n: Union[int, None] = 1,
    remove_stop_words: bool = False,
    pii_threshold: Union[float, None] = _cconf.PII_DEFAULT_THRESHOLD,
) -> List[_cls_models.MethodClassification]:
    """
    Perform similarity classification between an argument and a set of possible targets
    Args:
        input_text: Text for which to check similarity
        possible_targets: list of candidates to compare against
        top_n: number of similar responses to return in descending
        order. If None, all results will be returned
        remove_stop_words: flag to remove stop words from the text
        pii_threshold: similarity is classified as 'not-pii' if score is below this threshold. 'None' = ignored

    Returns:
        List of MethodClassifications containing the text and top_n most similar possible_targets
    """
    logging.debug("Performing context similarity classification...")

    if not isinstance(input_text, list):
        input_text = [input_text]

    target_docs = {
        possible_target: _nlp.tokenize(
            _nlp.preprocess_text(possible_target, remove_stop_words=remove_stop_words)
        )
        for possible_target in possible_targets
    }

    input_docs = {
        text: _nlp.tokenize(
            _nlp.preprocess_text(text, remove_stop_words=remove_stop_words)
        )
        for text in input_text
    }

    similarities = {}
    for raw_input, input_doc in input_docs.items():
        target_similarities = {}
        for raw_target, target_doc in target_docs.items():
            similarity_score = round(_nlp.similarity(input_doc, target_doc), 4)
            if pii_threshold and similarity_score < pii_threshold:
                logging.debug(
                    f"Similarity score [{similarity_score}] between "
                    f"[{raw_input}] and [{raw_target}] below threshold [{pii_threshold}], skipping"
                )
                continue
            target_similarities[raw_target] = similarity_score
        # grab top n similar entries
        similarities[raw_input] = _nlp.get_top_n_dict(target_similarities, top_n=top_n)

    # format the output to meet the model standard
    formatted_output = []
    for sim_word, similar in similarities.items():
        formatted_output.append(
            _cls_models.MethodClassification(
                input=sim_word,
                labels=[
                    _cls_models.MethodLabel(
                        label=label_score[0],
                        score=label_score[1],
                        position_start=None,
                        position_end=None,
                    )
                    for label_score in similar
                ],
            )
        )

    return formatted_output
