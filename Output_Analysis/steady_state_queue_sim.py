import csv
import random
import statistics
from pathlib import Path

SEED = 42
NUM_CUSTOMERS = 5000
MEAN_INTERARRIVAL = 2.0
MEAN_SERVICE = 1.6
NUM_REPLICATIONS = 10
BATCH_SIZE = 500
OUTPUT_DIR = Path(__file__).resolve().parent

random.seed(SEED)


def exp_rv(mean: float) -> float:
    return random.expovariate(1.0 / mean)


def simulate_mm1(
    num_customers=NUM_CUSTOMERS,
    mean_interarrival=MEAN_INTERARRIVAL,
    mean_service=MEAN_SERVICE,
):
    arrivals = []
    service_times = []
    start_service = []
    departures = []
    waits = []
    system_times = []
    queue_lengths_on_arrival = []

    current_time = 0.0
    last_departure = 0.0

    for _ in range(num_customers):
        current_time += exp_rv(mean_interarrival)
        service = exp_rv(mean_service)
        begin = max(current_time, last_departure)
        depart = begin + service
        wait = begin - current_time
        system = depart - current_time

        q_len = 0
        for j in range(len(departures)):
            if arrivals[j] <= current_time < departures[j]:
                q_len += 1
        q_len = max(0, q_len - 1)

        arrivals.append(current_time)
        service_times.append(service)
        start_service.append(begin)
        departures.append(depart)
        waits.append(wait)
        system_times.append(system)
        queue_lengths_on_arrival.append(q_len)
        last_departure = depart

    return {
        "arrivals": arrivals,
        "service_times": service_times,
        "start_service": start_service,
        "departures": departures,
        "waits": waits,
        "system_times": system_times,
        "queue_lengths_on_arrival": queue_lengths_on_arrival,
    }


def moving_average(values, window):
    result = []
    for i in range(len(values)):
        lo = max(0, i - window + 1)
        chunk = values[lo:i + 1]
        result.append(sum(chunk) / len(chunk))
    return result


def welch_warmup(replications, window=25):
    min_len = min(len(rep["waits"]) for rep in replications)
    cross_rep_avg = []

    for i in range(min_len):
        avg = sum(rep["waits"][i] for rep in replications) / len(replications)
        cross_rep_avg.append(avg)

    smoothed = moving_average(cross_rep_avg, window)

    tail = smoothed[-500:]
    tail_mean = sum(tail) / len(tail)
    threshold = 0.05 * tail_mean if tail_mean > 0 else 0.01

    warmup = 0
    for i in range(len(smoothed)):
        future = smoothed[i:i + 100]
        if len(future) < 100:
            break
        if max(abs(x - tail_mean) for x in future) <= threshold:
            warmup = i
            break

    return warmup, cross_rep_avg, smoothed, tail_mean


def replication_deletion(replications, delete_n):
    means = []
    for rep in replications:
        trimmed = rep["waits"][delete_n:]
        means.append(sum(trimmed) / len(trimmed))

    grand_mean = sum(means) / len(means)
    s = statistics.stdev(means) if len(means) > 1 else 0.0
    return grand_mean, s, means


def batch_means(single_run_waits, delete_n, batch_size):
    data = single_run_waits[delete_n:]
    num_batches = len(data) // batch_size
    batches = []

    for i in range(num_batches):
        batch = data[i * batch_size:(i + 1) * batch_size]
        batches.append(sum(batch) / len(batch))

    grand_mean = sum(batches) / len(batches)
    s = statistics.stdev(batches) if len(batches) > 1 else 0.0
    return grand_mean, s, batches


def save_customer_trace(run):
    path = OUTPUT_DIR / "customer_trace.csv"
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "customer_id",
            "arrival_time",
            "service_time",
            "service_start",
            "departure_time",
            "waiting_time",
            "time_in_system",
            "queue_length_on_arrival",
        ])

        for i in range(len(run["waits"])):
            writer.writerow([
                i + 1,
                round(run["arrivals"][i], 6),
                round(run["service_times"][i], 6),
                round(run["start_service"][i], 6),
                round(run["departures"][i], 6),
                round(run["waits"][i], 6),
                round(run["system_times"][i], 6),
                run["queue_lengths_on_arrival"][i],
            ])
    return path


def save_welch_csv(cross_rep_avg, smoothed):
    path = OUTPUT_DIR / "welch_plot_data.csv"
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "customer_index",
            "cross_replication_avg_wait",
            "smoothed_avg_wait",
        ])
        for i, (a, s) in enumerate(zip(cross_rep_avg, smoothed), start=1):
            writer.writerow([i, round(a, 6), round(s, 6)])
    return path


def save_summary(rep_means, batch_means_list, welch_delete, rd_mean, bm_mean):
    path = OUTPUT_DIR / "summary_results.csv"
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["suggested_warmup_customers_welch", welch_delete])
        writer.writerow(["replication_deletion_mean_wait", round(rd_mean, 6)])
        writer.writerow(["batch_means_mean_wait", round(bm_mean, 6)])
        writer.writerow(["number_of_replications", len(rep_means)])
        writer.writerow(["number_of_batches", len(batch_means_list)])
    return path


def main():
    replications = [simulate_mm1() for _ in range(NUM_REPLICATIONS)]

    welch_delete, cross_rep_avg, smoothed, tail_mean = welch_warmup(replications)
    rd_mean, rd_sd, rep_means = replication_deletion(replications, welch_delete)

    long_run = simulate_mm1(num_customers=NUM_CUSTOMERS * 2)
    bm_mean, bm_sd, batches = batch_means(long_run["waits"], welch_delete, BATCH_SIZE)

    save_customer_trace(long_run)
    save_welch_csv(cross_rep_avg, smoothed)
    save_summary(rep_means, batches, welch_delete, rd_mean, bm_mean)

    print("Simulation completed.")
    print("Generated files:")
    print("- customer_trace.csv")
    print("- welch_plot_data.csv")
    print("- summary_results.csv")


if __name__ == "__main__":
    main()