import json
import matplotlib.pyplot as plt


def load():
    with open("results.json", "r") as f:
        return json.load(f)


def main():
    data = load()["general_compute"]["step_times"]

    plt.plot(range(len(data)), data)
    plt.title("General Compute Latency per Step")
    plt.xlabel("Step")
    plt.ylabel("Latency (s)")
    plt.show()


if __name__ == "__main__":
    main()