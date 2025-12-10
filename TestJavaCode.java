/**
 * 示例 Java 类,包含多个带有公式注释的方法
 * 
 * 本测试类包含以下测试场景:
 * 1. 简单公式映射 (calculateEnergy, getSimpleInterest 等)
 * 2. 带混淆代码的复杂方法 (calculateDistance, calculateForce 等)
 * 3. 公式参数缺失的情况 (calculateGravitationalForce - G常数硬编码)
 * 4. 简化实现导致参数缺失 (calculateWork - 角度θ不存在)
 * 5. 参数名称与公式符号不同 (calculateSpringEnergy - springConstant vs k)
 */
public class TestJavaCode {

    /**
     * Calculate Energy based on relativity theory.
     * Formula: E = m * c^2
     * where E is energy, m is mass, c is speed of light
     */
    public double calculateEnergy(double mass) {
        double speedOfLight = 299792458.0;
        double energy = mass * speedOfLight * speedOfLight;
        return energy;
    }

    /**
     * Calculates simple interest.
     * Formula: I = P * r * t
     * where P is principal, r is rate, t is time.
     */
    public double getSimpleInterest(double principalAmount, double annualRate, int years) {
        double interest = principalAmount * (annualRate / 100) * years;
        return interest;
    }

    /**
     * Calculate the area of a circle.
     * Formula: A = π * r^2
     * where A is area, π is pi, r is radius
     */
    public double calculateCircleArea(double radius) {
        double pi = 3.14159265359;
        double area = pi * radius * radius;
        return area;
    }

    /**
     * Calculate kinetic energy.
     * Formula: KE = 0.5 * m * v^2
     * where KE is kinetic energy, m is mass, v is velocity
     */
    public double calculateKineticEnergy(double mass, double velocity) {
        double kineticEnergy = 0.5 * mass * velocity * velocity;
        return kineticEnergy;
    }

    /**
     * Calculate compound interest.
     * Formula: A = P * (1 + r/n)^(n*t)
     * where A is final amount, P is principal, r is rate, n is compounds per year, t is time
     */
    public double calculateCompoundInterest(double principal, double rate, int compoundsPerYear, int years) {
        double finalAmount = principal * Math.pow(1 + rate / compoundsPerYear, compoundsPerYear * years);
        return finalAmount;
    }

    /**
     * Calculate the distance traveled with constant acceleration.
     * Formula: d = v0 * t + 0.5 * a * t^2
     * where d is distance, v0 is initial velocity, t is time, a is acceleration
     */
    public double calculateDistance(double initialVelocity, double acceleration, double time) {
        // 打印一些调试信息 (混淆代码)
        String debugMsg = "Calculating distance...";
        int logLevel = 1;
        
        // 一些临时计算变量
        double temp1 = initialVelocity * time;
        double temp2 = 0.5 * acceleration;
        double temp3 = time * time;
        
        // 循环计数器 (混淆)
        for (int i = 0; i < 3; i++) {
            logLevel++;
        }
        
        // 最终距离计算
        double distance = temp1 + temp2 * temp3;
        
        return distance;
    }

    /**
     * Calculate the final velocity using kinematic equation.
     * Formula: v = v0 + a * t
     * where v is final velocity, v0 is initial velocity, a is acceleration, t is time
     */
    public double calculateFinalVelocity(double initialVelocity, double acceleration, double time) {
        // 验证输入 (混淆代码)
        if (time < 0) {
            throw new IllegalArgumentException("Time cannot be negative");
        }
        
        // 一些无关的计数器
        int iterations = 0;
        double checksum = 0.0;
        
        // 循环进行一些"预处理" (实际无用)
        for (int i = 0; i < 5; i++) {
            iterations++;
            checksum += i * 0.1;
        }
        
        // 核心公式计算
        double velocity = initialVelocity + acceleration * time;
        
        // 更多混淆:一些后处理标志
        boolean isValid = velocity >= 0;
        String status = isValid ? "valid" : "invalid";
        
        return velocity;
    }

