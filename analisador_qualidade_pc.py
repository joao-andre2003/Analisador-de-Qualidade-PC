import minimalmodbus
import serial
import struct
import time
import requests

TB_SERVER = ""
TB_TOKEN = ""

MEASUREMENT_INTERVAL = 60
START_MEASUREMENT_ON_ZERO = False

PORT_COM = 'COM3'
BAUDRATE  = 57600
SLAVE_ID  = 2

RGSTR_ADDR = 0
RGSTR_N    = 1

ATIVAR_HARMONICO = True

g_Measures_Names = ['U0', 'U12', 'U23', 'U31', 'U1', 'U2', 'U3', 'I0', 'IN', 'I1', 'I2', 'I3', 'F1', 'F2', 'F3', 'F1IEC', 'P0', 'P1', 'P2', 'P3', 'Q0', 'Q1', 'Q2', 'Q3', 'S0', 'S1', 'S2', 'S3', 'FP0', 'FP1', 'FP2', 'FP3', 'FP0D', 'FP1D', 'FP2D', 'FP3D', 'FATORK', 'EApositivo', 'ERpositivo', 'EAnegativo', 'ERnegativo', 'MDA', 'DA', 'MDS', 'DS', 'UANTHD', 'UBNTHD', 'UCNTHD', 'IATHD', 'IBTHD', 'ICTHD', 'U1THDagrup', 'U2THDagrup', 'U3THDagrup', 'I1THDagrup', 'I2THDagrup', 'I3THDagrup', 'U1AgrupH1', 'U1AgrupH2', 'U1AgrupH3', 'U1AgrupH4', 'U1AgrupH5', 'U1AgrupH6', 'U1AgrupH7', 'U1AgrupH8', 'U1AgrupH9', 'U1AgrupH10', 'U1AgrupH11', 'U1AgrupH12', 'U1AgrupH13', 'U1AgrupH14', 'U1AgrupH15', 'U1AgrupH16', 'U1AgrupH17', 'U1AgrupH18', 'U1AgrupH19', 'U1AgrupH20', 'U1AgrupH21', 'U1AgrupH22', 'U1AgrupH23', 'U1AgrupH24', 'U1AgrupH25', 'U1AgrupH26', 'U1AgrupH27', 'U1AgrupH28', 'U1AgrupH29', 'U1AgrupH30', 'U1AgrupH31', 'U1AgrupH32', 'U1AgrupH33', 'U1AgrupH34', 'U1AgrupH35', 'U1AgrupH36', 'U1AgrupH37', 'U1AgrupH38', 'U1AgrupH39', 'U1AgrupH40', 'U2AgrupH1', 'U2AgrupH2', 'U2AgrupH3', 'U2AgrupH4', 'U2AgrupH5', 'U2AgrupH6', 'U2AgrupH7', 'U2AgrupH8', 'U2AgrupH9', 'U2AgrupH10', 'U2AgrupH11', 'U2AgrupH12', 'U2AgrupH13', 'U2AgrupH14', 'U2AgrupH15', 'U2AgrupH16', 'U2AgrupH17', 'U2AgrupH18', 'U2AgrupH19', 'U2AgrupH20', 'U2AgrupH21', 'U2AgrupH22', 'U2AgrupH23', 'U2AgrupH24', 'U2AgrupH25', 'U2AgrupH26', 'U2AgrupH27', 'U2AgrupH28', 'U2AgrupH29', 'U2AgrupH30', 'U2AgrupH31', 'U2AgrupH32', 'U2AgrupH33', 'U2AgrupH34', 'U2AgrupH35', 'U2AgrupH36', 'U2AgrupH37', 'U2AgrupH38', 'U2AgrupH39', 'U2AgrupH40', 'U3AgrupH1', 'U3AgrupH2', 'U3AgrupH3', 'U3AgrupH4', 'U3AgrupH5', 'U3AgrupH6', 'U3AgrupH7', 'U3AgrupH8', 'U3AgrupH9', 'U3AgrupH10', 'U3AgrupH11', 'U3AgrupH12', 'U3AgrupH13', 'U3AgrupH14', 'U3AgrupH15', 'U3AgrupH16', 'U3AgrupH17', 'U3AgrupH18', 'U3AgrupH19', 'U3AgrupH20', 'U3AgrupH21', 'U3AgrupH22', 'U3AgrupH23', 'U3AgrupH24', 'U3AgrupH25', 'U3AgrupH26', 'U3AgrupH27', 'U3AgrupH28', 'U3AgrupH29', 'U3AgrupH30', 'U3AgrupH31', 'U3AgrupH32', 'U3AgrupH33', 'U3AgrupH34', 'U3AgrupH35', 'U3AgrupH36', 'U3AgrupH37', 'U3AgrupH38', 'U3AgrupH39', 'U3AgrupH40', 'I1AgrupH1', 'I1AgrupH2', 'I1AgrupH3', 'I1AgrupH4', 'I1AgrupH5', 'I1AgrupH6', 'I1AgrupH7', 'I1AgrupH8', 'I1AgrupH9', 'I1AgrupH10', 'I1AgrupH11', 'I1AgrupH12', 'I1AgrupH13', 'I1AgrupH14', 'I1AgrupH15', 'I1AgrupH16', 'I1AgrupH17', 'I1AgrupH18', 'I1AgrupH19', 'I1AgrupH20', 'I1AgrupH21', 'I1AgrupH22', 'I1AgrupH23', 'I1AgrupH24', 'I1AgrupH25', 'I1AgrupH26', 'I1AgrupH27', 'I1AgrupH28', 'I1AgrupH29', 'I1AgrupH30', 'I1AgrupH31', 'I1AgrupH32', 'I1AgrupH33', 'I1AgrupH34', 'I1AgrupH35', 'I1AgrupH36', 'I1AgrupH37', 'I1AgrupH38', 'I1AgrupH39', 'I1AgrupH40', 'I2AgrupH1', 'I2AgrupH2', 'I2AgrupH3', 'I2AgrupH4', 'I2AgrupH5', 'I2AgrupH6', 'I2AgrupH7', 'I2AgrupH8', 'I2AgrupH9', 'I2AgrupH10', 'I2AgrupH11', 'I2AgrupH12', 'I2AgrupH13', 'I2AgrupH14', 'I2AgrupH15', 'I2AgrupH16', 'I2AgrupH17', 'I2AgrupH18', 'I2AgrupH19', 'I2AgrupH20', 'I2AgrupH21', 'I2AgrupH22', 'I2AgrupH23', 'I2AgrupH24', 'I2AgrupH25', 'I2AgrupH26', 'I2AgrupH27', 'I2AgrupH28', 'I2AgrupH29', 'I2AgrupH30', 'I2AgrupH31', 'I2AgrupH32', 'I2AgrupH33', 'I2AgrupH34', 'I2AgrupH35', 'I2AgrupH36', 'I2AgrupH37', 'I2AgrupH38', 'I2AgrupH39', 'I2AgrupH40', 'I3AgrupH1', 'I3AgrupH2', 'I3AgrupH3', 'I3AgrupH4', 'I3AgrupH5', 'I3AgrupH6', 'I3AgrupH7', 'I3AgrupH8', 'I3AgrupH9', 'I3AgrupH10', 'I3AgrupH11', 'I3AgrupH12', 'I3AgrupH13', 'I3AgrupH14', 'I3AgrupH15', 'I3AgrupH16', 'I3AgrupH17', 'I3AgrupH18', 'I3AgrupH19', 'I3AgrupH20', 'I3AgrupH21', 'I3AgrupH22', 'I3AgrupH23', 'I3AgrupH24', 'I3AgrupH25', 'I3AgrupH26', 'I3AgrupH27', 'I3AgrupH28', 'I3AgrupH29', 'I3AgrupH30', 'I3AgrupH31', 'I3AgrupH32', 'I3AgrupH33', 'I3AgrupH34', 'I3AgrupH35', 'I3AgrupH36', 'I3AgrupH37', 'I3AgrupH38', 'I3AgrupH39', 'I3AgrupH40']

