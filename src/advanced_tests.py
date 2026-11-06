import stim
import pymatching
import numpy as np
import time
from reproduction import generate_circuit

if __name__ == "__main__":
    
    #Repeatability (Random Seeds)
    print("--- DAY 21: Random Seed Variance Test ---")
    print("Testing Distance 5, Noise 0.005 with 100,000 shots across 3 seeds...")
    
    d_seed, p_seed, shots_seed = 5, 0.005, 100_000
    seeds = [42, 100, 2026] 
    
    circuit = generate_circuit(distance=d_seed, noise=p_seed)
    dem = circuit.detector_error_model(decompose_errors=True)
    matching = pymatching.Matching.from_detector_error_model(dem)
    
    for seed in seeds:
        sampler = circuit.compile_detector_sampler(seed=seed)
        events, obs = sampler.sample(shots=shots_seed, separate_observables=True)
        preds = matching.decode_batch(events)
        fails = np.any(preds != obs, axis=1).sum()
        
        print(f"Seed {seed:>4} -> Logical failures: {fails}/{shots_seed} (LER: {fails/shots_seed:.5f})")

    #Distance 11 Scale-Up
    print("\n--- DAY 22: Distance 11 Scale-Up ---")
    d_11, p_11, shots_11 = 11, 0.005, 100_000
    
    circuit_11 = generate_circuit(distance=d_11, noise=p_11)
    dem_11 = circuit_11.detector_error_model(decompose_errors=True)
    matching_11 = pymatching.Matching.from_detector_error_model(dem_11)
    sampler_11 = circuit_11.compile_detector_sampler()
    
    print(f"Detectors in Distance 11: {circuit_11.num_detectors}")
    print(f"Sampling and decoding {shots_11:,} shots... (This might take a minute)")
    
    events_11, obs_11 = sampler_11.sample(shots=shots_11, separate_observables=True)
    
    start = time.perf_counter()
    preds_11 = matching_11.decode_batch(events_11)
    end = time.perf_counter()
    
    fails_11 = np.any(preds_11 != obs_11, axis=1).sum()
    print(f"Distance 11 Logical failures: {fails_11}/{shots_11} (LER: {fails_11/shots_11:.6f})")
    print(f"Decoding Speed: {shots_11 / (end - start):,.0f} shots/s")