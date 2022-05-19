import PRICES as P
import PySimpleGUI as sg
import calculations as cl


chosed_fej_layers = []
chosed_screw = []
item_types = [
"тип WW-1 ",
"тип WW-2",
"тип WW-10",
"тип WW-10W",
"тип WW-2SF",
]  


frame_screw_layout = [
        [ sg.T('КРЕПЕЖ', font='GothamPro 15'),],
        [sg.I(k='-SCREW_QTY-', size=(5)), sg.T('Кол-во [шт.]', size=(10, 1)),],
        [sg.Combo(values=list(P.raw_screw_prices.keys()), k='-SCREW-',size=(30, 15)), sg.B('➕', k='ADD_S', button_color='whiteongreen'), sg.B('➖', k='DEL_S' ,button_color='whiteoncoral')],
        [sg.Listbox(values=chosed_screw, k='-SCREW_LIST-',
                size=(30, 10)), ],
]

frame_fabric_layout = [
        [sg.T('ТКАНЕВАЯ ЧАСТЬ', font='GothamPro 15') ,],
        [sg.I(key='-FEJ_AREA-', size=(15)), sg.T('Площадь ТК [м2]', size=(15, 1)), ],
        [sg.I(k='-FABRIC_WIDTH-', size=(15, 1)) ,sg.T('Ширина полотна [мм]', font='Gotham 10',),],
        [sg.T('Усиление фланца' , font = 'GothamPro 12')],
        [sg.Combo(values=list(P.raw_fabric_prices.keys()), k='-FLANGE_REINFORCEMENT-', size=(30, 15)),],
        [sg.T('Слои от внутренних к наружным' , font = 'GothamPro 12')],
        [sg.Combo(values=list(P.raw_fabric_prices.keys()), k='-LAYER-', size=(30, 15)), sg.B('➕', k='ADD_L' , button_color='whiteongreen' ),  sg.B('➖', k='DEL_L' ,button_color='whiteoncoral') ],
        [sg.Listbox(values=chosed_fej_layers, k='-LAYERS_LIST-', size=(30, 10)), ],

]

layout = [
        [sg.I(k='-CLIENT-', size=(15, 1)), sg.T('Заказчик'), ],
        [sg.I(k='-DRAWING_NUM-', size=(15, 1)), sg.T('Номер чертежа')],
        [sg.Combo(values=item_types, size=(15, 1),
                  k='-FEJ_TYPE-'), sg.T('Тип ТК')],
        #   METALL 
        [sg.T('Металл', font='GothamPro 15', text_color='#fff', )],
        [sg.I(k='-STAINLESS_STEEL_WEIGHT-', size=(15)), sg.T('Нерж. сталь [кг.]')],
        [sg.I(k='-STEEL_WEIGHT-', size=(15)), sg.T('Сталь [кг.] ')],
        #  WORK CONDITION 
        [sg.T('Рабочие условия:', font='GothamPro 15')],
        [sg.I(k='-TEMPERATURE-', size=(15, 1)), sg.T('Температура, [°С]')],
        [sg.I(k='-PRESSURE-', size=(15)),  sg.T('Давление, [бар]')],
        [sg.I(k='-MEDIA-', size=(15)), sg.T('Среда')],
        #  FABRIC
        # [sg.VPush()],
        sg.vtop( [  sg.Frame('',frame_fabric_layout) , sg.Frame('', frame_screw_layout, expand_y=True)  ]),

        # SCREW 
        #INSOLATION  
        [sg.T("Изоляция", font='GothamPro 15 bold', text_color='gold')],
        [sg.I(k='-INSOLATION_VOLUME-', size=(15, 1),), sg.T('Объем изоляции')],
        # FOOTER
        [sg.Ok(),sg.Cancel(),sg.B('Отчет', k='-REPORT-'),],
        [sg.T('Цифры через точку.',text_color = 'lightgreen')],
            


    ]









window = sg.Window('cost price app', layout, size=(800, 800) , element_justification='lt')

