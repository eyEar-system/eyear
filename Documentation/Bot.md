# 🧠 دراسة مقارنة لاختيار نموذج LLM مفتوح المصدر لتطبيق دردشة على Google Colab (CPU)

### إعداد: أحمد محمد سعيد علي  
**السياق**: بحث عن نموذج شبيه ChatGPT لكن مفتوح المصدر ويقدر يشتغل على Google Colab CPU

---

## أولًا: أفضل 3 موديلات Open Source من نوع ChatGPT (LLMs)

### في فئات مختلفة:

| الفئة | الموديل | نبذة |
|--------|-------------|--------|
| الذكاء العالي | Mistral 7B Instruct | قوي في المحادثات والمنطق |
| الخفة والكفاءة | Phi-2 | الذكاء والسرعة مع حجم صغير |
| الحجم الأقل | TinyLLaMA 1.1B | لا يحتاج RAM عالي |

---

## السؤال: هل نقصد meta-llama/Llama-3.2-1B-Instruct؟

الإجابة: نعم. هذا هو النموذج الذي يمكن تشغيله في بيئات CPU مثل Google Colab.

---

## أنا باستخدم Google Colab (CPU Mode)

وعلى الأساس ده احتاجنا نموذج:
- صغير حجمًا
- متوافق مع transformers
- مينفع عليه LoRA لحقن النماذج لحقًا


---

## المقارنة النهائية:

| النموذج                  | الحجم   | الذكاء العام | الموارد | السرعة | اللغة العربية | نقاط قوة | نقاط ضعف |
|--------------------------|---------|------------------|----------------------|------------------|------------------------|---------------|--------------|
| LLaMA-3.2-1B-Instruct    | 1B      | جيد جدًا         | خفيف                 | متوسط             | مقبول                 | حديث – موجه Instruct | قليل التوسيق |
| Phi-2                    | 1.7B    | ممتاز في المنطق  | خفيف جدًا            | سريع              | ضعيف                  | ذكاء عالي | لا يفهم عربي |
| TinyLLaMA-1.1B           | 1.1B    | متوسط            | أخفهم                | سريع جدًا         | ضعيف جدًا             | ممتاز للتعلم | استجابات سطحية |

---

## نتيجة الاختيار:

**meta-llama/Llama-3.2-1B-Instruct** هو الموديل المختار للأسباب التالية:

1. مناسب لـ CPU
2. مبني على LLaMA 3.2 الحديث
3. مدرب على نمط Instruct
4. يقدم استجابات ذكية وموجهة

---

## التجربة الأولى

```python
!pip install transformers accelerate

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# تعريف النموذج
model_id = "meta-llama/Llama-3.2-1B-Instruct"

# تحميل النموذج
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32)
tokenizer = AutoTokenizer.from_pretrained(model_id)

prompt = "اشرح لي الذكاء الاصطناعي بطريقة مبسطة."
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=150)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

---

## استنتاج نهائي

من خلال هذه الدراسة تم الوصول إلى أن نموذج **LLaMA-3.2-1B-Instruct** هو الخيار الأمثل لمن يختار التطوير على Google Colab CPU بالمجان. ويمكن تطويره لحقًا لتدعيم اللغة العربية وتشغيله مع مشاريع مثل eyEar وغيرها.

