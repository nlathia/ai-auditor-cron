# ai-api-auditor-cron

This service audits an Artificial Intelligence (AI) API by regularly querying it for predictions with the test set entries of an open source dataset.

The initial version is set up to analyse the [Google Cloud Sentiment](https://cloud.google.com/natural-language/docs/analyzing-sentiment) service using the [Rotten Tomatoes](https://huggingface.co/datasets/rotten_tomatoes) dataset. The service could be extended to other APIs (for example, [Amazon's Comprehend](https://docs.aws.amazon.com/comprehend/latest/dg/how-sentiment.html) and datasets).

The website with the results is here: https://sentiment-ai-api-audit.herokuapp.com/

This cloud run container was created with the [kettle-cli](https://github.com/nlathia/kettle-cli).

