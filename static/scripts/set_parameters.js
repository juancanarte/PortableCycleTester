//Obtener referecncias a los objetos del html
const dropdowns = document.querySelectorAll('.form-select');
const dropdownsParams = document.querySelectorAll('.form-select');
var buttonSetParameters = document.getElementById('nextSetParameters');
var idDutAlone = document.getElementById('idDutAlone');
var LabelDutAlone = document.getElementById('labelDutAlone');
var LabelDut1 = document.getElementById('LabelDut1');
var LabelDut2 = document.getElementById('LabelDut2');
var arrayParams = Array(38);
var node_1 = document.getElementById('node_1');
var node_2 = document.getElementById('node_2');
const load = document.getElementById('load');
const conditionalField = document.getElementById('conditionalField');
const modoPCT = document.getElementById('modo');
const divCycleTestDataForm = document.getElementById('divCycleTestDataForm');
const testerName = document.getElementById('testerName');
var formAux = document.getElementById('formAux');
var formMain = document.getElementById('formMain');

var arrayLabels = [idDutAlone,LabelDutAlone,LabelDut1,LabelDut2];

function hideLoadDetails() {
  if (load.checked) {
      conditionalField.style.display = 'flex';
    } else {
      conditionalField.style.display = 'none';
    }
}

//Solo mostrar el formulario de datos cuando sea Cycle test
if (modoPCT.innerHTML != 'Show')
{
  divCycleTestDataForm.style.display = 'flex';
  
}
else{
  divCycleTestDataForm.style.display = 'none';
  testerName.removeAttribute("required");
}

function saveData() {
  const quantityInput = document.getElementById('manual_porcent_cafe_a');
  $.ajax({
      type: "POST",
      url: '/show_open_cafe_alone/',
      data: {csrfmiddlewaretoken: '{{ csrf_token }}',"porcPos": quantityInput.value},
      success: function (data) {
      }
  });
  bOpen_a.disabled = true;
  bOpen_a.style.backgroundColor = "#6f6e6e";
  bOpen_a.style.fontSize = "12px";
  bClose_a.disabled = false;
  bClose_a.style.backgroundColor = "#143a51";
  bClose_a.style.fontSize = "16px"; 
}

//Identificar cuantos DUT hay conectados y en que puerto (PCT DUT's)
for (let m = 0; m < arrayLabels.length; m++)
{
  if(arrayLabels[m] != null)
  {
    arrayParams[m] = arrayLabels[m].textContent;
  }
  else if (arrayLabels[m] == null)
  {
    arrayParams[m] = 0;
  }
}
var arrayParamsTest = arrayParams;

//------------------------------------------------------------------------------------------------------------//
buttonSetParameters.addEventListener('click', function() 
{
    //document.getElementById('formAux').submit();
    //------------------------------------Asignar al Array parametros de los DUT Alone------------------------------------//

  if (arrayParamsTest[1] == 'CAFE')                                   //Si el DUT Alone es CAFE
  {
    const dropdownsParams = document.querySelectorAll('.form-select');
    const node_a = document.querySelector('input[type="number"]');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+4] = label + '|' + optionD;                   //Asignado desde la posicion 4 en adelante
    }
    arrayParamsTest[10] = node_a.value;
  }
  else if (arrayParams[1] == 'COIL')                                   //Si el DUT Alone es COIL
  {
    const dropdownsParams = document.querySelectorAll('.form-select');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+11] = label + '|' + optionD;                   //Asignado desde la posicion 11 en adelante
    }
  }
  else if (arrayParams[1] == 'LIMIT SWITCH')                           //Si el DUT Alone es LIMIT SWITCH
  {
    const dropdownsParams = document.querySelectorAll('.form-select');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+13] = label + '|' + optionD;                   //Asignado desde la posicion 13 en adelante
    }
  }

  //------------------------------------Asignar al Array parametros de los DUT 1 ------------------------------------//

  if (arrayParamsTest[2] == 'CAFE')                                   //Si el DUT 1 es CAFE
  {
    const divEspecifico = document.querySelector('#divParamsDut1');
    const dropdownsParams = divEspecifico.querySelectorAll('.form-select');
    var node_1 = document.getElementById('node_1');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+14] = label + '|' + optionD;                   //Asignado desde la posicion 20 en adelante
    }
    arrayParamsTest[20] = node_1.value;
  }
  else if (arrayParams[2] == 'COIL')                                   //Si el DUT 1 es COIL
  {
    const divEspecifico = document.querySelector('#divParamsDut1');
    const dropdownsParams = divEspecifico.querySelectorAll('.form-select');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+28] = label + '|' + optionD;                   //Asignado desde la posicion 28 en adelante
    }
  }
  else if (arrayParams[2] == 'LIMIT SWITCH')                           //Si el DUT 1 es LIMIT SWITCH
  {
    const divEspecifico = document.querySelector('#divParamsDut1');
    const dropdownsParams = divEspecifico.querySelectorAll('.form-select');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+32] = label + '|' + optionD;                   //Asignado desde la posicion 32 en adelante
    }
  }

  //------------------------------------Asignar al Array parametros de los DUT 2 ------------------------------------//

  if (arrayParamsTest[3] == 'CAFE')                                   //Si el DUT 2 es CAFE
  {
    const divEspecifico = document.querySelector('#divParamsDut2');
    const dropdownsParams = divEspecifico.querySelectorAll('.form-select');
    var node_2 = document.getElementById('node_2');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+21] = label + '|' + optionD;                   //Asignado desde la posicion 21 en adelante
    }
    arrayParamsTest[27] = node_2.value;
  }
  else if (arrayParams[3] == 'COIL')                                   //Si el DUT 2 es COIL
  {
    const divEspecifico = document.querySelector('#divParamsDut2');
    const dropdownsParams = divEspecifico.querySelectorAll('.form-select');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+30] = label + '|' + optionD;                   //Asignado desde la posicion 30 en adelante
    }
  }
  else if (arrayParams[3] == 'LIMIT SWITCH')                           //Si el DUT 2 es LIMIT SWITCH
  {
    const divEspecifico = document.querySelector('#divParamsDut2');
    const dropdownsParams = divEspecifico.querySelectorAll('.form-select');
    for (let j = 0; j < dropdownsParams.length; j++)
    {
      var label = dropdownsParams[j].value;
      var optionD = dropdownsParams[j].id;
      arrayParamsTest[j+33] = label + '|' + optionD;                   //Asignado desde la posicion 33 en adelante
    }
  }


  //------------------------------------alto y bajo dut 1 ------------------------------------//
  var highCaf_1 = document.getElementById('InputHighValue_1');
  var lowCaf_1 = document.getElementById('InputLowValue_1');

  var highCaf_2 = document.getElementById('InputHighValue_2');
  var lowCaf_2 = document.getElementById('InputLowValue_2');

  if (highCaf_1 != null)
  {
    arrayParamsTest[35] = highCaf_1.value;
    arrayParamsTest[36] = lowCaf_1.value;
  }

  if (highCaf_2 != null)
    {
      arrayParamsTest[37] = highCaf_2.value;
      arrayParamsTest[38] = lowCaf_2.value;
    }

    console.log(arrayParamsTest);

  buttonSetParameters.value = arrayParamsTest;
});
//Estructura del arreglo
//array:['idDutAlone','LabelDutAlone','LabelDut1','LabelDut2',...parameters...]


