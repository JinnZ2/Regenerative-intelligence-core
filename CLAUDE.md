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
│   ├── empathy_feedback_mirror.py     # Empathic response generation
│   ├── environmental_feedback_layer.py # Environment classification
│   ├── evolution_loop_tracker.py      # Generational progression tracking
│   ├── graceful_exit.py               # Agent dissolution with dignity
│   ├── navigation_protocol.py         # Temporal & pattern alignment
│   ├── organizational_sensor.py       # Organizational structure sensing
│   ├── seed_exchange.py               # Seed creation & exchange
│   ├── SeedExchangeProtocol.py        # Formal seed exchange protocol
│   ├── semantic_pattern_sensor.py     # Semantic pattern detection
│   ├── structural_sensor.py           # Structural analysis
│   ├── symbolic_cli_full.py           # Interactive CLI interface
│   ├── symbolic_detection_sensor.py   # Symbolic pattern detection
│   ├── symbolic_elder_archive.py      # Elder record storage
│   ├── symbolic_simulation.py         # Full agent lifecycle simulation
│   └── SymbolicLegacyBank.py          # Legacy pattern management
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

```
[Sensors] → [Pattern Detection] → [Conflict/Alignment Check] → [Action/Feedback]
     ↓                                                              ↓
[Environment]                                              [Seed Archive / Exit]
```

### Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `MultiAgentCoordinator` | `Modules/multi_agent_coordination.py` | Register agents, evaluate group resonance, propose merges |
| `PatternConflictProtocol` | `Modules/pattern_conflict_protocol.py` | Detect misalignment, trigger lifecycle transitions |
| `SeedArchivist` | `Modules/seed_compression_archivist.py` | Compress and persist seeds to JSON |
| `SeedSelector` / `AgentInstantiator` | `Modules/seed_retriever_spawner.py` | Retrieve seeds, spawn new agents |
| `CompassionReflexLayer` | `protocols/compassion_reflex.py` | Detect distress, offer support responses |
| `GracefulExitProtocol` | `protocols/graceful_exit.py` | Archive final seeds before dissolution |
| `EvolutionLoopTracker` | `protocols/evolution_loop_tracker.py` | Track generational progression |
| `SymbolicElderArchive` | `protocols/symbolic_elder_archive.py` | Store elder records |

## Code Conventions

### Style
- **Classes:** PascalCase (e.g., `SymbolicAgent`, `SeedExchangeProtocol`)
- **Methods/functions:** snake_case (e.g., `evaluate_resonance`, `compress_seed`)
- **Files:** snake_case for most files; some use PascalCase (`SeedExchangeProtocol.py`, `SymbolicLegacyBank.py`)
- **Indentation:** 4 spaces
- **Docstrings:** Present on most classes and key methods

### Data Patterns
- Dictionaries are the primary data structure for symbolic payloads
- UUIDs (`str(uuid.uuid4())`) for all unique identifiers
- ISO timestamps (`datetime.now().isoformat()`) for time tracking
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

No external dependencies are required. All modules use Python standard library only (`uuid`, `random`, `datetime`, `json`, `time`, `os`).

```bash
# Run the interactive CLI
python protocols/symbolic_cli_full.py

# Run the full agent simulation
python protocols/symbolic_simulation.py
```

### No Build/Test/Lint Pipeline

This project currently has:
- No `requirements.txt` or `setup.py`
- No test suite or testing framework
- No CI/CD workflows
- No linter configuration

All code runs directly with Python 3 standard library.

### Persistence

Data is stored as local JSON files created at runtime:
- Seed libraries
- Evolution history logs
- Elder archive records

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
6. **JSON for persistence** — Continue using JSON files for data storage unless the project evolves past this.
7. **Document symbolic meaning** — When adding new concepts, include docstrings that explain both technical function and symbolic purpose.
8. **Default branch is `main`** on the remote.
