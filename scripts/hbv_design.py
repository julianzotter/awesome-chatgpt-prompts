"""Simple discrete connector design example for timber-concrete composite (HBV) members.

This script demonstrates a minimal approach to compute connector slip
and internal forces using the discrete method according to ONR CEN/TS 19103.
The model is highly simplified and intended only as a template for further
development and verification.
"""

from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class Connector:
    position: float  # position along the member [m]
    stiffness: float  # slip modulus [N/mm]

class HBVSystem:
    def __init__(self, span: float):
        self.span = span
        self.connectors: List[Connector] = []

    def add_connector(self, position: float, stiffness: float):
        self.connectors.append(Connector(position, stiffness))

    def assemble_matrix(self):
        n = len(self.connectors)
        K = np.zeros((n, n))
        F = np.zeros(n)
        for i, c in enumerate(self.connectors):
            K[i, i] = c.stiffness
        return K, F

    def solve(self):
        K, F = self.assemble_matrix()
        if np.linalg.matrix_rank(K) < K.shape[0]:
            raise ValueError("Stiffness matrix is singular. Check connector data.")
        u = np.linalg.solve(K, F)
        return u

if __name__ == "__main__":
    # Example: simplified benchmark configuration
    system = HBVSystem(span=7.8)
    notch_positions = [0.3, 0.9, 1.5, 2.1, 2.7]
    k_notch = 1e8  # placeholder stiffness per notch [N/mm]
    for pos in notch_positions:
        system.add_connector(pos, k_notch)
        system.add_connector(system.span - pos, k_notch)

    deformations = system.solve()
    for i, u in enumerate(deformations, 1):
        print(f"Connector {i}: slip = {u:.4e} mm")
