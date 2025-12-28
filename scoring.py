def score_candidate(resume_skills, job_skills, weights=None):
    """Score candidate based on job requirements."""
    if weights is None:
        weights = {'python': 0.3, 'leadership': 0.25, 'web': 0.25, 'data': 0.2}
    
    score = 0
    total_weight = 0
    for skill, job_weight in weights.items():
        resume_count = resume_skills.get(skill, 0)
        score += resume_count * job_weight * 10  # Scale to 0-10
        total_weight += job_weight
    
    return round(score / total_weight, 2)
