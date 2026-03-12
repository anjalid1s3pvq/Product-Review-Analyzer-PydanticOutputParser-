"""
Product Review Analyzer using LangChain's PydanticOutputParser
Extracts structured insights from product reviews using Pydantic model validation
"""

import os
from typing import Optional
from dotenv import load_dotenv
from langchain_core.pydantic_v1 import ValidationError
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from models import ReviewAnalysis

# Load environment variables from .env file
load_dotenv()


def create_review_analyzer():
    """
    Create a review analyzer chain using PydanticOutputParser and Groq API
    
    Returns:
        tuple: (chain, parser, prompt) for analysis workflow
        
    Raises:
        ValueError: If GROQ_API_KEY environment variable is not set
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable is not set. "
            "Please set it with your free Groq API key from https://console.groq.com"
        )
    
    # Initialize the language model
    llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=api_key,
    temperature=0.7
)
    
    # Initialize the Pydantic output parser
    parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)
    
    # Create the prompt template with format instructions
    prompt_template = """Analyze the following product review and extract structured insights.

Review:
{review}

{format_instructions}

Ensure your analysis is:
1. Accurate and based on the review content
2. Sentiment is one of: positive, negative, or neutral
3. Rating is an integer between 1 and 5
4. Key features are specific product features mentioned
5. Improvement suggestions are constructive recommendations from the review

Provide your response in the specified JSON format."""

    prompt = PromptTemplate(
        input_variables=["review"],
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Create the processing chain
    chain = prompt | llm | parser
    
    return chain, parser, prompt


def analyze_review(review: str, chain) -> Optional[ReviewAnalysis]:
    """
    Analyze a product review and extract structured insights
    
    Args:
        review (str): The product review text
        chain: The LLM processing chain
        
    Returns:
        Optional[ReviewAnalysis]: Validated review analysis or None if parsing fails
    """
    try:
        print(f"\n{'='*60}")
        print("ANALYZING REVIEW")
        print(f"{'='*60}")
        print(f"Review: {review}\n")
        
        # Process the review through the chain
        analysis = chain.invoke({"review": review})
        
        print("✓ Analysis completed successfully!\n")
        print("Parsed Analysis:")
        print(f"  Sentiment: {analysis.sentiment}")
        print(f"  Rating: {analysis.rating}/5")
        print(f"  Key Features: {', '.join(analysis.key_features) if analysis.key_features else 'None'}")
        print(f"  Improvement Suggestions: {', '.join(analysis.improvement_suggestions) if analysis.improvement_suggestions else 'None'}")
        print(f"{'='*60}\n")
        
        return analysis
        
    except ValidationError as e:
        print(f"\n✗ Validation Error: {e}")
        print("The LLM output did not match the expected schema.")
        return None
    except Exception as e:
        print(f"\n✗ Error analyzing review: {e}")
        print("Make sure your GOOGLE_API_KEY is set correctly.")
        return None


def main():
    """
    Main function to demonstrate the Product Review Analyzer
    """
    print("\n" + "="*60)
    print("PRODUCT REVIEW ANALYZER")
    print("Using Pydantic + PydanticOutputParser + Groq")
    print("="*60)
    
    # Initialize the analyzer
    try:
        chain, parser, prompt = create_review_analyzer()
        print("\n✓ Analyzer initialized successfully!\n")
    except ValueError as e:
        print(f"\n✗ Initialization Error: {e}")
        print("Get your free API key from: https://console.groq.com")
        return
    
    # Sample product reviews to analyze
    sample_reviews = [
        """This laptop is amazing! The build quality is excellent and the performance is blazing fast. 
        Battery life is decent for a workstation. The only downside is the keyboard could be more comfortable 
        for long typing sessions. Overall, highly recommended for professionals.""",
        
        """Terrible purchase. The product arrived broken and customer service was unhelpful. 
        The price is way too high for the quality offered. Don't waste your money on this.""",
        
        """It's okay. Does what it's supposed to do but nothing special. 
        Good value for the price. Could use better packaging to protect during shipping."""
    ]
    
    # Analyze each review
    results = []
    for i, review in enumerate(sample_reviews, 1):
        print(f"\n>>> Processing Review {i}/{len(sample_reviews)}")
        analysis = analyze_review(review, chain)
        if analysis:
            results.append(analysis)
    
    # Summary
    print("\n" + "="*60)
    print(f"SUMMARY: Successfully analyzed {len(results)}/{len(sample_reviews)} reviews")
    print("="*60)
    
    if results:
        avg_rating = sum(r.rating for r in results) / len(results)
        print(f"Average Rating: {avg_rating:.1f}/5")
        
        sentiment_counts = {}
        for result in results:
            sentiment_counts[result.sentiment] = sentiment_counts.get(result.sentiment, 0) + 1
        print(f"Sentiment Distribution: {sentiment_counts}")


if __name__ == "__main__":
    main()
