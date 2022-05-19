import math as m
import PySimpleGUI as sg
import PRICES as P
import PySimpleGUI as sg
from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime


def validate(arr):
    try:
        data = [eval(i) for i in arr]
        return list(data)

    except:
        sg.popup('Проверь введенные значения')


def calculate_metall_price(data):
    try:
        sp = P.raw_metall_prices['steel']
        ssp = P.raw_metall_prices['stainless steel']

        sw, ssw = validate(data)
        total_metal_price = round(sp*sw + ssp*ssw,2)
        return total_metal_price
    except:
        return


def calculate_fabric_layers(choosed_layers, area , fw, flange_reinforcement):
    try:
        area = eval(area)
        fw = float(fw)
        # длинна фланцевой ленты 
        fl = area/(fw/1000)

        flange_tape_area = 2*fl*0.2 


        current_layers = [P.raw_fabric_prices[i] for i in choosed_layers]
        total_price = round(sum(current_layers)*area + flange_tape_area*P.raw_fabric_prices[flange_reinforcement] , 2) 



        return total_price
    except:
        return None


def calculate_screw(cs):
    current_screw = [P.raw_screw_prices[i[0]]*int(i[1]) for i in cs]
    total_cost = sum(current_screw)
    return round(total_cost,2)


def calculate_insolation(v):
    try: 
        price = P.raw_insolation_prices['insolation']
        total = v*price
        return total
    except: 
        print('WTF IN INSOLATION ')



def calculate_final_cost(arr):

    try:
        total = sum(arr)
        print(f'ВСЕГО {total}')
        return round(total,2)
    except:
        sg.popup('где то что то не введено')


def create_report(arr):
    
    client, drawing_number, fej_type, steel_weight, steel_cost,  stain_less_steel_weight, stain_less_steel_cost,  temperature, pressure, media, fej_layers, fej_area, fej_cost,flange_reinforcement, insolation_volume, insolation_cost,  screw, screw_cost, final_cost = arr

    current_date = datetime.today().strftime('%Y-%m-%d')

    template_path = Path(__file__).parent/'kp_report.docx'
    doc = DocxTemplate(template_path)
    context = {
        "DATE": current_date,
        "CLIENT": client,
        "DRAWING_NUMBER": drawing_number,
        "FEJ_TYPE": fej_type,
        "STEEL_WEIGHT": steel_weight,
        "STEEL_COST": steel_cost,
        "STAIN_LESS_STEEL_WEIGHT": stain_less_steel_weight,
        "STAIN_LESS_STEEL_COST": stain_less_steel_cost,
        "TEMPERATURE": temperature,
        "PRESSURE": pressure,
        "MEDIA": media,
        "FEJ_LAYERS": fej_layers,
        "FEJ_AREA": fej_area,
        "FEJ_COST": fej_cost,
        "INSOLATION_VOLUME": insolation_volume,
        "INSOLATION_COST": insolation_cost,
        "SCREW": screw,
        "SCREW_COST": screw_cost,
        "FINAL_COST": final_cost,
        "FLANG_REINF": flange_reinforcement,
    }

    doc.render(context)
    final_file_name = f'{client} {drawing_number}.docx'

    try:
        choosed_path = sg.popup_get_folder('please enter folder')
        doc.save(Path(choosed_path)/final_file_name)

    except:
        PermissionError
        sg.popup('файл открыт, ошибка доступа :(')
