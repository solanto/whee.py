#include <Arduino.h>
#include <Wire.h>

const int MPU_addr = 0x68; // I2C address of the MPU-6050
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;
float psi = 0, theta = 0, phi = 0, psiAdjust = 0, thetaAdjust = 0, phiAdjust = 0;

const int baud               = 9600,
          sampleRate         = 8000,
          calibrationSamples = 300;
const String d               = ","; // delimiter

const float sampleTime = 1.0 / sampleRate;

void read() {
    Wire.beginTransmission(MPU_addr);
    Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers
    AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
    AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp = Wire.read() << 8 | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX = Wire.read() << 8 | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY = Wire.read() << 8 | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

    psi   += GyX * sampleTime - psiAdjust;
    theta += GyY * sampleTime - thetaAdjust;
    phi   += GyZ * sampleTime - phiAdjust;
}

void calibrate(const int samples) {
    float dPsiSum = 0, dThetaSum = 0, dPhiSum = 0;

    read();
    float lastPsi   = psi,
          lastTheta = theta,
          lastPhi   = phi;

    for (int i = 0; i < samples - 1; i++) {
        read();

        dPsiSum   += psi   - lastPsi;
        dThetaSum += theta - lastTheta;
        dPhiSum   += phi   - lastPhi;

        lastPsi   = psi;
        lastTheta = theta;
        lastPhi   = phi;

        Serial.println("0,0,0");
        delay(sampleTime);
    }

    psiAdjust   = dPsiSum   / samples;
    thetaAdjust = dThetaSum / samples;
    phiAdjust   = dPhiSum   / samples;

    psi = theta = phi = 0;
}

void setup() {
    Wire.begin();
    Wire.beginTransmission(MPU_addr);
    Wire.write(0x6B); // PWR_MGMT_1 register
    Wire.write(0);    // set to zero (wakes up the MPU-6050)
    Wire.endTransmission(true);
    Serial.begin(baud);
    calibrate(calibrationSamples);
    Serial.println("yaw,pitch,roll");
}

void loop() {
    read();
    Serial.println(psi +d+ theta +d+ phi);
    delay(sampleTime);
}
