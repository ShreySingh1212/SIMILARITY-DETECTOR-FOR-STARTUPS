"""
AI-powered gap analysis using Groq (Llama 3)
"""
from groq import Groq
from app.config import settings
from app.schemas import GapAnalysisResult
import json
import logging

logger = logging.getLogger(__name__)


def analyze_gaps(user_idea: str, similar_startups: list) -> GapAnalysisResult:
    """
    Use Groq LLM to analyze gaps between user's idea and existing startups.
    Returns structured analysis with strengths, weaknesses, differentiators.
    """
    if not settings.groq_api_key:
        logger.warning("No Groq API key configured. Returning default analysis.")
        return _default_analysis()

    try:
        client = Groq(api_key=settings.groq_api_key)

        # Build context from similar startups
        startup_context = ""
        for i, startup in enumerate(similar_startups[:5], 1):
            startup_context += f"\n{i}. **{startup.name}** ({startup.category})\n"
            startup_context += f"   Description: {startup.description}\n"
            startup_context += f"   Similarity: {startup.similarity_percentage}%\n"
            if startup.funding_stage:
                startup_context += f"   Funding: {startup.funding_stage}\n"
            if startup.status:
                startup_context += f"   Status: {startup.status}\n"

        prompt = f"""You are a startup analyst. Analyze this startup idea compared to existing similar startups.

**User's Startup Idea:**
{user_idea}

**Most Similar Existing Startups:**
{startup_context}

Provide a JSON response with this exact structure (no markdown, just raw JSON):
{{
    "summary": "A 2-3 sentence executive summary of the competitive landscape",
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "weaknesses": ["weakness/risk 1", "weakness/risk 2", "weakness/risk 3"],
    "differentiators": ["what makes this idea different 1", "differentiator 2", "differentiator 3"],
    "suggestions": ["actionable suggestion 1", "suggestion 2", "suggestion 3"],
    "market_saturation": "low/medium/high"
}}

Be specific, actionable, and realistic. Base your analysis on the actual competitors shown above."""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
        )

        content = response.choices[0].message.content.strip()

        # Try to parse JSON from the response
        # Handle cases where LLM wraps in ```json ... ```
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        data = json.loads(content)

        return GapAnalysisResult(
            summary=data.get("summary", "Analysis completed."),
            strengths=data.get("strengths", [])[:5],
            weaknesses=data.get("weaknesses", [])[:5],
            differentiators=data.get("differentiators", [])[:5],
            suggestions=data.get("suggestions", [])[:5],
            market_saturation=data.get("market_saturation", "medium")
        )

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response as JSON: {e}")
        return _default_analysis()
    except Exception as e:
        logger.error(f"Gap analysis failed: {e}")
        return _default_analysis()


def _default_analysis() -> GapAnalysisResult:
    """Fallback analysis when LLM is unavailable"""
    return GapAnalysisResult(
        summary="AI gap analysis is currently unavailable. Review the similar startups below to manually assess your competitive landscape.",
        strengths=["Your idea has been submitted for analysis"],
        weaknesses=["Unable to perform detailed competitive analysis at this time"],
        differentiators=["Review the similarity scores to understand your positioning"],
        suggestions=["Compare your idea with the listed startups manually", "Focus on unique value propositions"],
        market_saturation="medium"
    )
