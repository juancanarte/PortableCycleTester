var ddOperMode = document.getElementById('operation_mode_1');
var ddInputSignal = document.getElementById('inputSignal_1');
var ddBaud = document.getElementById('baud_1');
var node = document.getElementById('node_1');
var ddSignalType = document.getElementById('signalType_1');
var ddWidthTime = document.getElementById('widthTime_1');

var divSignalType = document.getElementById('divSignalType_1');

var divBaud  = document.getElementById('divBaud_1');
var hidden = divBaud.getAttribute("hidden");

var divOpVoltage  = document.getElementById('divOpVoltage_1');
var hiddenOpVoltage = divOpVoltage.getAttribute("hidden");

var divInputSignal  = document.getElementById('divInputSignal_1');
var hiddenInputSignal = divInputSignal.getAttribute("hidden");

var divWidthTime  = document.getElementById('divWidthTime_1');
var hiddenWidthTime = divInputSignal.getAttribute("hidden");

const quantityInput = document.getElementById('node_1');
const incrementButton = document.getElementById('increment_1');
const decrementButton = document.getElementById('decrement_1');

var modo = document.getElementById('modo'); // Que modo es SHOW o CYCLE TEST
var resultado = (modo != null) && modo.textContent;
//Si es SHOW
if (resultado == 'Show')
{
    divWidthTime.setAttribute("hidden", "hidden");
    divSignalType.setAttribute("hidden", "hidden");
    document.getElementById('divHighValue_1').setAttribute("hidden", "hidden");
    document.getElementById('divLowValue_1').setAttribute("hidden", "hidden");
}

incrementButton.addEventListener('click', () => {
    quantityInput.stepUp();
  });
  
  decrementButton.addEventListener('click', () => {
    if (quantityInput.value > 1) {
      quantityInput.stepDown();
    }
  });

ddOperMode.addEventListener('change', function() 
{
    const selectedOption = this.value;
    if (selectedOption == 'digital')
    {
        divInputSignal.setAttribute("hidden", "hidden");
        divBaud.setAttribute("hidden", "hidden");
        ddInputSignal.innerHTML = 
        `<div class="dropdown">
            <select id="inputSignal_1" class="form-select">
            <option value="24vdc">24V DC</option>
            <option value="120vac">120V AC</option>
            <option value="240vac">240V AC</option>
            </select>
        </div>`;

        ddSignalType.innerHTML = 
        `<div class="dropdown">
            <select id="signalType_1" class="form-select">
            <option value="pulseSignal">Pulse Signal</option>
            </select>
        </div>`;

        ddWidthTime.innerHTML = 
        `<div class="dropdown">
            <select id="widthTime_1" class="form-select">
                <option value="1Sec">1 Sec</option>
                <option value="2Sec">2 Sec</option>
                <option value="3Sec">3 Sec</option>
                <option value="4Sec">4 Sec</option>
                <option value="5Sec">5 Sec</option>
            </select>
        </div>`;
    }
    else if (selectedOption == 'modulation')
    {
        divInputSignal.removeAttribute("hidden");
        divBaud.setAttribute("hidden", "hidden");
        ddInputSignal.innerHTML = 
        `<div class="dropdown">
            <select id="inputSignal_1" class="form-select">
                <option value="0v-10v">0V - 10V</option>
                <option value="2v-10v">2V - 10V</option>
                <option value="0mA-20mA">0mA - 20mA</option>
                <option value="4mA-20mA">4mA - 20mA</option>
            </select>
        </div>`;

        ddSignalType.innerHTML = 
        `<div class="dropdown">
            <select id="signalType_1" class="form-select">
                <option value="pulseSignal">Pulse Signal</option>
                <option value="sawSignal">Saw Signal</option>
                <option value="scaleSignal">Scale Signal</option>
            </select>
        </div>`;

        ddWidthTime.innerHTML = 
        `<div class="dropdown">
            <select id="widthTime_1" class="form-select">
            <option value="1Sec">1 Sec</option>
            <option value="2Sec">2 Sec</option>
            <option value="3Sec">3 Sec</option>
            <option value="4Sec">4 Sec</option>
            <option value="5Sec">5 Sec</option>
            </select>
        </div>`;
    }
    else if (selectedOption == 'modbus')
    {
        divBaud.removeAttribute("hidden");
        divInputSignal.setAttribute("hidden", "hidden");
        ddSignalType.innerHTML = 
        `<div class="dropdown">
            <select id="signalType_1" class="form-select">
            <option value="pulseSignal">Pulse Signal</option>
            <option value="sawSignal">Saw Signal</option>
            <option value="scaleSignal">Scale Signal</option>
            </select>
        </div>`;

        ddWidthTime.innerHTML = 
        `<div class="dropdown">
        <select id="widthTime_1" class="form-select">
            <option value="1Sec">1 Sec</option>
            <option value="2Sec">2 Sec</option>
            <option value="3Sec">3 Sec</option>
            <option value="4Sec">4 Sec</option>
            <option value="5Sec">5 Sec</option>
        </select>
        </div>`;
    }

    
});

ddSignalType.addEventListener('change', function() 
{
    const selectedOption = this.value;
    if (selectedOption == 'sawSignal')
    {
        divWidthTime.setAttribute("hidden", "hidden");
    }
    else
    {
        divWidthTime.removeAttribute("hidden");
    }
});