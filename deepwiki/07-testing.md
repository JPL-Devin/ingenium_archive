# Testing

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [tests/requirements.txt](tests/requirements.txt)
- [tests/test_ci_executions.py](tests/test_ci_executions.py)
- [tests/test_ci_health.py](tests/test_ci_health.py)
- [tests/test_ci_procedures.py](tests/test_ci_procedures.py)

</details>



The Ingenium Archive Service employs a two-tier testing strategy to ensure both the reliability of the API in a CI/CD environment and the correctness of complex graph database operations during development. This strategy balances high-level integration testing with low-level database exploration.

### Testing Strategy Overview

The testing infrastructure is divided into two primary directories based on the target and language:

1.  **Python Integration Tests (`tests/`)**: A comprehensive suite of end-to-end tests that interact with the service via its HTTP API. These are integrated into the Jenkins CI pipeline to validate releases and pull requests.
2.  **JavaScript Database Scripts (`tests/db/`)**: A collection of standalone Node.js scripts used by developers to test ArangoDB queries, graph traversals, and document manipulation logic in isolation.

### System Test Topology

The following diagram illustrates how the testing tiers interact with the system components:

**Testing Architecture and Data Flow**
```mermaid
graph TD
    subgraph "Test Suites"
        [Python_CI] -- "HTTP/REST" --> [Express_API]
        [JS_DB_Scripts] -- "ArangoJS Driver" --> [ArangoDB]
    end

    subgraph "Ingenium Archive Service"
        [Express_API] --> [Controller_Layer]
        [Controller_Layer] --> [Logic_Layer]
        [Logic_Layer] --> [ArangoDB]
    end

    subgraph "Infrastructure"
        [ArangoDB] -- "Persists" --> [Collections/Graphs]
    end

    style Python_CI stroke-dasharray: 5 5
    style JS_DB_Scripts stroke-dasharray: 5 5
```
Sources: `tests/test_ci_executions.py:1-31`(), `tests/test_ci_procedures.py:1-14`()

---

### 7.1 Python Integration Tests

The Python test suite serves as the primary validation gate for the service. It utilizes the `ingenium_client` library to simulate real-world client interactions, covering the full lifecycle of procedures and executions.

*   **Technology Stack**: Python 3, `unittest`, `requests`, and `ingenium_client`.
*   **Key Components**:
    *   **Core Logic**: Tests for procedures [tests/test_ci_procedures.py:14-21]() and executions [tests/test_ci_executions.py:31-32]() validate complex operations like element copying across executions [tests/test_ci_executions.py:132-135]() and versioning transitions.
    *   **Infrastructure Tests**: Health checks [tests/test_ci_health.py:12-19]() and logging level adjustments are verified to ensure operational stability.
    *   **Configuration**: The `config.py` file manages environment variables such as `ARCHIVE_ING_URL` to point tests at local, dev, or cluster environments.

For details on running these tests and the full list of test modules, see [Python Integration Tests](#7.1).

**Sources**: [tests/requirements.txt:1-8](), [tests/test_ci_executions.py:1-12](), [tests/test_ci_health.py:19-32]()

---

### 7.2 JavaScript Database Exploration Scripts

The `tests/db/` directory contains "sandbox" scripts designed for rapid prototyping and debugging of ArangoDB AQL queries and graph logic. Unlike the CI tests, these scripts often bypass the HTTP layer and interact directly with the database.

*   **Purpose**: To verify complex recursive logic (e.g., `promise_recursive.js`) and graph traversals (e.g., `traverse_test.js`) before implementing them in `base_funcs.js`.
*   **Fixture Support**: Uses JSON files like `execution.json` to seed the database with known states for reproducible testing of numbering and tree-building logic.
*   **Coverage**: Includes scripts for testing conditional updates, set operations, and large-scale tree structures (`big_tree_example.js`).

For a catalog of available scripts and their specific use cases, see [JavaScript Database Exploration Scripts](#7.2).

**Sources**: [tests/test_ci_executions.py:1-12]() (Contextual reference to test structure).

---

### Relationship Between Test Entities and Code

The following table maps the testing concerns to the specific code entities they validate.

| Testing Tier | Target Code Entity | Validation Focus |
| :--- | :--- | :--- |
| **Python CI** | `ProceduresService.js` | HTTP Status Codes, API Schema compliance, end-to-end workflows. |
| **Python CI** | `ExecutionService.js` | Lifecycle transitions (e.g., `START` to `COMPLETED`), permission scopes. |
| **JS Scripts** | `base_funcs.js` | AQL Query performance, recursive tree building, `update_number` logic. |
| **JS Scripts** | `node_funcs.js` | Graph edge consistency during `copyElement` or `moveElement`. |

**Entity Mapping Diagram**
```mermaid
graph LR
    subgraph "Python CI Space"
        [ExecutionsTest] -- "validates" --> [Execution_Controller]
        [ProcedureTest] -- "validates" --> [Procedures_Controller]
    end

    subgraph "JS DB Space"
        [ptest.js] -- "direct access" --> [procedure_graph]
        [etest.js] -- "direct access" --> [execution_graph]
        [tree_example.js] -- "logic test" --> [buildElementTree]
    end

    subgraph "Service Implementation"
        [Execution_Controller] --> [node_funcs.js]
        [Procedures_Controller] --> [procedure_funcs.js]
        [node_funcs.js] --> [base_funcs.js]
        [procedure_funcs.js] --> [base_funcs.js]
    end
```
Sources: `tests/test_ci_executions.py:31-61`(), `tests/test_ci_procedures.py:14-57`()

---
