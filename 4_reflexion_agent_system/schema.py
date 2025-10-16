from pydantic import BaseModel, Field
from typing import List

# --- Reflection Model ---
class Reflection(BaseModel):
    """
    Reflection on the quality of an answer.
    """
    missing: str = Field(
        description="What important or relevant information is missing from the answer."
    )
    superfluous: str = Field(
        description="What unnecessary or redundant content is present in the answer."
    )

# --- Initial Answer Model ---
class AnswerQuestion(BaseModel):
    """
    Initial response tool: answer + reflection + search queries.
    """
    answer: str = Field(
        description="A detailed (~250 words) answer to the user's question."
    )
    reflection: Reflection = Field(
        description="Critical self-evaluation of the answer, highlighting missing and superfluous parts."
    )
    search_queries: List[str] = Field(
        description="1 to 3 search queries that would help improve the answer."
    )

# --- Revised Answer Model ---
class ReviseAnswer(BaseModel):
    """
    Final, improved answer with citations.
    """
    answer: str = Field(
        description="A revised, improved answer under 250 words, including numerical citations."
    )
    reflection: Reflection = Field(
        description="Reflection on improvements made and remaining limitations."
    )
    search_queries: List[str] = Field(
        default_factory=list,
        description="Must be an empty list ([]). No further research is required after revision."
    )
    references: List[str] = Field(
        description="A list of reference URLs or citations, e.g., '[1] https://example.com' or 'https://example.com'."
    )
