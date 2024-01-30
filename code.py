# Write your code here :-)
import time

TdsSensorPin = 0  # A0 pin
VREF = 5.0  # analog reference voltage(Volt) of the ADC
SCOUNT = 30  # sum of sample point

analogBuffer = [0] * SCOUNT  # store the analog value in the array, read from ADC
analogBufferTemp = [0] * SCOUNT
analogBufferIndex = 0
copyIndex = 0

averageVoltage = 0
tdsValue = 0
temperature = 16  # current temperature for compensation

# median filtering algorithm
def getMedianNum(bArray, iFilterLen):
    bTab = bArray[:iFilterLen]
    for j in range(iFilterLen - 1):
        for i in range(iFilterLen - j - 1):
            if bTab[i] > bTab[i + 1]:
                bTab[i], bTab[i + 1] = bTab[i + 1], bTab[i]
    if iFilterLen & 1:
        bTemp = bTab[(iFilterLen - 1) // 2]
    else:
        bTemp = (bTab[iFilterLen // 2] + bTab[iFilterLen // 2 - 1]) / 2
    return bTemp


def setup():
    # Serial.begin(115200)  # Commented as there is no direct equivalent in Python
    pass


def loop():
    global analogBufferIndex, copyIndex, averageVoltage, tdsValue, temperature

    analogSampleTimepoint = int(time.time() * 1000)
    if (
        int(time.time() * 1000) - analogSampleTimepoint > 40
    ):  # every 40 milliseconds, read the analog value from the ADC
        analogSampleTimepoint = int(time.time() * 1000)
        analogBuffer[
            analogBufferIndex
        ] = 0  # Replace analogRead(TdsSensorPin) with 0 for simulation purposes
        analogBufferIndex += 1
        if analogBufferIndex == SCOUNT:
            analogBufferIndex = 0

    printTimepoint = int(time.time() * 1000)
    if int(time.time() * 1000) - printTimepoint > 800:
        printTimepoint = int(time.time() * 1000)
        for copyIndex in range(SCOUNT):
            analogBufferTemp[copyIndex] = analogBuffer[copyIndex]

            # read the analog value more stable by the median filtering algorithm, and convert to voltage value
            averageVoltage = getMedianNum(analogBufferTemp, SCOUNT) * VREF / 1024.0

            # temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
            compensationCoefficient = 1.0 + 0.02 * (temperature - 25.0)
            # temperature compensation
            compensationVoltage = averageVoltage / compensationCoefficient

            # convert voltage value to tds value
            tdsValue = (
                133.42 * compensationVoltage * compensationVoltage * compensationVoltage
                - 255.86 * compensationVoltage * compensationVoltage
                + 857.39 * compensationVoltage
            ) * 0.5

            # Serial.print("voltage:")
            # Serial.print(averageVoltage, 2)
            # Serial.print("V   ")
            print(f"TDS Value: {int(tdsValue)} ppm")


if __name__ == "__main__":
    setup()
    while True:
        loop()

