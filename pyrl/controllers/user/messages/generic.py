from __future__ import annotations

def article(subject: str) -> str:
    return f"{get_article(subject)} {subject}"

def get_article(subject: str) -> str:
    if not subject:
        return ""
    start_vowel_sounds = "AEIOUÅÄÖaeiouåäö"
    if subject[0] in start_vowel_sounds:
        return "an"
    return "a"
