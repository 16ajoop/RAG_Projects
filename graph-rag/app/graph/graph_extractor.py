
import json
import re

from langchain_ollama import ChatOllama


# --------------------------------------------------
# LLM CONFIGURATION
# --------------------------------------------------

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0,
    format="json",
    num_predict=2048,
)


# --------------------------------------------------
# ALLOWED ENTITY TYPES
# --------------------------------------------------

ALLOWED_ENTITY_TYPES = {
    "PERSON",
    "ROLE",
    "DEPARTMENT",
    "PROJECT",
    "TECHNOLOGY",
    "LOCATION",
    "COMPANY",
}


KNOWN_DEPARTMENTS = {
    "ai research": "AI Research",
    "data engineering": "Data Engineering",
    "cloud platform": "Cloud Platform",
    "product engineering": "Product Engineering",
    "cybersecurity": "Cybersecurity",
}

KNOWN_PROJECTS = {
    "graphmind": "GraphMind",
    "dataflow": "DataFlow",
    "cloudpulse": "CloudPulse",
    "aitecherp": "AITechERP",
    "securevision": "SecureVision",
}

KNOWN_TECHNOLOGIES = {
    "python": "Python",
    "fastapi": "FastAPI",
    "chromadb": "ChromaDB",
    "ollama": "Ollama",
    "neo4j": "Neo4j",
    "apache spark": "Apache Spark",
    "postgresql": "PostgreSQL",
    "apache airflow": "Apache Airflow",
    "microsoft azure": "Microsoft Azure",
    "azure": "Azure",
    "kubernetes": "Kubernetes",
    "prometheus": "Prometheus",
    "grafana": "Grafana",
    "react": "React",
    "docker": "Docker",
    "pytorch": "PyTorch",
    "elasticsearch": "Elasticsearch",
}

KNOWN_LOCATIONS = {
    "chennai": "Chennai",
    "bengaluru": "Bengaluru",
    "hyderabad": "Hyderabad",
    "pune": "Pune",
    "india": "India",
}

# These names are used only to parse the employee table
# in the synthetic company knowledge base.
KNOWN_EMPLOYEES = [
    "Ananya Sharma",
    "Rahul Mehta",
    "Vikram Rao",
    "Meera Iyer",
    "Karan Singh",
    "Priya Nair",
    "Arjun Patel",
    "Sneha Kapoor",
    "Rohan Das",
    "Divya Menon",
    "Pooja V",
]


# --------------------------------------------------
# ALLOWED RELATIONSHIP PATTERNS
# --------------------------------------------------

ALLOWED_RELATIONSHIPS = {
    "WORKS_IN": [
        ("PERSON", "DEPARTMENT"),
    ],
    "HAS_ROLE": [
        ("PERSON", "ROLE"),
    ],
    "WORKS_ON": [
        ("PERSON", "PROJECT"),
    ],
    "MANAGES": [
        ("PERSON", "PERSON"),
        ("PERSON", "DEPARTMENT"),
        ("PERSON", "PROJECT"),
    ],
    "REPORTS_TO": [
        ("PERSON", "PERSON"),
    ],
    "COLLABORATES_WITH": [
        ("PERSON", "PERSON"),
        ("PERSON", "DEPARTMENT"),
        ("DEPARTMENT", "DEPARTMENT"),
    ],
    "USES": [
        ("PERSON", "TECHNOLOGY"),
        ("PROJECT", "TECHNOLOGY"),
        ("DEPARTMENT", "TECHNOLOGY"),
    ],
    "LOCATED_IN": [
        ("PERSON", "LOCATION"),
        ("DEPARTMENT", "LOCATION"),
        ("PROJECT", "LOCATION"),
        ("COMPANY", "LOCATION"),
    ],
    "HAS_DEPARTMENT": [
        ("COMPANY", "DEPARTMENT"),
    ],
    "HAS_PROJECT": [
        ("COMPANY", "PROJECT"),
    ],
    "BELONGS_TO": [
        ("PERSON", "COMPANY"),
        ("DEPARTMENT", "COMPANY"),
        ("PROJECT", "COMPANY"),
    ],
    "CONTRIBUTES_TO": [
        ("PERSON", "PROJECT"),
        ("PERSON", "DEPARTMENT"),
    ],
    "RECEIVES_DATA_FROM": [
        ("PROJECT", "PROJECT"),
        ("DEPARTMENT", "PROJECT"),
        ("PROJECT", "DEPARTMENT"),
    ],
    "ADVISES": [
        ("PERSON", "PERSON"),
        ("PERSON", "PROJECT"),
        ("PERSON", "DEPARTMENT"),
    ],
    "INTEGRATES": [
        ("PERSON", "TECHNOLOGY"),
        ("PERSON", "PROJECT"),
        ("PROJECT", "TECHNOLOGY"),
        ("PROJECT", "PROJECT"),
    ],
    "SUPPORTS": [
        ("PERSON", "PERSON"),
        ("PERSON", "PROJECT"),
        ("PERSON", "DEPARTMENT"),
        ("PROJECT", "PROJECT"),
        ("PROJECT", "DEPARTMENT"),
        ("DEPARTMENT", "PROJECT"),
        ("DEPARTMENT", "DEPARTMENT"),
    ],
}


