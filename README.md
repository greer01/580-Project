# CaddySense: AI-Powered Golf Performance Assistant

CaddySense is an AI-driven tool designed to help golfers analyze their performance, receive personalized coaching advice, and get recommendations on the type of courses that best suit their skills. By combining data analytics, structured storage, and AI reasoning, CaddySense transforms raw golfing stats into actionable insights.

## Overview

CaddySense is a command-line golf performance assistant that allows users to:

- Store golfer performance data (driving distance, putting, GIR %, etc.)

- Analyze aggregated trends using synthetic or real data

- Generate skill visualizations (histogram, scatter plot, radar chart)

- Receive personalized course-type recommendations

- Ask an AI golf coach custom questions based on stored golfer stats

- Save all golfer profiles inside SQLite database

## Installation Requirements

- Python 3.10+

- To make sure you have all libraries run:

```python
pip install matplotlib numpy pandas
```

- Download Ollama: ```https://ollama.com/download```

- After Downloading:

```python
ollama pull phi3

```

- Make sure Ollama is running:

```python
ollama serve
```

## Running the Program

- In the terminal, navigate to the main file by: 

```python
cd src/
```

- Run the program:

```python
python main.py
```

- you should then see:

```python
1. Add Golfer
2. List Golfers
3. Recommend Course Type
4. Ask AI Coach
5. Quit
```

- Select and option to use that part of the program!

## Optional Tools

- Reset the database by putting this in your terminal:

```python
python reset_db.py
```

- To get a completely new generated synthetic dataset:

```python
python data_generator.py
```

- To view the graphs:

```python
python visualize_golfers.py
```

## Example Input Question for the AI golf coach

'How can I improve my GIR?'
