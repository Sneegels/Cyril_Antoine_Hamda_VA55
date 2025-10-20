import matplotlib.pyplot as plt

def load_trajectory(filename):
    xs, ys = [], []
    with open(filename) as f:
        for line in f:
            x, y = map(float, line.strip().split(","))
            xs.append(x)
            ys.append(y)
    return xs, ys

def main():
    xs_brute, ys_brute = load_trajectory("trajectory_brute.csv")
    xs_kalman, ys_kalman = load_trajectory("trajectory_kalman.csv")

    plt.plot(xs_brute, ys_brute, label="Brute (sans Kalman)")
    plt.plot(xs_kalman, ys_kalman, label="Filtrée (Kalman)")
    plt.title("Comparaison des trajectoires du robot")
    plt.xlabel("x (mm)")
    plt.ylabel("y (mm)")
    plt.legend()
    plt.axis("equal")
    plt.show()

if __name__ == "__main__":
    main()