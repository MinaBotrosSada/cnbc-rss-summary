# Welcome to MB' RSS Feed Summarizer 

This is an app which used Vertex AI GenAI Text Bison Model to summarize RSS feeds. The RSS feed URL can be changed in the UI, the default is FoxNews.

Edit [rss.py](./rss.py) to customize this app to your heart's desire. ❤️

## Approach
- I experimented with Zero-shot prompting and the results were decent
- I experimented with Few-shot Promoting and the results were at time longer than expected in terms of number of output sentences but still acceptable


## Setup steps

1. `gcloud auth application-default login`
2. `gcloud config set project PROJECT_ID`
3. `gcloud auth application-default set-quota-project PROJECT_ID`