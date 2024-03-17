from werkzeug.security import check_password_hash

class User:
    
    def _init_(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        
    @staticmethod
    def is_authenticated(self):
        return True
    
    @staticmethod
    def is_active(self):
        return True
    
    @staticmethod
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.username
    
    def check_password(self, input_password):
        return check_password_hash(self.password, input_password)
    
        