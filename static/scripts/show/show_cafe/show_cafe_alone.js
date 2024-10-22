const modalTurnON_waiting_cafe_a = document.getElementById("modalTurnON_waiting_cafe_a");
const progressBarTurnOn_cafe_a = document.getElementById("progressBarTurnOn_cafe_a");

const modalGoTo_0_cafe_a = document.getElementById("modalGoTo_0_cafe_a");
const progressBarGoTo0_cafe_a = document.getElementById("progressBarGoTo0_cafe_a");

var txt_drive_a = document.getElementById('txt_drive_a');

var ddDrive_a = document.getElementById('drive_a');
var divStart_a = document.getElementById('divStart_a');
var divStop_a = document.getElementById('divStop_a');
var divOpen_a = document.getElementById('divOpen_a')
var divClose_a = document.getElementById('divClose_a')
var divPorcent_cafe_a = document.getElementById('divPorcent_cafe_a')
var ddAuto_manual_cafe_a = document.getElementById('ddAuto_manual_cafe_a')
var divButtons_cafe_a = document.getElementById('divButtons_cafe_a')

var divShowParamsCafe_a = document.getElementById('divShowParamsCafe_a');
var divHideParamsCafe_a = document.getElementById('divHideParamsCafe_a');
var divParamsCafe_a = document.getElementById('divParamsCafe_a');

var modo_cafe_a = document.getElementById('modo_cafe_a');

var bStart_a = document.getElementById('bStart_a');
var bStop_a = document.getElementById('bStop_a');
var bOpen_a = document.getElementById('bOpen_a');
var bClose_a = document.getElementById('bClose_a');

var bPowerOn_Cafe_a = document.getElementById('powerOn_Cafe_a');
var bPowerOff_Cafe_a = document.getElementById('powerOff_Cafe_a');

const quantityInput = document.getElementById('manual_porcent_cafe_a');
const incrementButton = document.getElementById('increment_cafe_a');
const decrementButton = document.getElementById('decrement_cafe_a');


function iniciarConexion()
{
  socket = new WebSocket("ws://" + window.location.host + "/ws/sh_read_cafe_alone/");
  socket.onmessage = function(event){
    var data = JSON.parse(event.data);
    var rotationDegrees = map(data.pos, 0, 100, 180, 90);
    document.querySelector('#position_a').innerText = "POSITION: " + data.pos + "%";
    document.querySelector('#setPoint_a').innerText = "SETPOINT: " + data.setPos + "%";
    $('#knob_a').css('transform', 'translate(-114%,34%) rotate(' + rotationDegrees + 'deg)');
  }
  socket.onclose = function(event) {
    socket.close(); // Cierra la conexión WebSocket
    detenerConexion();
  };
}

// Detener el consumidor
function leerSensor() {
  socket.send(JSON.stringify({
    'message':'start'
  }))
}