while True:
    e, v = window.read()

    if e == 'Cancel' or e == sg.WIN_CLOSED:
        break

    if e == '-START-':
        # apps[v['-COMBO-']]()
        print('')

    if e == "ADD_L":
        chosed_fej_layers.append(v['-LAYER-'])
        window['-LAYERS_LIST-'].update(chosed_fej_layers)

    if e == "DEL_L" and v['-LAYERS_LIST-'] != []:
        chosed_fej_layers.remove(v['-LAYERS_LIST-'][0])
        window['-LAYERS_LIST-'].update(chosed_fej_layers)

    if e == "ADD_S" and v['-SCREW-'] != [] and v['-SCREW_QTY-'] != '':
        chosed_screw.append((v["-SCREW-"], v["-SCREW_QTY-"], 'шт.'))
        window['-SCREW_LIST-'].update(chosed_screw)
        print(chosed_screw)

    if e == "DEL_S" and v['-SCREW_LIST-'] != []:
        chosed_screw.remove(v['-SCREW_LIST-'][0])
        window['-SCREW_LIST-'].update(chosed_screw)

    if e == '-METALL-':
        metall_data = [
            v['-STAINLESS_STEEL_WEIGHT-'],
            v['-STEEL_WEIGHT-']
        ]

        cl.calculate_metall_price(metall_data)

    if e == '-FABRIC-' and chosed_fej_layers != [] and v['-FEJ_AREA-'] != '':
        cl.calculate_fabric_layers(chosed_fej_layers, v['-FEJ_AREA-'], v['-FABRIC_WIDTH-'])



    if e == '-CALC_INSOLATION-':
        insolation_volume = int(v['-INSOLATION_VOLUME-'])
        cl.calculate_insolation(insolation_volume)

    if e == '-REPORT-':
        # try:

            screw = '; \n'.join([', '.join(i) for i in chosed_screw])
            client = v['-CLIENT-']
            drawing_number = v['-DRAWING_NUM-']

            fej_type = v['-FEJ_TYPE-']
            fej_layers = ', \n'.join(chosed_fej_layers)
            fej_area = v['-FEJ_AREA-']

            steel_weight = float(v['-STEEL_WEIGHT-'])
            steel_cost = P.raw_metall_prices['steel'] * steel_weight
            stain_less_steel_weight = float(v['-STAINLESS_STEEL_WEIGHT-'])
            stain_less_steel_cost = P.raw_metall_prices['stainless steel'] * \
                stain_less_steel_weight
            temperature = v['-TEMPERATURE-']
            pressure = v['-PRESSURE-']
            media = v['-MEDIA-']
            screw_cost = cl.calculate_screw(chosed_screw)
            flange_reinforcement = v['-FLANGE_REINFORCEMENT-']

            fej_cost = cl.calculate_fabric_layers(
                chosed_fej_layers,
                v['-FEJ_AREA-'] , 
                v['-FABRIC_WIDTH-'],
                flange_reinforcement

                )

                
            insolation_volume = 0 if v['-INSOLATION_VOLUME-'] == '' else float(v['-INSOLATION_VOLUME-'])
            insolation_cost = cl.calculate_insolation(insolation_volume)

            final_cost = cl.calculate_final_cost([
                insolation_cost,
                screw_cost,
                fej_cost, 
                cl.calculate_metall_price([
                    v['-STAINLESS_STEEL_WEIGHT-'],
                    v['-STEEL_WEIGHT-']
                ])
            ]

            )

            cl.create_report(
                [
                    client,
                    drawing_number,
                    fej_type,
                    steel_weight,
                    steel_cost,
                    stain_less_steel_weight,
                    stain_less_steel_cost,
                    temperature,
                    pressure,
                    media,
                    fej_layers,
                    fej_area,
                    fej_cost,
                    flange_reinforcement,
                    insolation_volume,
                    insolation_cost,
                    screw,
                    screw_cost,
                    final_cost,
                ]


            )
        # except:
        #     sg.popup('похоже где то не введены данные')



window.close()
