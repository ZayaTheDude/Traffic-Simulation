# Entry point to run the simulation locally

from app.simulator import Simulator

if __name__ == "__main__":
    simulator = Simulator()
    simulator.run()
