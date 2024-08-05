const modalTurnON_waiting_cafe_1 = document.getElementById("modalTurnON_waiting_cafe_1");
const progressBarTurnOn_cafe_1 = document.getElementById("progressBarTurnOn_cafe_1");

const modalGoTo_0_cafe_1 = document.getElementById("modalGoTo_0_cafe_1");
const progressBarGoTo0_cafe_1 = document.getElementById("progressBarGoTo0_cafe_1");

  var txt_drive_1 = document.getElementById('txt_drive_1');
  var txt_position_1 = document.getElementById('position_1');
  var txt_setPoint_1 = document.getElementById('setPoint_1');
  const resize_ob = new ResizeObserver(function(entries) 
  {
    // since we are observing only a single element, so we access the first element in entries array
    let rect = entries[0].contentRect;

    // current width & height
    let width = rect.width;
    let height = rect.height;
    var newFont = Number(width)/9.5;
    txt_drive_1.style.fontSize = newFont+'px';
    txt_position_1.style.fontSize = newFont+'px';
    txt_setPoint_1.style.fontSize = newFont+'px';
  });
// start observing for resize
resize_ob.observe(document.querySelector("#txt_cafe_1"));

  var ddDrive_1 = document.getElementById('drive_1');
  var divStart_1 = document.getElementById('divStart_1');
  var divStop_1 = document.getElementById('divStop_1');
  var divOpen_1 = document.getElementById('divOpen_1')
  var divClose_1 = document.getElementById('divClose_1')
  var divPorcent_cafe_1 = document.getElementById('divPorcent_cafe_1')
  var ddAuto_manual_cafe_1 = document.getElementById('ddAuto_manual_cafe_1')
  var divButtons_cafe_1 = document.getElementById('divButtons_cafe_1')

  var divShowParamsCafe_1 = document.getElementById('divShowParamsCafe_1');
  var divHideParamsCafe_1 = document.getElementById('divHideParamsCafe_1');
  var divParamsCafe_1 = document.getElementById('divParamsCafe_1');

  var modo_cafe_1 = document.getElementById('modo_cafe_1');

  var bStart_1 = document.getElementById('bStart_1');
  var bStop_1 = document.getElementById('bStop_1');
  var bOpen_1 = document.getElementById('bOpen_1');
  var bClose_1 = document.getElementById('bClose_1');

  var bPowerOn_Cafe_1 = document.getElementById('powerOn_Cafe_1');
  var bPowerOff_Cafe_1 = document.getElementById('powerOff_Cafe_1');

  const quantityInput_1 = document.getElementById('manual_porcent_cafe_1');
  const incrementButton_1 = document.getElementById('increment_cafe_1');
  const decrementButton_1 = document.getElementById('decrement_cafe_1');


  function iniciarConexion_1()
  { 
    socket_1 = new WebSocket("ws://" + window.location.host + "/ws/sh_read_cafe_1/");
    socket_1.onmessage = function(event){
      var data = JSON.parse(event.data);
      var rotationDegrees = map_1(data.pos, 0, 100, 180, 90);

      document.querySelector('#position_1').innerText = "POSITION: " + data.pos + "%";
      document.querySelector('#setPoint_1').innerText = "SETPOINT: " + data.setPos + "%";
      $('#knob_1').css('transform', 'translate(-114%,34%) rotate(' + rotationDegrees + 'deg)');
    }
    socket_1.onclose = function(event) {
      socket_1.close(); // Cierra la conexión WebSocket
      detenerConexion_1();
  };
  }

  // Detener el consumidor
function leerSensor_1() {
  socket_1.send(JSON.stringify({
    'message':'start'
  }))
}

