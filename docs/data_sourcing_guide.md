# Web3 Data Sourcing Guide

## Where does the data normally come from?
In a real professional environment, "Big Data" in Web3 comes from three main places:

1.  **RPC Nodes (The "hard" way)**: You run a node (like Geth) and query it directly. This gives you raw blocks. It is very hard to manage and query.
2.  **Indexing Services (The "Developer" way)**: Services like **The Graph** organize blockchain data into GraphQL APIs. This is what we tried to use, but the free public endpoints are often limited or deprecated.
3.  **Data Warehouses (The "Analyst" way)**: This is the industry standard for Data Analysts.
    *   **Dune Analytics**: Structured SQL tables of decoded smart contract data.
    *   **Google BigQuery (Crypto Public Datasets)**: massive datasets of raw blockchain logs.
    *   **Snowflake / Flipside Crypto**: Enterprise-grade data warehouses.

## Why are we simulating it?
Real "Big Data" (Terabytes of transaction logs) is expensive to download and host. 
- **Dune** doesn't let you download millions of rows easily for free.
- **The Graph** charges per query.

## The "Big Data" Simulation
To build a portfolio that *looks* and *feels* like a Big Data project without paying thousands of dollars:
1.  We will simulate a **CSV Export** from a Data Warehouse (like you ran a query on Dune and exported the results).
2.  We will generate **1,000,000+ rows** of transaction data.
3.  This allows you to show off **Pandas optimization** skills (handling large files, memory management) which is what interviewers care about.

## The Data Structure
We will simulate a `transactions.csv` with:
- `timestamp`: Precise time of trade.
- `hash`: Transaction hash.
- `sender`: Wallet address.
- `amount_usdc`: Amount swapped.
- `fee_tier`: Which pool was used.
- `gas_cost`: Cost of the transaction (for net profit analysis).

## How to get REAL Data for Free (Step-by-Step)

If you want to replace the simulated data with **Real Blockchain Data**, follow these steps. This is exactly what a professional analyst does.

1.  **Go to Dune Analytics**: [dune.com](https://dune.com) and create a free account.
2.  **Create a New Query**: Click "New Query" in the top right.
3.  **Paste the SQL**: Copy the code from `analysis/dune_query.sql` in your project folder.
4.  **Run**: Click "Run" (CMD+Enter). It will take about 2-3 minutes to scan the Ethereum blockchain.
5.  **Export**: Once finished, click "Export to CSV" below the results table.
6.  **Replace**: Save the file as `Data/real_uniswap_data.csv` and update the Python script to use this file.

### Why Dune?
Dune indexes the entire blockchain into SQL tables. It is the #1 tool for Web3 Analysts. Using it proves you know where the data lives.

