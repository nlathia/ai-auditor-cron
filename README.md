# ai-auditor-cron

This service audits an Artificial Intelligence (AI) API by regularly querying it for predictions with the test set entries of an open source dataset.

The initial version is set up to analyse the [Google Cloud Sentiment](https://cloud.google.com/natural-language/docs/analyzing-sentiment) service using the [Rotten Tomatoes](https://huggingface.co/datasets/rotten_tomatoes) dataset. The service could be extended to other APIs (for example, [Amazon's Comprehend](https://docs.aws.amazon.com/comprehend/latest/dg/how-sentiment.html) and datasets).

The website with the results is here: https://sentiment-ai-api-audit.herokuapp.com/

### Implementation details

This cloud run container was created and deployed with the [kettle-cli](https://github.com/nlathia/kettle-cli). It streams the Rotten Tomatoes test set, which is hosted by Hugging Face, and queries Google's sentiment API for each entry. Overall performance metrics are tracked with the Hugging Face [evaluate](https://huggingface.co/docs/evaluate/index) library, and a sample of misclassifications are retained.

The results are `POST`'ed to a Heroku app, where they can be displayed. The repository for that website is open source [in the ai-auditor-web repository](https://github.com/nlathia/ai-auditor-web).


