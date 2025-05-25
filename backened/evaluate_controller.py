import logging
from typing import Dict, Any, Optional


# Import your layers
from layers.uniqueness_checker import check_uniqueness
from layers.type_detector import detect_idea_type
from layers.metric_scorer import score_idea
from layers.summary_generator import generate_summary
from layers.leaderboard_manager import update_leaderboard

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def evaluate_idea_pipeline(text: str, user_id: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    End-to-end idea evaluation pipeline.
    
    Args:
        text: User's idea input
        user_id: Unique identifier for the user
        categories: Optional custom categories for idea typing
        
    Returns:
        Structured response with scores, metadata, and summary
    """
    try:
        # Default categories if none provided
        if categories is None:
            categories = ["Technology", "Social", "Art", "Science", "Business"]
        
        # --- Pipeline Execution ---
        # 1. Uniqueness Check
        uniqueness_result = check_uniqueness(text)
        if uniqueness_result.get("exists", True):
            logger.warning(f"Potential non-unique idea from user {user_id}")
        
        # 2. Type Detection
        idea_type = detect_idea_type(text, categories)
        
        # 3. Metric Scoring
        scores = score_idea(text, idea_type)
        
        # 4. Summary Generation
        summary = generate_summary(text, scores)
        
        # 5. Leaderboard Update
        leaderboard_entry = {
            "user_id": user_id,
            "idea": text,
            "type": idea_type,
            **scores
        }
        update_leaderboard(leaderboard_entry)
        
        # --- Response Formatting ---
        return {
            "status": "success",
            "data": {
                "scores": {
                    "originality": scores.get("originality", 0),
                    "creativity": scores.get("creativity", 0),
                    "critical_thinking": scores.get("critical_thinking", 0),
                    "total": sum(scores.values())
                },
                "uniqueness": {
                    "score": uniqueness_result.get("score", 0),
                    "reason": uniqueness_result.get("reason", "")
                },
                "type": idea_type,
                "summary": summary,
                "leaderboard_position": None  # Can add DB query later
            }
        }
        
    except Exception as e:
        logger.error(f"Pipeline failed for user {user_id}: {str(e)}")
        # For FastAPI:
        # raise HTTPException(status_code=500, detail="Idea evaluation failed")
        return {
            "status": "error",
            "error": str(e)
        }

# Example synchronous wrapper
def evaluate_idea_pipeline_sync(text: str, user_id: str) -> Dict[str, Any]:
    """Synchronous version for non-async contexts."""
    import asyncio
    return asyncio.run(evaluate_idea_pipeline(text, user_id))