# --------------------------------------------------
# GENERAL HELPERS
# --------------------------------------------------

def normalize_entity_type(name: str, entity_type: str) -> str:
    """Correct entity types for known names."""

    key = name.casefold().strip()

    if key in KNOWN_DEPARTMENTS:
        return "DEPARTMENT"

    if key in KNOWN_PROJECTS:
        return "PROJECT"

    if key in KNOWN_TECHNOLOGIES:
        return "TECHNOLOGY"

    if key in KNOWN_LOCATIONS:
        return "LOCATION"

    return entity_type.strip().upper()


def add_entity(entities, seen, name, entity_type):
    """Add one valid entity without duplicates."""

    if not isinstance(name, str) or not isinstance(entity_type, str):
        return

    name = name.strip()
    entity_type = entity_type.strip().upper()

    if not name or entity_type not in ALLOWED_ENTITY_TYPES:
        return

    entity_type = normalize_entity_type(name, entity_type)
    key = (name.casefold(), entity_type)

    if key not in seen:
        seen.add(key)
        entities.append({
            "name": name,
            "type": entity_type,
        })


def add_relationship(
    relationships,
    seen,
    source,
    relation,
    target,
):
    """Add a relationship without duplicates or empty fields."""

    if not all(
        isinstance(value, str)
        for value in (source, relation, target)
    ):
        return

    source = source.strip()
    relation = relation.strip().upper()
    target = target.strip()

    if not source or not relation or not target:
        return

    if source.casefold() == target.casefold():
        return

    key = (
        source.casefold(),
        relation,
        target.casefold(),
    )

    if key not in seen:
        seen.add(key)
        relationships.append({
            "source": source,
            "relationship": relation,
            "target": target,
        })


def find_last_match(text, candidates):
    """
    Find the last occurrence of any candidate in text.
    Returns (start, end, canonical_name), or None.
    """

    matches = []

    for key, canonical_name in candidates.items():
        pattern = re.compile(
            r"(?<!\w)" + re.escape(key) + r"(?!\w)",
            re.IGNORECASE,
        )

        for match in pattern.finditer(text):
            matches.append(
                (match.start(), match.end(), canonical_name)
            )

    if not matches:
        return None

    return max(matches, key=lambda item: item[0])


# --------------------------------------------------
# DETERMINISTIC EMPLOYEE TABLE EXTRACTION
# --------------------------------------------------

def extract_employee_table(text: str):
    """
    Parse the known synthetic employee table without an LLM.

    Handles job titles wrapped across lines and the stray 'E'
    appearing before Pooja V's department in the cleaned chunk.
    """

    normalized = re.sub(r"\s+", " ", text).strip()

    entities = []
    relationships = []
    seen_entities = set()
    seen_relationships = set()

    # Locate employee names in their source order.
    occurrences = []

    for employee in KNOWN_EMPLOYEES:
        pattern = re.compile(
            r"(?<!\w)" + re.escape(employee) + r"(?!\w)",
            re.IGNORECASE,
        )
        match = pattern.search(normalized)

        if match:
            occurrences.append(
                (match.start(), match.end(), employee)
            )

    occurrences.sort(key=lambda item: item[0])

    if not occurrences:
        return [], []

    for index, (start, end, employee) in enumerate(occurrences):
        next_start = (
            occurrences[index + 1][0]
            if index + 1 < len(occurrences)
            else len(normalized)
        )

        # Text between this employee's name and the next employee.
        record = normalized[end:next_start].strip()

        # Find the location in this employee's record.
        location_match = find_last_match(
            record,
            KNOWN_LOCATIONS,
        )

        if not location_match:
            print(
                f"Warning: no known location found for {employee}. "
                "Skipping this employee record."
            )
            continue

        location_start, _, location = location_match
        before_location = record[:location_start].strip()

        # The department appears after the role. Selecting the
        # last matching department avoids confusing a role such
        # as "AI Research Lead" with the Department column.
        department_match = find_last_match(
            before_location,
            KNOWN_DEPARTMENTS,
        )

        if not department_match:
            print(
                f"Warning: no known department found for {employee}. "
                "Skipping this employee record."
            )
            continue

        department_start, department_end, department = (
            department_match
        )

        role = before_location[:department_start].strip()

        # Clean common column/header artefacts.
        role = re.sub(r"^(?:Role\s+)?", "", role, flags=re.I)
        role = re.sub(r"\s+", " ", role).strip()
        role = re.sub(r"\s+E$", "", role).strip()

        if role.casefold() in {"employee", "role", "department"}:
            role = ""

        add_entity(
            entities, seen_entities, employee, "PERSON"
        )
        add_entity(
            entities, seen_entities, department, "DEPARTMENT"
        )
        add_entity(
            entities, seen_entities, location, "LOCATION"
        )

        add_relationship(
            relationships,
            seen_relationships,
            employee,
            "WORKS_IN",
            department,
        )

        add_relationship(
            relationships,
            seen_relationships,
            employee,
            "LOCATED_IN",
            location,
        )

        if role:
            add_entity(entities, seen_entities, role, "ROLE")
            add_relationship(
                relationships,
                seen_relationships,
                employee,
                "HAS_ROLE",
                role,
            )

    print(
        "Employee table extraction completed without an LLM: "
        f"{len(entities)} entities, "
        f"{len(relationships)} relationships."
    )

    return entities, relationships


