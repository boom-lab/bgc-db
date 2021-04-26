# 2021/04/22 Ben Greenwood
# raw binned data from 1201.003.msg
import struct
import codecs
 
raw=['02853986793AFF2BBA9C1AE4A240000AE2027E160008C222173EA242',
     '0296395C793AFF2BBAA91AE88CFF000AE1027E150008C2FC173E6EFF',
     '02A8397F7939FF2BBAE11AE586FF000AE2027E150008C2FF173E07FF',
     '02B23ABB793A432BAE9E1AC8020E000AE1027E160008BD06173F5610']
 
# Park Obs and Discrete measurements
print('$                        Date        p       t      s   O2ph     O2tV    phVrs     phVk       phIb       phIk')
print('ParkObs: Mar 05 2021 15:25:22    68.80 15.7158 31.027 18.414 0.739856 -0.968494 -0.979705 -2.597e-08 -5.734e-08')
print('ParkObs: Mar 05 2021 20:46:18    66.00 18.2260 31.033 18.120 0.683474 -0.973418 -0.990211 -2.415e-08 -4.871e-08')
print('$       p       t      s    no3   O2ph     O2tV   Mch1   Mch2   Mch3    phVrs     phVk       phIb       pHIk')
print('    65.40 15.6408 31.034    nan 18.617 0.740795   2298 162850   1736 -0.976205 -0.992971 -2.250e-08 -4.612e-08 (Park Sample)')
print('    63.77 15.0277 31.036  -54.9    nan      nan    nan    nan    nan      nan      nan      nan      nan')

decode_hex = codecs.getdecoder("hex_codec")

for line in raw:
     rec={}
     # Byte offset --         6 7   10   13 14     23 24 26 27 28
     # variable    --       PTS # O2ph o2tV  #  MCOMS  # pH  #
     vars = struct.unpack('>HHH B   HB   HB  B HBHBHB  B HB  B  ', codecs.decode(line, "hex_codec")[0:28])

     print(codecs.decode(line, "hex_codec"))
     print(vars)
     rec['p'] = vars[0]/10.0
     rec['t'] = vars[1]/1000.0
     rec['s'] = vars[2]/1000.0
     rec['ctd_scans'] = vars[3]
     rec['o2ph'] = (vars[4]*256 + vars[5])/1e5 - 10
     rec['o2tV'] = (vars[6]*256 + vars[7])/1e6 - 1
     rec['o2_scans'] = vars[8]
     rec['Mch1'] = (vars[9]*256 + vars[10]) - 500
     rec['Mch2'] = (vars[11]*256 + vars[12]) - 500
     rec['Mch3'] = (vars[13]*256 + vars[14]) - 500
     rec['MCOMS_scans'] = (vars[15])
     rec['pHVrs'] = ((vars[16]*256 + vars[17])-0.5)/1e6 - 2.5
     rec['ph_scans'  ] = vars[18]
     #print(rec)