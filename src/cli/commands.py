"""
Stock Tracker CLI - Command-Line Interface

This module provides the CLI presentation layer for the Stock Exchange Tracker.
It uses the core workflow and formats output for console display.
"""

from ..workflows.tracker import StockTrackerWorkflow
from ..core.logger import setup_logger
from datetime import datetime
import sys

# Set up logger
logger = setup_logger()


def display_results(result: dict):
    """
    Display workflow results in CLI format.
    
    Args:
        result: Workflow result dictionary
    """
    if not result.get("success"):
        logger.error(f"Workflow failed: {result.get('error', 'Unknown error')}")
        return
    
    analysis = result.get("analysis", {})
    index_comparison = result.get("index_comparison", {})
    ai_summary = result.get("ai_summary")
    metadata = result.get("metadata", {})
    
    # Header
    logger.info("=" * 60)
    logger.info("Daily Market Summary")
    logger.info("=" * 60)
    
    # Display AI summary if available
    if ai_summary:
        logger.info("\n[AI Market Summary]")
        logger.info("-" * 60)
        logger.info(ai_summary)
        logger.info("-" * 60)
        logger.info("")
    
    # Summary statistics
    if "summary" in analysis:
        summary = analysis["summary"]
        logger.info(f"Date: {metadata.get('date', datetime.now().date())}")
        logger.info(f"Total Stocks Tracked: {summary.get('total_stocks', 0)}")
        logger.info(f"Gainers: {summary.get('gainers', 0)}")
        logger.info(f"Losers: {summary.get('losers', 0)}")
        logger.info(f"Unchanged: {summary.get('unchanged', 0)}")
        logger.info(f"Average Change: {summary.get('average_change_percent', 0):.2f}%")
        logger.info("")
    
    # Top gainers
    if "top_gainers" in analysis and analysis["top_gainers"]:
        logger.info("Top 5 Gainers:")
        for i, stock in enumerate(analysis["top_gainers"], 1):
            logger.info(f"  {i}. {stock['symbol']} ({stock.get('name', 'N/A')}): "
                  f"+{stock['change_percent']:.2f}% @ ${stock['close']:.2f}")
        logger.info("")
    
    # Top losers
    if "top_losers" in analysis and analysis["top_losers"]:
        logger.info("Top 5 Losers:")
        for i, stock in enumerate(analysis["top_losers"], 1):
            logger.info(f"  {i}. {stock['symbol']} ({stock.get('name', 'N/A')}): "
                  f"{stock['change_percent']:.2f}% @ ${stock['close']:.2f}")
        logger.info("")
    
    # Index comparison
    if index_comparison:
        logger.info("Index Performance:")
        for index_name, stats in index_comparison.items():
            logger.info(f"  {index_name}:")
            logger.info(f"    Stocks: {stats['stock_count']}")
            logger.info(f"    Avg Change: {stats['average_change_percent']:.2f}%")
            logger.info(f"    Gainers: {stats['gainers']} | Losers: {stats['losers']}")
        logger.info("")
    
    # File paths
    file_paths = result.get("file_paths", {})
    if file_paths.get("data"):
        logger.info(f"Data saved to: {file_paths['data']}")
    if file_paths.get("summary"):
        logger.info(f"Summary saved to: {file_paths['summary']}")
    
    logger.info("=" * 60)
    logger.info("Daily tracking complete!")
    logger.info("=" * 60)


def main():
    """CLI entry point for stock tracker."""
    logger.info("=" * 60)
    logger.info("Stock Exchange Tracker - Daily Data Collection")
    logger.info("=" * 60)
    logger.debug("Starting CLI interface")
    
    try:
        # Create and run workflow
        workflow = StockTrackerWorkflow()
        result = workflow.run(use_screener=True)
        
        # Display results
        display_results(result)
        
        logger.debug("CLI completed successfully")
        
    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Exiting.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

