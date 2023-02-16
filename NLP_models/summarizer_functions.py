from summarizer import Summarizer, TransformerSummarizer


def bert_extractive(text, n):
    model = Summarizer()
    result = model(text, num_sentences=n, min_length=60)
    full = ''.join(result)
    return full


def gpt_summarizer(text, n):
    GPT2_model = TransformerSummarizer(transformer_type="GPT2")
    full = ''.join(GPT2_model(text, min_length=60, num_sentences=n))
    return full


def xlnet_summarizer(text, n):
    model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
    full = ''.join(model(text, min_length=60, num_sentences=n))
    return full
