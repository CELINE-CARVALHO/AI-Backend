def summarize_text(text: str) -> str:
    """
    Mock AI summarization.
    This will be replaced with real LLM calls later.
    """

    if not text or len(text.strip()) == 0:
        return "No content to summarize."

    # Simple heuristic summary (safe placeholder)
    sentences = text.split(".")
    summary = sentences[0]

    if len(sentences) > 1:
        summary += "."

    return summary.strip()
