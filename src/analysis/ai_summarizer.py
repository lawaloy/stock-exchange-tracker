"""
Stock Exchange Tracker - AI Summarizer Module

Uses OpenAI API to generate natural language summaries of market data.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv
from ..core.logger import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger("ai_summarizer")


class AISummarizer:
    """Generates AI-powered summaries of stock market data."""
    
    def __init__(self):
        """Initialize the AI summarizer with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.enabled = self.api_key is not None
        
        if not self.enabled:
            logger.info("OpenAI API key not found. Using demo summary mode.")
            logger.info("To enable AI summaries: Set OPENAI_API_KEY environment variable or add to .env file")
    
    def generate_demo_summary(self, analysis: Dict, exchange_comparison: Dict) -> str:
        """
        Generate a simple template-based summary (demo mode, no API needed).
        
        Args:
            analysis: Analysis dictionary from StockAnalyzer
            exchange_comparison: Exchange comparison dictionary
        
        Returns:
            Generated summary text
        """
        summary_data = analysis.get("summary", {})
        top_gainers = analysis.get("top_gainers", [])[:2]
        top_losers = analysis.get("top_losers", [])[:2]
        
        # Build a simple summary
        summary_parts = []
        
        # Overall market sentiment
        gainers = summary_data.get('gainers', 0)
        losers = summary_data.get('losers', 0)
        avg_change = summary_data.get('average_change_percent', 0)
        
        if gainers > losers:
            sentiment = "positive"
        elif losers > gainers:
            sentiment = "negative"
        else:
            sentiment = "mixed"
        
        summary_parts.append(f"Today's market showed {sentiment} sentiment with {gainers} gainers and {losers} losers, averaging {avg_change:.2f}% change overall.")
        
        # Highlight top movers
        if top_gainers:
            top_gainer = top_gainers[0]
            summary_parts.append(f"{top_gainer['symbol']} led gains with a {top_gainer['change_percent']:.2f}% increase.")
        
        if top_losers:
            top_loser = top_losers[0]
            summary_parts.append(f"{top_loser['symbol']} declined {abs(top_loser['change_percent']):.2f}%, marking the largest drop.")
        
        # Exchange performance
        best_exchange = max(exchange_comparison.items(), key=lambda x: x[1].get('average_change_percent', 0), default=None)
        if best_exchange:
            exchange_name, stats = best_exchange
            summary_parts.append(f"The {exchange_name} exchange performed best with an average {stats['average_change_percent']:.2f}% gain.")
        
        return " ".join(summary_parts)
    
    def generate_summary(self, analysis: Dict, exchange_comparison: Dict) -> Optional[str]:
        """
        Generate a natural language summary of the market data.
        
        Args:
            analysis: Analysis dictionary from StockAnalyzer
            exchange_comparison: Exchange comparison dictionary
        
        Returns:
            Generated summary text or None if API key not available
        """
        if not self.enabled:
            # Return demo summary instead of None
            return self.generate_demo_summary(analysis, exchange_comparison)
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Prepare data for the prompt
            summary_data = analysis.get("summary", {})
            top_gainers = analysis.get("top_gainers", [])[:3]  # Top 3
            top_losers = analysis.get("top_losers", [])[:3]  # Top 3
            
            # Build prompt
            prompt = f"""Write a brief, professional market summary (2-3 sentences) based on this stock market data:

Date: {analysis.get('date', 'Today')}
Total Stocks: {summary_data.get('total_stocks', 0)}
Gainers: {summary_data.get('gainers', 0)}, Losers: {summary_data.get('losers', 0)}
Average Change: {summary_data.get('average_change_percent', 0):.2f}%

Top Gainers:
"""
            for stock in top_gainers:
                prompt += f"- {stock['symbol']} ({stock.get('name', 'N/A')}): +{stock['change_percent']:.2f}%\n"
            
            prompt += "\nTop Losers:\n"
            for stock in top_losers:
                prompt += f"- {stock['symbol']} ({stock.get('name', 'N/A')}): {stock['change_percent']:.2f}%\n"
            
            prompt += "\nExchange Performance:\n"
            for exchange, stats in list(exchange_comparison.items())[:3]:
                prompt += f"- {exchange}: Avg {stats['average_change_percent']:.2f}% ({stats['gainers']} gainers, {stats['losers']} losers)\n"
            
            prompt += "\nWrite a concise, informative summary in a professional tone."
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial market analyst. Write clear, concise market summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            logger.warning("OpenAI package not installed. Install with: pip install openai")
            return None
        except Exception as e:
            logger.warning(f"Failed to generate AI summary: {str(e)}")
            return None

