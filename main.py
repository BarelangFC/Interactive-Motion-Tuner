import sys
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDoubleSpinBox, QTextEdit, QRadioButton


# Fungsi untuk menangani output terminal
def Terminal(terminal_output, message):
    terminal_output.append(message)
    terminal_output.ensureCursorVisible()


class SensorShm:
    @staticmethod
    def get_position():
        # Kembalikan data posisi sebagai list atau tuple
        return [0.5, 1.0, -1.5]  # Ganti dengan data nyata

class ActuatorShm:
    @staticmethod
    def get_hardness():
        # Kembalikan data kekerasan sebagai list atau tuple
        return [0.9, 0.8, 1.0]  # Ganti dengan data nyata


# Kelas untuk menangani data Servo
class Servo:
    def __init__(self):
        self.angles = []
        self.stiffnesses = []
        self.time_exec = []

    def update_angle(self, index, value):
        if index < len(self.angles):
            self.angles[index] = value
        else:
            self.angles.append(value)

    def update_stiffness(self, index, value):
        if index < len(self.stiffnesses):
            self.stiffnesses[index] = value
        else:
            self.stiffnesses.append(value)

    def update_time_exec(self, value):
        self.time_exec = [value]  # Karena hanya ada satu nilai untuk waktu eksekusi

    def get_angles(self):
        return self.angles

    def get_stiffnesses(self):
        return self.stiffnesses

    def get_time_exec(self):
        return self.time_exec


# Kelas untuk menangani Radio Button
class RadioButtonHandler:
    def __init__(self, window):
        self.window = window
        self.free_move_radio_button = self.window.findChild(QRadioButton, "freeMoveRadioButton")
        self.motion_radio_button = self.window.findChild(QRadioButton, "motionRadioButton")

        # Set 'freeMoveRadioButton' sebagai pilihan default
        self.free_move_radio_button.setChecked(True)

        # Hubungkan sinyal toggled ke fungsi handler, menggunakan lambda
        self.free_move_radio_button.toggled.connect(
            lambda: self.radio_button_toggled(self.free_move_radio_button))
        self.motion_radio_button.toggled.connect(
            lambda: self.radio_button_toggled(self.motion_radio_button))

    def radio_button_toggled(self, button):
        if button.isChecked():  # Mengakses langsung radio button
            if button == self.free_move_radio_button:
                print("Free Move Mode selected")
                Terminal(self.terminal_output, "Free Move Mode selected")
            elif button == self.motion_radio_button:
                print("Motion Mode selected")
                Terminal(self.terminal_output, "Motion Mode selected")


# Kelas untuk menangani Button
class ButtonHandler:
    def __init__(self, window):
        self.window = window
        self.window.loadButton.clicked.connect(self.openFile)
        self.window.saveButton.clicked.connect(self.saveFile)

    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.window, "Open Lua File", "", "Lua Files (*.lua)", options=options)
        if file_name:
            QMessageBox.information(self.window, "File Selected", f"You selected: {file_name}")
        else:
            QMessageBox.warning(self.window, "No File Selected", "No file was selected.")

    def saveFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.window, "Save Lua File", "", "Lua Files (*.lua)", options=options)
        if file_name:
            QMessageBox.information(self.window, "File Saved", f"File has been saved: {file_name}")
        else:
            QMessageBox.warning(self.window, "No File Saved", "The file was not saved.")