function detenerConexion() {
  socket.send(JSON.stringify({
    'message':'stop'
  }))
}

  incrementButton.addEventListener('click', () => {
    quantityInput.stepUp(5);
  });
  
  decrementButton.addEventListener('click', () => {
    if (quantityInput.value > 5) {
      quantityInput.stepDown(5);
    }
  });

  if (modo_cafe_a.textContent == 'DIGITAL')
  {
    divPorcent_cafe_a.setAttribute("hidden", "hidden");
  }

 ddDrive_a.addEventListener('change', function() 
  {
      const selectedOption = this.value;
      if (selectedOption == 'auto')
      {
        divPorcent_cafe_a.setAttribute("hidden", "hidden");
        divStart_a.removeAttribute("hidden");
        divStop_a.removeAttribute("hidden");
        divOpen_a.setAttribute("hidden", "hidden");
        divClose_a.setAttribute("hidden", "hidden");
        txt_drive_a.innerHTML = "AUTO";
      }
      else if (selectedOption == 'manual' && modo_cafe_a.textContent != 'digital')
      {
        divPorcent_cafe_a.removeAttribute("hidden");
        divOpen_a.removeAttribute("hidden");
        divClose_a.removeAttribute("hidden");
        divStop_a.setAttribute("hidden", "hidden");
        divStart_a.setAttribute("hidden", "hidden");
        txt_drive_a.innerHTML = "MANUAL";
      }
      else if (selectedOption == 'manual' && modo_cafe_a.textContent == 'digital')
      {
        divOpen_a.removeAttribute("hidden");
        divClose_a.removeAttribute("hidden");
        divStop_a.setAttribute("hidden", "hidden");
        divStart_a.setAttribute("hidden", "hidden");
        divPorcent_cafe_a.setAttribute("hidden", "hidden");
        txt_drive_a.innerHTML = "MANUAL";
      }

      bStart_a.disabled = false;
      bStop_a.disabled = false;
      bOpen_a.disabled = false;
      bClose_a.disabled = false;

      bStart_a.style.backgroundColor = "#143a51";
      bStop_a.style.backgroundColor = "#143a51";
      bOpen_a.style.backgroundColor = "#143a51";
      bClose_a.style.backgroundColor = "#143a51";

      bStart_a.style.fontSize = "14px";
      bStop_a.style.fontSize = "14px";
      bOpen_a.style.fontSize = "14px";
      bClose_a.style.fontSize = "14px";
  });

  function powerOn_Cafe_a() {
    turnOn();
    
    window.modalTurnON_waiting_cafe_a.showModal();
    let progress = 0;
    const interval = setInterval(function() {
    progress += 1;
    progressBarTurnOn_cafe_a.value = progress;
    if (progress >= 100) {
      clearInterval(interval);
      modalTurnON_waiting_cafe_a.close();
    }
    }, 70); // Actualizar la barra de progreso cada 20ms

    bPowerOn_Cafe_a.setAttribute("hidden", "hidden");
    bPowerOff_Cafe_a.removeAttribute("hidden");
    ddAuto_manual_cafe_a.removeAttribute("hidden");
    divButtons_cafe_a.removeAttribute("hidden");
    iniciarConexion();
    setTimeout(leerSensor, 2000);

  }

  function powerOff_Cafe_a() {
    window.modalTurnOff_cafe_a.close();
    turnOff();
    detenerConexion();
    bPowerOff_Cafe_a.setAttribute("hidden", "hidden");
    bPowerOn_Cafe_a.removeAttribute("hidden");
    ddAuto_manual_cafe_a.setAttribute("hidden", "hidden");
    divButtons_cafe_a.setAttribute("hidden", "hidden");
  }

  function startRead() {
      intervalId_a = setInterval(readToCafe, 100);
    }
  
  function readToCafe() {
          $.ajax({
              url: '/show_read_cafe_alone/',
              success: function (data) {
                 //var pos =  str(data.data1);
                 var rotationDegrees = map(data.data1, 0, 100, 180, 0);
                  $('#position_a').text('POSITION: ' + data.data1 + '%');
                  $('#setPoint_a').text('SETPOINT: ' + data.data2 + '%');
                  $('#knob_a').css('transform', 'translate(-114%,34%)rotate('+rotationDegrees+'deg)');
              }
          });
    }

  function start() {
        $.ajax({
            url: '/show_start_cafe_alone/',
            success: function (data) {
            }
        });
        bStart_a.disabled = true;
        bStart_a.style.backgroundColor = "#6f6e6e";
        bStart_a.style.fontSize = "12px";
        bStop_a.disabled = false;
        bStop_a.style.backgroundColor = "#143a51";
        bStop_a.style.fontSize = "16px";
    }

  function stop() {
        $.ajax({
            url: '/show_stop_cafe_alone/',
            success: function (data) {
            }
        });
        //clearInterval(intervalId_a);
        bStart_a.disabled = false;
        bStart_a.style.backgroundColor = "#143a51";
        bStart_a.style.fontSize = "16px";
        bStop_a.disabled = true;
        bStop_a.style.backgroundColor = "#6f6e6e";
        bStop_a.style.fontSize = "12px";
    }

  function openn() {
        const quantityInput = document.getElementById('manual_porcent_cafe_a');
        $.ajax({
            type: "POST",
            url: '/show_open_cafe_alone/',
            data: {csrfmiddlewaretoken: '{{ csrf_token }}',"porcPos": quantityInput.value},
            success: function (data) {
            }
        });
        //bOpen_a.disabled = true;
        //bOpen_a.style.backgroundColor = "#6f6e6e";
        //bOpen_a.style.fontSize = "12px";
        bClose_a.disabled = false;
        bClose_a.style.backgroundColor = "#143a51";
        bClose_a.style.fontSize = "16px"; 
    }

  function closee() {
        $.ajax({
            url: '/show_close_cafe_alone/',
            success: function (data) {
            }
        });
        bClose_a.disabled = true;
        bClose_a.style.backgroundColor = "#6f6e6e";
        bClose_a.style.fontSize = "12px";
        bOpen_a.disabled = false;
        bOpen_a.style.backgroundColor = "#143a51";
        bOpen_a.style.fontSize = "16px"; 
    }

  function turnOn() {
        $.ajax({
            url: '/turnOn_cafe_alone/',
            success: function (data) {
            }
        });
    }

  function turnOff() {
        $.ajax({
            url: '/turnOff_cafe_alone/',
            success: function (data) {
            }
        });
    }

  function showParams_a() {
      divParamsCafe_a.removeAttribute("hidden");
      divShowParamsCafe_a.setAttribute("hidden", "hidden");
      divHideParamsCafe_a.removeAttribute("hidden");
  }

  function hideParams_a() {
      divParamsCafe_a.setAttribute("hidden", "hidden");
      divHideParamsCafe_a.setAttribute("hidden", "hidden");
      divShowParamsCafe_a.removeAttribute("hidden");
  }

    function map(valor, desde_min, desde_max, a_min, a_max) {
      // Asegurarse de que el valor esté dentro del rango original
      valor = Math.max(desde_min, Math.min(valor, desde_max));

      // Calcular el mapeo
      return (valor - desde_min) * (a_max - a_min) / (desde_max - desde_min) + a_min;
    }
