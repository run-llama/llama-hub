## Cogniswitch ToolSpec

**Use CogniSwitch to build production ready applications that can consume, organize and retrieve knowledge flawlessly. Using the framework of your choice, in this case LlamaIndex, CogniSwitch helps alleviate the stress of decision making when it comes to, choosing the right storage and retrieval formats. It also eradicates reliability issues and hallucinations when it comes to responses that are generated. Get started by interacting with your knowledge in just three simple steps**

visit [https://www.cogniswitch.ai/developer](https://www.cogniswitch.ai/developer?utm_source=llamaindex&utm_medium=llamaindexbuild&utm_id=dev).

**Registration:**
- Signup with your email and verify your registration
- You will get a mail with a platform token and OAuth token for using the services.


**Step 1: Instantiate the Cogniswitch ToolSpec:**
- Use your Cogniswitch token, openAI API key, OAuth token to instantiate the toolspec.  

**Step 2: Cogniswitch Store data:**
- Use store_data function in the toolspec and input your file or url. 
- It will be processed and stored in your knowledge store. 
- You can check the status of document processing in cogniswitch console. 

**Step 3: Cogniswitch Answer:**
- Use query_knowledge function in the toolspec and input your query. 
- You will get the answer from your knowledge as the response. 


### Import Required Libraries


```python
import warnings

warnings.filterwarnings("ignore")
from llama_hub.tools.cogniswitch import CogniswitchToolSpec
```

### Cogniswitch Credentials and OpenAI token


```python
# cs_token = <your cogniswitch platform token>
# OAI_token = <your openai token>
# oauth_token = <your cogniswitch apikey>
```

### Instantiate the Tool Spec


```python
toolspec = CogniswitchToolSpec(
    cs_token=cs_token, OAI_token=OAI_token, apiKey=oauth_token
)
```

### Use the Tool Spec for storing data in cogniswitch with a single call


```python
store_response = toolspec.store_data(
    url="https://cogniswitch.ai/developer",
    document_name="Cogniswitch dev",
    document_description="This is a cogniswitch website for developers.",
)
print(store_response)
```

    {'data': {'knowledgeSourceId': 43, 'sourceType': 'https://cogniswitch.ai/developer', 'sourceURL': None, 'sourceFileName': None, 'sourceName': 'Cogniswitch dev', 'sourceDescription': 'This is a cogniswitch website for developers.', 'status': 'UPLOADED'}, 'list': None, 'message': "We're processing your content & will send you an email on completion, hang tight!", 'statusCode': 1000}
    

### Use Tool Spec for answering using the query knowledge with a single call


```python
answer_response = toolspec.query_knowledge("tell me about cogniswitch")
print(answer_response)
```

    {'data': {'answer': 'CogniSwitch is a technology platform that enhances the reliability of Generative AI applications for enterprises. It does this by gathering and organizing knowledge from documented sources, eliminating hallucinations and bias in AI responses. The platform uses AI to automatically gather and organize knowledge, which can then be reviewed and curated by experts before being published. The CogniSwitch API enables Gen AI applications to access this knowledge as needed, ensuring reliability. It is specifically designed to complement Generative AI and offers customized solutions for different business functions within an enterprise.'}, 'list': None, 'message': None, 'statusCode': 1000}
    
The tool is designed to store data and retrieve answers based on the knowledge provided. check out the [link](https://github.com/run-llama/llama-hub/blob/main/llama_hub/tools/notebooks/cogniswitch.ipynb) for examples.
