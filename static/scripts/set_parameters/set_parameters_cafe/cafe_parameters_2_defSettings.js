var ddSignalType_2 = document.getElementById('signalType_2');
var ddWidthTime_2 = document.getElementById('widthTime_2');
var divSignalType_2 = document.getElementById('divSignalType_2');
var divWidthTime_2  = document.getElementById('divWidthTime_2');

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