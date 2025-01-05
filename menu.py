from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20

class Menu:
    def __init__(self, display):
        self.display = display
        self.gfx = GFX(display.width, display.height, display.pixel)
        self.write20 = Write(display, ubuntu_mono_20)

    def show_main_menu(self):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text("Waiting for", 15, 32)
        self.display.text("your NFC-TAG", 10, 42)
        self.display.show()

    def show_admin_main_menu(self, selected_option):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text("COFFEE-TIME :)", 0, 32)
        #self.gfx.rect(0, 49, 50, 14, 1)
        self.display.text("Start", 4, 52)
        self.display.text("Admin", 85, 52)
        if selected_option == 0:
            self.gfx.rect(0, 49, 50, 14, 1)
        else:
            self.gfx.rect(80, 49, 50, 14, 1)
        self.display.show()

    def show_user_main_menu(self):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text("COFFEE-TIME :)", 0, 32)
        self.gfx.rect(0, 49, 50, 14, 1)
        self.display.text("Start", 4, 52)
        self.display.show()

    def show_incorrect_nfc(self):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text("User not", 28, 32)
        self.display.text("recognized!", 18, 42)
        self.display.show()

    def show_admin_menu(self, selected_option):
        self.display.fill(0)
        self.display.text("Admin-Menu", 0, 0)
        self.display.text("New User", 0, 20)
        self.display.text("Reset Counter", 0, 30)
        self.display.text("Brew-Time", 0, 40)
        self.display.text("Back", 0, 50)
        self.gfx.rect(0, 20 + selected_option * 10, 128, 10, 1)
        self.display.show()

    def show_coffee_started(self):
        self.display.fill(0)
        self.display.text("Coffee", 30, 20)
        self.display.text("Started!", 25, 40)
        self.display.show()
        
    def show_new_user_menu(self):
        self.display.fill(0)
        self.display.text("Show new RF-TAG", 0, 20)
        self.display.show()

    def show_new_user_registered(self):
        self.display.fill(0)
        self.display.text("New User", 30, 20)
        self.display.text("registered", 20, 40)
        self.display.show()
        
    def show_set_time_menu(self, brew_time):
        self.display.fill(0)
        self.display.text("Set Brew Time", 0, 0)
        self.display.text(f"Time: {brew_time}s", 20, 30)
        self.gfx.rect(80, 50, 40, 14, 1)
        self.display.text("Save", 85, 53)
        self.display.show()
        
    def show_rf_tag_prompt(self):
        self.display.fill(0)
        self.display.text("Show RF-Tag", 10, 20)
        self.display.text("Waiting...", 20, 40)
        self.display.show()

    def show_reset_counter_menu(self, coffee_count):
        self.display.fill(0)
        self.display.text(f"Count: {coffee_count}", 20, 30)
        self.gfx.rect(0, 50, 40, 14, 1)
        self.display.text("Reset", 5, 53)
        self.gfx.rect(88, 50, 40, 14, 1)
        self.display.text("Back", 93, 53)
        self.display.show()
        
    def show_timeout_message(self):
        self.display.fill(0)
        self.display.text("Timeout", 30, 20)
        self.display.text("No RF-Tag detected", 0, 40)
        self.display.show()
