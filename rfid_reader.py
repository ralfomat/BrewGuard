from mfrc522 import MFRC522

class RFIDReader:
    def __init__(self, config):
        self.rfid = MFRC522(spi_id=0, sck=config['RFID_SCK'], miso=config['RFID_MISO'],
                            mosi=config['RFID_MOSI'], cs=config['RFID_CS'], rst=config['RFID_RST'])
        print("RFID Reader inizialized")

    async def read_card(self):
        self.rfid.init()
        (card_status, card_type) = self.rfid.request(self.rfid.REQIDL)
        if card_status == self.rfid.OK:
            (card_status, card_id) = self.rfid.SelectTagSN()
            if card_status == self.rfid.OK:
                print(card_id)
                return int.from_bytes(bytes(card_id), "little", False)
            
        return None
