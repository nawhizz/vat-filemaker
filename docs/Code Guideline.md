# 🐍 Python + PySide6 Code Guideline for Cursor Development

This guideline is defined to ensure **consistency, maintainability**, and maximize the **code generation efficiency of the Cursor AI**, based on the provided TRD (Technical Requirements Document) and PRD (Product Requirements Document). All code must adhere to these principles.

---

## 1. 📘 General Python & Style

### PEP 8 Compliance
All Python code must strictly adhere to the **PEP 8 style guide**.

### Type Hinting (Mandatory)
* **Mandatory Use**: All function and method arguments, as well as return values, must explicitly use **type hints**.
    * This not only improves code clarity but also **critically impacts the accuracy** of Cursor's code analysis and generation.
* **Complex Types**: Use **`TypedDict`** or **`dataclass`** for explicitly defining complex data structures. (Utilize `app/utils/types.py`)
* **Clarity**: Clearly use `Optional` (for potential `None` values) and `Callable` (for callbacks).

### Docstrings
* All public modules, functions, classes, and methods must include **Docstrings** in the **Google or reST format**.
* Include clear explanations that the AI can reference during Cursor's `@` referencing and code analysis.

### Imports
* Imports must always be located at the top of the file and separated into **three groups**:
    1.  Standard Library
    2.  External Libraries (PySide6, pandas, etc.)
    3.  Internal Modules (`app...`)
* Internal module imports within `app/` should use **absolute paths** (e.g., `from app.services.vat_service import ...`).

### Environment
* Use a **project isolation environment (`venv`)** managed by **`uv`**. Dependencies must be managed via `requirements.txt` (or `pyproject.toml`).

---

## 2. 🏛️ Architecture (MVA and Logic Separation)

Strictly adhere to the **MVA (Model-View-Architecture)** and **Layered Architecture** defined in the TRD and PRD. This is crucial for future extensibility (e.g., with FastAPI).

### View (`app/views/`)
* **Role**: Responsible only for **pure UI logic** (widget creation, layout, signal connection).
* **Prohibited**: Absolutely **NO** business logic (e.g., complex calculations, conditional statements), database calls, or API calls.
* **Interaction**: Receives user input (signals), calls the **Service layer**, and updates the screen based on data change signals from the **Model**.

### Model (`app/models/`)
* **Role**: Must be a derivative of **`QAbstractItemModel`** (primarily `QAbstractTableModel`).
* **Responsibility**: Acts solely as an **interface** connecting the View (e.g., `QTableView`) and the data.
* **Prohibited**: Models **must not** call the DB or API directly. Data must be **injected (Set)** into the Model via the Service layer.

### Service (`app/services/`)
* **Role**: Responsible for **all business logic** (e.g., determining VAT exclusion status, statistical calculations).
* **Interaction**: Receives requests from the View, calls the Repository or API to process the data, and returns the result.
* **Prohibited**: Absolutely **NO** importing of PySide6/Qt-related modules (e.g., `PySide6.QtWidgets`). (Must be completely decoupled from the UI).

### Repository (`app/repositories/`)
* **Role**: Responsible for **all database access (CRUD) logic**.
* **Implementation**: Must be implemented using **SQLAlchemy ORM**. Models are defined in `schema.py`.
* **Prohibited**: **NO** inclusion of business logic. Focus solely on simple data input/output.

### Dependency Injection
* Dependencies between classes (e.g., `VatService` using `TaxpayerRepository`) must be injected through the **constructor (`__init__`)**.
* This facilitates the use of Mock objects for **unit testing** with `pytest`.

---

## 3. 🎨 PySide6 and UI

### Widget Naming
* Class variables for declared widgets must use **`snake_case`** and explicitly state the **widget type** in the name or type hint.
    * **Example**: `self.card_table_view: QTableView`, `self.taxpayer_search_bar: SearchBar`, `self.save_button: PushButton`

### Signals & Slots
* Slot method naming must follow the convention: **`on_[widget_name]_[signal_name]`**.
    * **Example**: `self.save_button.clicked.connect(self.on_save_button_clicked)`
* Avoid using `lambda` for anything more than simple argument passing; define clear slot methods instead.

### UI Design Consistency
* All UI components must use **`PySide6-Fluent-Widgets`** to maintain design consistency.
* Avoid mixing standard Qt widgets (e.g., `QPushButton`) with Fluent widgets (e.g., `PrimaryPushButton`).

### Resource Management
* Icons, QSS, and other resources must be managed in the **`resources/`** directory. It is recommended to embed them into the binary using the **Qt Resource System (.qrc)**.

### Handling Long Operations
* Tasks taking longer than **0.5 seconds** (e.g., Excel loading, API calls) must be processed in a separate thread using **`QThread`** or **`QRunnable`**. (Prevents the UI from 'freezing').

---

## 4. 🤖 Cursor (AI IDE) Utilization

### Prompt Clarity
* When requesting code generation from the AI, use the **`@` symbol** to explicitly reference relevant files or folders.
    * **Example**: "In the `@app/services/vat_service.py` file, add VAT exclusion logic using the `VatExclusionRule` type from `@app/utils/types.py`."

### TRD/PRD Reference
* Use the `@` feature to include this guideline, `trd.md`, and `prd.md` in the AI's context to encourage the generation of consistent code.

### AI Code Verification (Trust but Verify)
* **Never blindly trust** the code generated by Cursor.
* **Always review and correct** the generated code to ensure it adheres to the MVA architecture principles (e.g., the Service layer doesn't encroach on the UI) and type hinting rules.

---

## 5. 🧪 Testing and Logging

### Testing
* Use **`pytest`**. Write test code in the **`tests/`** directory, mirroring the architecture structure.
* **Service** and **Repository** layers are mandatory for unit testing.
* Use **`pytest-mock`** to Mock dependencies (e.g., DB, API).

### Logging
* Avoid using `print()`. Use the **Python standard `logging` module**.
* Configure the logger in `app/utils/logger.py` or `main.py`.
* Clearly differentiate and use `DEBUG`, `INFO`, `WARNING`, and `ERROR` levels for recording logs.