# Resumer Screener Pack

This LlamaPack loads a resume file, and review it against a user specified job description and screening criteria.


## Usage

You can download the pack to a `./resume_screener_pack` directory:

```python
from llama_index.llama_packs import download_llama_pack

# download and install dependencies
ResumeScreenerPack = download_llama_pack(
  "ResumeScreenerPack", "./resume_screener_pack"
)
```

From here, you can use the pack, or inspect and modify the pack in `./resume_screener_pack`.

Then, you can set up the pack like so:

```python
# create the pack
resume_screener = ResumeScreenerPack(
    job_description="<general job description>",
    criteria=[
        "<job criterion>",
        "<another job criterion>"
    ]
)
```

The `run()` function is a light wrapper around `llm.complete()`.

```python
response = resume_screener.run(resume_path="resume.pdf")
print(response.overall_decision)
```

The `response` will be a pydantic model with the following schema

```python
class CriteriaDecision(BaseModel):
    """The decision made based on a single criteria"""
    decision: Field(type=bool, description="The decision made based on the criteria")
    reasoning: Field(type=str, description="The reasoning behind the decision")

class ResumeScreenerDecision(BaseModel):
    """The decision made by the resume screener"""
    criteria_decisions: Field(type=List[CriteriaDecision], description="The decisions made based on the criteria")
    overall_reasoning: Field(type=str, description="The reasoning behind the overall decision")
    overall_decision: Field(type=bool, description="The overall decision made based on the criteria")
```
