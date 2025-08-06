"""
This module contains logic for risk analysis used in the movie
“Along Came Polly”. It defines a risk table with severity ratings and
risk scores for two individuals—Polly and Lisa—and provides functions
to compute weighted risk scores.

The goal is to mirror the simplistic risk calculation shown in the
film: each trait has a severity rating (1–10) that multiplies the
subject’s risk value. Higher totals indicate greater perceived risk.
"""

from typing import Dict, Tuple, List

# Define the risk factors, their severity multipliers, and individual scores
RISK_TABLE: List[Dict[str, object]] = [
    {
        "factor": "Spontaneous Behavior",
        "severity": 8,
        "Polly": 2,  # Polly is spontaneous (riskier)
        "Lisa": 2,
    },
    {
        "factor": "Career Stability",
        "severity": 7,
        "Polly": 2,  # Freelance/waitress jobs (high risk)
        "Lisa": 2,   # Corporate job (low risk)
    },
    {
        "factor": "Insurance/Health Coverage",
        "severity": 9,
        "Polly": 2,   # No insurance
        "Lisa": -2,   # Good coverage reduces risk
    },
    {
        "factor": "Lifestyle Stability",
        "severity": 6,
        "Polly": 4,   # Frequent moves and lack of plan
        "Lisa": -2,   # Predictable lifestyle
    },
    {
        "factor": "High School Compatibility",
        "severity": 3,
        "Polly": 0,
        "Lisa": 0,
    },
    {
        "factor": "Childhood Affection",
        "severity": 5,
        "Polly": 0,
        "Lisa": 1,  # Long history with Lisa reduces risk slightly
    },
    {
        "factor": "Food Allergy & IBS",
        "severity": 4,
        "Polly": 3,  # Polly’s IBS is a known issue
        "Lisa": 0,
    },
    {
        "factor": "Credit Score",
        "severity": 7,
        "Polly": 3,   # Lower credit/bad debt history
        "Lisa": -2,   # Good credit reduces risk
    },
    {
        "factor": "Family Health Background",
        "severity": 6,
        "Polly": 4,  # Unknown/unfavorable family medical history
        "Lisa": 0,   # Known and relatively safe
    },
]


def compute_weighted_risk(person: str) -> Tuple[float, List[Tuple[str, float]]]:
    """
    Compute the weighted risk score for a given person.

    Parameters
    ----------
    person : str
        Either "Polly" or "Lisa". This must match the keys in RISK_TABLE.

    Returns
    -------
    total_risk : float
        The summed weighted risk across all traits.
    details : List[Tuple[str, float]]
        A list of (factor, weighted_risk) tuples for inspection.
    """
    if person not in ("Polly", "Lisa"):
        raise ValueError("person must be 'Polly' or 'Lisa'")
    total_risk = 0.0
    details: List[Tuple[str, float]] = []
    for row in RISK_TABLE:
        severity = float(row["severity"])
        score = float(row[person])
        weighted = severity * score
        details.append((row["factor"], weighted))
        total_risk += weighted
    return total_risk, details


def compute_all_risks() -> Dict[str, Dict[str, object]]:
    """
    Compute risk scores for all people defined in RISK_TABLE.

    Returns
    -------
    results : Dict[str, Dict[str, object]]
        A mapping from person names to their total risk and per-factor details.
    """
    persons = [key for key in RISK_TABLE[0] if key not in ("factor", "severity")]
    results: Dict[str, Dict[str, object]] = {}
    for person in persons:
        total, details = compute_weighted_risk(person)
        results[person] = {"total": total, "details": details}
    return results