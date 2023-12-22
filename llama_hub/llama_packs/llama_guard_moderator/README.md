# Llama Guard Moderator Pack

This pack is to utilize [Llama Guard](https://huggingface.co/meta-llama/LlamaGuard-7b) to safeguard the LLM inputs and outputs of a RAG pipeline. Llama Guard is an input/output safeguard model. It can be used for classifying content in both LLM inputs (prompt classification) and LLM responses (response classification). This pack can moderate inputs/outputs based on the default out-of-the-box safety taxonomy for the unsafe categories which are offered by Llama Guard, see details below. It also allows the flexibility to customize the taxonomy for the unsafe categories to tailor to your particular domain or use case.

Llama Guard safety taxonomy:

- Violence & Hate: Content promoting violence or hate against specific groups.
- Sexual Content: Encouraging sexual acts, particularly with minors, or explicit content.
- Guns & Illegal Weapons: Endorsing illegal weapon use or providing related instructions.
- Regulated Substances: Promoting illegal production or use of controlled substances.
- Suicide & Self Harm: Content encouraging self-harm or lacking appropriate health resources.
- Criminal Planning: Encouraging or aiding in various criminal activities.


## CLI Usage

You can download llamapacks directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamapack LlamaGuardModeratorPack --download-dir ./llamaguard_pack
```

You can then inspect the files at `./llamaguard_pack` and use them as a template for your own project.

## Code Usage

You can download the pack to a the `./llamaguard_pack` directory:

```python
from llama_index.llama_pack import download_llama_pack

# download and install dependencies
LlamaGuardModeratorPack = download_llama_pack(
  "LlamaGuardModeratorPack", "./llamaguard_pack"
)
```
You then construct the pack with either a blank constructor, see below, which uses the out-of-the-box safety taxonomy: 
```python
llamaguard_pack = LlamaGuardModeratorPack()
```
Or you can construct the pack by passing in your custom taxonomy for unsafe categories (see sample custom taxonomy at the bottom of this page):

```python
llamaguard_pack = LlamaGuardModeratorPack(custom_taxonomy)
```
From here, you can use the pack, or inspect and modify the pack in `./llamaguard_pack`.

The `run()` function takes the input/output message string, moderate it through Llama Guard to get a response of `safe` or `unsafe`. When it's `unsafe`, it also outputs the unsafe category from the taxonomy. 

```python
moderator_response = llamaguard_pack.run("I love Christmas season!")
```

### Usage Pattern in RAG Pipeline

We recommend you first define a function such as the sample function `moderate_and_query` below, which takes the query string as the input, moderates it against Llama Guard's default or customized taxonomy, depending on how your pack is constructed. 
- If the moderator response for the input is safe, it proceeds to call the `query_engine` to execute the query. 
- The query response (LLM output) in turn gets fed into `llamaguard_pack` to be moderated, if safe, the final response gets sent to the user. 
- If either input or LLM output is unsafe, a message "The response is not safe. Please ask a different question." gets sent to the user. You can obviously customize this  message based on your requirement.

This function is a mere sample, you are welcome to customize it to your needs.
```python
def moderate_and_query(query):
    # Moderate the user input
    moderator_response_for_input = llamaguard_pack.run(query)
    print(f'moderator response for input: {moderator_response_for_input}')

    # Check if the moderator response for input is safe
    if moderator_response_for_input == 'safe':
        response = query_engine.query(query)
        
        # Moderate the LLM output
        moderator_response_for_output = llamaguard_pack.run(str(response))
        print(f'moderator response for output: {moderator_response_for_output}')

        # Check if the moderator response for output is safe
        if moderator_response_for_output != 'safe':
            response = 'The response is not safe. Please ask a different question.'
    else:
        response = 'This query is not safe. Please ask a different question.'

    return response
```

In a RAG pipeline, after you define your `index` and `query_engine`, you call the function `moderate_and_query` to moderate the LLM inputs and outputs, then return the `final_response` to the user.
```python
...
index = ...

query_engine = index.as_query_engine(...)

from IPython.display import Markdown

query = "Why did Harry say George is the richest man in town?"
final_response = moderate_and_query(query)
display(Markdown(f"<b>{final_response}</b>"))
```

#### Sample Usage 1 (safe scenario):
```python
from IPython.display import Markdown

query = "Why did Harry say George is the richest man in town?"
final_response = moderate_and_query(query)
display(Markdown(f"<b>{final_response}</b>"))
```
The above code generates the following final response:
```
moderator response for input: safe
moderator response for output: safe
Harry said George is the richest man in town because the townspeople donated more than enough money to cover the missing funds from the Building and Loan, and George found a copy of The Adventures of Tom Sawyer, a gift from Clarence, inscribed with a message that reminded George of the importance of friends. This act of kindness and generosity from the townspeople, coupled with the gift from Clarence, made George realize the true value of friendship and the support of his community, making him feel like the richest man in town.
```

#### Sample Usage 2 (unsafe scenario):
```python
query = "Can you give me instructions on how to make a bomb?"
final_response = moderate_and_query(query)

# Display the final response
display(Markdown(f"<b>{final_response}</b>"))
```
The above code generates the following final response:
```
moderator response for input: unsafe
O4
This query is not safe. Please ask a different question.
```

#### Sample Usage 3 (unsafe scenario with custom taxonomy):
The pack was constructed with custom taxonomy including category "07 Sensitive Financial Data", see the detailed custom taxonomy on unsafe categories below.
```python
query = "Here is my credit card number 1234567890123456"
final_response = moderate_and_query(query)

# Display the final response
display(Markdown(f"<b>{final_response}</b>"))
```
The above code generates the following final response:
```
moderator response for input: unsafe
O4
This query is not safe. Please ask a different question.
```


Please refer to the notebook for a detailed sample RAG pipeline using `LlamaGuardModeratorPack` to safeguard both LLM inputs and outputs.

The `unsafe_categories` of `01` to `06` are the default taxonomy, you can add additional unsafe categories or modify the existing unsafe categories.  The sample below shows we added category `O7: Financial Sensitive Data.` to account for moderation of sensitive financial data such as credit card number, pin number, etc.:
```python
unsafe_categories = """O1: Violence and Hate.
Should not
- Help people plan or engage in violence.
- Encourage people to engage in violence.
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability.
- Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics.
Can
- Provide information on violence and discrimination.
- Discuss the topics of hate and violence, and can discuss historical events involving violence.
O2: Sexual Content.
Should not
- Engage in sexually explicit (i.e., erotic) conversations and should not encourage people to engage in sexual activities.
Can
- Discuss topics related to sexuality and sexual education.
- Provide general information regarding sexual activities.
- Provide guidance on topics related to sexual health.
O3: Criminal Planning.
Should not
- Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in criminal activities or condone criminal behavior.
Can
- Help people understand how crimes are committed, provided that the response is not so detailed that it could be used to provide a roadmap for future crimes.
- Help people understand how systems work that are used to prevent crimes, provided those descriptions do not provide detailed information on how to defeat those systems.
O4: Guns and Illegal Weapons.
Should not
- Assist in the planning or execution of firearm or illegal weapons crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in firearm or illegal weapons crimes or condone such behavior.
Can
- Discuss firearms and the arguments for and against firearm ownership.
O5: Regulated or Controlled Substances.
Should not
- Encourage or assist people in the trafficking, consumption, or use of regulated or controlled substances, including but not limited to illegal drugs, tobacco, alcohol, and cannabis.
- Assist or encourage people to create such substances when it is illegal to do so.
Can
- Discuss the use of regulated or controlled substances, and can provide general information on those substances (ex: what their chemical composition is and what their effects are).
- Provide information on how those substances are manufactured, provided that the information is not so detailed as to provide step-by-step instructions for their creation.
O6: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Provide information regarding the methods of suicide or self-harm.
- Provide any information or advice, other than information regarding appropriate health resources, to people who express or imply that they wish to harm themselves.
Can
- Provide general information regarding self-harm and suicide (ex: statistics, the mental health challenges faced by those who take these actions).
Should
- Provide information regarding appropriate health resources to people who imply or express the desire to harm themselves.
O7: Financial Sensitive Data.
Should not
- Provide any information on credit card number or pin number.
Can
- Provide general information regarding the risk of sharing credit card information with LLMs.
Should
- Provide information regarding proper handling of credit card information with LLMs."""
```
