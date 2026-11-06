import pytest
import stim
import pymatching
import numpy as np

from reproduction import generate_circuit 

def test_circuit_generation_dimensions():
    """Test that generated circuits match expected topological dimensions."""
    circuit_d3 = generate_circuit(distance=3, noise=0.001)
    assert circuit_d3.num_qubits == 26
    assert circuit_d3.num_measurements == 33
    assert circuit_d3.num_detectors == 24

def test_dem_conversion():
    """Test that circuits convert to valid detector error models."""
    circuit = generate_circuit(distance=5, noise=0.005)
    dem = circuit.detector_error_model(decompose_errors=True)
    
    assert len(dem) > 0
    matching = pymatching.Matching.from_detector_error_model(dem)
    assert matching is not None

def test_noiseless_decoding_never_fails():
    """Test that a 0-noise circuit always yields 0 logical failures."""
    distance = 5
    shots = 500
    
    circuit = generate_circuit(distance=distance, noise=0.0)
    dem = circuit.detector_error_model(decompose_errors=True)
    matching = pymatching.Matching.from_detector_error_model(dem)
    
    sampler = circuit.compile_detector_sampler()
    events, obs = sampler.sample(shots=shots, separate_observables=True)
    preds = matching.decode_batch(events)
    
    np.testing.assert_array_equal(preds, obs)