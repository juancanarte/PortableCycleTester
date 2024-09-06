const modalTurnON_waiting_cafe_2 = document.getElementById("modalTurnON_waiting_cafe_2");
const progressBarTurnOn_cafe_2 = document.getElementById("progressBarTurnOn_cafe_2");

const modalGoTo_0_cafe_2 = document.getElementById("modalGoTo_0_cafe_2");
const progressBarGoTo0_cafe_2 = document.getElementById("progressBarGoTo0_cafe_2");

  var txt_drive_2 = document.getElementById('txt_drive_2');
  var txt_position_2 = document.getElementById('position_2');
  var txt_setPoint_2 = document.getElementById('setPoint_2');
  const resize_ob_2 = new ResizeObserver(function(entries) 
  {
    // since we are observing only a single element, so we access the first element in entries array
    let rect = entries[0].contentRect;

    // current width & height
    let width = rect.width;
    let height = rect.height;
    var newFont = Number(width)/9.5;
    txt_drive_2.style.fontSize = newFont+'px';
    txt_position_2.style.fontSize = newFont+'px';
    txt_setPoint_2.style.fontSize = newFont+'px';
  });
// start observing for resize
resize_ob_2.observe(document.querySelector("#txt_cafe_2"));


  var ddDrive_2 = document.getElementById('drive_2');
  var divStart_2 = document.getElementById('divStart_2');
  var divStop_2 = document.getElementById('divStop_2');
  var divOpen_2 = document.getElementById('divOpen_2')
  var divClose_2 = document.getElementById('divClose_2')
  var divPorcent_cafe_2 = document.getElementById('divPorcent_cafe_2')
  var ddAuto_manual_cafe_2 = document.getElementById('ddAuto_manual_cafe_2')
  var divButtons_cafe_2 = document.getElementById('divButtons_cafe_2')

  var divShowParamsCafe_2 = document.getElementById('divShowParamsCafe_2');
  var divHideParamsCafe_2 = document.getElementById('divHideParamsCafe_2');
  var divParamsCafe_2 = document.getElementById('divParamsCafe_2');

  var modo_cafe_2 = document.getElementById('modo_cafe_2');

  var bStart_2 = document.getElementById('bStart_2');
  var bStop_2 = document.getElementById('bStop_2');
  var bOpen_2 = document.getElementById('bOpen_2');
  var bClose_2 = document.getElementById('bClose_2');

  var bPowerOn_Cafe_2 = document.getElementById('powerOn_Cafe_2');
  var bPowerOff_Cafe_2 = document.getElementById('powerOff_Cafe_2');

  const quantityInput_2 = document.getElementById('manual_porcent_cafe_2');
  const incrementButton_2 = document.getElementById('increment_cafe_2');
  const decrementButton_2 = document.getElementById('decrement_cafe_2');

  function iniciarConexion_2()
  {
    socket_2 = new WebSocket("ws://" + window.location.host + "/ws/sh_read_cafe_2/");
    socket_2.onmessage = function(event){
      var data = JSON.parse(event.data);
      var rotationDegrees = map_2(data.pos, 0, 100, 180, 90);

      document.querySelector('#position_2').innerText = "POSITION: " + data.pos + "%";
      document.querySelector('#setPoint_2').innerText = "SETPOINT: " + data.setPos + "%";
      $('#knob_2').css('transform', 'translate(-114%,34%) rotate(' + rotationDegrees + 'deg)');    }
      socket_2.onclose = function(event) {
        socket_2.close(); // Cierra la conexión WebSocket
        detenerConexion_2();
    };
  }

  function leerSensor_2() {
    socket_2.send(JSON.stringify({
      'message':'start'
    }))
  }
  // Detener el consumidor
  function detenerConexion_2() {
    socket_2.send(JSON.stringify({
      'message':'stop'
    }))
  }


  incrementButton_2.addEventListener('click', () => {
    quantityInput_2.stepUp(5);
  });
  
  decrementButton_2.addEventListener('click', () => {
    if (quantityInput_2.value > 5) {
      quantityInput_2.stepDown(5);
    }
  });

  if (modo_cafe_2.textContent == 'DIGITAL')
  {
    divPorcent_cafe_2.setAttribute("hidden", "hidden");
  }

 ddDrive_2.addEventListener('change', function() 
  {
      const selectedOption_2 = this.value;
      if (selectedOption_2 == 'auto')
      {
        divPorcent_cafe_2.setAttribute("hidden", "hidden");
        divStart_2.removeAttribute("hidden");
        divStop_2.removeAttribute("hidden");
        divOpen_2.setAttribute("hidden", "hidden");
        divClose_2.setAttribute("hidden", "hidden");
        txt_drive_2.innerHTML = "AUTO";
      }
      else if (selectedOption_2 == 'manual' && modo_cafe_2.textContent != 'digital')
      {
        divPorcent_cafe_2.removeAttribute("hidden");
        divOpen_2.removeAttribute("hidden");
        divClose_2.removeAttribute("hidden");
        divStop_2.setAttribute("hidden", "hidden");
        divStart_2.setAttribute("hidden", "hidden");
        txt_drive_2.innerHTML = "MANUAL";
      }
      else if (selectedOption_2 == 'manual' && modo_cafe_2.textContent == 'digital')
      {
        divPorcent_cafe_2.setAttribute("hidden", "hidden");
        divOpen_2.removeAttribute("hidden");
        divClose_2.removeAttribute("hidden");
        divStop_2.setAttribute("hidden", "hidden");
        divStart_2.setAttribute("hidden", "hidden");
        txt_drive_2.innerHTML = "MANUAL";
      }

      bStart_2.disabled = false;
      bStop_2.disabled = false;
      bOpen_2.disabled = false;
      bClose_2.disabled = false;

      bStart_2.style.backgroundColor = "#143a51";
      bStop_2.style.backgroundColor = "#143a51";
      bOpen_2.style.backgroundColor = "#143a51";
      bClose_2.style.backgroundColor = "#143a51";

      bStart_2.style.fontSize = "14px";
      bStop_2.style.fontSize = "14px";
      bOpen_2.style.fontSize = "14px";
      bClose_2.style.fontSize = "14px";
  });

  function powerOn_Cafe_2() {
    turnOn_2();

    window.modalTurnON_waiting_cafe_2.showModal();
    let progress = 0;
    const interval = setInterval(function() {
    progress += 1;
    progressBarTurnOn_cafe_2.value = progress;
    if (progress >= 100) {
      clearInterval(interval);
      modalTurnON_waiting_cafe_2.close();
    }
    }, 70); // Actualizar la barra de progreso cada 20ms

    bPowerOn_Cafe_2.setAttribute("hidden", "hidden");
    bPowerOff_Cafe_2.removeAttribute("hidden");
    ddAuto_manual_cafe_2.removeAttribute("hidden");
    divButtons_cafe_2.removeAttribute("hidden");
    iniciarConexion_2();
    setTimeout(leerSensor_2, 2000);
  }

  function powerOff_Cafe_2() {
    window.modalTurnOff_cafe_2.close();
    turnOff_2();
    detenerConexion_2();
    bPowerOff_Cafe_2.setAttribute("hidden", "hidden");
    bPowerOn_Cafe_2.removeAttribute("hidden");
    ddAuto_manual_cafe_2.setAttribute("hidden", "hidden");
    divButtons_cafe_2.setAttribute("hidden", "hidden");
  }

  function startRead_2() {
      intervalId_2 = setInterval(readToCafe_2, 200);
    }
  
  function readToCafe_2() {
          $.ajax({
              url: '/show_read_cafe_2/',
              success: function (data_2) {
                 //var pos =  str(data.data1);
                 var rotationDegrees_2 = map_2(data_2.data1, 0, 100, 180, 0);
                  $('#position_2').text('POSITION: ' + data_2.data1 + '%');
                  $('#setPoint_2').text('SETPOINT: ' + data_2.data2 + '%');
                  $('#knob_2').css('transform', 'translate(-114%,34%)rotate('+rotationDegrees_2+'deg)');
              }
          });
    }

  function start_2() {
        $.ajax({
            url: '/show_start_cafe_2/',
            success: function (data) {
            }
        });
        bStart_2.disabled = true;
        bStart_2.style.backgroundColor = "#6f6e6e";
        bStart_2.style.fontSize = "12px";
        bStop_2.disabled = false;
        bStop_2.style.backgroundColor = "#143a51";
        bStop_2.style.fontSize = "16px";
    }

  function stop_2() {
        $.ajax({
            url: '/show_stop_cafe_2/',
            success: function (data) {
            }
        });
        //clearInterval(intervalId_a);
        bStart_2.disabled = false;
        bStart_2.style.backgroundColor = "#143a51";
        bStart_2.style.fontSize = "16px";
        bStop_2.disabled = true;
        bStop_2.style.backgroundColor = "#6f6e6e";
        bStop_2.style.fontSize = "12px";
    }

  function openn_2() {
        const quantityInput_2 = document.getElementById('manual_porcent_cafe_2');
        $.ajax({
            type: "POST",
            url: '/show_open_cafe_2/',
            data: {csrfmiddlewaretoken: '{{ csrf_token }}',"porcPos": quantityInput_2.value},
            success: function (data) {
            }
        });
        bOpen_2.disabled = true;
        bOpen_2.style.backgroundColor = "#6f6e6e";
        bOpen_2.style.fontSize = "12px";
        bClose_2.disabled = false;
        bClose_2.style.backgroundColor = "#143a51";
        bClose_2.style.fontSize = "16px"; 
    }

  function closee_2() {
        $.ajax({
            url: '/show_close_cafe_2/',
            success: function (data) {
            }
        });
        bClose_2.disabled = true;
        bClose_2.style.backgroundColor = "#6f6e6e";
        bClose_2.style.fontSize = "12px";
        bOpen_2.disabled = false;
        bOpen_2.style.backgroundColor = "#143a51";
        bOpen_2.style.fontSize = "16px"; 
    }

  function turnOn_2() {
        $.ajax({
            url: '/turnOn_cafe_2/',
            success: function (data) {
            }
        });
    }

  function turnOff_2() {
        $.ajax({
            url: '/turnOff_cafe_2/',
            success: function (data) {
            }
        });
    }

    function showParams_2() {
      divParamsCafe_2.removeAttribute("hidden");
      divShowParamsCafe_2.setAttribute("hidden", "hidden");
      divHideParamsCafe_2.removeAttribute("hidden");
  }

  function hideParams_2() {
      divParamsCafe_2.setAttribute("hidden", "hidden");
      divHideParamsCafe_2.setAttribute("hidden", "hidden");
      divShowParamsCafe_2.removeAttribute("hidden");
  }

    function map_2(valor, desde_min, desde_max, a_min, a_max) {
      // Asegurarse de que el valor esté dentro del rango original
      valor = Math.max(desde_min, Math.min(valor, desde_max));

      // Calcular el mapeo
      return (valor - desde_min) * (a_max - a_min) / (desde_max - desde_min) + a_min;
    }    
