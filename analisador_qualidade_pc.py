import minimalmodbus
import time

PORTA_COM = 'COM3'
SLAVE_ID = 2
BAUDRATE = 57600

while(True):
    try: 
        analisador = minimalmodbus.Instrument(PORTA_COM, SLAVE_ID)

        analisador.serial.baudrate = BAUDRATE
        analisador.serial.bytesize = 8
        analisador.serial.parity   = minimalmodbus.serial.PARITY_NONE
        analisador.serial.stopbits = 1
        analisador.serial.timeout  = 1.0
        break
    except Exception as e:
        print(f"Erro no USB {PORTA_COM}: {e}")
    time.sleep(1)
    

while(True):
    try:
        dados = analisador.read_registers(registeraddress=2, number_of_registers=74, functioncode=4)
        print(f"Total de valores recebidos: {len(dados)}")
        print("Valores brutos dos registradores:", dados)

    except Exception as e:
        print(f"Erro na comunicação: {e}")
    time.sleep(2)