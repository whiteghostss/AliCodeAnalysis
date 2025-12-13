
# Java Formula Semantic Mapper (Java 公式语义映射服务)

这是一个基于 **Flask** + **AST (javalang)** + **LLM (Qwen-Max)** 的微服务。
它的主要功能是分析 Java 源代码，提取方法上的数学公式注释（Javadoc），并将公式中的参数精确映射到代码内部的变量、函数调用或常量表达式。

> **核心特性更新 (v2.0)**：
> *   ✅ 支持**嵌套函数调用**提取（如 `b.sqr(c)`）。
> *   ✅ 支持**对象方法**提取（如 `particle.getEnergy()`）。
> *   ✅ 修复了公式结果（左值）错误映射到输入参数的问题。
> *   ✅ 引入严格的优先级逻辑：变量 > 表达式 > 常量 > Null。

---

## 🛠 环境准备

### 1. 依赖安装
请确保 Python 版本 >= 3.8。在项目根目录下创建 `requirements.txt` 并运行安装：

```bash
# requirements.txt 内容:
flask
javalang
dashscope
```

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key (重要)
为了安全起见，**不要**将 Key 硬编码在代码中。请设置环境变量：

**Linux / macOS:**
```bash
export DASHSCOPE_API_KEY="sk-你的阿里云百炼Key"
```

**Windows (PowerShell):**
```powershell
$env:DASHSCOPE_API_KEY="sk-你的阿里云百炼Key"
```

### 3. 启动服务
```bash
python app.py
```
服务默认运行在 `http://0.0.0.0:5000`。

---

## 🚀 接口文档

### 1. 代码分析接口
**端点 (Endpoint)**: `/analyze`
**方法 (Method)**: `POST`
**描述**: 上传 Java 代码，返回每个方法的公式参数映射结果。

#### 调用方式 A: 直接发送代码文本 (JSON)
适用于前端编辑器或文本流。
*   **Content-Type**: `application/json`
*   **Body**:
    ```json
    {
        "code": "public class Test { ... }"
    }
    ```

#### 调用方式 B: 上传文件 (Multipart)
适用于批量处理或文件上传组件。
*   **Content-Type**: `multipart/form-data`
*   **Body**:
    *   `file`: (Java源文件)

---

### 2. 响应示例 (Response)

假设输入的 Java 代码如下：
```java
/**
 * Formula: R = base + term
 */
public double calculate(double base, double freq) {
    return mathService.sum(base, noiseReducer.calc(freq));
}
```

**响应结果 (JSON)**:
```json
{
    "success": true,
    "data": [
        {
            "method_name": "calculate",
            "mapping": {
                "R": "mathService.sum(base, noiseReducer.calc(freq))", // 结果映射
                "base": "base",                                        // 变量直接映射
                "term": "noiseReducer.calc(freq)"                      // 嵌套调用映射
            }
        }
    ]
}
```

---

## 🧠 映射逻辑详解 (对接必读)

为了解决复杂代码场景下的映射准确性，本服务采用了以下优先级规则：

1.  **优先级 1 (最高)：语义变量**
    *   如果公式参数能找到同名或语义高度相似的**局部变量/参数**，直接输出变量名。
    *   *示例*: `m` -> `mass`。

2.  **优先级 2：函数调用与表达式**
    *   如果参数没有对应的中间变量，而是直接通过**函数嵌套**计算的，输出完整的调用语句。
    *   *示例*: 公式中的 `term` 对应代码中的 `b.sqr(c)`。

3.  **优先级 3：硬编码常量**
    *   如果代码中直接写死了数值且无变量定义，输出该数值。
    *   *示例*: `G` -> `9.8`。

4.  **优先级 4：Null**
    *   如果找不到任何合理的对应关系，输出 `null`。
    *   **注意**: 接口不会为了填满字段而强行关联不相关的变量。

---

## 🧪 测试用例 (Test Cases)

你可以使用以下代码测试接口的健壮性：

```java
public class ComplexTest {
    /**
     * Formula: Dist = x + D
     */
    public double complexDistance(double x, double y, double z) {
        // 测试复杂表达式提取
        return x + Math.sqrt(Math.pow(y, 2) + Math.pow(z, 2));
    }
}
```
**预期输出**:
*   `x`: "x"
*   `D`: "Math.sqrt(Math.pow(y, 2) + Math.pow(z, 2))"

---

## ❓ 常见问题 (FAQ)

**Q1: 为什么我的代码分析失败了？**
*   检查 Java 代码是否有**语法错误**。服务底层依赖 `javalang` 解析 AST，如果代码连编译都过不了（比如少了分号），解析会直接报错。
*   确保注释格式包含公式，且大模型能理解该公式。

**Q2: 为什么有些参数返回 null？**
*   这说明模型在代码中没找到对应的实现。请检查代码逻辑是否完整，或者公式参数命名是否过于晦涩。

**Q3: 接口响应速度慢？**
*   因为后端调用了大模型（Qwen-Max）进行深度语义分析，通常耗时在 2-5 秒之间，请前端做好 Loading 状态处理。

---

## 📞 联系开发者
*   后端维护: [你的名字/ID]
*   对接状态: **Ready**