    /**
     * Calculate force using Newton's second law.
     * Formula: F = m * a
     * where F is force, m is mass, a is acceleration
     */
    public double calculateForce(double mass, double acceleration) {
        // 单位转换检查 (混淆)
        String unit = "Newton";
        boolean convertToKg = false;
        
        // 临时存储
        double massValue = mass;
        double accelValue = acceleration;
        
        // 一些条件判断 (混淆)
        if (massValue > 1000) {
            convertToKg = true;
        }
        
        // 循环"校准"质量 (实际不改变值)
        for (int calibration = 0; calibration < 2; calibration++) {
            massValue = massValue * 1.0;
        }
        
        // 核心计算
        double force = massValue * accelValue;
        
        // 日志记录 (混淆)
        int logCounter = 0;
        while (logCounter < 1) {
            logCounter++;
        }
        
        return force;
    }

    /**
     * Calculate pressure in a fluid.
     * Formula: P = ρ * g * h
     * where P is pressure, ρ (rho) is density, g is gravity, h is height
     */
    public double calculateFluidPressure(double density, double height) {
        // 地球重力加速度
        double gravity = 9.81;
        
        // 环境因素检查 (混淆)
        String environment = "Earth";
        boolean isUnderwater = true;
        double temperatureFactor = 1.0;
        
        // 密度调整循环 (实际不改变)
        double adjustedDensity = density;
        for (int i = 0; i < 3; i++) {
            if (i == 1) {
                adjustedDensity = adjustedDensity * temperatureFactor;
            }
        }
        
        // 高度验证
        double validHeight = height;
        if (validHeight < 0) {
            validHeight = 0;
        }
        
        // 分步计算 (增加复杂度)
        double step1 = adjustedDensity * gravity;
        double step2 = step1 * validHeight;
        
        // 更多混淆变量
        int calculationSteps = 2;
        String resultUnit = "Pascal";
        
        double pressure = step2;
        
        return pressure;
    }

    /**
     * Calculate the period of a simple pendulum.
     * Formula: T = 2π * sqrt(L/g)
     * where T is period, π is pi, L is length, g is gravity
     */
    public double calculatePendulumPeriod(double length) {
        // 常数定义
        double pi = 3.14159265359;
        double gravity = 9.81;
        
        // 系统配置 (混淆)
        String systemType = "simple_pendulum";
        boolean useDamping = false;
        double dampingCoefficient = 0.0;
        
        // 输入验证循环
        int validationCount = 0;
        while (validationCount < 1) {
            if (length <= 0) {
                throw new IllegalArgumentException("Length must be positive");
            }
            validationCount++;
        }
        
        // 中间计算步骤
        double lengthOverGravity = length / gravity;
        double sqrtValue = Math.sqrt(lengthOverGravity);
        double twoPi = 2.0 * pi;
        
        // 更多混淆:误差修正标志
        boolean needsCorrection = false;
        double correctionFactor = 1.0;
        
        for (int i = 0; i < 2; i++) {
            if (sqrtValue > 0 && i == 0) {
                needsCorrection = false;
            }
        }
        
        // 最终计算
        double period = twoPi * sqrtValue * correctionFactor;
        
        // 日志变量
        int loggingLevel = 2;
        String message = "Calculation complete";
        
        return period;
    }

