import re
import difflib

def has_ocr_tags(text):
    """Check if text contains <ocr> </ocr> tags"""
    return 1 if re.search(r'<ocr>.*?</ocr>', text, re.DOTALL) is not None else 0

def has_think_tags(text):
    """Check if text contains <think> </think> tags"""
    return 1 if re.search(r'<think>.*?</think>', text, re.DOTALL) is not None else 0

def has_final_answer_tags(text):
    """Check if text contains <final_answer> </final_answer> tags"""
    return 1 if re.search(r'<final_answer>.*?</final_answer>', text, re.DOTALL) is not None else 0

def reward_ocr_accuracy(ocr_ground_truth, answer_ocr):
    """Compare OCR ground truth with model's OCR output"""
    if not ocr_ground_truth or not answer_ocr:
        return 0
    
    # Extract OCR text if it's in tags
    if '<ocr>' in answer_ocr and '</ocr>' in answer_ocr:
        answer_ocr = re.search(r'<ocr>(.*?)</ocr>', answer_ocr, re.DOTALL).group(1).strip()
    
    # Calculate similarity using difflib
    matcher = difflib.SequenceMatcher(None, ocr_ground_truth, answer_ocr)
    similarity = matcher.ratio()
    return similarity

def reward_exact_match(ground_truth, model_answer):
    """Check if ground truth exactly matches model answer"""
    return 1 if ground_truth.strip() == model_answer.strip() else 0


def compute_train_rewards(prompts, completions, ocr_ground_truth=None, answer_ground_truth=None, **kwargs):
    assignment = prompts[0][0]["content"].split(":")[1].strip()
    responses = [completion[0]["content"] for completion in completions]
    extracted_responses = [
        r.strip()
        for r in responses
    ]
    scores = []
    for response in extracted_responses:
        score = 0
        score += has_think_tags(response)
        if ocr_ground_truth and has_ocr_tags(response):
            score += reward_ocr_accuracy(ocr_ground_truth, response)
        if answer_ground_truth and has_final_answer_tags(response):
            final_answer = re.search(r'<final_answer>(.*?)</final_answer>', response, re.DOTALL)
            if final_answer:
                final_answer = final_answer.group(1).strip()
                score += reward_exact_match(answer_ground_truth, final_answer)
        scores.append(score)
    return scores