g_RgtrsInfo = [
    [30003 - 30001, 74],
    [30201 - 30001, 16]
]
g_RgtrsInfo_TwoBytes = [
    [33001 - 30001, 12]
]
g_RgtrsInfo_Harmonico = [
    [34001 - 30001, 80], # U1 
    [34081 - 30001, 80], # U2
    [34161 - 30001, 80], # U3
    [34241 - 30001, 80], # I1
    [34321 - 30001, 80], # I2
    [34401 - 30001, 80]  # I3
]

g_analisador = None
def setup_analisador():
    global g_analisador
    g_analisador = minimalmodbus.Instrument(PORT_COM, SLAVE_ID)
    g_analisador.serial.baudrate = BAUDRATE
    g_analisador.serial.bytesize = 8
    g_analisador.serial.parity = serial.PARITY_NONE
    g_analisador.serial.stopbits = 2
    g_analisador.serial.timeout = 1.0

def get_float_from_bytes(two_bytes_a: int, two_bytes_b: int) -> float:
    four_bytes_array = bytes([
        (two_bytes_a >> 8) & 0xFF,  # Byte alto de A
         two_bytes_a & 0xFF,        # Byte baixo de A
        (two_bytes_b >> 8) & 0xFF,  # Byte alto de B
         two_bytes_b & 0xFF         # Byte baixo de B
    ])
    return struct.unpack('<f', four_bytes_array)[0]

