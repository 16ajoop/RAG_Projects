import json

from langchain_ollama import ChatOllama


# Local Ollama model
llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0,
    format="json"
)


def extract_relationships(
    text: str,
    entities: list[dict]
) -> list[dict]:
    """
    Extract relationships between entities mentioned in a text chunk.
    """

    entity_names = [entity["name"] for entity in entities]

    prompt = f"""
You are a precise relationship extraction system for a GraphRAG application.

Your job is to extract ONLY relationships that are explicitly stated
or clearly expressed in the provided text.

Known entities:
{entity_names}

Allowed relationship types:

WORKS_IN
- PERSON -> DEPARTMENT

WORKS_ON
- PERSON -> PROJECT

MANAGES
- PERSON -> PERSON
- PERSON -> DEPARTMENT
- PERSON -> PROJECT

COLLABORATES_WITH
- PERSON -> PERSON
- PERSON -> DEPARTMENT
- DEPARTMENT -> DEPARTMENT

USES
- PERSON -> TECHNOLOGY
- PROJECT -> TECHNOLOGY
- DEPARTMENT -> TECHNOLOGY

LOCATED_IN
- PERSON -> LOCATION
- DEPARTMENT -> LOCATION
- PROJECT -> LOCATION
- COMPANY -> LOCATION

HAS_DEPARTMENT
- COMPANY -> DEPARTMENT

HAS_PROJECT
- COMPANY -> PROJECT

BELONGS_TO
- PERSON -> COMPANY
- DEPARTMENT -> COMPANY
- PROJECT -> COMPANY

STRICT RULES:

1. A relationship MUST be supported by the actual text.

2. Do NOT create a relationship simply because two entities
   appear in the same paragraph or chunk.

3. Do NOT use world knowledge.

4. Do NOT guess.

5. Do NOT assume that every entity has a relationship with
   the company.

6. Relationship direction matters.

7. COMPANY can only be the source of:
   - HAS_DEPARTMENT
   - HAS_PROJECT
   - LOCATED_IN

8. COMPANY can NEVER be the source of:
   - WORKS_IN
   - WORKS_ON
   - MANAGES
   - BELONGS_TO

9. BELONGS_TO means the source entity is organizationally
   part of the target company.

10. If the text does not clearly support a relationship,
    DO NOT return it.

11. Use exact entity names from the known entity list.

12. Do not create new entities.

13. Do not duplicate relationships.

14. Return an empty list if no valid relationship exists.

Return ONLY valid JSON in exactly this format:

{{
    "relationships": [
        {{
            "source": "entity name",
            "relationship": "RELATIONSHIP_TYPE",
            "target": "entity name"
        }}
    ]
}}

Text:
{text}
"""

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)

        relationships = result.get("relationships", [])

        # Map each entity name to its entity type
        entity_types = {
            entity["name"].lower(): entity["type"]
            for entity in entities
        }

        # Allowed source -> target entity types
        allowed_relationships = {
            "WORKS_IN": [
                ("PERSON", "DEPARTMENT")
            ],

            "WORKS_ON": [
                ("PERSON", "PROJECT")
            ],

            "MANAGES": [
                ("PERSON", "PERSON"),
                ("PERSON", "DEPARTMENT"),
                ("PERSON", "PROJECT")
            ],

            "COLLABORATES_WITH": [
                ("PERSON", "PERSON"),
                ("PERSON", "DEPARTMENT"),
                ("DEPARTMENT", "DEPARTMENT")
            ],

            "USES": [
                ("PERSON", "TECHNOLOGY"),
                ("PROJECT", "TECHNOLOGY"),
                ("DEPARTMENT", "TECHNOLOGY")
            ],

            "LOCATED_IN": [
                ("PERSON", "LOCATION"),
                ("DEPARTMENT", "LOCATION"),
                ("PROJECT", "LOCATION"),
                ("COMPANY", "LOCATION")
            ],

            "HAS_DEPARTMENT": [
                ("COMPANY", "DEPARTMENT")
            ],

            "HAS_PROJECT": [
                ("COMPANY", "PROJECT")
            ],

            "BELONGS_TO": [
                ("PERSON", "COMPANY"),
                ("DEPARTMENT", "COMPANY"),
                ("PROJECT", "COMPANY")
            ]
        }

        valid_relationships = set(allowed_relationships.keys())

        unique_relationships = []
        seen = set()

        # Validate every relationship returned by the LLM
        for relationship in relationships:

            source = relationship.get("source", "").strip()
            relation = relationship.get("relationship", "").strip()
            target = relationship.get("target", "").strip()

            # Basic validation
            if not source or not relation or not target:
                continue

            # Relationship type must be allowed
            if relation not in valid_relationships:
                continue

            # Source and target must be different
            if source.lower() == target.lower():
                continue

            # Get entity types
            source_type = entity_types.get(source.lower())
            target_type = entity_types.get(target.lower())

            # Both entities must exist
            if not source_type or not target_type:
                continue

            # Check whether this source -> relationship -> target
            # combination is allowed
            allowed_pairs = allowed_relationships.get(
                relation,
                []
            )

            if (source_type, target_type) not in allowed_pairs:
                continue

            # Remove duplicates
            key = (
                source.lower(),
                relation.lower(),
                target.lower()
            )

            if key not in seen:
                seen.add(key)

                unique_relationships.append({
                    "source": source,
                    "relationship": relation,
                    "target": target
                })

        return unique_relationships

    except json.JSONDecodeError:
        print("Could not parse LLM response as JSON.")
        print(response.content)
        return []