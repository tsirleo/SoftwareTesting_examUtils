import struct

def clean_binary_input(binary_str):
    return binary_str.replace(" ", "")

def float_to_ieee754(value):
    """
    Converts a floating-point value to IEEE 754 binary32 representation.
    Returns the binary string.
    """
    packed = struct.pack('>f', value)  # '>f' for big-endian float
    binary_str = ''.join(f'{byte:08b}' for byte in packed)
    return binary_str

def ieee754_to_float(binary_str):
    """
    Converts an IEEE 754 binary32 string back to a floating-point value.
    """
    binary_str = clean_binary_input(binary_str)
    byte_array = [int(binary_str[i:i + 8], 2) for i in range(0, len(binary_str), 8)]
    packed = bytes(byte_array)
    return struct.unpack('>f', packed)[0]
    
def print_float_to_ieee754(float_inputs):
    for i, value in enumerate(float_inputs):
        ieee754_binary = float_to_ieee754(value)
        print(f"Float Input {i + 1}: {value}")
        print(f"IEEE 754 Binary Representation: {ieee754_binary}\n")
    print("---------------------------------------------------------")
    
def print_ieee754_to_ieee754_float(float_inputs):
    for i, value in enumerate(binary_inputs):
        float_value = ieee754_to_float(value)
        print(f"Binary Input {i + 1}: {value}")
        print(f"Converted Float Value: {float_value}\n")   
    print("---------------------------------------------------------")
    
def print_matches(float_inputs, binary_inputs):
    cleaned_binary_inputs = [clean_binary_input(b) for b in binary_inputs]

    for i, float_val in enumerate(float_inputs):
        float_binary = float_to_ieee754(float_val)

        matches = [
            j for j, binary in enumerate(cleaned_binary_inputs) if binary == float_binary
        ]
        
        print(f"Float Input {i + 1}: {float_val} ({float_binary})")
        if matches:
            print(f"  Matches Binary Input(s): {', '.join(str(m + 1) for m in matches)}\n")
        else:
            print("  No Matches Found.\n")
    print("---------------------------------------------------------")        


if __name__ == "__main__":
    # Float inputs to convert to IEEE 754
    float_inputs = [
        -0.0,
        2**-126,
        -2.0,
        1/4 + 1/8,
        -2**-126 * (1 + 2**-23)
    ]

    # Binary inputs to convert back to floats
    binary_inputs = [
        "0 00000001 00000000000000000000000",
        "0 10000000 10000000000000000000000",
        "1 00000001 00000000000000000000001",
        "1 00000000 00000000000000000000000",
        "0 01111101 10000000000000000000000"
    ]

    print_matches(float_inputs, binary_inputs)

