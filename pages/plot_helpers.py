import numpy as np

var_translation = {
    "TEMP":"Temperature (°C)",
    "PRES":"Pressure (dbar)",
    "PSAL": "Practical Salinity",
    "DOXY":"Dissolved Oxygen (μmol/kg)",
    "CHLA":"Chlorophyll a (mg/m<sup>3</sup>)",
    "BBP700":"Particle backscattering at 700 nm (m<sup>-1</sup>)",
    "PH_IN_SITU_TOTAL":"pH total scale",
    "NITRATE":"Nitrate (μmol/kg)",
    "CDOM":"Coloured dissolved organic matter (ppb)",
    "VRS_PH":"pH Vrs",
    "VK_PH":"pH Vk",
    "IB_PH":"pH Ib",
    "IK_PH":"pH Ik"
}

var_ranges = {
    "TEMP":[0, 30],
    "PRES":[-2000,0],
    "PSAL": [34.5, 37.5],
    "DOXY":[0, 300],
    "CHLA":[0, .7],
    "BBP700":[0, .0004],
    "PH_IN_SITU_TOTAL":[7.7, 8.2],
    "NITRATE":[-5, 35],
    "CDOM":[0, 3],
    "VRS_PH":[-2,0],
    "VK_PH":[-3,0],
    "IB_PH":[-.0000001,0],
    "IK_PH":[-.0000001,0]
}

def cmocean_to_plotly_simple(cmap, pl_entries):
    """Function to sample cmocean colors and output list of rgb values for plotly
    cmap = color map from cmocean
    pl_entries = number of samples to take"""
    
    h = 1.0/(pl_entries-1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append('rgb'+str((C[0], C[1], C[2])))

    return pl_colorscale


def cmocean_to_plotly(cmap, pl_entries):
    """Function to sample cmocean colors and output list of rgb values for plotly
    cmap = color map from cmocean
    pl_entries = number of samples to take"""
    
    #Sample 40 colors from cmap
    colors_n = 40
    h = 1.0/(colors_n-1)
    pl_colorscale = []
    for k in range(colors_n):
        C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
        pl_colorscale.append('rgb'+str((C[0], C[1], C[2])))
    
    #Add light blue colors if older than 40 profiles
    solid_add = pl_entries - colors_n
    i = 0
    while i < solid_add:
        pl_colorscale.insert(0, 'rgb(207, 230, 233)')
        i+=1

    #chop scale if younger than 40 profiles
    if pl_entries < colors_n:
        final_scale = pl_colorscale[pl_entries*-1:]
    else:
        final_scale = pl_colorscale

    
    return final_scale