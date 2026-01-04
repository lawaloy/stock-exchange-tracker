"""
stock_tracker — canonical CLI for Stock Exchange Tracker

This module provides the main CLI workflow and is exposed as the
`stock-tracker` console script.
"""

from ..services.data_fetcher import StockDataFetcher
from ..storage.data_storage import DataStorage
from ..analysis.analyzer import StockAnalyzer
from ..analysis.ai_summarizer import AISummarizer
from ..core.logger import setup_logger
from ..core.config import get_indices_to_track
from datetime import datetime
import json
import pandas as pd
import sys

# Set up logger
logger = setup_logger()


def main():
    """Console entry point that runs the daily tracking workflow."""
    logger.info("=" * 60)
    logger.info("Stock Exchange Tracker - Daily Data Collection")
    logger.info("=" * 60)
    logger.debug("Starting daily tracking workflow")

    try:
        # Initialize components
        logger.debug("Initializing components")
        fetcher = StockDataFetcher()
        storage = DataStorage()
        analyzer = StockAnalyzer()
        ai_summarizer = AISummarizer()

        # Step 1: Fetch data from all configured indices (with screening)
        indices_to_track = get_indices_to_track()
        logger.info(f"Step 1: Fetching data from indices: {', '.join(indices_to_track)}")
        logger.info("-" * 60)
        
        # Screener is enabled by default for trading focus - finds best stocks automatically
        use_screener = True
        logger.info(f"Stock screener enabled: {use_screener} (finds best trading candidates)")
        
        all_index_data = fetcher.fetch_all_indices(use_screener=use_screener)

        # Combine all data into a single list
        all_data = []
        for index_name, data in all_index_data.items():
            all_data.extend(data)
            logger.info(f"  {index_name}: {len(data)} stocks fetched")
            logger.debug(f"Fetched {len(data)} stocks from {index_name}")

        logger.info(f"Total stocks fetched: {len(all_data)}")
        logger.debug(f"Total data points: {len(all_data)}")

        if not all_data:
            logger.warning("No data was fetched. Exiting.")
            return

        # Step 2: Save data to CSV
        logger.info("Step 2: Saving data to CSV...")
        logger.info("-" * 60)
        file_path = storage.save_daily_data(all_data)
        if file_path:
            logger.info(f"  Data saved to: {file_path}")
            logger.debug(f"CSV file saved at: {file_path}")
        else:
            logger.error("Failed to save data")
        logger.info("")

        # Step 3: Analyze data
        logger.info("Step 3: Analyzing data...")
        logger.info("-" * 60)
        analysis = analyzer.analyze_daily_data(all_data)
        # Convert index_data format for comparison (use index_name instead of exchange_code)
        index_comparison = {}
        for index_name, data in all_index_data.items():
            if data:
                df = pd.DataFrame(data)
                avg_change = df['change_percent'].mean()
                total_volume = df['volume'].sum()
                index_comparison[index_name] = {
                    'stock_count': len(df),
                    'average_change_percent': round(avg_change, 2),
                    'total_volume': int(total_volume),
                    'gainers': len(df[df['change_percent'] > 0]),
                    'losers': len(df[df['change_percent'] < 0]),
                }
        exchange_comparison = index_comparison  # Keep variable name for compatibility
        logger.debug("Data analysis completed")

        # Generate AI summary (or demo summary if no API key)
        logger.info("  Generating market summary...")
        ai_summary = ai_summarizer.generate_summary(analysis, exchange_comparison)
        if ai_summary:
            if ai_summarizer.enabled:
                logger.info("  AI summary generated")
                logger.debug("AI summary generated using OpenAI API")
            else:
                logger.info("  Demo summary generated")
                logger.debug("Demo summary generated (no API key)")
        logger.info("")

        # Save summary
        summary_data = {
            "analysis": analysis,
            "exchange_comparison": exchange_comparison
        }
        if ai_summary:
            summary_data["ai_summary"] = ai_summary
        summary_path = storage.save_summary(summary_data)
        if summary_path:
            logger.info(f"  Summary saved to: {summary_path}")
            logger.debug(f"Summary JSON saved at: {summary_path}")
        logger.info("")

        # Step 4: Display results
        logger.info("Step 4: Daily Market Summary")
        logger.info("=" * 60)

        # Display AI summary if available
        if ai_summary:
            logger.info("\n[AI Market Summary]")
            logger.info("-" * 60)
            logger.info(ai_summary)
            logger.info("-" * 60)
            logger.info("")

        if "summary" in analysis:
            summary = analysis["summary"]
            logger.info(f"Date: {analysis.get('date', datetime.now().date())}")
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
        if exchange_comparison:
            logger.info("Index Performance:")
            for index_name, stats in exchange_comparison.items():
                logger.info(f"  {index_name}:")
                logger.info(f"    Stocks: {stats['stock_count']}")
                logger.info(f"    Avg Change: {stats['average_change_percent']:.2f}%")
                logger.info(f"    Gainers: {stats['gainers']} | Losers: {stats['losers']}")
            logger.info("")

        logger.info("=" * 60)
        logger.info("Daily tracking complete!")
        logger.info("=" * 60)
        logger.debug("Workflow completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main workflow: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Exiting.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
