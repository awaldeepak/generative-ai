import tiktoken as ttk

encoding_model = ttk.encoding_for_model("gpt-4o")
text = "I am Deepak!"

encoded_text = encoding_model.encode(text)
print(encoded_text)