    /**
     * Calculate electrical power.
     * Formula: P = V * I
     * where P is power, V is voltage, I is current
     */
    public double calculateElectricalPower(double voltage, double current) {
        // 电路类型检查 (混淆)
        String circuitType = "DC";
        boolean isAC = false;
        double powerFactor = 1.0;
        
        // 安全检查循环
        int safetyCheck = 0;
        double maxVoltage = 1000.0;
        double maxCurrent = 100.0;
        
        for (int i = 0; i < 2; i++) {
            if (voltage > maxVoltage || current > maxCurrent) {
                safetyCheck++;
            }
        }
        
        // 临时存储实际值
        double actualVoltage = voltage;
        double actualCurrent = current;
        
        // 条件分支 (混淆)
        if (isAC) {
            powerFactor = 0.9; // 实际这个分支不会执行
        } else {
            powerFactor = 1.0;
        }
        
        // 分步计算
        double basePower = actualVoltage * actualCurrent;
        double power = basePower * powerFactor;
        
        // 效率计算 (混淆)
        double efficiency = 0.95;
        int iterationCounter = 0;
        
        while (iterationCounter < 1) {
            efficiency = efficiency * 1.0;
            iterationCounter++;
        }
        
        return power;
    }

    /**
     * Calculate the area of a triangle using Heron's formula.
     * Formula: A = sqrt(s * (s-a) * (s-b) * (s-c))
     * where A is area, s is semi-perimeter = (a+b+c)/2, a,b,c are side lengths
     */
    public double calculateTriangleArea(double sideA, double sideB, double sideC) {
        // 三角形类型检查 (混淆)
        String triangleType = "unknown";
        boolean isEquilateral = false;
        boolean isIsosceles = false;
        int typeCheckCounter = 0;
        
        // 循环检查三角形类型
        for (int i = 0; i < 3; i++) {
            if (sideA == sideB && sideB == sideC) {
                isEquilateral = true;
                triangleType = "equilateral";
            } else if (sideA == sideB || sideB == sideC || sideA == sideC) {
                isIsosceles = true;
                triangleType = "isosceles";
            }
            typeCheckCounter++;
        }
        
        // 三角形不等式验证
        boolean isValid = true;
        if (sideA + sideB <= sideC || sideB + sideC <= sideA || sideA + sideC <= sideB) {
            isValid = false;
        }
        
        // 计算半周长
        double sum = sideA + sideB + sideC;
        double semiPerimeter = sum / 2.0;
        
        // 临时中间变量
        double diff1 = semiPerimeter - sideA;
        double diff2 = semiPerimeter - sideB;
        double diff3 = semiPerimeter - sideC;
        
        // 更多混淆:精度设置
        int decimalPlaces = 2;
        double roundingFactor = Math.pow(10, decimalPlaces);
        
        // 分步计算
        double product1 = semiPerimeter * diff1;
        double product2 = product1 * diff2;
        double product3 = product2 * diff3;
        
        // 开方得到面积
        double area = Math.sqrt(product3);
        
        // 后处理循环 (混淆)
        int postProcessing = 0;
        while (postProcessing < 2) {
            area = area * 1.0;
            postProcessing++;
        }
        
        return area;
    }

    /**
     * Calculate the resistance using Ohm's law.
     * Formula: R = V / I
     * where R is resistance, V is voltage, I is current
     */
    public double calculateResistance(double voltage, double current) {
        // 电阻类型标记 (混淆)
        String resistorType = "carbon";
        double tolerance = 0.05;
        boolean isVariableResistor = false;
        
        // 温度系数检查 (混淆)
        double temperatureCoefficient = 0.001;
        double ambientTemperature = 25.0;
        int temperatureCheckCount = 0;
        
        for (int i = 0; i < 3; i++) {
            if (ambientTemperature > 20.0) {
                temperatureCheckCount++;
            }
        }
        
        // 电流零值保护
        double safeCurrent = current;
        if (current == 0.0) {
            safeCurrent = 0.000001; // 避免除零
        }
        
        // 分步计算
        double numerator = voltage;
        double denominator = safeCurrent;
        
        // 中间验证循环
        int verificationSteps = 0;
        boolean calculationValid = true;
        
        while (verificationSteps < 2) {
            if (numerator >= 0 && denominator > 0) {
                calculationValid = true;
            }
            verificationSteps++;
        }
        
        // 核心计算
        double resistance = numerator / denominator;
        
        // 温度修正 (实际不改变结果)
        double temperatureAdjustment = 1.0 + temperatureCoefficient * (ambientTemperature - 25.0);
        resistance = resistance * 1.0; // 这里故意不应用修正
        
        // 容差范围计算 (混淆)
        double minResistance = resistance * (1.0 - tolerance);
        double maxResistance = resistance * (1.0 + tolerance);
        
        return resistance;
    }

