from app.rag_pipeline import ask_question


test_cases = [
    {
        "question": "What are the company's working hours?",
        "expected_keywords": [
            "Monday",
            "9:00 AM",
            "6:00 PM"
        ]
    },
    {
        "question": "How many annual leave days do employees get?",
        "expected_keywords": [
            "18",
            "annual leave"
        ]
    },
    {
        "question": "How many paid sick leave days do employees get?",
        "expected_keywords": [
            "10",
            "sick leave"
        ]
    },
    {
        "question": "How much is the annual learning allowance?",
        "expected_keywords": [
            "20,000"
        ]
    },
    {
        "question": "Within how many days must travel expense claims be submitted?",
        "expected_keywords": [
            "15",
            "calendar days"
        ]
    }
]


passed = 0
total = len(test_cases)


for test in test_cases:

    question = test["question"]
    expected_keywords = test["expected_keywords"]

    answer = ask_question(question)

    answer_lower = answer.lower()

    is_correct = all(
        keyword.lower() in answer_lower
        for keyword in expected_keywords
    )

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("ANSWER:", answer)

    if is_correct:
        print("RESULT: PASS")
        passed += 1
    else:
        print("RESULT: FAIL")


print("\n" + "=" * 70)
print("RAG EVALUATION")
print("=" * 70)

print("Passed:", passed)
print("Total:", total)

accuracy = (passed / total) * 100

print("Keyword-based answer match:", f"{accuracy:.2f}%")