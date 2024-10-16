# Motion-Maker
This is a qt5 based application created by [BarelangFC](https://github.com/BarelangFC) member which is used to make a motion using lua for humanoid robot

## Feature
- [x] Connect to multiple servos
- [x] Read and write value based on shared memory 
- [x] Make a new motion
- [x] Change angle, stiffnes and time execution based on input
- [x] Load and save from existing motion
- [x] Dual mode: Free motion (record motion) and forward kinematics
- [x] Play motion, state, stand up and stance
- [x] Show list state and program
- [ ] Responsive GUI (Under developments)

## Requirement
### 1. Pyside6
Jika belum install pip:
```
sudo apt update
sudo apt install python3 python3-pip
```

Jika sudah menginstall pip:
```
pip install PySide6
```
### 2. Lua
```
sudo apt update
sudo apt install lua5.3
```

