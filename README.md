

# Sequential Inference Workflow Benchmark

<img width="2594" height="1540" alt="image" src="https://github.com/user-attachments/assets/2c24f221-8fa4-4619-9262-328878db516c" />

## Overview

Most LLM benchmarks focus on a single request.

Typical metrics include:

* Tokens per second
* Time to first token
* Single-request latency
* Throughput

While useful, these measurements often fail to capture how LLMs are used in real workflows.

Many applications perform a sequence of dependent inference calls where each model response becomes the input to the next request.

This project benchmarks latency in that setting.

Rather than measuring a single inference call, it measures how end-to-end latency evolves across a multi-step sequential workflow.

---

## Motivation

Inference performance is often discussed in terms of isolated requests.

However, many practical workloads involve iterative refinement:

* Debugging assistance
* Code review loops
* Document improvement
* Multi-step reasoning
* AI-assisted research

In these workflows, each step depends on the output of the previous step.

The total user experience is determined not only by individual request latency, but by the cumulative latency across the entire sequence.

This benchmark explores that behavior using a simple and reproducible setup.

---

## Benchmark Methodology

The benchmark begins with a fixed prompt:

```text
You are debugging a distributed system. Improve root cause analysis step by step.
```

For each iteration:

1. Send the current prompt to the model
2. Measure end-to-end request latency
3. Store the generated response
4. Construct the next prompt using the previous output

Example workflow:

```text
Initial Prompt
      ↓
Model Response
      ↓
"Improve this analysis:"
      +
Previous Response
      ↓
Next Request
      ↓
Repeat
```

This creates a chain of dependent inference requests that simulates an iterative refinement workflow.

---

## Metrics Collected

For every step, the benchmark records:

* Request latency
* Model output

It also reports:

* Total workflow latency
* Average latency per step

Example output:

```json
{
  "steps": 3,
  "step_times": [
    4.80,
    9.40,
    36.46
  ],
  "total_latency": 50.66,
  "avg_latency": 16.89
}
```

Results are stored in:

```text
results.json
```

---

## Running the Benchmark

### Create Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install openai matplotlib
```

### Configure API Key

```bash
export GENERAL_COMPUTE_API_KEY="your_key_here"
```

### Run

```bash
python run.py
```

Example output:

```text
🚀 Running General Compute Benchmark...

Step 1/3
Step 2/3
Step 3/3

✅ DONE
Total latency: 50.66
Avg latency: 16.89
```

---

## Visualizing Results

Generate a latency plot:

```bash
python plot.py
```

This displays latency for each workflow step.

---

## Interpreting Results

This benchmark measures end-to-end request latency across a sequence of dependent inference calls.

If latency increases between steps, several factors may contribute:

### Prompt Growth

Each response becomes part of the next request.

As responses grow, later prompts may contain more tokens.

### Response Length Variation

Different steps may generate different amounts of text.

Longer generations generally require more computation.

### Infrastructure Effects

Observed latency may also be influenced by:

* Queueing delays
* Backend load
* Request routing
* Resource contention
* Network overhead

The benchmark intentionally measures total workflow latency rather than attempting to isolate individual system components.

---

## What This Benchmark Measures

This benchmark is useful for evaluating:

* Sequential inference workflows
* Iterative LLM refinement patterns
* Latency accumulation across dependent requests
* Relative performance between inference providers

---

## What This Benchmark Does Not Measure

This project does not directly measure:

* Prefill latency
* Decode latency
* GPU utilization
* KV cache efficiency
* Scheduling behavior
* Throughput
* Time to first token

Similarly, it should not be used to conclude that latency growth is caused by any single factor without additional instrumentation.

---

## Why This Project Exists

A large portion of inference benchmarking focuses on isolated requests.

Real applications increasingly rely on chains of dependent inference calls.

Understanding how latency behaves across those chains can provide useful insight into the practical responsiveness of an inference platform.

This project provides a lightweight framework for exploring that behavior.

---

## Future Improvements

Potential extensions include:

* Prompt token tracking
* Completion token tracking
* Multiple benchmark runs
* p50 / p95 / p99 latency reporting
* Provider-to-provider comparisons
* Streaming inference support
* Constant-context versus growing-context experiments
* Prefill and decode analysis when provider metrics are available

---

## Repository Structure

```text
client_gc.py      # General Compute API client
client_vast.py    # Alternate provider client
config.py         # Configuration
run.py            # Benchmark runner
plot.py           # Visualization
test_gc.py        # Connectivity test
results.json      # Benchmark output
README.md
```
