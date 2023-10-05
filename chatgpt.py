import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate 


class InvoiceGPT(object):
    
    def __init__(self, temperature = 0 , model_name = "gpt-3.5-turbo-16k"):
        self.name = 'InvoiceGPT'
        self.model_name = model_name
        self.temperature = temperature

    def create_prompt_template(self, input_variables, validate_template):
    
        template = """以下の[テキスト]を[制約]に従って[出力フォーマット]で出力してください。
        [制約]
        * 出力は[出力フォーマット]のみ出力してください。
        * [出力フォーマット]以外の余計な文章は出力しないでください。
        [出力フォーマット]
        {sample_json} 
        [テキスト] {ocr_text}"""
        
        prompt_template = PromptTemplate(
                            input_variables   = input_variables,   # 入力変数 
                            template          = template,          # テンプレート
                            validate_template = validate_template, # 入力変数とテンプレートの検証有無
                        )
        return prompt_template

    def create_llm(self, model_name, temperature = 0, n = 1):
        LLM = OpenAI(
            model_name        = model_name,  # OpenAIモデル名
            temperature       = temperature, # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
            n                 = n,           # いくつの返答を生成するか           
        )
        return LLM

    def process_invoice_ocr(self, ocr_text: str) -> str:
        # ====================================================================================
        # Prompt Templateを適用しLLM実行
        # ====================================================================================
        input_variables=["ocr_text", "sample_json"]
        prompt_template = self.create_prompt_template(input_variables, validate_template=True)
        # プロンプトテンプレートにフォーマット適用
        sample_json = self.get_sample_output_format()
        prompt_format = prompt_template.format(ocr_text=ocr_text, sample_json=sample_json)
        llm = self.create_llm(self.model_name, self.temperature)
        # LLMにPrompt Templateを指定
        response = llm(prompt_format)

        # 出力
        return response

    def get_sample_output_format(self):
        sample_json = json.dumps("{ '明細': [{  '適用': 'テスト', '数量': 2,'単価': 1000, '合計': 2000}],'合計金額': 10000,'振込期限': '2023/10/04','振込先':'A銀行 B支店' }", ensure_ascii=False)
        return sample_json
