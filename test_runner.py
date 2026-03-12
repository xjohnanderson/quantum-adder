from qiskit import QuantumCircuit, transpile, ClassicalRegister
from qiskit_aer import AerSimulator
from circuit_builder import n_bit_adder

def initialize_register(circuit, register, value_decimal, n_bits):
    binary_str = bin(value_decimal)[2:].zfill(n_bits)
    for i, bit in enumerate(binary_str):
        if bit == '1':
            circuit.x(register[n_bits - 1 - i])

def run_test(n_bits, a_val, b_val, cin_val):
    adder = n_bit_adder(n_bits)
    full_circuit = QuantumCircuit(*adder.qregs)
    
    initialize_register(full_circuit, full_circuit.qregs[0], a_val, n_bits)
    initialize_register(full_circuit, full_circuit.qregs[1], b_val, n_bits)
    if cin_val == 1:
        full_circuit.x(full_circuit.qregs[2][0])

    full_circuit.append(adder, full_circuit.qubits)
    
    c_sum = ClassicalRegister(n_bits, 'c_S')
    c_cout = ClassicalRegister(1, 'c_Cout')
    full_circuit.add_register(c_sum, c_cout)
    
    full_circuit.measure(full_circuit.qregs[3], c_sum)
    full_circuit.measure(full_circuit.qregs[2][n_bits], c_cout)
    
    sim = AerSimulator()
    job = sim.run(transpile(full_circuit, sim), shots=1024)
    counts = job.result().get_counts()
    outcome = max(counts, key=counts.get).split(' ')
    
    return int(outcome[0], 2), int(outcome[1], 2)

if __name__ == "__main__":
    cout, s = run_test(2, 1, 2, 0)
    print(f"Test A=1, B=2, Cin=0 -> Cout={cout}, Sum={s}")