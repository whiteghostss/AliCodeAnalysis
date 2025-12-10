# Java 公式映射分析工具

这是一个利用 AI 大模型(通义千问)自动分析 Java 代码中公式注释与变量映射关系的工具。

## 功能特点

- 🔍 自动解析 Java 代码结构(使用 javalang)
- 📝 提取方法注释中的数学公式
- 🧠 利用通义千问 AI 进行语义推理
- 🎯 自动映射公式符号到代码变量
- 📊 生成 JSON 格式的分析报告

## 安装依赖

```bash
# 激活虚拟环境(如果有)
source .venv/Scripts/activate  # Windows Git Bash
# 或
.venv\Scripts\activate  # Windows CMD

# 安装依赖包
pip install javalang dashscope
```

## 使用方法

### 1. 分析默认测试文件

```bash
python Ali.py
```

这将分析项目目录下的 `TestJavaCode.java` 文件。

### 2. 分析指定的 Java 文件

```bash
python Ali.py path/to/your/JavaFile.java
```

### 3. 查看分析结果

分析完成后,结果会:

- 在控制台打印显示
- 保存到 `mapping_results.json` 文件

## 示例

### 输入 (TestJavaCode.java)

```java
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
```

### 输出 (mapping_results.json)

```json
{
  "method_name": "calculateEnergy",
  "mapping": {
    "E": "energy",
    "m": "mass",
    "c": "speedOfLight"
  }
}
```

## 测试文件说明

`TestJavaCode.java` 包含了多个带公式注释的方法示例:

1. **calculateEnergy** - 相对论能量公式 E = m \* c²
2. **getSimpleInterest** - 简单利息公式 I = P _ r _ t
3. **calculateCircleArea** - 圆面积公式 A = π \* r²
4. **calculateKineticEnergy** - 动能公式 KE = 0.5 _ m _ v²
5. **calculateCompoundInterest** - 复利公式 A = P * (1 + r/n)^(n*t)

您可以直接在 `TestJavaCode.java` 中添加新的方法进行测试!

## 项目结构

```
AliCodeAnalysis/
├── Ali.py                    # 主程序
├── TestJavaCode.java         # 测试用 Java 文件
├── mapping_results.json      # 分析结果输出(自动生成)
├── README.md                 # 说明文档
└── .venv/                    # Python 虚拟环境
```

## 注意事项

1. 需要配置有效的通义千问 API Key (在 `Ali.py` 中设置)
2. Java 代码必须符合语法规范才能被正确解析
3. 建议在方法注释中明确写出公式和参数说明
4. 支持的数值类型: int, long, double, float, short, Integer, Long, Double, Float, BigDecimal

## 扩展使用

如果您想分析自己的 Java 项目:

1. 将您的 Java 文件放到项目目录
2. 运行: `python Ali.py YourFile.java`
3. 查看 `mapping_results.json` 获取映射结果

Happy Coding! 🚀
