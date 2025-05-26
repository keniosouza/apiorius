# utils/validation.py

import re
import html


class InputSanitizer:

    @staticmethod
    def clean_text(text: str) -> str:
        """Trim spaces, escape HTML entities, collapse multiple spaces."""
        text = text.strip()
        text = html.escape(text)
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if email has a valid structure"""
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

    @staticmethod
    def has_script(text: str) -> bool:
        """Detect basic XSS attempts"""
        return "<script" in text.lower() or "javascript:" in text.lower()

    @staticmethod
    def is_safe(text: str) -> bool:
        """Detect common XSS/SQL injection characters or patterns"""
        blacklist = ["<script", "javascript:", "--", ";", "/*", "*/", "@@", "char(", "nchar(", "varchar(", "alter", "drop", "exec"]
        text_lower = text.lower()
        return not any(p in text_lower for p in blacklist)