# Kelas untuk menangani SpinBox
class SpinBoxHandler:
    def __init__(self, window, terminal_output, servo):
        self.window = window
        self.servo = servo  # Menyimpan referensi ke instance Servo
        self.terminal_output = terminal_output  # Menyimpan referensi ke output terminal

        self.angle_object_names = [
            "RShoulderPitchAngle", "LShoulderPitchAngle", "RShoulderRollAngle", "LShoulderRollAngle",
            "RElbowYawAngle", "LElbowYawAngle", "RHipYawAngle", "LHipYawAngle", "RHipRollAngle",
            "LHipRollAngle", "RHipPitchAngle", "LHipPitchAngle", "RKneePitchAngle", "LKneePitchAngle",
            "RAnklePitchAngle", "LAnklePitchAngle", "RAnkleRollAngle", "LAnkleRollAngle",
            "HeadYawAngle", "HeadPitchAngle"
        ]

        self.stiffness_object_names = [
            "RShoulderPitchStiffness", "LShoulderPitchStiffness", "RShoulderRollStiffness", "LShoulderRollStiffness",
            "RElbowYawStiffness", "LElbowYawStiffness", "RHipYawStiffness", "LHipYawStiffness",
            "RHipRollStiffness", "LHipRollStiffness", "RHipPitchStiffness", "LHipPitchStiffness",
            "RKneePitchStiffness", "LKneePitchStiffness", "RAnklePitchStiffness", "LAnklePitchStiffness",
            "RAnkleRollStiffness", "LAnkleRollStiffness", "HeadYawStiffness", "HeadPitchStiffness"
        ]

        self.exec_time_object_name = "ExecTime"
        
        self.initialize_spinboxes()

    def initialize_spinboxes(self):
        
        position_data = SensorShm.get_position()
        hardness_data = ActuatorShm.get_hardness()
        
        # Loop untuk menginisialisasi QDoubleSpinBox berdasarkan angle_object_names
        for index, object_name in enumerate(self.angle_object_names):
            angle_spinbox = self.window.findChild(QDoubleSpinBox, object_name)
            if angle_spinbox:
                angle_spinbox.setRange(-360.0, 360.0)
                angle_spinbox.setSingleStep(1.0)
                #angle_spinbox.setValue(100.0)
                if index < len(position_data):
                    angle_value = position_data[index] * 180 / 3.14159  # Konversi dari radian ke derajat
                    angle_spinbox.setValue(angle_value)
                    self.servo.update_angle(index, angle_value)
                angle_spinbox.valueChanged.connect(
                    lambda value, name=object_name, idx=index: (
                        self.servo.update_angle(idx, value),
                        print(f"{name} angle changed to {value}"),
                        Terminal(self.terminal_output, f"{name} angle changed to {value}")
                    )
                )
            else:
                print(f"Angle spinbox {object_name} not found!")

        # Loop untuk menginisialisasi QDoubleSpinBox berdasarkan stiffness_object_names
        for index, object_name in enumerate(self.stiffness_object_names):
            stiffness_spinbox = self.window.findChild(QDoubleSpinBox, object_name)
            if stiffness_spinbox:
                stiffness_spinbox.setRange(0.0, 1.0)
                stiffness_spinbox.setSingleStep(0.1)
                #stiffness_spinbox.setValue(1.0)
                if index < len(hardness_data):
                    stiffness_value = hardness_data[index]
                    stiffness_spinbox.setValue(stiffness_value)
                    self.servo.update_stiffness(index, stiffness_value)
                stiffness_spinbox.valueChanged.connect(
                    lambda value, name=object_name, idx=index: (
                        self.servo.update_stiffness(idx, value),
                        print(f"{name} stiffness changed to {value}"),
                        Terminal(self.terminal_output, f"{name} stiffness changed to {value}")
                    )
                )
            else:
                print(f"Stiffness spinbox {object_name} not found!")

        # Inisialisasi QDoubleSpinBox untuk ExecTime
        exec_time_spinbox = self.window.findChild(QDoubleSpinBox, self.exec_time_object_name)
        if exec_time_spinbox:
            exec_time_spinbox.setRange(0.0, 20.0)
            exec_time_spinbox.setSingleStep(0.1)
            exec_time_spinbox.setValue(5.0)
            self.servo.update_time_exec(exec_time_spinbox.value())
            exec_time_spinbox.valueChanged.connect(
                lambda value: (
                    self.servo.update_time_exec(value),
                    print(f"ExecTime changed to {value}"),
                    Terminal(self.terminal_output, f"ExecTime changed to {value}")
                )
            )
        else:
            print(f"ExecTime spinbox {self.exec_time_object_name} not found!")

        # Cetak nilai servo saat inisialisasi
        self.print_servo_values()

    # Metode untuk mencetak nilai servo ke terminal
    def print_servo_values(self):
        print("Servo Angle Values       :", self.servo.get_angles())
        print("Servo Stiffness Values   :", self.servo.get_stiffnesses())
        print("Servo Execution Time     :", self.servo.get_time_exec())

        Terminal(self.terminal_output, f"Servo Angle Values        : {self.servo.get_angles()}")
        Terminal(self.terminal_output, f"Servo Stiffness Values  : {self.servo.get_stiffnesses()}")
        Terminal(self.terminal_output, f"Servo Execution Time   : {self.servo.get_time_exec()}")


# Kelas utama untuk menginisialisasi aplikasi
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Memuat file .ui
        loader = QUiLoader()
        self.window = loader.load("tunning.ui", None)
        self.window.setWindowTitle("All In One Barelang FC")

        # Ambil TextEdit untuk terminal output
        terminal_output = self.window.findChild(QTextEdit, "TerminalOutput")

        # Buat instance dari Servo
        self.servo = Servo()

        # Buat instance dari handler class
        self.radio_button_handler = RadioButtonHandler(self.window)
        self.button_handler = ButtonHandler(self.window)
        self.spinbox_handler = SpinBoxHandler(self.window, terminal_output, self.servo)

        # Tampilkan jendela
        self.window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()  # Membuat instance dari kelas MainWindow
    sys.exit(app.exec())
