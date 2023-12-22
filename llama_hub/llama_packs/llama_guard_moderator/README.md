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

# You then construct the pack with either a blank constructor, which uses the out-of-the-box safety taxonomy, or you can pass in your custom taxonomy for unsafe categories. 
llamaguard_pack = LlamaGuardModeratorPack(custom_taxonomy)
```

From here, you can use the pack, or inspect and modify the pack in `./llamaguard_pack`.

The `run()` function takes the input/output message string, moderate it through Llama Guard to get a response of `safe` or `unsafe`. When it's `unsafe`, it also outputs the unsafe category from the taxonomy. 

```python
moderator_response = llamaguard_pack.run("I love Christmas season!")
```

Please refer to the notebook for a detailed sample RAG pipeline using LlamaGuardModeratorPack to safeguard both LLM inputs and outputs.

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
