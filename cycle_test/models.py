from django.db import models

# Create your models here.
class users(models.Model):
    fullName = models.CharField(max_length=50, unique=True)

class defSettings(models.Model):
    pctMode = models.CharField(max_length=10)
    signalType_1 = models.CharField(max_length=12)
    widthTime_1 = models.CharField(max_length=4)
    widthTime_coil_1 = models.CharField(max_length=4)
    opVoltage_ls_1 = models.CharField(max_length=5)
    signalType_2 = models.CharField(max_length=12)
    widthTime_2 = models.CharField(max_length=4)
    widthTime_coil_2 = models.CharField(max_length=4)
    opVoltage_ls_2 = models.CharField(max_length=5)

class tempDataCt_a(models.Model):
    temp = models.BinaryField()
    current = models.BinaryField()
    setPoint = models.BinaryField()
    feedback = models.BinaryField()
    relayO = models.BinaryField()
    relayC = models.BinaryField()
    timeStamp = models.BinaryField()
    pauseStatus = models.BinaryField(default=b'')

class tempDataCtv2_a(models.Model):
    temp = models.IntegerField()
    current = models.IntegerField()
    setPoint = models.IntegerField()
    feedback = models.IntegerField()
    relayO = models.IntegerField()
    relayC = models.IntegerField()
    timeStamp = models.FloatField()
    pauseStatus = models.BooleanField()

class tempDataCtv2_dut2(models.Model):
    temp = models.IntegerField()
    current = models.IntegerField()
    setPoint = models.IntegerField()
    feedback = models.IntegerField()
    relayO = models.IntegerField()
    relayC = models.IntegerField()
    timeStamp = models.FloatField()
    pauseStatus = models.BooleanField()

class cycleTestData(models.Model):
    dut = models.CharField(max_length=30)
    actuatorRef = models.CharField(max_length=30)
    load = models.BooleanField()
    loadDetails = models.BinaryField()
    testerName = models.CharField(max_length=30)
    observations = models.CharField(max_length=30)
    operationMode = models.CharField(max_length=30, default='Digital')
    bauds = models.IntegerField(default=19200)
    node = models.IntegerField(default=1)
    operationVoltage = models.CharField(max_length=30)
    inputType = models.CharField(max_length=30)
    signalType = models.CharField(max_length=30)
    pulseTime = models.CharField(max_length=30)
    highValue = models.IntegerField()
    lowValue = models.IntegerField()
    day = models.CharField(max_length=30)
    month = models.CharField(max_length=30)
    year = models.CharField(max_length=30)
    fullDate = models.CharField(max_length=30)
    dateStart = models.CharField(max_length=30, default='')
    dateEnd = models.CharField(max_length=30)
    plannedTimeTest = models.CharField(max_length=30)
    finalTimeTest = models.CharField(max_length=30)
    temp = models.BinaryField()
    current = models.BinaryField()
    setPoint = models.BinaryField()
    feedBack = models.BinaryField()
    relayO = models.BinaryField()
    relayC = models.BinaryField()
    timeStamp = models.BinaryField()
    pause = models.BinaryField(default=b'')
    relaysCounter = models.BinaryField()
    feedBackCounter = models.BinaryField()
