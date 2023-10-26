## Cogniswitch ToolSpec

**Use cogniswitch to have chat with your knowledge in just three steps**

visit https://www.cogniswitch.ai/developer.<br>

**Registration:**
- Signup with your email and verify your registration
- You will get a mail with a platform token and oauth token for using the services.


**step 1: Instantiate the Cogniswitch ToolSpec:**<br>
- Use your cogniswitch token, openAI API key, oauth token to instantiate the toolspec. <br> 

**step 2: Cogniswitch Store data:**<br>
- use store_data function in the toolspec and input your file or url. <br>
- it will be processed and stored in your knowledge store. <br> 
- you can check the status of document processing in cogniswitch console. <br>

**step 3: Cogniswitch Answer:**<br>
- Use query_knowledge function in the toolspec and input your query. <br>
- You will get the answer from your knowledge as the response. <br>


### Import Required Libraries


```python
import warnings
warnings.filterwarnings("ignore")
from llama_hub.tools import CogniswitchToolspec
```

### Cogniswitch Credentials and OpenAI token


```python
# cs_token = <your cogniswitch platform token>
# OAI_token = <your openai token>
# oauth_token = <your cogniswitch apikey>
```

### Instantiate the Tool Spec


```python
toolspec = CogniswitchToolSpec(cs_token=cs_token, OAI_token=OAI_token, apiKey=oauth_token)
```

### Use the Tool Spec for storing data in cogniswitch with a single call


```python
store_response = toolspec.store_data(url = "https://cogniswitch.ai/dev",
                                    document_name="Cogniswitch dev",
                                    document_description="This is a cogniswitch website for developers.")
print(store_response)
```

    {'data': {'knowledgeSourceId': 42, 'sourceType': 'https://cogniswitch.ai/dev', 'sourceURL': None, 'sourceFileName': None, 'sourceName': 'Cogniswitch dev', 'sourceDescription': 'This is a cogniswitch website for developers.', 'status': 'UPLOADED'}, 'list': None, 'message': "We're processing your content & will send you an email on completion, hang tight!", 'statusCode': 1000}
    

### Use Tool Spec for answering using the query knowledge with a single call


```python
answer_response = toolspec.query_knowledge("tell me about cogniswitch")
print(answer_response)
```

    {'data': {'answer': 'CogniSwitch is a technology platform that enhances the reliability of Generative AI applications for enterprises. It does this by gathering and organizing knowledge from documented sources, eliminating hallucinations and bias in AI responses. The platform uses AI to automatically gather and organize knowledge, which can then be reviewed and curated by experts before being published. The CogniSwitch API enables Gen AI applications to access this knowledge as needed, ensuring reliability. It is specifically designed to complement Generative AI and offers customized solutions for different business functions within an enterprise.'}, 'list': None, 'message': None, 'statusCode': 1000}
