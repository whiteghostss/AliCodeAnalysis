import os
import json
import javalang
import dashscope
from http import HTTPStatus

# 配置 API KEY
dashscope.api_key = "sk-b4d710d02b0f49b1908ff05a08263918"

class JavaFormulaMapper:
    def __init__(self):
        # 使用通义千问 Max 模型，逻辑推理能力最强
        self.model = dashscope.Generation.Models.qwen_max

    def parse_java_code(self, java_code_snippet):
        """
        利用 javalang 解析 Java 代码，提取注释和数值型变量
        """
        # javalang 需要完整的类结构才能解析，所以这里包装一层 dummy class
        wrapped_code = f"public class DummyClass {{\n{java_code_snippet}\n}}"
        
        try:
            tree = javalang.parse.parse(wrapped_code)
        except javalang.parser.JavaSyntaxError as e:
            return None, f"Syntax Error: {e}"

        method_info = {}

        # 遍历 AST 寻找方法定义
        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            # 1. 提取注释 (Javadoc)
            javadoc = node.documentation
            method_info['comment'] = javadoc if javadoc else "No comment found"
            
            # 2. 提取变量 (参数 + 局部变量)
            variables = []
            
            # 2.1 提取参数
            for param in node.parameters:
                # 简单判断是否为数值类型 (int, double, float, long, or boxed types)
                if self._is_numeric_type(param.type.name):
                    variables.append({
                        "name": param.name,
                        "type": param.type.name,
                        "source": "parameter"
                    })
            
            # 2.2 提取方法体内的局部变量
            if node.body:
                for path, child in node.filter(javalang.tree.LocalVariableDeclaration):
                    if self._is_numeric_type(child.type.name):
                        for declarator in child.declarators:
                            variables.append({
                                "name": declarator.name,
                                "type": child.type.name,
                                "source": "local_variable"
                            })
            
            method_info['variables'] = variables
            method_info['code'] = java_code_snippet # 保存原始代码供 LLM 参考
            
            # 我们只处理第一个找到的方法
            return method_info, None

        return None, "No method found in snippet"

    def _is_numeric_type(self, type_name):
        """判断是否为数值类型"""
        numeric_types = [
            'int', 'long', 'double', 'float', 'short', 
            'Integer', 'Long', 'Double', 'Float', 'BigDecimal'
        ]
        return type_name in numeric_types

    def get_semantic_mapping(self, method_info):
        """
        利用通义千问大模型进行语义映射
        """
        comment = method_info['comment']
        variables = [v['name'] for v in method_info['variables']]
        code = method_info['code']

        # 构建 Prompt
        prompt = f"""
        你是一个代码分析专家。你的任务是将Java代码中的变量映射到注释中公式的参数。
        
        ### 输入信息
        1. **Java代码**:
        ```java
        {code}
        ```
        
        2. **代码对应的注释(包含公式)**:
        {comment}
        
        3. **从AST提取的数值型变量候选列表**:
        {json.dumps(variables)}
        
        ### 任务要求
        请分析代码逻辑，找出公式中的符号（例如 'a', 'b', 'x' 等）对应代码中的哪个变量。
        注意：
        1. 这种对应是语义上的。例如公式是 F = m*a，代码可能是 `double force = mass * accel;`，则 F->force, m->mass, a->accel。
        2. 忽略循环变量或临时计数器，只关注公式核心参数。
        3. 如果公式中的常数在代码中也是硬编码的，不需要映射。
        
        ### 输出格式
        请直接返回一个JSON对象，Key是公式中的参数符号，Value是代码中的变量名。不要包含Markdown格式（如 ```json）。
        
        示例输出: {{"E": "energy", "m": "mass", "c": "lightSpeed"}}
        """

        messages = [
            {'role': 'system', 'content': '你是一个精通Java代码分析和数学公式的助手。'},
            {'role': 'user', 'content': prompt}
        ]

        try:
            response = dashscope.Generation.call(
                self.model,
                messages=messages,
                result_format='message',
            )

            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0].message.content
                # 清洗一下返回结果，防止包含 markdown 标记
                content = content.replace("```json", "").replace("```", "").strip()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {"error": "LLM returned invalid JSON", "raw_output": content}
            else:
                return {"error": f"API Error: {response.code} - {response.message}"}

        except Exception as e:
            return {"error": str(e)}

    def process(self, java_code):
        print(f"[-] 正在解析代码结构...")
        info, err = self.parse_java_code(java_code)
        
        if err:
            print(f"[!] 解析失败: {err}")
            return

        print(f"[-] 提取到注释: {info['comment'].strip()[:50]}...")
        print(f"[-] 提取到变量: {[v['name'] for v in info['variables']]}")
        
        print(f"[-] 正在调用通义千问进行语义推理...")
        mapping = self.get_semantic_mapping(info)
        
        print(f"[+] 映射结果:")
        print(json.dumps(mapping, indent=4, ensure_ascii=False))
        return mapping

# ================= 使用示例 =================

if __name__ == "__main__":
    mapper = JavaFormulaMapper()

    # 示例 1: 简单的物理公式
    # 公式: E = m * c^2
    java_func_1 = """
    /**
     * Calculate Energy based on relativity theory.
     * Formula: E = m * c^2
     */
    public double calculateEnergy(double mass) {
        double speedOfLight = 299792458.0;
        double energy = mass * speedOfLight * speedOfLight;
        return energy;
    }
    """

    # 示例 2: 稍微复杂的金融公式
    # 公式: I = P * r * t (Simple Interest)
    java_func_2 = """
    /**
     * Calculates simple interest.
     * Formula: I = P * r * t
     * where P is principal, r is rate, t is time.
     */
    public double getSimpleInterest(double principalAmount, double annualRate, int years) {
        double interest = principalAmount * (annualRate / 100) * years;
        return interest;
    }
    """

    print("=== 测试案例 1 ===")
    mapper.process(java_func_1)
    
    print("\n=== 测试案例 2 ===")
    mapper.process(java_func_2)