# Capacity Management

Interactive lecture slides on capacity management, queueing theory, and staffing decisions — built with [marimo](https://marimo.io).

## Topics Covered

1. **Queueing Fundamentals** — arrival rate (λ), service rate (μ), utilization (ρ), Little's Law
2. **What Drives Waiting** — the nonlinear relationship between utilization and wait times
3. **Design Levers** — pooling resources and reducing variability
4. **Staffing Decisions** — matching capacity to time-varying demand

## Getting Started

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
# Clone the repository
git clone https://github.com/OperationsManagmentMBA/05_CapacityManagement.git
cd 05_CapacityManagement

# Install dependencies
uv sync

# Run the notebook
uv run marimo run capacity.py
```

### Slide Mode

To view as a presentation:

```bash
uv run marimo run capacity.py --include-code=false
```

Then click the "Slides" button in the marimo interface.
