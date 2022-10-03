from google.cloud import language_v1 as language

_type = language.Document.Type.PLAIN_TEXT
_encoding_type = language.EncodingType.UTF8
_language = "en"


def get_client() -> language.LanguageServiceClient:
    return language.LanguageServiceClient()


def _transform(y_pred: float, y_mag: float) -> int:
    """ Transform the score (& magnitude) into 0/1 labels to match 
    the rotten tomatoes dataset """
    # score of the sentiment ranges between -1.0 (negative) and 1.0 (positive) and 
    # corresponds to the overall emotional leaning of the text.

    # magnitude indicates the overall strength of emotion (both positive and negative) 
    # within the given text, between 0.0 and +inf

    # @TODO: consider other approaches to handle mixed/neutral text responses
    return 1 if y_pred > 0 else 0, y_mag


def predict(client: language.LanguageServiceClient, input_text: str) -> int:
    """ Retrieve a sentiment prediction for a string of input text"""
    request = {
        "document": {
            "content": input_text,
            "type_": _type,
            "language": _language,
        },
        "encoding_type": _encoding_type,
    }

    response = client.analyze_sentiment(request=request)
    return _transform(response.document_sentiment.score, response.document_sentiment.magnitude)
