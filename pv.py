"""
    @author Leonardo Rossi Leão
    @create february, 02, 2022
"""

import pandas as pd
from calibration import Calibration as cal

class PvProperties():
    
    file = pd.read_excel("pvs.xlsx")
    
    @staticmethod
    def pvName(mux, canal, ch):
        file = PvProperties.file
        linha = file.loc[((file["Mux"] == mux) & (file["Canal"] == canal))]
        
        if not linha.empty:
            sensor     = cal.muxHeader["mux%d" % mux][canal-1]
            local      = str(linha["Local"].values[0])
            setor      = int(linha["Setor"].values[0])
            setor      = ("0" + str(setor)) if setor < 10 else str(setor)
            posicao    = (str(linha["Posição"].values[0])).replace("L", "").replace("P", "")
            nivel      = str(linha["Nível"].values[0])
            nivel      = "" if nivel == "nan" else nivel
            orientacao = str(linha["Orientação"].values[0])
            orientacao = "" if orientacao == "nan" else orientacao
            
            if((sensor == "PT100" or sensor == "VWTS6000") and ch == "A"):
                return (f"{setor}{local}:SS-Concrete-{posicao}{nivel}{sensor[0]}:Temp-Mon")
            if(sensor == "VWTS6000" and ch == "B"):
                return (f"{setor}{local}:SS-Concrete-{posicao}{nivel}N:Temp-Mon")
            if(sensor == "VWS2100" and ch == "A"):
                return (f"{setor}{local}:SS-Concrete-{posicao}{nivel}:Strain{orientacao}-Mon")
            if(sensor == "VWS2100" and ch == "B"):
                return (f"{setor}{local}:SS-Concrete-{posicao}{nivel}N:Temp-Mon")

    @staticmethod
    def pvdb():
        pvdb = {}
        for index, row in PvProperties.file.iterrows():
            mux        = row["Mux"]
            canal      = row["Canal"]
            sensor     = cal.muxHeader["mux%d" % mux][canal-1]
            if("PT100" in sensor):
                pvdb[PvProperties.pvName(mux, canal, "A")] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            elif ("VWTS6000" in sensor):
                pvdb[PvProperties.pvName(mux, canal, "A")] = {'prec': 3, 'scan': 1, 'unit': 'C'}
                pvdb[PvProperties.pvName(mux, canal, "B")] = {'prec': 3, 'scan': 1, 'unit': 'C'}
            else:
                pvdb[PvProperties.pvName(mux, canal, "A")] = {'prec': 3, 'scan': 1, 'unit': 'uE'}
                pvdb[PvProperties.pvName(mux, canal, "B")] = {'prec': 3, 'scan': 1, 'unit': 'C'}

        return pvdb