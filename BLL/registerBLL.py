# BLL/registerBLL.py

from VanPhuTung.BLL.loginBLL import LoginBLL
from VanPhuTung.DTO.userDTO import UserDTO

class RegisterBLL:
    def __init__(self):
        self.loginBLL = LoginBLL()

    def register_user(self, username, password):
        user = UserDTO(username=username, password=password)
        success = self.loginBLL.add_user(user)
        return success
