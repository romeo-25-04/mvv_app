from mvv_parser import Stations


stations = Stations()
stations.get_stations()

output = '\n'.join(stations.stations)
with open('stations.txt', 'w') as file_handler:
    file_handler.write(output)

print(output)
