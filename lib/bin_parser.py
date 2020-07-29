f = open("test_samples/2020_07_22_U_4.8_0deg_2.BIN", "rb")

for i in range(0, 100):
    byte = list(f.readline())
    print(byte)
    next(f)

f.close()
