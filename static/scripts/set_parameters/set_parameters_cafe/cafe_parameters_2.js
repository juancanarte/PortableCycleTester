var ddOperMode_2 = document.getElementById('operation_mode_2');
var ddInputSignal_2 = document.getElementById('inputSignal_2');
var ddBaud_2 = document.getElementById('baud_2');
var node_2 = document.getElementById('node_2');
var ddSignalType_2 = document.getElementById('signalType_2');
var ddWidthTime_2 = document.getElementById('widthTime_2');

var divSignalType_2 = document.getElementById('divSignalType_2');

var divBaud_2 = document.getElementById('divBaud_2');
var hidden_2 = divBaud_2.getAttribute("hidden");

var divOpVoltage_2  = document.getElementById('divOpVoltage_2');
var hiddenOpVoltage_2 = divOpVoltage_2.getAttribute("hidden");

var divInputSignal_2 = document.getElementById('divInputSignal_2');
var hiddenInputSignal_2 = divInputSignal_2.getAttribute("hidden");

var divWidthTime_2  = document.getElementById('divWidthTime_2');
var hiddenWidthTime_2 = divWidthTime_2.getAttribute("hidden");

const quantityInput_2 = document.getElementById('node_2');
const incrementButton_2 = document.getElementById('increment_2');
const decrementButton_2 = document.getElementById('decrement_2');

var modo = document.getElementById('modo'); // Que modo es SHOW o CYCLE TEST
var resultado = (modo != null) && modo.textContent;
//Si es SHOW
if (resultado == 'Show')
{
    divWidthTime_2.setAttribute("hidden", "hidden");
    divSignalType_2.setAttribute("hidden", "hidden");
    document.getElementById('divHighValue_2').setAttribute("hidden", "hidden");
    document.getElementById('divLowValue_2').setAttribute("hidden", "hidden");
}

incrementButton_2.addEventListener('click', () => {
    quantityInput_2.stepUp();
  });
  
  decrementButton_2.addEventListener('click', () => {
    if (quantityInput_2.value > 1) {
      quantityInput_2.stepDown();
    }
  });

ddOperMode_2.addEventListener('change', function() 
{
    const selectedOption_2 = this.value;
    if (selectedOption_2 == 'digital')
    {
        divInputSignal_2.setAttribute("hidden", "hidden");
        divBaud_2.setAttribute("hidden", "hidden");
        ddInputSignal_2.innerHTML = 
        `<div class="dropdown">
            <select id="inputSignal_2" class="form-select">
            <option value="24vdc">24V DC</option>
            <option value="120vac">120V AC</option>
            <option value="240vac">240V AC</option>
            </select>
        </div>`;

        ddSignalType_2.innerHTML = 
        `<div class="dropdown">
            <select id="signalType_2" class="form-select">
            <option value="pulseSignal">Pulse Signal</option>
            </select>
        </div>`;

        ddWidthTime_2.innerHTML = 
        `<div class="dropdown">
            <select id="widthTime_2" class="form-select">
                <option value="1Sec">1 Sec</option>
                <option value="2Sec">2 Sec</option>
                <option value="3Sec">3 Sec</option>
                <option value="4Sec">4 Sec</option>
                <option value="5Sec">5 Sec</option>
            </select>
        </div>`;
    }
    else if (selectedOption_2 == 'modulation')
    {
        divInputSignal_2.removeAttribute("hidden");
        divBaud_2.setAttribute("hidden", "hidden");
        ddInputSignal_2.innerHTML = 
        `<div class="dropdown">
            <select id="inputSignal_2" class="form-select">
                <option value="0v-10v">0V - 10V</option>
                <option value="2v-10v">2V - 10V</option>
                <option value="0mA-20mA">0mA - 20mA</option>
                <option value="4mA-20mA">4mA - 20mA</option>
            </select>
        </div>`;

        ddSignalType_2.innerHTML = 
        `<div class="dropdown">
            <select id="signalType_2" class="form-select">
                <option value="pulseSignal">Pulse Signal</option>
                <option value="sawSignal">Saw Signal</option>
                <option value="scaleSignal">Scale Signal</option>
            </select>
        </div>`;

        ddWidthTime_2.innerHTML = 
        `<div class="dropdown">
            <select id="widthTime_2" class="form-select">
            <option value="1Sec">1 Sec</option>
            <option value="2Sec">2 Sec</option>
            <option value="3Sec">3 Sec</option>
            <option value="4Sec">4 Sec</option>
            <option value="5Sec">5 Sec</option>
            </select>
        </div>`;
    }
    else if (selectedOption_2 == 'modbus')
    {
        divBaud_2.removeAttribute("hidden");
        divInputSignal_2.setAttribute("hidden", "hidden");

        ddSignalType_2.innerHTML = 
        `<div class="dropdown">
            <select id="signalType_2" class="form-select">
            <option value="pulseSignal">Pulse Signal</option>
            <option value="sawSignal">Saw Signal</option>
            <option value="scaleSignal">Scale Signal</option>
            </select>
        </div>`;

        ddWidthTime_2.innerHTML = 
        `<div class="dropdown">
        <select id="widthTime_2" class="form-select">
            <option value="1Sec">1 Sec</option>
            <option value="2Sec">2 Sec</option>
            <option value="3Sec">3 Sec</option>
            <option value="4Sec">4 Sec</option>
            <option value="5Sec">5 Sec</option>
        </select>
        </div>`;
    }
});

ddSignalType_2.addEventListener('change', function() 
{
    const selectedOption = this.value;
    if (selectedOption == 'sawSignal')
    {
        divWidthTime_2.setAttribute("hidden", "hidden");
    }
    else
    {
        divWidthTime_2.removeAttribute("hidden");
    }
});