from pybricks.parameters import Port

# =============================================================================
# CONFIGURATION HARDWARE
# =============================================================================
LEFT_MOTOR_PORT = Port.B
RIGHT_MOTOR_PORT = Port.C
COLOR_SENSOR_PORT = Port.S3
GYRO_SENSOR_PORT = Port.S1

# =============================================================================
# CONFIGURATION DRIVEBASE
# =============================================================================
WHEEL_DIAMETER = 55  # mm - Diamètre des roues
AXLE_TRACK = 108  # mm - Distance entre roues

# =============================================================================
# CONFIGURATION CONTRÔLEURS
# =============================================================================
# Thresholds et setpoints (basé sur mesures: blanc=68, noir=9)
OPTIMAL_THRESHOLD = 39  # Seuil optimal calculé: (68+9)/2 ≈ 39

# Bang-Bang Controller
BANGBANG_THRESHOLD = OPTIMAL_THRESHOLD
BANGBANG_DELTA = 50
BANGBANG_SPEED = 100  # mm/s

# Proportional Controller
P_KP = 2.0
P_SETPOINT = OPTIMAL_THRESHOLD
P_SPEED = 150  # mm/s

# Proportional-Integral Controller
PI_KP = 1.5
PI_KI = 0.10
PI_SETPOINT = OPTIMAL_THRESHOLD
PI_SPEED = 125  # mm/s

# Proportional-Integral-Derivative Controller
PID_KP = 0.6
PID_KI = 0.04
PID_KD = 1.2
PID_SETPOINT = OPTIMAL_THRESHOLD
PID_SPEED = 140  # mm/s


# Paramètres généraux
LOOP_ITERATIONS = 1000  # Nombre d'itérations par test
LOOP_DELAY = 0.1  # Délai entre itérations (secondes)