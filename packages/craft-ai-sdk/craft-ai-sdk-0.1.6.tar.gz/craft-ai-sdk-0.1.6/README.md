# Craft AI Python SDK

This Python SDK lets you interact with Craft AI MLOps Platform.

## Installation
This project relies on **Python 3.8+**. Once a supported version of Python is installed, you can install `craft-ai-sdk` from PyPI with:

```console
pip install craft-ai-sdk
```

## Basic usage
You can configure the SDK by instantiating the `CraftAiSdk` class in this way:

```python
from craft_ai_sdk import CraftAiSdk

CRAFT_AI_ACCESS_TOKEN =  # your access token
CRAFT_AI_ENVIRONMENT_URL =  # url to your environment

sdk = CraftAiSdk(access_token=CRAFT_AI_ACCESS_TOKEN, environment_url=CRAFT_AI_ENVIRONMENT_URL)
```
