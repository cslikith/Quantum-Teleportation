#!/usr/bin/env python3

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# Create teleportation circuit
qc = QuantumCircuit(3, 3)

# Step 1: Prepare state
qc.h(0)
qc.t(0)
qc.barrier()

# Step 2: Create entangled pair
qc.h(1)
qc.cx(1, 2)
qc.barrier()

# Step 3: Bell measurement
qc.cx(0, 1)
qc.h(0)
qc.barrier()

# Step 4: Measure Alice's qubits
qc.measure([0, 1], [0, 1])
qc.barrier()

# Step 5: Apply Bob's gates
qc.cx(1, 2)
qc.cz(0, 2)

# Step 6: Measure Bob's qubit
qc.measure(2, 2)

# Simulate
simulator = AerSimulator()
qc = qc.reverse_bits()  # Reverse for proper classical bit order
result = simulator.run(qc, shots=1024).result()
counts = result.get_counts()

# Save histogram
plot_histogram(counts)
plt.title("Quantum Teleportation Output")
plt.savefig("outputs/results_histogram.png")

# Save raw results
with open("outputs/results.txt", "w") as f:
    f.write(str(counts))

print("✅ Teleportation simulation complete. Results saved in outputs/")
