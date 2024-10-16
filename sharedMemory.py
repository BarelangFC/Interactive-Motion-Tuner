from multiprocessing import shared_memory
import numpy as np
import time

class ServoSharedMemory:
    def __init__(self, angle_shm_name='dcmSensor', stiffness_shm_name='dcmActuator', number_of_servos=20):
        # Nama shared memory
        self.angle_shm_name = angle_shm_name
        self.stiffness_shm_name = stiffness_shm_name
        self.number_of_servos = number_of_servos

        # Membuka shared memory untuk sensor (angle servo)
        self.angle_servo = shared_memory.SharedMemory(name=self.angle_shm_name)
        self.angle_array = np.ndarray((self.number_of_servos,), dtype=np.float32, buffer=self.angle_servo.buf)

        # Membuka shared memory untuk aktuator (stiffness servo)
        self.stiffness_servo = shared_memory.SharedMemory(name=self.stiffness_shm_name)
        self.stiffness_array = np.ndarray((self.number_of_servos,), dtype=np.float32, buffer=self.stiffness_servo.buf)

    def read_data(self):
        """ Membaca data sudut dan kekakuan dari shared memory """
        angles = self.angle_array[:]  # Membaca sudut servo
        stiffness = self.stiffness_array[:]  # Membaca kekakuan servo
        return angles, stiffness

    def close(self):
        """ Menutup shared memory """
        self.angle_servo.close()
        self.stiffness_servo.close()


class ServoSharedMemoryWriter:
    def __init__(self, angle_shm_name='dcmSensor', stiffness_shm_name='dcmActuator', number_of_servos=20):
        # Nama shared memory
        self.angle_shm_name = angle_shm_name
        self.stiffness_shm_name = stiffness_shm_name
        self.number_of_servos = number_of_servos

        # Membuka shared memory untuk sensor (angle servo)
        self.angle_servo = shared_memory.SharedMemory(name=self.angle_shm_name)
        self.angle_array = np.ndarray((self.number_of_servos,), dtype=np.float32, buffer=self.angle_servo.buf)

        # Membuka shared memory untuk aktuator (stiffness servo)
        self.stiffness_servo = shared_memory.SharedMemory(name=self.stiffness_shm_name)
        self.stiffness_array = np.ndarray((self.number_of_servos,), dtype=np.float32, buffer=self.stiffness_servo.buf)

    def write_angles(self, angles):
        """ Menulis sudut servo ke shared memory """
        if len(angles) != self.number_of_servos:
            raise ValueError(f"Input array must have exactly {self.number_of_servos} elements.")
        self.angle_array[:] = angles  # Menulis sudut servo ke shared memory

    def write_stiffness(self, stiffness):
        """ Menulis kekakuan servo ke shared memory """
        if len(stiffness) != self.number_of_servos:
            raise ValueError(f"Input array must have exactly {self.number_of_servos} elements.")
        self.stiffness_array[:] = stiffness  # Menulis kekakuan servo ke shared memory

    def close(self):
        """ Menutup shared memory """
        self.angle_servo.close()
        self.stiffness_servo.close()


# Contoh penggunaan
if __name__ == "__main__":
    # Membaca shared memory
    reader = ServoSharedMemory()
    writer = ServoSharedMemoryWriter()

    try:
        while True:
            # Contoh menulis data ke shared memory
            new_angles = np.random.uniform(-180, 180, size=20).astype(np.float32)  # Menghasilkan sudut acak
            new_stiffness = np.random.uniform(0, 1, size=20).astype(np.float32)  # Menghasilkan kekakuan acak

            writer.write_angles(new_angles)
            writer.write_stiffness(new_stiffness)

            # Membaca data dari shared memory
            angles, stiffness = reader.read_data()

            print("Servo Angles:", angles)
            print("Servo Stiffness:", stiffness)

            time.sleep(1)  # Menunggu sebelum membaca lagi

    except KeyboardInterrupt:
        print("Terminating...")
    finally:
        # Menutup shared memory saat keluar
        reader.close()
        writer.close()
