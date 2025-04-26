"""
Risk assessment module for legal documents
Uses pattern matching and keyword analysis to identify potential risk levels
"""
import re

def assess_risk_level(text):
    """
    Assess risk level of a legal document based on keyword and pattern analysis
    
    Args:
        text (str): Legal document text
        
    Returns:
        tuple: (risk_level, risk_factors) 
               where risk_level is 'Low', 'Medium', or 'High'
               and risk_factors is a list of identified risk factors
    """
    if not text:
        return "Unknown", []
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Define risk keywords and patterns
    high_risk_terms = [
        "terminate", "termination", "damages", "liability", "unlimited liability",
        "indemnity", "indemnification", "lawsuit", "litigation", "arbitration",
        "penalty", "penalties", "punitive", "confidential information", "trade secret",
        "intellectual property", "data breach", "security breach", "dispute", "legal action",
        "non-compliance", "breach of contract", "violation", "revoke", "revocation",
        "void", "compensation", "fine", "legal proceedings", "injunction",
        "liquidated damages", "default", "claim", "sue", "court proceeding"
    ]
    
    medium_risk_terms = [
        "amendment", "modify", "cancellation", "disclaim", "disclaimer",
        "warranty", "guarantee", "limited liability", "insurance", "regulation",
        "compliance", "policy", "governance", "confidentiality", "non-disclosure",
        "exclusion", "restriction", "obligation", "compliance", "right to",
        "subject to", "approval", "permission", "consent", "notification",
        "privacy", "personal data", "protection", "ownership", "title"
    ]
    
    low_risk_terms = [
        "agreement", "contract", "term", "condition", "service", "product",
        "payment", "fee", "renewal", "extension", "standard", "guideline",
        "notice", "communication", "cooperation", "support", "maintenance",
        "schedule", "delivery", "acceptance", "process", "procedure"
    ]
    
    # Count occurrences of risk terms
    high_risk_count = sum(text_lower.count(term) for term in high_risk_terms)
    medium_risk_count = sum(text_lower.count(term) for term in medium_risk_terms)
    low_risk_count = sum(text_lower.count(term) for term in low_risk_terms)
    
    # Check for specific high-risk patterns
    high_risk_patterns = [
        r"termin.*\s.{0,20}(immediately|without.*notice)",
        r"disclaim.*\s.{0,30}(all|any).{0,30}(warrant|liab)",
        r"indemnif.*\s.{0,50}(all|any).{0,50}(loss|damage|claim)",
        r"confiden.*\s.{0,50}(perpet|indef|surviv)",
        r"non.{0,3}compl.*\s.{0,30}(termin|penal)",
        r"damage.{0,20}exceed",
        r"liab.*\s.{0,30}(unlimit|not.{0,10}limit)",
    ]
    
    high_risk_pattern_matches = [
        bool(re.search(pattern, text_lower)) 
        for pattern in high_risk_patterns
    ]
    
    # Check for document length - longer documents typically contain more complex legal terms
    doc_length = len(text)
    
    # Calculate risk factors
    risk_factors = []
    
    # Add high-risk terms found
    for term in high_risk_terms:
        if term in text_lower:
            occurrences = text_lower.count(term)
            if occurrences > 0:
                risk_factors.append(f"High-risk term: '{term.capitalize()}' found {occurrences} times")
    
    # Add medium-risk terms if they appear more than twice
    for term in medium_risk_terms:
        occurrences = text_lower.count(term)
        if occurrences > 2:
            risk_factors.append(f"Medium-risk term: '{term.capitalize()}' found {occurrences} times")
    
    # Add pattern-based risks
    for i, matched in enumerate(high_risk_pattern_matches):
        if matched:
            pattern_desc = {
                0: "Immediate termination clause",
                1: "Broad warranty disclaimer",
                2: "Broad indemnification requirement",
                3: "Perpetual confidentiality clause",
                4: "Non-compliance penalties",
                5: "Unlimited damages clause",
                6: "Unlimited liability clause"
            }.get(i, "Complex legal pattern")
            risk_factors.append(f"High-risk pattern: {pattern_desc}")
    
    # Determine overall risk level based on multiple factors
    # Calculate risk score based on term frequency and patterns
    risk_score = (high_risk_count * 3) + sum(high_risk_pattern_matches) * 5 + (medium_risk_count * 1) - (low_risk_count * 0.5)
    
    # Adjust for document length
    if doc_length > 10000:  # Long documents
        risk_score += 5
    elif doc_length > 5000:  # Medium-length documents
        risk_score += 2
        
    # Determine risk level based on score
    if risk_score > 20 or any(high_risk_pattern_matches) or high_risk_count > 10:
        risk_level = "High"
    elif risk_score > 10 or medium_risk_count > 15 or high_risk_count > 5:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Limit risk factors to top 5 most significant
    risk_factors = sorted(risk_factors, key=lambda x: "High-risk" in x and 2 or "Medium-risk" in x and 1 or 0, reverse=True)
    risk_factors = risk_factors[:5] if len(risk_factors) > 5 else risk_factors
    
    return risk_level, risk_factors


def get_risk_color(risk_level):
    """
    Get appropriate color for a risk level
    
    Args:
        risk_level (str): 'Low', 'Medium', or 'High'
        
    Returns:
        str: CSS color string
    """
    colors = {
        "High": "#FF4B4B",     # Red
        "Medium": "#FFA726",   # Orange
        "Low": "#4CAF50",      # Green
        "Unknown": "#9E9E9E"   # Gray
    }
    return colors.get(risk_level, colors["Unknown"])