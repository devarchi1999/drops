import re
class ValidateRegisterDetails:

    def validate(self,email,password,confirm_password,username,playlist):


        val=-2


        # validating email id
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if len(username)>0:
            val=-1
            if re.search(regex,email):
                val=0
                if len(password)>=6:
                    val = 1
                    if password==confirm_password:
                        val = 2
                        if len(playlist)>0:
                            val=3


        return val