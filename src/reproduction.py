import stim
import pymatching
import numpy as np
import time
import pandas as pd


def print_environment():
    print("--- Environment Manifest ---")
    print(f"Stim version: {stim.__version__}")
    print(f"PyMatching version: {pymatching.__version__}")
    print(f"NumPy version: {np.__version__}")
    print("----------------------------\n")


def generate_circuit(distance: int, noise: float) -> stim.Circuit:
    """
    Generates a rotated surface code memory circuit.
    """
    return stim.Circuit.generated(
        "surface_code:rotated_memory_x",
        distance=distance,
        rounds=distance,
        after_clifford_depolarization=noise,
        after_reset_flip_probability=noise,
        before_measure_flip_probability=noise,
    )


if __name__ == "__main__":
    print_environment()

    # ==================================================
    # DAYS 16-17: DISTANCE + NOISE SWEEP
    # ==================================================

    distances = [3, 5, 7, 9]
    noise_levels = [0.001, 0.003, 0.005]

    shots = 100_000

    results = []

    for d in distances:
        for p in noise_levels:

            print(f"\n--- Running Distance {d}, Noise {p} ---")

            # Generate circuit
            circuit = generate_circuit(
                distance=d,
                noise=p
            )

            # Detector Error Model
            dem = circuit.detector_error_model(
                decompose_errors=True
            )

            # Build decoder
            matching = pymatching.Matching.from_detector_error_model(
                dem
            )

            # Sample detector events
            sampler = circuit.compile_detector_sampler()

            detection_events, actual_observables = (
                sampler.sample(
                    shots=shots,
                    separate_observables=True
                )
            )

            # Time ONLY decoding
            start_time = time.perf_counter()

            predicted_observables = matching.decode_batch(
                detection_events
            )

            end_time = time.perf_counter()

            decoding_time = end_time - start_time

            # Logical failures
            logical_failures = np.any(
                predicted_observables != actual_observables,
                axis=1
            ).sum()

            logical_error_rate = (
                logical_failures / shots
            )

            speed = shots / decoding_time

            print(
                f"Logical failures: "
                f"{logical_failures}/{shots} "
                f"(LER: {logical_error_rate:.6f})"
            )

            print(
                f"Speed: {speed:,.0f} shots/s"
            )

            results.append({
                "Distance": d,
                "Noise": p,
                "Logical_Failures": logical_failures,
                "Shots": shots,
                "Logical_Error_Rate": logical_error_rate,
                "Decoding_Time": decoding_time,
                "Speed_Shots_Per_Sec": speed,
                "Detectors": circuit.num_detectors
            })

    
    # RESULTS TABLE
    df = pd.DataFrame(results)

    print("\n=== Noise Sweep Summary ===")
    print(df.to_string(index=False))

    # Save results

    output_file = "results/noise_sweep_results.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"\nResults saved to '{output_file}'")