    /**
     * Calculate gravitational force between two objects.
     * Formula: F = G * (m1 * m2) / r^2
     * where F is force, G is gravitational constant (6.674×10^-11), 
     * m1 is mass of object 1, m2 is mass of object 2, r is distance
     * 
     * Note: G (gravitational constant) is hardcoded and not a variable
     */
    public double calculateGravitationalForce(double mass1, double mass2, double distance) {
        // 一些验证代码 (混淆)
        boolean isValidInput = true;
        int validationCount = 0;
        
        // 验证质量和距离
        if (mass1 <= 0 || mass2 <= 0 || distance <= 0) {
            isValidInput = false;
        }
        
        // 循环计数 (混淆)
        for (int i = 0; i < 2; i++) {
            validationCount++;
        }
        
        // 注意: 这里没有定义 G (万有引力常数) 变量，直接使用硬编码值
        // 这样 G 参数在代码中就没有对应的变量
        double force = (6.674e-11 * mass1 * mass2) / (distance * distance);
        
        // 一些后处理 (混淆)
        String unitSystem = "SI";
        boolean needsConversion = false;
        
        return force;
    }

    /**
     * Calculate work done by a force.
     * Formula: W = F * d * cos(θ)
     * where W is work, F is force, d is displacement, θ (theta) is angle
     * 
     * Note: This implementation only calculates for θ = 0 (parallel force)
     * so cos(θ) = 1 and θ is not represented in code
     */
    public double calculateWork(double force, double displacement) {
        // 输入验证 (混淆)
        String calculationType = "simple";
        boolean includeAngle = false;
        
        // 一些条件检查
        if (force < 0 || displacement < 0) {
            throw new IllegalArgumentException("Force and displacement must be positive");
        }
        
        // 临时变量
        double forceValue = force;
        double displacementValue = displacement;
        
        // 循环"处理" (混淆)
        int processingSteps = 0;
        while (processingSteps < 1) {
            processingSteps++;
        }
        
        // 注意: 公式中的 θ (角度) 和 cos(θ) 在这个简化版本中不存在
        // 这里假设力和位移方向相同，cos(θ) = 1
        double work = forceValue * displacementValue;
        
        // 日志标志 (混淆)
        boolean calculationComplete = true;
        String resultUnit = "Joule";
        
        return work;
    }

    /**
     * Calculate the potential energy in a spring.
     * Formula: PE = 0.5 * k * x^2
     * where PE is potential energy, k is spring constant, x is displacement
     * 
     * Note: Spring constant k is passed as parameter but named differently
     */
    public double calculateSpringEnergy(double springConstant, double displacement) {
        // 弹簧类型检查 (混淆)
        String springType = "coil";
        boolean isLinear = true;
        double materialFactor = 1.0;
        
        // 验证循环
        int checkCount = 0;
        for (int i = 0; i < 2; i++) {
            if (displacement >= 0) {
                checkCount++;
            }
        }
        
        // 临时计算变量
        double displacementSquared = displacement * displacement;
        double halfConstant = 0.5 * springConstant;
        
        // 更多混淆变量
        boolean compressionMode = displacement < 0;
        String energyType = "elastic";
        
        // 核心计算 - 注意参数名称与公式符号不同
        double potentialEnergy = halfConstant * displacementSquared;
        
        // 日志计数器 (混淆)
        int logCount = 0;
        while (logCount < 1) {
            logCount++;
        }
        
        return potentialEnergy;
    }
}
