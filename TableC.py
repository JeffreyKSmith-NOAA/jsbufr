

def apply_C(piece, C_fxy):

    if C_fxy[1:3] == "05":
        piece.nbits += 8*int(C_fxy[3:])
    elif C_fxy[1:3] == "06":
        piece.nbits = int(C_fxy[3:])

    return
