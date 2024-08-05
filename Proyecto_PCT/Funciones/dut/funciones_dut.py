def dut_parametros(opcion_presionada, modo):
    _dut_1 = opcion_presionada.split('|')[0]
    _dut_2 = opcion_presionada.split('|')[1]
    #Si el modo seleccionado fue SHOW hacer lo siguiente:
    print(_dut_1,_dut_2)
    if _dut_1 == 'CAFE':
        _template_dut_1 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/set_parameters_cafe/cafe_params_1.html"
        sDUT_1 = 1
        name_dut_1 = 'CAFE'
    elif _dut_1 == 'COIL':
        _template_dut_1 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/set_parameters_coil/coil_params_1.html"
        sDUT_1 = 1
        name_dut_1 = 'COIL'
    elif _dut_1 == 'LIMIT SWITCH':
        _template_dut_1 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/set_parameters_ls/ls_params_1.html"
        sDUT_1 = 1
        name_dut_1 = 'LIMIT SWITCH'
    elif _dut_1 == 'NONE':
        _template_dut_1 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/dut_empty.html"
        sDUT_1 = 0
        name_dut_1 = 'NONE'

    if _dut_2 == 'CAFE':
        _template_dut_2 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/set_parameters_cafe/cafe_params_2.html"
        sDUT_2 = 1
        name_dut_2 = 'CAFE'
    elif _dut_2 == 'COIL':
        _template_dut_2 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/set_parameters_coil/coil_params_2.html"
        sDUT_2 = 1
        name_dut_2 = 'COIL'
    elif _dut_2 == 'LIMIT SWITCH':
        _template_dut_2 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/set_parameters_ls/ls_params_2.html"
        sDUT_2 = 1
        name_dut_2 = 'LIMIT SWITCH'
    elif _dut_2 == 'NONE':
        _template_dut_2 = "Proyecto_PCT/templates/set_parameters/set_parameters_box/dut_empty.html"
        sDUT_2 = 0
        name_dut_2 = 'NONE'

    infoDut_1 = [sDUT_1, _template_dut_1, name_dut_1]
    infoDut_2 = [sDUT_2, _template_dut_2, name_dut_2]
    return infoDut_1, infoDut_2