class User:
    def __init__(self, rf_id, coffee_count, privileges):
        self.rf_id = rf_id
        self.coffee_count = coffee_count
        self.privileges = privileges

    def increment_coffee_count(self):
        self.coffee_count += 1
        UserManager.save_users()

    def reset_coffee_count(self):
        self.coffee_count = 0
        UserManager.save_users()
        

class UserManager:
    users = {}

    @classmethod
    def load_users(cls):
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    rf_id, coffee_count, privileges = line.strip().split(',')
                    cls.users[int(rf_id)] = User(int(rf_id), int(coffee_count), privileges)
        except OSError:
            print("Error loading users file")

    @classmethod
    def save_users(cls):
        try:
            with open('users.txt', 'w') as f:
                for user in cls.users.values():
                    f.write(f"{user.rf_id},{user.coffee_count},{user.privileges}\n")
        except OSError:
            print("Error saving users")

    @classmethod
    def get_user(cls, rf_id):
        return cls.users.get(rf_id)

    @classmethod
    def add_user(cls, rf_id, privileges):
        new_user = User(rf_id, 0, privileges)
        cls.users[rf_id] = new_user
        cls.save_users()

UserManager.load_users()
