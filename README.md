# Sparse Blossom Reproduction

An independent reproduction of the decoding performance and logical error rate (LER) benchmarks presented in the paper:

> **Sparse Blossom: Correcting a Million Errors per Core Second with Sparse Blossom**
>
> Oscar Higgott and Craig Gidney

This repository implements a complete surface-code benchmarking pipeline using **Stim** and **PyMatching v2** for:

- Surface code circuit generation
- Detector Error Model (DEM) extraction
- Sparse Blossom decoding
- Logical Error Rate (LER) measurement
- Decoder throughput benchmarking
- Scaling analysis and visualization

The goal of this project is to reproduce and validate the practical behavior of Sparse Blossom on small- and medium-distance rotated surface codes under phenomenological noise.

---

## Features

- Rotated surface-code memory experiments
- Distance sweep: `d ∈ {3, 5, 7, 9}`
- Noise sweep: `p ∈ {0.001, 0.003, 0.005}`
- 100,000 shots per configuration
- Noiseless validation tests
- Decoder throughput measurements
- Automated CSV export
- Publication-style log-log plots

---

## Repository Structure

```text
sparse_blossom_reproduction/
├── src/
│   ├── reproduction.py
│   ├── plot_results.py
│   ├── advanced_tests.py
│   └── test_reproduction.py
│
├── results/
│   ├── noise_sweep_results.csv
│   └── reproduction_plots.png
│
├── requirements.txt
├── README.md
└── blossom_env/
```

### Files

| File | Description |
|--------|-------------|
| `reproduction.py` | Main benchmarking pipeline |
| `plot_results.py` | Generates LER and scaling plots |
| `advanced_tests.py` | Extended experiments and high-distance tests |
| `test_reproduction.py` | Validation tests for reproducibility |
| `noise_sweep_results.csv` | Raw benchmark results |
| `reproduction_plots.png` | Generated figures |

---

## Environment Setup

Clone the repository and create a clean Python environment.

### Create Virtual Environment

```bash
python -m venv blossom_env
```

### Activate Environment

#### Linux / macOS

```bash
source blossom_env/bin/activate
```

#### Windows

```powershell
blossom_env\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Requirements

Core dependencies:

```text
stim
pymatching
numpy
scipy
pandas
matplotlib
pytest
```

A frozen environment can be generated using:

```bash
pip freeze > requirements.txt
```

---

## Usage

### 1. Run the Benchmark Sweep

Executes a parameter sweep over:

- Distances: `{3, 5, 7, 9}`
- Noise levels: `{0.001, 0.003, 0.005}`
- Shots: `100,000`

```bash
python src/reproduction.py
```

Output:

```text
results/noise_sweep_results.csv
```

---

### 2. Generate Plots

Reads the benchmark CSV and produces publication-style visualizations.

```bash
python src/plot_results.py
```

Output:

```text
results/reproduction_plots.png
```

Generated plots:

1. Logical Error Rate vs Physical Noise
2. Decoder Scaling vs Number of Detectors

---

### 3. Run Validation Tests

Execute the test suite:

```bash
pytest src/test_reproduction.py
```

The tests verify:

- Correct Stim installation
- Correct PyMatching installation
- Deterministic circuit generation
- Detector Error Model construction
- Successful zero-noise decoding

---

## Experimental Methodology

For each parameter configuration:

1. Generate a rotated surface-code memory circuit using Stim.
2. Convert the circuit into a Detector Error Model (DEM).
3. Construct a Sparse Blossom decoder using PyMatching.
4. Sample detector events from the noisy circuit.
5. Decode all shots using `decode_batch()`.
6. Compare predicted logical observables against actual observables.
7. Compute:

```text
Logical Error Rate (LER)
=
Logical Failures / Total Shots
```

8. Measure decoder throughput:

```text
Shots per Second
=
Shots / Decoding Time
```

---

## Example Results

Typical output:

```text
Distance  Noise  Logical_Error_Rate
3         0.005  1.21e-02
5         0.005  2.04e-03
7         0.005  3.90e-04
9         0.005  5.00e-05
```

These values may vary slightly depending on:

- CPU architecture
- Operating system
- PyMatching version
- Stim version
- Random sampling noise

---

## Reproduced Trends

This reproduction confirms the expected qualitative behavior reported in the Sparse Blossom paper:

### Error Suppression

At fixed physical noise:

```text
LER(d=9)
    <
LER(d=7)
    <
LER(d=5)
    <
LER(d=3)
```

Larger code distances provide stronger logical protection.

### Decoder Scaling

As detector count grows:

```text
More Detectors
      ↓
Larger Matching Graph
      ↓
Longer Decode Times
```

Despite increasing graph sizes, Sparse Blossom maintains highly efficient decoding throughput.

---

## Noiseless Validation

Every distance is validated using a zero-noise test:

```python
assert np.array_equal(
    predicted_observables,
    actual_observables
)
```

Any failure indicates an issue with:

- DEM generation
- Matching graph construction
- Observable indexing
- Decoder configuration

---

## Reproducibility Checklist

Before finalizing results:

### Freeze Dependencies

```bash
pip freeze > requirements.txt
```

### Commit Source Code

```bash
git add .
git commit -m "Final reproduction results"
```

### Archive Outputs

Preserve:

```text
results/noise_sweep_results.csv
results/reproduction_plots.png
requirements.txt
README.md
```

---

## Future Work

Possible extensions include:

- Distance-11 and Distance-13 surface-code experiments
- Threshold estimation studies
- Decoder comparisons (Union-Find vs Sparse Blossom)
- Circuit-level noise models
- Parallelized benchmarking
- Integration with FRQI and NEQR quantum image encodings
- Fault-tolerant quantum image processing experiments

---

## References

- Oscar Higgott, Craig Gidney, *Sparse Blossom: Correcting a Million Errors per Core Second with Sparse Blossom*
- Stim Quantum Error Correction Simulator
- PyMatching v2 Decoder Framework
- Surface Code Literature on Minimum-Weight Perfect Matching (MWPM)

---

## License

This repository is intended for educational and research purposes. Please cite the original Sparse Blossom paper when using or extending this work.