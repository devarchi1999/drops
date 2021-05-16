import re
class ValidateLoginDetails:
    def validate(self,email,password):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        val=0
        if re.search(regex,email):
            val=1
            if len(password)>=6:
                val=2
        print(val)
        return val







