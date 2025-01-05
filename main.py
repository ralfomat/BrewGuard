import uasyncio as asyncio
from machine import Pin, I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20, bookerly_20
from menu import Menu
from rfid_reader import RFIDReader
from user_manager import UserManager
import relay
import utime

# Konfiguration
CONFIG = {
    'WIDTH': 128,
    'HEIGHT': 64,
    'SCL_PIN': 17,
    'SDA_PIN': 16,
    'UP_PIN': 10,
    'DOWN_PIN': 11,
    'ENTER_PIN': 12,
    'RFID_SCK': 2,
    'RFID_MISO': 4,
    'RFID_MOSI': 7,
    'RFID_CS': 5,
    'RFID_RST': 18
}

def read_brew_time():
    try:
        with open('brew_time.txt', 'r') as file:
            brew_time = int(file.read().strip())
            return max(1, min(255, brew_time))
    except (FileNotFoundError, ValueError):
        return 30  # Standardwert, falls die Datei fehlt oder ungültig ist

def save_brew_time(new_brew_time):
    with open('brew_time.txt', 'w') as file:
        file.write(str(new_brew_time))

async def wait_for_rf_tag(rfid_reader, timeout=5000):  # timeout in Millisekunden
    start_time = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start_time) < timeout:
        card_id = await rfid_reader.read_card()
        if card_id:
            return card_id
        await asyncio.sleep_ms(100)
    return None

last_button_press = {
    'up': 0,
    'down': 0,
    'enter': 0
}

DEBOUNCE_TIME = 250  

def debounce(pin):
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_button_press[pin]) > DEBOUNCE_TIME:
        last_button_press[pin] = current_time
        return True
    return False

async def button_pressed(buttons):
    button_names = ['up', 'down', 'enter']
    while True:
        for button, name in zip(buttons, button_names):
            if button.value():
                if debounce(name):
                    # Warte kurz und prüfe erneut, um sicherzustellen, dass es kein Prellen war
                    await asyncio.sleep_ms(50)
                    if button.value():
                        return button
        await asyncio.sleep_ms(10)

async def wait_for_button(buttons, timeout=5000):
    try:
        return await asyncio.wait_for(button_pressed(buttons), timeout / 1000)
    except asyncio.TimeoutError:
        return None

async def wait_for_new_tag(rfid_reader):
    while True:
        new_tag_id = await rfid_reader.read_card()
        if new_tag_id:
            return new_tag_id
        await asyncio.sleep_ms(100)

async def main():
    i2c = I2C(0, scl=Pin(CONFIG['SCL_PIN']), sda=Pin(CONFIG['SDA_PIN']), freq=400000)
    display = SSD1306_I2C(CONFIG['WIDTH'], CONFIG['HEIGHT'], i2c)
    
    menu = Menu(display)
    rfid_reader = RFIDReader(CONFIG)
    user_manager = UserManager()

    up = Pin(CONFIG['UP_PIN'], Pin.IN, Pin.PULL_DOWN)
    down = Pin(CONFIG['DOWN_PIN'], Pin.IN, Pin.PULL_DOWN)
    enter = Pin(CONFIG['ENTER_PIN'], Pin.IN, Pin.PULL_DOWN)

    current_menu = "main"
    selected_option = 0
    
    brew_time = read_brew_time()

    while True:
        if current_menu == "main":
            menu.show_main_menu()
            card_id = await rfid_reader.read_card()
            
            if card_id:
                user = user_manager.get_user(card_id)
                if user:
                    if user.privileges == 'admin':
                        current_menu = "admin_main"
                    else:
                        current_menu = "user_main"
                else:
                    menu.show_incorrect_nfc()
                    await asyncio.sleep(2)
        
        elif current_menu == "admin_main":
            menu.show_admin_main_menu(selected_option, user.coffee_count)
            button = await wait_for_button([up, down, enter])
            
            if button is None:
                current_menu = "main"
                continue
            
            if button == up:
                selected_option = (selected_option - 1) % 2
            elif button == down:
                selected_option = (selected_option + 1) % 2
            elif button == enter:
                if selected_option == 0:  # Start
                    relay.relay_on()
                    user.increment_coffee_count()
                    menu.show_coffee_started(user.coffee_count)
                    await asyncio.sleep(brew_time)
                    relay.relay_off()
                    current_menu = "main"
                else:  # Admin
                    current_menu = "admin_menu"
                    selected_option = 0
        
        elif current_menu == "user_main":
            menu.show_user_main_menu(user.coffee_count)
            button = await wait_for_button([enter])
            
            if button is None:
                current_menu = "main"
                continue
            
            if button == enter:
                relay.relay_on()
                user.increment_coffee_count()
                menu.show_coffee_started(user.coffee_count)
                await asyncio.sleep(brew_time)
                relay.relay_off()
                current_menu = "main"
            
        elif current_menu == "admin_menu":
            menu.show_admin_menu(selected_option)
            button = await wait_for_button([up, down, enter])
            
            if button is None:
                current_menu = "main"
                continue
                        
            if button == up:
                selected_option = (selected_option - 1) % 4
            elif button == down:
                selected_option = (selected_option + 1) % 4
            elif button == enter:
                if selected_option == 0:  # New User
                    menu.show_new_user_menu()
                    new_tag_id = await wait_for_new_tag(rfid_reader)
                    try:
                        result = user_manager.add_user(new_tag_id, 'user')
                        menu.show_user_added_success(new_tag_id)
                    except ValueError as e:
                        menu.show_user_exists_error(new_tag_id)
                    await asyncio.sleep(2)
                    
                elif selected_option == 1:  # Reset Counter
                    menu.show_rf_tag_prompt()
                    card_id = await wait_for_rf_tag(rfid_reader)
                    if card_id:
                        current_menu = "reset_counter"
                    else:
                        menu.show_timeout_message()
                        await asyncio.sleep(2)
                        current_menu = "admin_menu"
                
                elif selected_option == 2:  # Brew Time
                    current_menu = "set_time"
                
                elif selected_option == 3:  # Back
                    current_menu = "admin_main"
            
        elif current_menu == "set_time":
            menu.show_set_time_menu(brew_time)
            button = await wait_for_button([up, down, enter])

            if button is None:
                current_menu = "admin_menu"
                continue

            if button == up:
                brew_time = min(255, brew_time + 1)
            elif button == down:
                brew_time = max(1, brew_time - 1)
            elif button == enter:
                save_brew_time(brew_time)
                current_menu = "admin_menu"
                
        elif current_menu == "reset_counter":
            user = user_manager.get_user(card_id)
            if user:
                selected_option = 0  # 0 für "Reset", 1 für "Back"
                while True:
                    menu.show_reset_counter_menu(user.coffee_count, selected_option)
                    button = await wait_for_button([up, down, enter])
                    
                    if button is None:
                        current_menu = "admin_menu"
                        break
                    elif button == up or button == down:
                        selected_option = 1 - selected_option  # Wechselt zwischen 0 und 1
                    elif button == enter:
                        if selected_option == 0:  # Reset
                            user.reset_coffee_count()
                            menu.show_reset_counter_menu(0, selected_option)
                            await asyncio.sleep(1)
                        current_menu = "admin_menu"
                        break
            else:
                menu.show_incorrect_nfc()
                await asyncio.sleep(2)
                current_menu = "admin_menu"
                
                await asyncio.sleep_ms(100)

if __name__ == "__main__":
    asyncio.run(main())