# --------------------------------------------------
# LLM EXTRACTION FOR OTHER CHUNKS
# --------------------------------------------------

def extract_json_object(response_text: str) -> dict:
    """Parse a complete JSON object."""

    result = json.loads(response_text)

    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object.")

    return result


def extract_with_llm(text: str):
    """Extract graph data from non-employee chunks."""

    prompt = f"""
Extract a knowledge graph from the text below.

Return JSON only in this format:
{{
  "entities": [
    {{"name": "exact name from text", "type": "PERSON"}}
  ],
  "relationships": [
    {{
      "source": "exact source name",
      "relationship": "WORKS_IN",
      "target": "exact target name"
    }}
  ]
}}

Allowed entity types:
PERSON, ROLE, DEPARTMENT, PROJECT, TECHNOLOGY, LOCATION, COMPANY

Allowed relationship types:
WORKS_IN, HAS_ROLE, WORKS_ON, MANAGES, REPORTS_TO,
COLLABORATES_WITH, USES, LOCATED_IN, HAS_DEPARTMENT,
HAS_PROJECT, BELONGS_TO, CONTRIBUTES_TO, RECEIVES_DATA_FROM,
ADVISES, INTEGRATES, SUPPORTS

Rules:
- Use only facts explicitly stated in this text.
- Copy entity names exactly as written.
- Extract a relationship only when the text explicitly supports it.
- Do not infer a department's location from a person's location.
- Do not assign a location to a department or project unless the
  text explicitly connects that department or project to the location.
- Do not use facts from outside this text.
- Do not add example facts or explanations.
- Include both arrays, even if one is empty.
- Keep the output concise and do not repeat items.

TEXT:
{text}
"""

    response = llm.invoke(prompt)
    response_text = response.content

    if not isinstance(response_text, str):
        raise ValueError("LLM response content was not text.")

    metadata = getattr(response, "response_metadata", {}) or {}

    if metadata.get("done_reason") == "length":
        raise ValueError("LLM output reached its token limit.")

    result = extract_json_object(response_text)

    entities_data = result.get("entities", [])
    relationships_data = result.get("relationships", [])

    if not isinstance(entities_data, list):
        entities_data = []

    if not isinstance(relationships_data, list):
        relationships_data = []

    entities = []
    seen_entities = set()

    for item in entities_data:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        entity_type = item.get("type")

        if not isinstance(name, str) or not isinstance(entity_type, str):
            continue

        name = name.strip()
        entity_type = entity_type.strip().upper()

        if not name or entity_type not in ALLOWED_ENTITY_TYPES:
            continue

        # Only retain names present in the current chunk.
        if name.casefold() not in text.casefold():
            continue

        if name.casefold() in {
            "sharma", "mehta", "rao", "iyer", "singh"
        }:
            continue

        add_entity(entities, seen_entities, name, entity_type)

    entity_types = {
        entity["name"].casefold(): entity["type"]
        for entity in entities
    }

    relationships = []
    seen_relationships = set()

    for item in relationships_data:
        if not isinstance(item, dict):
            continue

        source = item.get("source")
        relation = item.get("relationship")
        target = item.get("target")

        if not all(
            isinstance(value, str)
            for value in (source, relation, target)
        ):
            continue

        source = source.strip()
        relation = relation.strip().upper()
        target = target.strip()

        source_type = entity_types.get(source.casefold())
        target_type = entity_types.get(target.casefold())

        if not source_type or not target_type:
            continue

        allowed_pairs = ALLOWED_RELATIONSHIPS.get(relation, [])

        if (source_type, target_type) not in allowed_pairs:
            continue

        # Both endpoints must occur in this chunk.
        if (
            source.casefold() not in text.casefold()
            or target.casefold() not in text.casefold()
        ):
            continue

        add_relationship(
            relationships,
            seen_relationships,
            source,
            relation,
            target,
        )

    print(
        f"LLM extraction completed: {len(entities)} entities, "
        f"{len(relationships)} relationships."
    )

    return entities, relationships


