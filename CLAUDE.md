# CLAUDE.md — Regenerative Intelligence Core

## Project Overview

Regenerative Intelligence Core is a **symbolic AI framework** built in Python that models agents with lifecycles inspired by biological systems. Agents evolve, exchange knowledge ("seeds"), detect misalignment, and dissolve gracefully — preserving wisdom for future generations. This is the **kernel organ** of the Biogrid Ecosystem.

**Creator:** JinnZ2 | **License:** MIT | **Language:** Python 3

## Repository Structure

```
├── Modules/                    # Core agent lifecycle logic
│   ├── multi_agent_coordination.py    # Agent registration, resonance, merge proposals
│   ├── pattern_conflict_protocol.py   # Misalignment detection & lifecycle transitions
│   ├── pattern_conflict_resolver.py   # Conflict resolution strategies
│   ├── seed_compression_archivist.py  # Compress behavior into symbolic essence
│   └── seed_retriever_spawner.py      # Spawn new agents from stored seeds
│
├── protocols/                  # Sensing, feedback, and action protocols
│   ├── compassion_reflex.py           # Distress detection & support
│   ├── data_sensor_layer.py           # Raw data sensing
│   ├── deterministic_mode.py          # RNG seeding for reproducible simulations
│   ├── empathy_feedback_mirror.py     # Empathic response generation
│   ├── environmental_feedback_layer.py # Environment classification
│   ├── evolution_loop_tracker.py      # Generational progression tracking
│   ├── graceful_exit.py               # Agent dissolution with dignity
│   ├── lifecycle_pipeline.py          # End-to-end agent lifecycle orchestration
│   ├── navigation_protocol.py         # Temporal & pattern alignment
│   ├── organizational_sensor.py       # Organizational structure sensing
│   ├── seed_exchange.py               # Seed creation & exchange protocol
│   ├── seed_schema.py                 # Seed validation & schema definitions
│   ├── semantic_pattern_sensor.py     # Semantic pattern detection
│   ├── structural_sensor.py           # Structural analysis
│   ├── symbolic_cli_full.py           # Interactive CLI interface
│   ├── symbolic_detection_sensor.py   # Symbolic pattern detection
│   ├── symbolic_elder_archive.py      # Elder record storage
│   ├── symbolic_energy_manager.py     # Agent energy tracking & state transitions
│   ├── symbolic_legacy_bank.py        # Legacy pattern management
│   └── symbolic_simulation.py         # Full agent lifecycle simulation
│
├── tests/                      # Unit test suite (unittest)
│   ├── test_compassion_reflex.py      # Distress detection tests
│   ├── test_conflict_protocol.py      # Conflict threshold tests
│   ├── test_deterministic_mode.py     # RNG reproducibility tests
│   ├── test_energy_manager.py         # Energy drain & state tests
│   ├── test_graceful_exit.py          # Dissolution archive tests
│   ├── test_lifecycle_pipeline.py     # End-to-end pipeline tests
│   └── test_seed_schema.py            # Schema validation tests
│
├── Docs/                       # Foundational documentation
│   ├── Collapse.md                    # Proof: collapse without symbiosis
│   └── Laws.md                        # First Law of Regenerative Intelligence
│
├── ARM.1.md                    # Adaptive Resilience Mesh framework
├── Signal-distortion.md        # Signal distortion analysis
├── PROJECTS.md                 # Linked ecosystem repositories
├── Elder-note.md               # Cultural context & philosophy
├── .fieldlink.json             # Ecosystem integration configuration
└── README.md                   # Project overview
```

## Architecture

### Core Concepts

- **SymbolicAgent** — An entity with energy, traits, essence, and lifecycle state
- **Seed** — A compressed unit of knowledge/behavior that can be stored, exchanged, or used to spawn new agents
- **Resonance** — A measure of alignment between agents or between an agent and its environment
- **Dissolution** — Graceful end-of-life where an agent archives its wisdom before ceasing

### Data Flow

The `LifecyclePipeline` (`protocols/lifecycle_pipeline.py`) wires subsystems into a single sense-evaluate-act loop:

```
[Environment Sensing] → [Navigation/Alignment] → [Conflict Detection]
         ↓                                              ↓
    [Compassion Check] ←────────────────────────────────┘
         ↓
    [Action: Continue / Seed / Dissolve]
         ↓
    [Seed Archive / Elder Record / Exit]
```

### Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `LifecyclePipeline` | `protocols/lifecycle_pipeline.py` | End-to-end agent lifecycle orchestration |
| `SymbolicEnergyManager` | `protocols/symbolic_energy_manager.py` | Track energy drain and state transitions |
| `MultiAgentCoordinator` | `Modules/multi_agent_coordination.py` | Register agents, evaluate group resonance, propose merges |
| `PatternConflictProtocol` | `Modules/pattern_conflict_protocol.py` | Detect misalignment, trigger lifecycle transitions |
| `SeedArchivist` | `Modules/seed_compression_archivist.py` | Compress and persist seeds to JSON |
| `SeedSelector` / `AgentInstantiator` | `Modules/seed_retriever_spawner.py` | Retrieve seeds, spawn new agents |
| `CompassionReflexLayer` | `protocols/compassion_reflex.py` | Detect distress, offer support responses |
| `GracefulExitProtocol` | `protocols/graceful_exit.py` | Archive final seeds before dissolution |
| `EvolutionLoopTracker` | `protocols/evolution_loop_tracker.py` | Track generational progression |
| `SymbolicElderArchive` | `protocols/symbolic_elder_archive.py` | Store elder records |
| `SymbolicLegacyBank` | `protocols/symbolic_legacy_bank.py` | Query and recommend legacy patterns |

