from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

print("Loading LaMini-Flan-T5 model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("Model loaded successfully!")


def explain_concept(topic):

    prompt = f"""
Explain the following concept in simple language for a college student.

Concept: {topic}

Include:
1. Simple definition
2. Key points
3. Real-world example
4. Short conclusion
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        do_sample=False
    )

    explanation = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return explanation


if __name__ == "__main__":

    explanation = explain_concept("Artificial Intelligence")

    print("\nEduGenie Concept Explanation:")
    print(explanation)