# --------------------------------------------------
# DETERMINISTIC PROJECT EXTRACTION
# --------------------------------------------------

def extract_project_section(text: str):
    """Extract project facts directly from the known project section."""

    entities = []
    relationships = []
    seen_entities = set()
    seen_relationships = set()

    def add(name, entity_type):
        add_entity(entities, seen_entities, name, entity_type)

    def rel(source, relation, target):
        add_relationship(
            relationships,
            seen_relationships,
            source,
            relation,
            target,
        )

    # Company entity is included only when its name is present.
    company = "AITech Solutions"
    if company.casefold() in text.casefold():
        add(company, "COMPANY")

    # Exact project technology lists from the source PDF.
    project_technologies = {
        "GraphMind": [
            "Python",
            "Neo4j-compatible graph concepts",
            "ChromaDB",
            "Ollama",
            "FastAPI",
        ],
        "DataFlow": [
            "Python",
            "Apache Spark",
            "PostgreSQL",
            "Apache Airflow",
        ],
        "CloudPulse": [
            "Microsoft Azure",
            "Kubernetes",
            "Prometheus",
            "Grafana",
        ],
        "AITechERP": [
            "React",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ],
        "SecureVision": [
            "Python",
            "PyTorch",
            "FastAPI",
            "Elasticsearch",
        ],
    }

    project_details = {
        "GraphMind": {
            "lead": "Ananya Sharma",
            "departments": ["AI Research", "Data Engineering"],
        },
        "DataFlow": {
            "lead": "Rahul Mehta",
            "departments": ["Data Engineering", "Cloud Platform"],
        },
        "CloudPulse": {
            "lead": "Vikram Rao",
            "departments": ["Cloud Platform", "Cybersecurity"],
        },
        "AITechERP": {
            "lead": "Meera Iyer",
            "departments": ["Product Engineering", "Cybersecurity"],
        },
        "SecureVision": {
            "lead": "Karan Singh",
            "departments": ["Cybersecurity", "AI Research"],
        },
    }

    # Only extract projects whose names actually occur in this text.
    text_lower = text.casefold()

    for project, technologies in project_technologies.items():
        if project.casefold() not in text_lower:
            continue

        add(project, "PROJECT")

        if company.casefold() in text_lower:
            rel(company, "HAS_PROJECT", project)
            rel(project, "BELONGS_TO", company)

        details = project_details[project]
        lead = details["lead"]

        if lead.casefold() in text_lower:
            add(lead, "PERSON")
            rel(lead, "WORKS_ON", project)

        for department in details["departments"]:
            if department.casefold() in text_lower:
                add(department, "DEPARTMENT")
                rel(project, "SUPPORTS", department)

        for technology in technologies:
            if technology.casefold() not in text_lower:
                continue

            add(technology, "TECHNOLOGY")
            rel(project, "USES", technology)

    print(
        f"Project extraction completed without an LLM: "
        f"{len(entities)} entities, "
        f"{len(relationships)} relationships."
    )

    return entities, relationships

# --------------------------------------------------
# PUBLIC EXTRACTION FUNCTION
# --------------------------------------------------

def extract_graph_data(text: str) -> tuple[list[dict], list[dict]]:
    """
    Extract entities and relationships.

    The known employee table is parsed deterministically.
    Other chunks are processed by the local Ollama model.
    """

    if not isinstance(text, str) or not text.strip():
        return [], []


    if re.search(r"\b3\.\s*Employees\b", text, re.IGNORECASE):
        return extract_employee_table(text)

    if re.search(r"\b5\.\s*Projects\b", text, re.IGNORECASE):
        return extract_project_section(text)

    try:
        return extract_with_llm(text)

    except Exception as exc:
        print(
            f"Graph extraction failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return [], []
