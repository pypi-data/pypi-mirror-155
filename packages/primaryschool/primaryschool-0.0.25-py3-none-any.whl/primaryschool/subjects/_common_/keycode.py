class PsKeyCode:
    def __init__(self):
        pass

    def keycode_in_alpha_upper(self, code):
        return 65 <= code <= 90

    def keycode_in_alpha_lower(self, code):
        return 97 <= code <= 122

    def keycode_in_alpha(self, code):
        return self.keycode_in_alpha_lower(
            code
        ) or self.keycode_in_alpha_upper(code)

    def keycode_in_num_neg(self, code):
        return self.keycode_in_pure_num(code) or self.keycode_in_hyphen(code)

    def keycode_in_num_float(self, code):
        return self.keycode_in_pure_num(code) or self.keycode_in_dot(code)

    def keycode_in_pure_num(self, code):
        return 48 <= code <= 57

    def keycode_in_num(self, code):
        return (
            self.keycode_in_pure_num(code)
            or self.keycode_in_hyphen(code)
            or self.keycode_in_dot(code)
        )

    def keycode_in_dot(self, code):
        return code == 46

    def keycode_in_alpha_num(self, code):
        return self.keycode_in_num(code) or self.keycode_in_alpha(code)

    def keycode_in_space(self, code):
        return code == 32

    def keycode_in_hyphen(self, code):
        return code == 45

    def keycode_in_return(self, code):
        return code == 0xD
