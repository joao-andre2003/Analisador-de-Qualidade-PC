import minimalmodbus
import serial
import time

PORTA_COM = 'COM3'
BAUDRATE = 57600 

slave_ids = [1, 2, 3, 4, 5]
paridades = [
    ('Par (EVEN)', serial.PARITY_EVEN),
    ('Nenhuma (NONE)', serial.PARITY_NONE)
]

print(f"Varredura na {PORTA_COM} em {BAUDRATE} bps\n")

conectado = False

for slave_id in slave_ids:
    for nome_paridade, paridade in paridades:
        try:
            analisador = minimalmodbus.Instrument(PORTA_COM, slave_id)
            analisador.serial.baudrate = BAUDRATE
            analisador.serial.bytesize = 8
            analisador.serial.parity = paridade
            analisador.serial.stopbits = 1
            analisador.serial.timeout = 1.0
            
            dados = analisador.read_registers(registeraddress=2, number_of_registers=2, functioncode=4)
            
            print("="*60)
            print("SUCESSO CONECXÃO")
            print(f" -> Slave ID correto: {slave_id}")
            print(f" -> Paridade correta: {nome_paridade}")
            print(f" -> Dados de teste recebidos: {dados}")
            print("="*60)
            conectado = True
            break
        except Exception:
            pass
            
    if conectado:
        break

if not conectado:
    print("\n❌ Nenhuma combinação respondeu.")
    print("\nÚltima checagem:")
    print("1. O app RedeMB foi TOTALMENTE FECHADO? (Se ele estiver rodando, o Python não recebe resposta).")
    print("2. A velocidade 57600 está correta? Tente trocar BAUDRATE para 9600 no topo do script e rodar de novo.")