import json

from langchain_ollama import ChatOllama


# Local Ollama model
llm = ChatOllama(
    model = "llama3.2:latest",
    temperature = 0,
    format = "json",
    num_predict = 500
)

def extract_entities(text: str) -> list[dict]:
    """
    Extract entities from a text chunk using the local Ollama LLM.
    """

    prompt = f"""
Extract entities and explicitly stated relationships from this text.

Entity types:
PERSON, ROLE, DEPARTMENT, PROJECT, TECHNOLOGY, LOCATION, COMPANY

Relationship types:
WORKS_IN, WORKS_ON, MANAGES, COLLABORATES_WITH,
USES, LOCATED_IN, HAS_DEPARTMENT, HAS_PROJECT, BELONGS_TO

Rules:
- Extract only entities explicitly mentioned.
- Use exact names from the text.
- Do not invent entities or relationships.
- Do not infer relationships from simple co-occurrence.
- Use complete entity names.
- Return only valid JSON.

JSON format:
{{
  "entities": [
    {{"name": "X", "type": "PERSON"}}
  ],
  "relationships": [
    {{"source": "X", "relationship": "WORKS_IN", "target": "Y"}}
  ]
}}

TEXT:
{text}
"""

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)

        entities = result.get("entities", [])

        # Remove duplicate entities
        unique_entities = []
        seen = set()

        for entity in entities:
            name = entity.get("name", "").strip()
            entity_type = entity.get("type", "").strip()

            if not name or not entity_type:
                continue

            # Use lowercase name + type to detect duplicates
            key = (name.lower(), entity_type.lower())

            if key not in seen:
                seen.add(key)

                unique_entities.append({
                    "name": name,
                    "type": entity_type
                })

        return unique_entities



    except json.JSONDecodeError:
        print("Could not parse LLM response as JSON.")
        print(response.content)
        return []