function detenerConexion_1() {
  socket_1.send(JSON.stringify({
    'message':'stop'
  }))
}


  incrementButton_1.addEventListener('click', () => {
    quantityInput_1.stepUp(5);
  });
  
  decrementButton_1.addEventListener('click', () => {
    if (quantityInput_1.value > 5) {
      quantityInput_1.stepDown(5);
    }
  });

  if (modo_cafe_1.textContent == 'DIGITAL')
  {
    divPorcent_cafe_1.setAttribute("hidden", "hidden");
  }

 ddDrive_1.addEventListener('change', function() 
  {
      const selectedOption_1 = this.value;
      if (selectedOption_1 == 'auto')
      {
        divPorcent_cafe_1.setAttribute("hidden", "hidden");
        divStart_1.removeAttribute("hidden");
        divStop_1.removeAttribute("hidden");
        divOpen_1.setAttribute("hidden", "hidden");
        divClose_1.setAttribute("hidden", "hidden");
        txt_drive_1.innerHTML = "AUTO";
      }
      else if (selectedOption_1 == 'manual' && modo_cafe_1.textContent != 'DIGITAL')
      {
        divPorcent_cafe_1.removeAttribute("hidden");
        divOpen_1.removeAttribute("hidden");
        divClose_1.removeAttribute("hidden");
        divStop_1.setAttribute("hidden", "hidden");
        divStart_1.setAttribute("hidden", "hidden");
        txt_drive_1.innerHTML = "MANUAL";
      }
      else if (selectedOption_1 == 'manual' && modo_cafe_1.textContent == 'DIGITAL')
      {
        divOpen_1.removeAttribute("hidden");
        divClose_1.removeAttribute("hidden");
        divStop_1.setAttribute("hidden", "hidden");
        divStart_1.setAttribute("hidden", "hidden");
        txt_drive_1.innerHTML = "MANUAL";
      }

      bStart_1.disabled = false;
      bStop_1.disabled = false;
      bOpen_1.disabled = false;
      bClose_1.disabled = false;

      bStart_1.style.backgroundColor = "#143a51";
      bStop_1.style.backgroundColor = "#143a51";
      bOpen_1.style.backgroundColor = "#143a51";
      bClose_1.style.backgroundColor = "#143a51";

      bStart_1.style.fontSize = "14px";
      bStop_1.style.fontSize = "14px";
      bOpen_1.style.fontSize = "14px";
      bClose_1.style.fontSize = "14px";
  });

  function powerOn_Cafe_1() {
    turnOn_1();

    window.modalTurnON_waiting_cafe_1.showModal();
    let progress = 0;
    const interval = setInterval(function() {
    progress += 1;
    progressBarTurnOn_cafe_1.value = progress;
    if (progress >= 100) {
      clearInterval(interval);
      modalTurnON_waiting_cafe_1.close();
    }
    }, 70); // Actualizar la barra de progreso cada 20ms

    bPowerOn_Cafe_1.setAttribute("hidden", "hidden");
    bPowerOff_Cafe_1.removeAttribute("hidden");
    ddAuto_manual_cafe_1.removeAttribute("hidden");
    divButtons_cafe_1.removeAttribute("hidden");
    iniciarConexion_1();
    setTimeout(leerSensor_1, 2000);
  }

  function powerOff_Cafe_1() {
    window.modalTurnOff_cafe_1.close();
    turnOff_1();
    detenerConexion_1();
    bPowerOff_Cafe_1.setAttribute("hidden", "hidden");
    bPowerOn_Cafe_1.removeAttribute("hidden");
    ddAuto_manual_cafe_1.setAttribute("hidden", "hidden");
    divButtons_cafe_1.setAttribute("hidden", "hidden");
  }

  function startRead_1() {
      intervalId_1 = setInterval(readToCafe_1, 200);
    }
  
  function readToCafe_1() {
          $.ajax({
              url: '/show_read_cafe_1/',
              success: function (data_1) {
                 //var pos =  str(data.data1);
                 var rotationDegrees_1 = map_1(data_1.data1, 0, 100, 180, 0);
                  $('#position_1').text('POSITION: ' + data_1.data1 + '%');
                  $('#setPoint_1').text('SETPOINT: ' + data_1.data2 + '%');
                  $('#knob_1').css('transform', 'translate(-114%,34%)rotate('+rotationDegrees_1+'deg)');
              }
          });
    }

  function start_1() {
        $.ajax({
            url: '/show_start_cafe_1/',
            success: function (data) {
            }
        });
        bStart_1.disabled = true;
        bStart_1.style.backgroundColor = "#6f6e6e";
        bStart_1.style.fontSize = "12px";
        bStop_1.disabled = false;
        bStop_1.style.backgroundColor = "#143a51";
        bStop_1.style.fontSize = "16px";
    }

  function stop_1() {
        $.ajax({
            url: '/show_stop_cafe_1/',
            success: function (data) {
            }
        });
        //clearInterval(intervalId_a);
        bStart_1.disabled = false;
        bStart_1.style.backgroundColor = "#143a51";
        bStart_1.style.fontSize = "16px";
        bStop_1.disabled = true;
        bStop_1.style.backgroundColor = "#6f6e6e";
        bStop_1.style.fontSize = "12px";
    }

  function openn_1() {
        const quantityInput_1 = document.getElementById('manual_porcent_cafe_1');
        $.ajax({
            type: "POST",
            url: '/show_open_cafe_1/',
            data: {csrfmiddlewaretoken: '{{ csrf_token }}',"porcPos": quantityInput_1.value},
            success: function (data) {
            }
        });
        bOpen_1.disabled = true;
        bOpen_1.style.backgroundColor = "#6f6e6e";
        bOpen_1.style.fontSize = "12px";
        bClose_1.disabled = false;
        bClose_1.style.backgroundColor = "#143a51";
        bClose_1.style.fontSize = "16px"; 
    }

  function closee_1() {
        $.ajax({
            url: '/show_close_cafe_1/',
            success: function (data) {
            }
        });
        bClose_1.disabled = true;
        bClose_1.style.backgroundColor = "#6f6e6e";
        bClose_1.style.fontSize = "12px";
        bOpen_1.disabled = false;
        bOpen_1.style.backgroundColor = "#143a51";
        bOpen_1.style.fontSize = "16px"; 
    }

  function turnOn_1() {
        $.ajax({
            url: '/turnOn_cafe_1/',
            success: function (data) {
            }
        });
    }

  function turnOff_1() {
        $.ajax({
            url: '/turnOff_cafe_1/',
            success: function (data) {
            }
        });
    }
    function showParams_1() {
      divParamsCafe_1.removeAttribute("hidden");
      divShowParamsCafe_1.setAttribute("hidden", "hidden");
      divHideParamsCafe_1.removeAttribute("hidden");
  }

  function hideParams_1() {
      divParamsCafe_1.setAttribute("hidden", "hidden");
      divHideParamsCafe_1.setAttribute("hidden", "hidden");
      divShowParamsCafe_1.removeAttribute("hidden");
  }
    function map_1(valor, desde_min, desde_max, a_min, a_max) {
      // Asegurarse de que el valor esté dentro del rango original
      valor = Math.max(desde_min, Math.min(valor, desde_max));

      // Calcular el mapeo
      return (valor - desde_min) * (a_max - a_min) / (desde_max - desde_min) + a_min;
    }
