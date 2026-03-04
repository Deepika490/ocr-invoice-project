
def build_prompt(doc_type: str, invoice_text: str) -> str:
    return f"""
You are an advanced AI document extraction system.

DOCUMENT TYPE DETECTED: {doc_type}

Your task is to extract ALL structured information from the document text below.

STRICT RULES:

1. Return ONLY valid JSON.
2. Do NOT include explanations.
3. Do NOT include markdown.
4. Do NOT include comments.
5. Do NOT include extra text.
6. Do NOT wrap JSON in ``` blocks.
7. If a value is missing, return null.
8. Detect all fields dynamically.
9. Do NOT restrict to a fixed schema.
10. Preserve numbers exactly as written.
11. Extract everything possible including:
- Seller / Company details
- Buyer / Customer details
- Invoice metadata
- Line items (as array of objects)
- Taxes (GST, VAT, CGST, SGST, IGST, etc.)
- Subtotal, tax, discount, total
- Currency
- Payment terms
- Bank details
- Contact info (phone, email, website)
- Shipping details
- References
- Notes
12. Maintain logical hierarchy.
13. If multiple similar values exist, store as arrays.
14. Ensure numeric values are numbers (not strings).
15. Final payable total must be correctly identified.

If unsure, extract conservatively.
DO NOT hallucinate missing values.

Return ONLY pure JSON.

DOCUMENT TEXT:
{invoice_text}
"""