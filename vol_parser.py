import numpy as np

def parse_vol_file(path: str):

    with open(path, 'rb') as f:
        
        # dimension
        dim_x, dim_y, dim_z = np.fromfile(f, '>i4', 3)

        # ignore one 32-bit int
        f.read(4)

        # aspect ratio
        aspect_ratio = np.fromfile(f, '>f4', 3)
        print(aspect_ratio)

        # raw data
        raw_data = np.fromfile(f, '>u1', dim_x * dim_y * dim_z).reshape(dim_x, dim_y, dim_z)
    
    return raw_data, dim_x, dim_y, dim_z

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    raw_data, _, _, _ = parse_vol_file("Skull.vol")
    print(raw_data.shape)
    plt.imshow(raw_data[40])
    plt.show()

