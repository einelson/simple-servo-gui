# Servo GUI
This is a basic applicatin to test GUI and servo control.<br>
This was designed to run on the raspberry pi with the web server being hosted to [localhost](https://localhost:8080)


## Setting up
**Libraries needed:**
```bash
pip3 install dash
pip3 install plotly
pip3 install dash-bootstrap-components
pip3 install
```

**Raspberry Pi settings:**
Terminal
```bash
sudo raspi-config
'Interfacing options'
'Remote GPIO'
'Yes'
'Finish'

sudo systemctl start pigpiod
sudo systemctl enable pigpiod
```

**Pinout:**
Pin 18 is used for the servo

## Usage
```bash
python3 app.py
```