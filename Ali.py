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

    def parse_java_file(self, java_file_path):
        """
        解析整个 Java 文件，提取所有方法的信息
        """
        try:
            with open(java_file_path, 'r', encoding='utf-8') as f:
                java_code = f.read()
        except Exception as e:
            return None, f"Failed to read file: {e}"
        
        try:
            tree = javalang.parse.parse(java_code)
        except javalang.parser.JavaSyntaxError as e:
            return None, f"Syntax Error: {e}"

        methods_info = []

        # 遍历 AST 寻找所有方法定义
        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            method_info = {}
            
            # 1. 提取方法名
            method_info['method_name'] = node.name
            
            # 2. 提取注释 (Javadoc)
            javadoc = node.documentation
            method_info['comment'] = javadoc if javadoc else "No comment found"
            
            # 3. 提取变量 (参数 + 局部变量)
            variables = []
            
            # 3.1 提取参数
            for param in node.parameters:
                # 简单判断是否为数值类型 (int, double, float, long, or boxed types)
                if self._is_numeric_type(param.type.name):
                    variables.append({
                        "name": param.name,
                        "type": param.type.name,
                        "source": "parameter"
                    })
            
            # 3.2 提取方法体内的局部变量
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
            
            # 4. 提取方法的源代码（近似）
            # 注意：javalang 不保留完整的源代码位置，这里我们简化处理
            method_info['code'] = f"Method: {node.name}"
            
            methods_info.append(method_info)

        if not methods_info:
            return None, "No methods found in Java file"
        
        return methods_info, None

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
        3. 如果公式中的常数在代码中也是硬编码的（如 π=3.14159），需要映射到对应的常量变量。
        4. **特别重要**: 如果公式中某个参数在代码中完全没有对应的变量（既不是参数也不是局部变量），请将其值设为 null。
           例如: 公式是 F = m*a*g，但代码中只有 mass 和 accel，没有 g，则返回 {{"F": "force", "m": "mass", "a": "accel", "g": null}}
        
        ### 输出格式
        请直接返回一个JSON对象，Key是公式中的参数符号，Value是代码中的变量名（字符串）或 null（如果无对应变量）。
        不要包含Markdown格式（如 ```json）。
        
        示例输出1: {{"E": "energy", "m": "mass", "c": "speedOfLight"}}
        示例输出2: {{"F": "force", "m": "mass", "a": "acceleration", "g": null}}
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

    def process(self, java_file_path):
        """
        处理整个 Java 文件，分析所有方法
        """
        print(f"[*] 开始分析 Java 文件: {java_file_path}")
        print(f"[-] 正在解析代码结构...")
        
        methods_info, err = self.parse_java_file(java_file_path)
        
        if err:
            print(f"[!] 解析失败: {err}")
            return None

        print(f"[+] 成功提取到 {len(methods_info)} 个方法\n")
        
        all_results = []
        
        for idx, method_info in enumerate(methods_info, 1):
            print(f"{'='*60}")
            print(f"[{idx}/{len(methods_info)}] 分析方法: {method_info['method_name']}")
            print(f"{'='*60}")
            
            # 显示注释（截断显示）
            comment_preview = method_info['comment'].strip()[:100]
            print(f"[-] 注释: {comment_preview}{'...' if len(method_info['comment']) > 100 else ''}")
            
            # 显示变量
            var_names = [v['name'] for v in method_info['variables']]
            print(f"[-] 提取到变量: {var_names}")
            
            # 调用 LLM 进行语义推理
            print(f"[-] 正在调用通义千问进行语义推理...")
            mapping = self.get_semantic_mapping(method_info)
            
            print(f"[+] 映射结果:")
            print(json.dumps(mapping, indent=4, ensure_ascii=False))
            
            # 检查并标注空映射
            if isinstance(mapping, dict) and not mapping.get('error'):
                null_params = [key for key, value in mapping.items() if value is None]
                if null_params:
                    print(f"[!] 注意: 以下公式参数在代码中没有找到对应变量: {null_params}")
            print()
            
            all_results.append({
                'method_name': method_info['method_name'],
                'mapping': mapping
            })
        
        return all_results

# ================= 主程序 =================

if __name__ == "__main__":
    import sys
    
    # 默认的测试文件路径
    default_java_file = "TestJavaCode.java"
    
    # 支持命令行参数指定 Java 文件
    if len(sys.argv) > 1:
        java_file = sys.argv[1]
    else:
        # 使用当前目录下的默认文件
        script_dir = os.path.dirname(os.path.abspath(__file__))
        java_file = os.path.join(script_dir, default_java_file)
    
    # 检查文件是否存在
    if not os.path.exists(java_file):
        print(f"[!] 错误: 找不到 Java 文件: {java_file}")
        print(f"[*] 使用方法: python Ali.py [java_file_path]")
        print(f"[*] 示例: python Ali.py TestJavaCode.java")
        sys.exit(1)
    
    # 创建映射器并处理文件
    mapper = JavaFormulaMapper()
    results = mapper.process(java_file)
    
    # 保存结果到 JSON 文件
    if results:
        output_file = "mapping_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"[+] 分析结果已保存到: {output_file}")
