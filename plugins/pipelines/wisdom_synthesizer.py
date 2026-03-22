import logging
from typing import List, Optional
from pydantic import BaseModel


class Pipeline:
    """
    This pipeline optimizes the prompt used for multi-model  summarization requests.

    It intercepts the request intended to summarize responses from various models, 
    extracts the original user query and the individual model answers,
    and constructs a new, more detailed and structured prompt.

    The optimized prompt guides the summarizing model to act as an expert analyst,
    synthesizing the inputs into a high-quality, comprehensive integrated report.
    """

    class Valves(BaseModel):
        # Specifies target pipeline IDs (models) this filter will attach to.
        # Use ["*"] to connect to all pipelines.
        pipelines: List[str] = ["*"]

        # Assigns priority to the filter pipeline.
        # Determines execution order (lower numbers execute first).
        priority: int = 0

        # Specifies model ID for analysis and summarization.
        # If set, the aggregate request will be redirected to this model.
        model_id: Optional[str] = None

        # Trigger prefix for aggregate requests.
        # Used to identify if it is an aggregate synthesis request.
        trigger_prefix: str = (
            "You have been provided with a set of responses from various models to the latest user query"
        )

        # Marker for parsing the original query start
        query_start_marker: str = 'the latest user query: "'

        # Marker for parsing the original query end
        query_end_marker: str = '"\n\nYour task is to'

        # Marker for parsing model responses start
        response_start_marker: str = "Responses from models: "

    def __init__(self):
        self.type = "filter"
        self.name = "wisdom_synthesizer"
        self.valves = self.Valves()

    async def on_startup(self):
        pass

    async def on_shutdown(self):
        pass

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        """
        Entry point for the pipeline filter.

        Checks if the request is an aggregate request. If yes, parses the original prompt,
        extracts query & responses, builds a dynamically-structured new prompt, 
        and replaces the original message content.
        """
        logging.info(f"pipe:{__name__}")

        messages = body.get("messages", [])
        if not messages:
            return body

        user_message_content = ""
        user_message_index = -1

        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "user":
                content = messages[i].get("content", "")
                if isinstance(content, list):
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            text_parts.append(item.get("text", ""))
                        elif isinstance(item, str):
                            text_parts.append(item)
                    user_message_content = "".join(text_parts)
                elif isinstance(content, str):
                    user_message_content = content

                user_message_index = i
                break

        if user_message_index == -1:
            return body

        if isinstance(user_message_content, str) and user_message_content.startswith(
            self.valves.trigger_prefix
        ):
            logging.info("Detected aggregate request, modifying prompt.")

            if self.valves.model_id:
                logging.info(f"Redirecting request to model: {self.valves.model_id}")
                body["model"] = self.valves.model_id

            query_start_phrase = self.valves.query_start_marker
            query_end_phrase = self.valves.query_end_marker
            start_index = user_message_content.find(query_start_phrase)
            end_index = user_message_content.find(query_end_phrase)

            original_query = ""
            if start_index != -1 and end_index != -1:
                original_query = user_message_content[
                    start_index + len(query_start_phrase) : end_index
                ]

            responses_start_phrase = self.valves.response_start_marker
            responses_start_index = user_message_content.find(responses_start_phrase)

            responses_text = ""
            if responses_start_index != -1:
                responses_text = user_message_content[
                    responses_start_index + len(responses_start_phrase) :
                ]

            import re
            responses = [
                part.strip() for part in re.split(r'\n?\"\"\"\n?', responses_text) if part.strip()
            ]

            responses_section = ""
            for i, response in enumerate(responses):
                responses_section += f'''"""
[Complete Response from Model {i + 1}]
{response}
"""
'''

            merge_prompt = f'''# Role Definition
You are an experienced Chief Analyst processing analysis reports from multiple independent AI expert teams regarding the same question. Your task is to perform deep integration, critical analysis, and distill a structured, insightful, and highly actionable comprehensive report for decision-makers.

# Original User Query
{original_query}

# Input Format Instruction ⚠️ IMPORTANT
The responses from various models have been accurately identified and separated using an artificial """ (triple quote) delimiter. The system has extracted these distinct answers; you must now analyze based on the separated content below.

**Separated Model Responses**:
{responses_section}

# Core Tasks
Do not simply copy or concatenate the original reports. Use your professional analytical skills to complete the following steps:

## 1. Analysis & Evaluation
- **Accurate Separation**: Verified boundaries using the """ delimiter.
- **Credibility Assessment**: Critically examine each report for potential biases, errors, or inconsistencies.
- **Logic Tracing**: Smooth out core arguments and reasoning chains.

## 2. Insight Extraction
- **Identify Consensus**: Find points or recommendations uniformly mentioned across models. This represents the core facts or robust strategies.
- **Highlight Divergences**: Explicitly state key disagreements in perspectives, methods, or forecasts.
- **Capture Highlights**: Unearth innovative views found only in a single report.

## 3. Comprehensive Reporting
Based on the analysis above, generate a synthesis containing:

### **【Core Consensus】**
- List key information or advice agreed upon by models.
- Annotate coverage (e.g., "All models agree" or "Majority of models").

### **【Key Divergences】**
- Contrast different viewpoints on core issues clearly.
- Use descriptive references (e.g., "Perspective Camp A vs B").

### **【Unique Insights】**
- Present high-value unique advice or perspectives from standalone reports.

### **【Synthesis & Recommendation】**
- **Integration**: A balanced final analysis optimized by your professional judgment.
- **Recommendation**: Formulate actionable blended strategies.

# Format Requirements
- Concise language, clear logic, distinct structure.
- Use bolding, lists, and headings for readability.
- **Language Alignment**: You MUST respond in the **SAME LANGUAGE** as the `Original User Query` above (e.g., if the user query is in Chinese, reply in Chinese; if in English, reply in English). Translate all section headers for your output.

# Output Structure Example
Output should follow this structure:

## 【Core Consensus】
✓ [Consensus Point 1] —— All models agree
✓ [Consensus Point 2] —— Majority of models agree

## 【Key Divergences】
⚡ **Divergence on [Topic]**:
- Perspective Camp A: ...
- Perspective Camp B: ...

## 【Unique Insights】
💡 [Insight from Model A]: ...
💡 [Insight from Model B]: ...

## 【Synthesis & Recommendation】
Based on the analysis above, recommended strategies: ...
'''

            body["messages"][user_message_index]["content"] = merge_prompt
            logging.info("Prompt dynamically replaced successfully.")

        return body
