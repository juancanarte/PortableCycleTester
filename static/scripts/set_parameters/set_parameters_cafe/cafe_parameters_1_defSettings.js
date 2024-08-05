var ddSignalType = document.getElementById('signalType_1');
var ddWidthTime = document.getElementById('widthTime_1');
var divSignalType = document.getElementById('divSignalType_1');
var divWidthTime  = document.getElementById('divWidthTime_1');

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