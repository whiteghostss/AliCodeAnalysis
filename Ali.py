import json
import os
import re
import javalang
import dashscope
from http import HTTPStatus
from flask import Flask, request, jsonify

# ================= 配置区域 =================
app = Flask(__name__)
# 设置环境变量
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")
# dashscope.api_key = "sk-..."

class JavaFormulaMapper:
    def __init__(self):
        # 建议使用 qwen-max 以获得最强的逻辑理解能力
        self.model = dashscope.Generation.Models.qwen_max

    def _is_numeric_type(self, type_name):
        if not type_name: return False
        numeric_types = {
            'int', 'long', 'double', 'float', 'short', 'byte',
            'Integer', 'Long', 'Double', 'Float', 'Short', 'Byte',
            'BigDecimal', 'BigInteger', 'Number'
        }
        return type_name in numeric_types

    def _get_method_code(self, file_content, start_line):
        lines = file_content.split('\n')
        current_line_idx = start_line - 1
        brace_balance = 0
        found_start = False
        method_lines = []
        for i in range(current_line_idx, len(lines)):
            line = lines[i]
            method_lines.append(line)
            brace_balance += (line.count('{') - line.count('}'))
            if line.count('{') > 0: found_start = True
            if found_start and brace_balance == 0: break
        return "\n".join(method_lines)

    def _parse_ast(self, java_code):
        """解析 AST，重点提取：变量、方法调用、返回类型"""
        try:
            tree = javalang.parse.parse(java_code)
        except javalang.parser.JavaSyntaxError as e:
            return None, f"Syntax Error: {e}"

        methods_info = []

        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            method_info = {
                'method_name': node.name,
                'comment': node.documentation if node.documentation else "No comment",
                'return_type': node.return_type.name if node.return_type else "void"
            }
            
            # 1. 提取所有可能的候选变量 (参数 + 局部变量)
            variables = []
            if node.parameters:
                for param in node.parameters:
                    variables.append(param.name) # 不再过滤类型，防止遗漏对象类型
            
            if node.body:
                for path, child in node.filter(javalang.tree.LocalVariableDeclaration):
                    for declarator in child.declarators:
                        variables.append(declarator.name)

            method_info['variables'] = list(set(variables))
            
            # 2. 提取方法调用字符串作为"表达式候选"
            method_calls = []
            if node.body:
                for path, child in node.filter(javalang.tree.MethodInvocation):
                    prefix = (child.qualifier + ".") if child.qualifier else ""
                    # 尝试重组参数部分，虽然不完美但能给LLM提示
                    args = "..." if child.arguments else ""
                    call_str = f"{prefix}{child.member}({args})"
                    method_calls.append(call_str)
            
            method_info['method_calls'] = list(set(method_calls))

            if node.position:
                method_info['code'] = self._get_method_code(java_code, node.position.line)
            else:
                method_info['code'] = "// Extraction failed"
            
            methods_info.append(method_info)

        if not methods_info:
            return None, "No methods found"
        
        return methods_info, None

    def _call_llm(self, method_info):
        """
        核心 Prompt 更新：
        1. 强调公式左右值区分。
        2. 强调变量 > 表达式 > Null 的优先级。
        3. 修复 LHS 被错误映射到 RHS 变量的问题。
        """
        prompt = f"""
        你是一个代码语义分析专家。请分析Java代码并将其映射到数学公式参数。

        ### 输入上下文
        1. **代码**:
        ```java
        {method_info['code']}
        ```
        2. **公式**: {method_info['comment']}
        3. **可用变量**: {json.dumps(method_info['variables'])}
        4. **涉及调用**: {json.dumps(method_info['method_calls'])}

        ### 核心任务
        提取公式中的**所有符号**（包括等号左边的结果和右边的参数），并找到代码中对应的实现。

        ### 匹配优先级规则 (至关重要)
        对于公式中的每一个参数 Key：
        
        **优先级 1: 语义对应的变量 (最高)**
        - 如果代码中有变量名与Key语义一致（如 `m` -> `mass`，`a` -> `a`），必须输出**变量名**。
        - **注意**: 即使该变量是通过复杂计算得来的，只要有变量名，就优先用变量名。

        **优先级 2: 函数调用与表达式**
        - 如果没有对应的变量，但代码中通过函数调用直接计算了该参数。
        - 例如公式 `term` 对应代码 `b.sqr(c)`，且没有变量 `term`，则 Value 输出 **"b.sqr(c)"** (保留完整调用)。
        - 例如公式 `R` (结果) 对应 `return` 语句后的表达式，如果代码是 `return sum(...)`，则 Value 输出 **"sum(...)"**。

        **优先级 3: 常量**
        - 如果代码中写死数值（如 `9.8`），Value 输出该数值。

        **优先级 4: Null**
        - 如果代码中完全找不到对应的实现，Value 必须为 **null**。
        - **严禁凑数**：绝对不要把不相关的变量填进去。

        ### 特殊纠错规则
        1. **区分左右值**: 公式等号左边的符号（如 `R = ...` 中的 `R`）是**结果**。它通常对应 `return` 语句。如果代码没有定义 `R` 变量而是直接 `return`，请将 `R` 映射为 `return` 后的表达式，或者 `null`（如果无法提取表达式），**绝对不能映射到输入参数（如 base）上**。
        2. **全量输出**: 输出 JSON 的 Key 必须包含公式中出现的所有字母符号。

        ### 输出示例
        公式: R = base + term
        代码: return sum(base, calc(freq));
        输出:
        {{
            "R": "sum(base, calc(freq))",   // 对应 return 的整体结果
            "base": "base",                 // 对应输入变量
            "term": "calc(freq)"            // 对应嵌套函数调用
        }}
        
        请只输出 JSON。
        """

        messages = [{'role': 'system', 'content': '你是一个只输出JSON的助手。'}, {'role': 'user', 'content': prompt}]

        try:
            response = dashscope.Generation.call(self.model, messages=messages, result_format='message')
            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0].message.content.strip()
                # 清洗 Markdown
                if content.startswith("```"):
                    content = re.sub(r'^```json\s*', '', content)
                    content = re.sub(r'\s*```$', '', content)
                
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    return json.loads(match.group())
                return {"error": "No JSON found", "raw": content}
            return {"error": f"API Error: {response.code}"}
        except Exception as e:
            return {"error": str(e)}

    def analyze(self, java_code):
        """
        统一入口：接收 Java 代码字符串，返回分析结果列表
        """
        # 1. 解析 AST
        methods_info, err = self._parse_ast(java_code)
        if err:
            return None, err

        # 2. 遍历方法调用 LLM
        results = []
        for info in methods_info:
            mapping = self._call_llm(info)
            results.append({
                "method_name": info['method_name'],
                "mapping": mapping
            })
        return results, None

# ================= Flask 接口定义 =================

mapper = JavaFormulaMapper()

@app.route('/analyze', methods=['POST'])
def handle_analyze():
    """
    统一接口：处理 JSON 字符串或文件上传
    """
    java_code = ""
    try:
        # 1. 尝试获取代码内容
        if request.is_json:
            data = request.get_json()
            java_code = data.get('code', '')
        elif 'file' in request.files:
            uploaded_file = request.files['file']
            java_code = uploaded_file.read().decode('utf-8')

        # 2. 校验
        if not java_code.strip():
            return jsonify({"success": False, "error": "No code provided (JSON 'code' or File 'file')"}), 400
        
        # 3. 执行分析
        results, err = mapper.analyze(java_code)
        
        if err:
            return jsonify({"success": False, "error": err}), 422
            
        return jsonify({"success": True, "data": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# ================= 主程序 =================

if __name__ == "__main__":
    print("[*] 启动 Flask API 服务...")
    app.run(host='0.0.0.0', port=5000)
