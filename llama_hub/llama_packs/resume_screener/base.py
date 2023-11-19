from pathlib import Path
from typing import Any, Dict, List
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.readers import PDFReader
from llama_index.schema import NodeWithScore
from llama_index.response_synthesizers import TreeSummarize

from pydantic import BaseModel, Field

QUERY_TEMPLATE = """
You are an expert resume reviewer. 
You job is to decide if the candidate pass the resume screen given the job description and a list of criteria:

### Job Description
{job_description}

### Criteria
{criteria_str}
"""



class CriteriaDecision(BaseModel):
    """The decision made based on a single criteria"""
    decision: Field(type=bool, description="The decision made based on the criteria")
    reasoning: Field(type=str, description="The reasoning behind the decision")


class ResumeScreenerDecision(BaseModel):
    """The decision made by the resume screener"""
    criteria_decisions: Field(type=List[CriteriaDecision], description="The decisions made based on the criteria")
    overall_reasoning: Field(type=str, description="The reasoning behind the overall decision")
    overall_decision: Field(type=bool, description="The overall decision made based on the criteria")


class ResumeScreenerPack(BaseLlamaPack):
    def __init__(self, job_description: str, criteria: List[str]) -> None:
        self.reader = PDFReader()
        self.synthesizer = TreeSummarize()

        criteria_str = ""
        for criterion in criteria:
            criteria_str += f"- {criterion}\n"
        self.query = QUERY_TEMPLATE.format(job_description=job_description, criteria_str=criteria_str)

    def get_modules(self) -> Dict[str, Any]:
        return {
            "reader": self.reader,
            "synthesizer": self.synthesizer
        }
    
    def run(self, resume_path: str, *args: Any, **kwargs: Any) -> Any:
        docs = self.reader.load_data(Path(resume_path))
        output = self.synthesizer.synthesize(
            query=self.query,
            nodes=[NodeWithScore(node=doc, score=1.0) for doc in docs],
        )
        return output
    

