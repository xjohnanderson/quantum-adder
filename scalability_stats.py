from qiskit import transpile
from circuit_builder import n_bit_adder

def analyze_scalability(n_values):
    print("N | Depth | T-gate Count")
    for n in n_values:
        circ = n_bit_adder(n)
        transpiled = transpile(circ, basis_gates=['u', 'cx', 't', 'tdg'])
        ops = transpiled.count_ops()
        t_count = ops.get('t', 0) + ops.get('tdg', 0)
        print(f"{n} | {transpiled.depth()} | {t_count}")

if __name__ == "__main__":
    analyze_scalability([1, 2, 3, 4, 5])