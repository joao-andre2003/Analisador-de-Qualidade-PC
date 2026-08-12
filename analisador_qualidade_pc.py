import minimalmodbus
import time

PORTA_COM = 'COM3'
SLAVE_ID = 2
REGISTRADOR = 2

while(True):
    try: 
        analisador = minimalmodbus.Instrument(PORTA_COM, SLAVE_ID)

        analisador.serial.baudrate = 57600
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
        valor_inteiro = analisador.read_register(REGISTRADOR, functioncode=3)
        print(f"Leitura de registrador (Int): {valor_inteiro}")

    except Exception as e:
        print(f"Erro na comunicação: {e}")
    time.sleep(2)