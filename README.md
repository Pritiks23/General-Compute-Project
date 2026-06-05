General Compute Agent Latency Benchmark
<img width="2594" height="1540" alt="image" src="https://github.com/user-attachments/assets/2c24f221-8fa4-4619-9262-328878db516c" />


This project measures how inference latency behaves when you move from single-turn LLM calls to multi-step agent trajectories.

Most benchmarks focus on tokens/sec or single-request latency. That misses what actually matters for agents: latency compounds over sequential steps.

This repo simulates that effect and measures it using a simple, repeatable agent loop.

What this is testing

The core idea is simple:

An agent doesn’t run one request. It runs a chain of dependent requests.

Each step depends on the previous one, so:

latency doesn’t just matter per call
it accumulates across the full trajectory
small differences per step become large differences end-to-end

This benchmark models that directly.

Setup
1. Create environment
python3 -m venv .venv
source .venv/bin/activate
2. Install dependencies
pip install openai matplotlib
3. Set API key
export GENERAL_COMPUTE_API_KEY="your_key_here"
Run benchmark
python3 run.py
This runs a small agent loop and logs:

per-step latency
total runtime
outputs per step

Results are saved to:

results.json
Plot results
python3 plot.py
This produces a simple line plot of latency per step.
What the benchmark does

Each run follows this loop:

Start with a fixed debugging task
Send it to the model
Take the response
Feed it back as the next prompt
Repeat for N steps

No batching. No parallelism. Just sequential dependency.

This is intentional — it mirrors how agents behave in practice.
Why this matters

Most inference systems are optimized for throughput.

Agents care about something different:

step time
consistency of latency
how delays accumulate over a trajectory

Even small differences per request change what kinds of workflows are viable.

For example:

1.5s per step vs 3s per step doesn’t look dramatic
but over 10–20 steps, it becomes the difference between a usable agent and a stalled one



More:
step_times: [
  4.80s,
  9.40s,
  36.46s
]

This is the key signal.

You are not seeing stable latency. You are seeing latency amplification over a trajectory.

We are seeing:

non-linear latency growth in sequential agent execution

⚠️ Likely causes 
1. Context / prompt degradation (most likely)

Even though your code simplified state, the model still sees:

longer reasoning chains
more complex intermediate outputs
increasing token entropy

This causes:

decode gets slower as output becomes harder to produce

2. Decode-heavy response expansion

If outputs grow in length:

more tokens generated
decode time dominates
latency scales superlinearly

⚠️ The real metric that matters

Instead of average, your system is showing:

latency variance explosion

More informative view:

Step 1 → baseline
Step 2 → ~2x
Step 3 → ~8x

That pattern is the real signal.

Takeaway: inference latency is not constant across agent steps — it compounds under sequential reasoning, producing a heavy-tailed trajectory cost profile
