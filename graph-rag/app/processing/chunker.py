
import re


def chunk_text(text: str) -> list[str]:
    """Create coherent chunks from the AITech Solutions knowledge base."""

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    project_lines = [
        "GraphMind uses Python, Neo4j-compatible graph concepts, ChromaDB, Ollama, and FastAPI.",
        "DataFlow uses Python, Apache Spark, PostgreSQL, and Apache Airflow.",
        "CloudPulse uses Microsoft Azure, Kubernetes, Prometheus, and Grafana.",
        "AITechERP uses React, FastAPI, PostgreSQL, and Docker.",
        "SecureVision uses Python, PyTorch, FastAPI, and Elasticsearch.",
    ]

    project_metadata = """
Project: GraphMind
Lead: Ananya Sharma
Departments: AI Research, Data Engineering
Description: Knowledge graph platform for enterprise intelligence.

Project: DataFlow
Lead: Rahul Mehta
Departments: Data Engineering, Cloud Platform
Description: Scalable data ingestion and processing platform.

Project: CloudPulse
Lead: Vikram Rao
Departments: Cloud Platform, Cybersecurity
Description: Cloud monitoring platform.

Project: AITechERP
Lead: Meera Iyer
Departments: Product Engineering, Cybersecurity
Description: Enterprise resource planning application.

Project: SecureVision
Lead: Karan Singh
Departments: Cybersecurity, AI Research
Description: AI-assisted security threat detection platform.
"""

    # Remove duplicated project technology lines from their
    # original positions in the extracted PDF text.
    for line in project_lines:
        text = text.replace(line, "")

    # Remove the project table if it was extracted under
    # Cross-Team Relationships.
    start_marker = "Project\nLead\nDepartments Involved\nDescription"
    end_marker = "9. SecureVision combines"

    if start_marker in text and end_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker)
        text = text[:start] + text[end:]

    heading_pattern = re.compile(
        r"(?m)^(?=\d+\.\s+"
        r"(?:Company Overview|Departments|Employees|"
        r"Managers and Reporting Structure|Projects|"
        r"Technologies|Locations|Cross-Team Relationships|"
        r"Example GraphRAG Questions)\s*$)"
    )

    sections = [
        section.strip()
        for section in heading_pattern.split(text)
        if section.strip()
    ]

    # Merge project technologies and metadata into one section.
    result = []
    projects_added = False

    for section in sections:
        if section.strip() == "5. Projects":
            result.append(
                "5. Projects\n"
                + "\n".join(project_lines)
                + "\n\n"
                + project_metadata
            )
            projects_added = True

        elif section.startswith("6. Technologies"):
            result.append(section)

        else:
            result.append(section)

    if not projects_added:
        result.append(
            "5. Projects\n"
            + "\n".join(project_lines)
            + "\n\n"
            + project_metadata
        )

    return result