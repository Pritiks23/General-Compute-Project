import json
import time
from client_gc import call_gc
from config import STEPS


TASK = "You are debugging a distributed system. Improve root cause analysis step by step."


def run_agent():
    state = TASK
    step_times = []
    outputs = []

    print("\n🚀 Running General Compute Benchmark...\n")

    for i in range(STEPS):
        print(f"Step {i+1}/{STEPS}")

        start = time.time()

        res = call_gc([
            {"role": "user", "content": state}
        ])

        latency = time.time() - start

        step_times.append(latency)
        outputs.append(res["text"])

        # IMPORTANT: do NOT accumulate full history
        state = f"Improve this analysis:\n{res['text']}"

    result = {
        "steps": STEPS,
        "step_times": step_times,
        "total_latency": sum(step_times),
        "avg_latency": sum(step_times) / len(step_times),
        "outputs": outputs
    }

    with open("results.json", "w") as f:
        json.dump({"general_compute": result}, f, indent=2)

    print("\n✅ DONE")
    print("Total latency:", result["total_latency"])
    print("Avg latency:", result["avg_latency"])


if __name__ == "__main__":
    run_agent()