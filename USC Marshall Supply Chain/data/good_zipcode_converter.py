
import zipcode

def zip_to_coordinates(zip_file, coord_file):
    """ takes in a file of zipcodes and a blank file which it writes out each zipcode"s coordinates to """
    coordinate_list = []

    zipcodes = open(zip_file, "r")
    coordinates = open(coord_file, "w")

    #scan every line in the input file, apply conversion, and write to new file
    for line in zipcodes:
        digit = int(line)

        a_zip = zipcode.isequal(str(digit))

        #if the zipcode library doesn"t have it in system, leave the line blank and skip it over
        if a_zip == None:
            coordinates.write("\n")
            continue

        a_coords = str(a_zip.lat) + ", " + str(a_zip.lon)

        coordinates.write(a_coords)
        coordinates.write("\n")

    zipcodes.close()
    coordinates.close()



import nvector as nv 

def write_geodetic_to_ECEF(geodetic_file, ECEF_file):
    """ takes in a file with (geodetic) coordinates and writes out a new file with their ECEF equivalents 
    ex. lat = 33.73, long = -118.26, height = 13 m
        output: X : -2514.124   km, Y : -4677.054   km, Z : 3521.586   km

    """
    wgs84 = nv.FrameE(name="WGS84")

    geodetics = open(geodetic_file, "r")
    ECEFs = open(ECEF_file, "w")

    for line in geodetics:
        if line == "\n":
            ECEFs.write("\n")
            continue

        lat, lon, h = line.split(",")
        
        print(line)
        lat = float(lat)
        lon = float(lon)
        h = float(h)

        temp = wgs84.GeoPoint(lat, lon, h, degrees=True)
        ECEF = temp.to_ecef_vector()

        ECEFs.write(str(ECEF.pvector.ravel()))
        ECEFs.write("\n")

    geodetics.close()
    ECEFs.close()



from math import sin, cos, degrees

#ENU coordinates are relative to a chosen origin point; for this program the port will be our origin
port = [-2514113, 4677034, 3521571]
port_lat = 33.73
port_lon = -118.26

def write_ECEF_to_ENU(ECEF_file, ENU_file):
    """ takes in a file with ECEF coordinates and writes out a new file with their ENU equivalents """
    
    xvector = [ -sin(port_lon), cos(port_lon), 0 ]
    yvector = [ (-sin(port_lat) * cos(port_lon)), (-sin(port_lat) * sin(port_lon)), (cos(port_lat))]
    zvector = [ (cos(port_lat) * cos(port_lon)), (cos(port_lat) * sin(port_lon)), (sin(port_lat))]

    ECEFs = open(ECEF_file, "r")
    ENUs = open(ENU_file, "w")

    for line in ECEFs:
        if line == "\n":
            ENUs.write("\n")
            continue

        x, y, z = line.split(",")
        x = float(x)
        y = float(y)
        z = float(z)

        adj_vector = [(x - port[0]), (y - port[1]), (z - port[2])]
        
        new_x = (adj_vector[0] * xvector[0]) + (adj_vector[1] * xvector[1]) + (adj_vector[2] * xvector[2])
        new_y = (adj_vector[0] * yvector[0]) + (adj_vector[1] * yvector[1]) + (adj_vector[2] * yvector[2])
        new_z = (adj_vector[0] * zvector[0]) + (adj_vector[1] * zvector[1]) + (adj_vector[2] * zvector[2])

        #converted to km
        ENU_vector = [new_x/1000, new_y/1000, new_z/1000]

        ENUs.write(str(ENU_vector))
        ENUs.write("\n")


    ECEFs.close()
    ENUs.close()


#this aint perfect 
def convert_3d_to_2d(xyz, xy):
    """ convertz xyz coordinates to xy coordinates """

    xyz_coordinates = open(xyz, "r")
    xy_coordinates = open(xy, "w")
    
    for line in xyz_coordinates:
        if line == "\n":
            xy_coordinates.write("\n")
            continue

        x3d, y3d, z3d = line.split(" ")
        x3d = float(x3d)
        y3d = float(y3d)
        z3d = float(z3d)

        #converting the data
        x2d = x3d / z3d
        y2d = y3d / z3d

        xy_coordinates.write(str(x2d))
        xy_coordinates.write(" ")
        xy_coordinates.write(str(y2d))
        xy_coordinates.write("\n")


    xyz_coordinates.close()
    xy_coordinates.close()


#MAKE A LOOKUP TABLE FOR XY --> LAT LON












