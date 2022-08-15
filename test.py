import netCDF4 as nc

fn = "C:/Users/kanad/Desktop/GEBCO_2022_TID.nc"
ds = nc.Dataset(fn)
for var in ds.variables.values():
    print(var)
print(ds["lat"][:])

print(ds["lon"][:])
print(ds["tid"][-89.99791667, -179.99791667])