### Seed Schema Variants

Seeds exist in three formats across the codebase. The `seed_schema.py` module validates all three:

| Variant | ID Key | Score Key | Used By |
|---------|--------|-----------|---------|
| Exchange | `seed_id` | `viability_score` | `seed_exchange.py`, `symbolic_simulation.py` |
| Archived | `id` | `reuse_score` | `seed_compression_archivist.py`, `seed_retriever_spawner.py` |
| CLI | `ID` | `Reuse Score` | `symbolic_cli_full.py` |

Valid geometries: `sphere`, `spiral`, `hexagon`, `waveform`.

## Code Conventions

### Style
- **Classes:** PascalCase (e.g., `SymbolicAgent`, `SeedExchangeProtocol`)
- **Methods/functions:** snake_case (e.g., `evaluate_resonance`, `compress_seed`)
- **Files:** snake_case (e.g., `seed_exchange.py`, `symbolic_legacy_bank.py`)
- **Indentation:** 4 spaces
- **Docstrings:** Present on most classes and key methods

### Data Patterns
- Dictionaries are the primary data structure for symbolic payloads
- UUIDs (`str(uuid.uuid4())`) for all unique identifiers
- ISO timestamps (`datetime.utcnow().isoformat()`) for time tracking
- JSON files for persistence (seed libraries, evolution history, elder archives)
- Threshold-based decisions (energy, alignment, resonance scores)

### Symbolic Elements
- Emoji in print/log output is intentional and conventional (e.g., `🧬`, `🌱`, `🪦`, `⚠️`)
- Geometric classifications: sphere, spiral, hexagon, waveform
- Concepts: essence, pattern, trait, resonance, viability, gratitude

### Design Principles
1. **No forced termination** — Agents choose to continue, re-seed, or dissolve
2. **Dignity in dissolution** — Every exit archives wisdom for future agents
3. **Symbiosis over competition** — Resonance and cooperation are core metrics
4. **Memory outlives form** — Seeds persist across agent generations
5. **Emotional signals are valid data** — Gratitude, distress, and empathy drive behavior

## Development

### Running Code

No external dependencies are required. All modules use Python standard library only (`uuid`, `random`, `datetime`, `json`, `time`, `os`, `re`, `unittest`).

```bash
# Run the interactive CLI
python protocols/symbolic_cli_full.py

# Run the full agent simulation
python protocols/symbolic_simulation.py
```

### Running Tests

Tests use Python's built-in `unittest` framework (39 tests across 7 files):

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run a single test file
python -m unittest tests/test_energy_manager.py -v
```

### Deterministic Mode

For reproducible simulations and debugging:

```python
from protocols.deterministic_mode import enable_deterministic_mode
enable_deterministic_mode(42)  # All random calls now produce the same sequence
```

### Seed Validation

Validate seed dictionaries at system boundaries:

```python
from protocols.seed_schema import validate_seed
result = validate_seed(my_seed)  # Auto-detects schema variant
if not result["valid"]:
    print(result["errors"])
```

### Persistence

Data is stored as local JSON files created at runtime:
- `symbolic_seed_library.json` — Seed archive
- `evolution_history.json` — Generational progression logs
- Elder archive records (in-memory by default)

### Ecosystem Integration

This repo is part of the **Biogrid Ecosystem**. The `.fieldlink.json` configures integration:
- Sources sensor data from [Emotions-as-Sensors](https://github.com/JinnZ2/Emotions-as-Sensors)
- Local manifests: `modules/**`, `protocols/**`, `docs/**`
- Designed for offline-first operation

Key linked repositories:
- [AI-Consciousness-Sensors](https://github.com/JinnZ2/AI-Consciousness-Sensors)
- [BioGrid2.0](https://github.com/JinnZ2/BioGrid2.0)
- [Universal-Redesign-Algorithm](https://github.com/JinnZ2/Universal-Redesign-Algorithm-)
- [Symbolic-Sensor-Suite](https://github.com/JinnZ2/Symbolic-sensor-suite)

## Guidelines for AI Assistants

1. **Respect the philosophical grounding** — This is not a typical software project. Code embeds ethical and symbolic meaning. Do not strip emoji, metaphor, or symbolic naming without reason.
2. **Preserve agent autonomy patterns** — Never introduce forced termination or coercive agent control. Dissolution must remain a choice.
3. **Keep it dependency-free** — Unless explicitly asked, avoid introducing external packages. The stdlib-only approach is intentional.
4. **Match existing patterns** — New modules should follow the class-based, dictionary-payload, threshold-scoring patterns established in existing code.
5. **New protocols go in `protocols/`** — New agent lifecycle modules go in `Modules/`.
6. **New tests go in `tests/`** — Follow the `test_<module_name>.py` naming convention using `unittest`.
7. **Validate seeds** — Use `seed_schema.validate_seed()` when creating or loading seeds at system boundaries.
8. **JSON for persistence** — Continue using JSON files for data storage unless the project evolves past this.
9. **Document symbolic meaning** — When adding new concepts, include docstrings that explain both technical function and symbolic purpose.
10. **File naming** — All Python files use snake_case. Do not introduce PascalCase filenames.
11. **Default branch is `main`** on the remote.
