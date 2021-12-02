from transformers import GPT2LMHeadModel, GPT2Tokenizer

class TextGenerator:
    __paragraph_max_len = 100
    __tokenizer = None
    __model = None
    context_suffix = ''

    @staticmethod
    def __get_tokenizer():
        if not TextGenerator.__tokenizer:
            TextGenerator.__tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        return TextGenerator.__tokenizer

    @staticmethod
    def __get_model():
        if not TextGenerator.__model:
            TextGenerator.__model = GPT2LMHeadModel.from_pretrained('gpt2')
        return TextGenerator.__model

    @staticmethod
    def ready(context_suffix = ''):
        TextGenerator.__get_model()
        TextGenerator.__get_tokenizer()
        TextGenerator.context_suffix = context_suffix

    @staticmethod
    def generate(context):
        text = context + TextGenerator.context_suffix
        inputs = TextGenerator.__get_tokenizer().encode(text, return_tensors='pt')
        outputs = TextGenerator.__get_model().generate(
            inputs, max_length=len(inputs[0]) + TextGenerator.__paragraph_max_len, do_sample=True, top_k=50
        )
        generated_text = TextGenerator.__get_tokenizer().decode(outputs[0], skip_special_tokens=True)[len(text):]
        return generated_text[:len(generated_text) - generated_text[::-1].index('.')].replace('\n\n', ' ').replace('\n', ' ')

