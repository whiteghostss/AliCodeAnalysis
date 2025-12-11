import os
import json
import re
import javalang
import dashscope
from http import HTTPStatus


dashscope.api_key = "sk-b4d710d02b0f49b1908ff05a08263918"

class JavaFormulaMapper:
    def __init__(self):
        # 使用 Qwen-Max 模型，逻辑推理能力最强
        self.model = dashscope.Generation.Models.qwen_max

    def _is_numeric_type(self, type_name):
        """
        判断是否为数值类型，过滤掉无关的 String 或 boolean
        """
        if not type_name:
            return False
        numeric_types = {
            'int', 'long', 'double', 'float', 'short', 'byte',
            'Integer', 'Long', 'Double', 'Float', 'Short', 'Byte',
            'BigDecimal', 'BigInteger', 'Number'
        }
        return type_name in numeric_types

    def get_method_code(self, file_content, start_line):
        """
        基于括号匹配提取完整的方法源代码
        """
        lines = file_content.split('\n')
        current_line_idx = start_line - 1
        
        brace_balance = 0
        found_start = False
        method_lines = []
        max_lines = len(lines)
        
        for i in range(current_line_idx, max_lines):
            line = lines[i]
            method_lines.append(line)
            
            open_braces = line.count('{')
            close_braces = line.count('}')
            
            if open_braces > 0:
                found_start = True
            
            brace_balance += (open_braces - close_braces)
            
            if found_start and brace_balance == 0:
                break
                
        return "\n".join(method_lines)

    def parse_java_file(self, java_file_path):
        """
        解析 Java 文件，提取 AST 信息和源码
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

        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            method_info = {}
            method_info['method_name'] = node.name
            method_info['comment'] = node.documentation if node.documentation else "No comment"
            
            variables = []
            
            # 1. 提取参数
            for param in node.parameters:
                if self._is_numeric_type(param.type.name):
                    variables.append(param.name)
            
            # 2. 提取局部变量 (递归查找)
            if node.body:
                for path, child in node.filter(javalang.tree.LocalVariableDeclaration):
                    if self._is_numeric_type(child.type.name):
                        for declarator in child.declarators:
                            variables.append(declarator.name)
            
            method_info['variables'] = variables
            
            # 3. 提取源码
            if node.position:
                method_info['code'] = self.get_method_code(java_code, node.position.line)
            else:
                method_info['code'] = "// Extraction failed"
            
            methods_info.append(method_info)

        if not methods_info:
            return None, "No methods found"
        
        return methods_info, None

    def get_semantic_mapping(self, method_info):
        """
        核心方法：构造 Prompt 并调用 LLM，使用正则提取 JSON
        """
        comment = method_info['comment']
        variables = method_info['variables']
        code = method_info['code']

        # === Prompt 经过精心设计以满足你的所有需求 ===
        prompt = f"""
        你是一个严谨的代码分析专家。任务是分析Java代码，将代码中的实现映射回注释中的数学公式参数。

        ### 输入数据
        1. **代码 (Source)**:
        ```java
        {code}
        ```
        2. **注释与公式 (Formula)**:
        {comment}
        3. **数值型变量列表**:
        {json.dumps(variables)}

        ### 严格映射规则 (优先级从上到下)
        1. **范围限制**: 
           - **Output Key 只能是公式中出现的符号**。
           - 绝对不要输出公式中不存在的 Key（严禁编造 "constant_k", "temp" 等）。
           - 忽略中间计算变量，除非它们直接代表公式参数。

        2. **常数与变量的优先级 (重要)**:
           - **情况A (优先)**: 如果公式中的常数在代码中有对应的变量定义（例如 `double pi = 3.14;`），Value 必须是**变量名**（"pi"）。
           - **情况B (次要)**: 只有当代码中完全没有定义该变量，而是直接在计算式里写了数字（例如 `return mass * 9.8;`），Value 才是**数字**（9.8）。

        3. **忽略表达式**: 
           - 如果代码是 `annualRate / 100`，Value 必须是源变量名 `annualRate`，不能是表达式。

        4. **Null**: 
           - 如果公式里的参数在代码里既没变量也没硬编码数值，Value 设为 null。

        ### 输出格式
        - 只输出纯 JSON 字符串。
        - 不要输出 Markdown 标记。
        - 不要输出解释文字。
        
        示例目标格式: {{"F": "force", "m": "mass", "G": 6.674e-11}}
        """

        messages = [
            {'role': 'system', 'content': '你是一个只输出JSON的助手。严格遵守Key的范围限制。'},
            {'role': 'user', 'content': prompt}
        ]

        try:
            response = dashscope.Generation.call(
                self.model,
                messages=messages,
                result_format='message',
            )

            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0].message.content.strip()
                
                # 使用正则表达式提取 JSON，防止 LLM 说废话
                match = re.search(r'\{.*\}', content, re.DOTALL)
                
                if match:
                    json_str = match.group()
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        return {"error": "JSON Parse Error", "extracted": json_str}
                else:
                    return {"error": "No JSON found in output", "raw": content}
            else:
                return {"error": f"API Error: {response.code}"}

        except Exception as e:
            return {"error": str(e)}

    def process(self, java_file_path):
        print(f"[*] 正在分析文件: {java_file_path}")
        methods_info, err = self.parse_java_file(java_file_path)
        
        if err:
            print(f"[!] 解析错误: {err}")
            return None

        results = []
        total = len(methods_info)
        
        for idx, info in enumerate(methods_info, 1):
            print(f"[{idx}/{total}] 分析方法: {info['method_name']}")
            
            mapping = self.get_semantic_mapping(info)
            
            # 在控制台输出时使用 indent=4，满足"输出一对后换行"的视觉要求
            formatted_json = json.dumps(mapping, indent=4, ensure_ascii=False)
            print(f"    映射结果:\n{formatted_json}\n")
            
            results.append({
                "method_name": info['method_name'],
                "mapping": mapping
            })
        
        return results

if __name__ == "__main__":
    import sys
    
    # 默认文件名
    target_file = "TestJavaCode.java"
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
        
    if os.path.exists(target_file):
        mapper = JavaFormulaMapper()
        final_results = mapper.process(target_file)
        
        output_filename = "mapping_results.json"
        
        
        with open(output_filename, "w", encoding='utf-8') as f:
            json.dump(final_results, f, indent=4, ensure_ascii=False)
            
        print(f"[+] 分析完成！结果已保存至: {output_filename}")
    else:
        print(f"[!] 找不到文件: {target_file}")
