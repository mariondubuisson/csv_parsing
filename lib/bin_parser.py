import struct


def main():
    """Read catman 5.0 format"""
    with open(r"C:\Users\KNAPP\PycharmProjects\csv_parsing\test_samples\2020_07_22_U_4.8_0deg_2.BIN", "rb") as f:

        # read global section
        file_id = int.from_bytes(f.read(2), byteorder='little')
        data_offset = int.from_bytes(f.read(4), byteorder='little')
        comment_length = int.from_bytes(f.read(2), byteorder='little')
        comment = f.read(comment_length).decode(encoding='latin_1')

        # read reserved strings
        for i in range(32):
            header_length = int.from_bytes(f.read(2), byteorder='little')
            header = f.read(header_length).decode(encoding='latin_1')
            print(header_length, header)

        number_of_channels = int.from_bytes(f.read(2), byteorder='little')
        print(number_of_channels)
        maximum_channel_length = int.from_bytes(f.read(4), byteorder='little')
        print(maximum_channel_length)
        for i in range(number_of_channels):
            offset_channel = int.from_bytes(f.read(4), byteorder='little')
            print(i, offset_channel)
        reduction_factor = int.from_bytes(f.read(4), byteorder='little')
        print(reduction_factor)
        for i in range(number_of_channels):

            channel_number = int.from_bytes(f.read(2), byteorder='little')
            channel_length = int.from_bytes(f.read(4), byteorder='little')
            channel_name_length = int.from_bytes(f.read(2), byteorder='little')
            channel_name = f.read(channel_name_length).decode(
                encoding='latin_1')
            channel_unit_name_length = int.from_bytes(
                f.read(2), byteorder='little')
            channel_unit_name = f.read(
                channel_unit_name_length).decode(encoding='latin_1')
            channel_comment_length = int.from_bytes(
                f.read(2), byteorder='little')
            channel_comment = f.read(
                channel_comment_length).decode(encoding='latin_1')
            print(f"{channel_name}, ({channel_unit_name}) : {channel_comment}")
            channel_format = int.from_bytes(f.read(2), byteorder='little')
            channel_data_width = int.from_bytes(f.read(2), byteorder='little')
            channel_datum_time = struct.unpack('d', f.read(8))
            channel_extended_name_length = int.from_bytes(
                f.read(4), byteorder='little')
            channel_extended_name = f.read(
                channel_extended_name_length).decode(encoding='latin_1')
            channel_linearisation_mode = f.read(2).decode(encoding='latin_1')
            channel_user_scale = f.read(2).decode(encoding='latin_1')
            channel_linearisation_points = f.read(2).decode(encoding='latin_1')
            print(channel_linearisation_points)
            break


if __name__ == '__main__':
    main()
