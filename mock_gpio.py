class GPIO:
    BOARD = "BOARD"
    OUT = "OUT"
    IN = "IN"
    
    @staticmethod
    def setmode(mode):
        print(f"Mock GPIO: Setting mode to {mode}")
        
    @staticmethod
    def setup(pin, mode):
        print(f"Mock GPIO: Setting up pin {pin} in mode {mode}")
        
    @staticmethod
    def output(pin, value):
        print(f"Mock GPIO: Setting pin {pin} to {value}")
        
    @staticmethod
    def input(pin):
        print(f"Mock GPIO: Reading from pin {pin}")
        return 0
        
    @staticmethod
    def cleanup():
        print("Mock GPIO: Cleaning up")