def read_2bytes_registor(data: list[float]) -> list[float]:
    global g_RgtrsInfo_TwoBytes, g_analisador
    new_data = []
    for register in g_RgtrsInfo_TwoBytes:
        new_data = g_analisador.read_registers(registeraddress=register[RGSTR_ADDR], 
                                            number_of_registers=register[RGSTR_N], 
                                            functioncode=4)
    data.extend(new_data)
    return data

def read_4bytes_registor(data: list[float], RgtrsInfo: list[int]) -> list[float]:
    global g_analisador
    new_data = []
    for register in RgtrsInfo:
        new_data_bytes = g_analisador.read_registers(registeraddress=register[RGSTR_ADDR], 
                                            number_of_registers=register[RGSTR_N], 
                                            functioncode=4)
        for i in range(0, register[RGSTR_N], 2):
            new_data.append(get_float_from_bytes(new_data_bytes[i], new_data_bytes[i+1]))

    data.extend(new_data)
    return data

def send_data_https(data: list[float], Measures_Names: list[str]) -> bool:
    url = f"https://{TB_SERVER}/api/v1/{TB_TOKEN}/telemetry"
    data_dict = {}

    timestamp_mili = int(time.time()) * 1000
    data_dict["ts"] = timestamp_mili

    values_dict = dict(zip(Measures_Names, data))
    data_dict["values"] = values_dict

    print(f"Enviando dados: {data_dict}")
    return requests.post(url, json = data_dict)

def main():
    setup_analisador()

    timestamp_measurement = int(time.time())
    if START_MEASUREMENT_ON_ZERO:
        seconds_to_next_minute = 60 - (timestamp_measurement % 60)
        timestamp_measurement += seconds_to_next_minute

        print(f"{seconds_to_next_minute} segundos para o proximo minuto. Esperando para inciar...")
        time.sleep(seconds_to_next_minute)

    print(" > Iniciando programa <")
    while(True):
        try:
            data = []
            data = read_4bytes_registor(data, g_RgtrsInfo)
            data = read_2bytes_registor(data)
            if ATIVAR_HARMONICO: data = read_4bytes_registor(data, g_RgtrsInfo_Harmonico)

            print(f"Dados lidos.")
            response = send_data_https(data, g_Measures_Names)

            print(f"HTTPS Post Status: {response}")
        except Exception as e:
            print(f"ERRO: {e}")

        timestamp_measurement += MEASUREMENT_INTERVAL
        timestamp = int(time.time())

        wait_time = timestamp_measurement - timestamp
        if wait_time > 0:
            time.sleep(wait_time)
main()