from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20, bookerly_20

class Menu:
    def __init__(self, display):
        self.display = display
        self.gfx = GFX(display.width, display.height, display.pixel)
        self.write20 = Write(display, bookerly_20)

    def show_main_menu(self):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text("Waiting for", 15, 32)
        self.display.text("your RF-TAG", 10, 42)
        self.display.show()

    def show_admin_main_menu(self, selected_option, coffee_count):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text(f"Coffees: {coffee_count}", 0, 32)
        self.display.text("Start", 4, 52)
        self.display.text("Admin", 85, 52)
        if selected_option == 0:
            self.gfx.rect(0, 49, 50, 14, 1)
        else:
            self.gfx.rect(80, 49, 50, 14, 1)
        self.display.show()

    def show_user_main_menu(self, coffee_count):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text(f"Coffees: {coffee_count}", 0, 32)
        self.gfx.rect(0, 49, 50, 14, 1)
        self.display.text("Start", 4, 52)
        self.display.show()

    def show_incorrect_nfc(self):
        self.display.fill(0)
        self.write20.text("BrewGuard", 10, 0)
        self.display.text("User not", 28, 32)
        self.display.text("recognized!", 18, 42)
        self.display.show()

    def show_admin_menu(self, options, start_index, selected_index):
        self.display.fill(0)
        self.display.text("Admin Menu", 0, 0)
        for i in range(4):
            if start_index + i < len(options):
                self.display.text(options[start_index + i], 5, 16 + i * 12)
        selected_y = 14 + ((selected_index - start_index) % 4) * 12
        self.gfx.rect(0, selected_y, 128, 12, 1)
        self.display.show()

    def show_coffee_started(self, coffee_count):
        self.display.fill(0)
        self.display.text("Coffee", 30, 10)
        self.display.text("Started!", 25, 25)
        self.display.text(f"Coffee No. {coffee_count}", 20, 40)
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

    def show_reset_counter_menu(self, coffee_count, selected_option):
        self.display.fill(0)
        self.display.text(f"Count: {coffee_count}", 20, 20)
        self.display.text("Reset", 5, 53)
        self.display.text("Back", 93, 53)
        if selected_option == 0:
            self.gfx.rect(0, 50, 50, 14, 1)
        else:
            self.gfx.rect(88, 50, 40, 14, 1)
        self.display.show()
        
    def show_timeout_message(self):
        self.display.fill(0)
        self.display.text("Timeout", 30, 20)
        self.display.text("No RF-TAG detected", 0, 40)
        self.display.show()
        
    def show_user_exists_error(self, user_id):
        self.display.fill(0)
        self.display.text("Error:", 0, 10)
        self.display.text(f"User ID {user_id}", 0, 30)
        self.display.text("already exists", 0, 40)
        self.display.show()

    def show_user_added_success(self, user_id):
        self.display.fill(0)
        self.display.text("Success:", 0, 10)
        self.display.text(f"User ID {user_id}", 0, 30)
        self.display.text("added", 0, 40)
        self.display.show()

    def show_all_users(self, users, start_index):
        self.display.fill(0)
        self.display.text("Users:", 0, 0)
        for i in range(4):
            if start_index + i < len(users):
                user = users[start_index + i]
                self.display.text(f"{user.rf_id}: {user.coffee_count}", 0, 16 + i * 12)
        self.display.show()

    def show_reset_all_confirmation(self, selected_option):
        self.display.fill(0)
        self.display.text("Reset all User", 0, 10)
        self.display.text("Counters?", 0, 22)
        self.display.text("Back", 9, 52)
        self.display.text("OK", 102, 52)
        if selected_option == 0:
            self.gfx.rect(5, 48, 40, 16, 1)
        else:
            self.gfx.rect(95, 48, 30, 16, 1)
        self.display.show()
        
    def show_counter_reset(self):
        self.display.fill(0)
        self.display.text("All counters", 0, 20)
        self.display.text("are reset!", 0, 40)
        self.display.show()
        
    def show_message(self, message):
        self.display.fill(0)
        lines = message.split('\n')
        for i, line in enumerate(lines):
            self.display.text(line, 0, i * 12)
        self.display.show()