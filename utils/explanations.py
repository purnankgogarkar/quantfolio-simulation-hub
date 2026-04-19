def get_simulation_explanations():
    """Returns detailed explanations for each simulation type"""
    
    explanations = {
        "Monte Carlo": {
            "title": "🎲 Monte Carlo Simulation",
            "what_is_it": """
            **What is Monte Carlo Simulation?**
            
            Imagine you're trying to predict what might happen to your investment portfolio over time. 
            Instead of just guessing, Monte Carlo runs thousands of possible scenarios automatically.
            
            Think of it like this: If you flip a coin 10,000 times, you'll see different patterns emerge. 
            Similarly, Monte Carlo simulates thousands of possible market movements and shows you the range 
            of outcomes your portfolio might experience.
            """,
            "how_it_works": """
            **How does it work?**
            
            1. **Historical Analysis**: The tool first analyzes how your stocks moved in the past
            2. **Pattern Recognition**: It identifies the average movement and variability (volatility)
            3. **Random Simulation**: Using these patterns, it generates 10,000+ random market scenarios
            4. **Portfolio Impact**: For each scenario, it calculates how much money you'd make or lose
            5. **Results**: Shows you all possible outcomes and their probabilities
            """,
            "why_useful": """
            **Why is this useful?**
            
            ✅ Shows the **full range** of possible outcomes (best case to worst case)
            ✅ Based on **historical patterns** but creates new scenarios
            ✅ Accounts for **market volatility** (ups and downs)
            ✅ Most **realistic** simulation for diverse portfolios
            ✅ Helps you prepare for **unexpected market moves**
            """,
            "best_for": "📌 Best for: General investors who want a comprehensive view of all possibilities"
        },
        
        "Historical": {
            "title": "📚 Historical Simulation",
            "what_is_it": """
            **What is Historical Simulation?**
            
            Instead of creating imaginary scenarios, Historical Simulation uses **actual past events** 
            to predict the future.
            
            Think of it like this: If you studied every rainy day in the past 50 years to understand 
            rain patterns, you could say "based on history, here's what tomorrow might bring."
            Similarly, this method replays actual market movements from the past on your portfolio.
            """,
            "how_it_works": """
            **How does it work?**
            
            1. **Historical Data**: Collects actual daily returns of your stocks over the past year
            2. **Real Scenarios**: Takes every real market day from history
            3. **Portfolio Replay**: Applies each historical day's actual returns to your portfolio
            4. **Loss Calculation**: Calculates how much you would have lost on each day
            5. **Sorting**: Arranges all losses from smallest to largest to show the distribution
            """,
            "why_useful": """
            **Why is this useful?**
            
            ✅ Uses **real market events** (not theoretical)
            ✅ Captures **actual market behavior** and extreme events
            ✅ **Simple to understand** (actually happened!)
            ✅ No assumptions about future = past patterns
            ✅ Good for detecting **genuine market risks**
            """,
            "best_for": "📌 Best for: Conservative investors who trust 'what actually happened' more than predictions"
        },
        
        "Bootstrap": {
            "title": "🔄 Bootstrap Simulation",
            "what_is_it": """
            **What is Bootstrap Simulation?**
            
            Bootstrap is like **resampling with replacement** - imagine drawing from a hat of past market days, 
            writing down the result, then putting it back and drawing again.
            
            Think of it like this: You have 252 trading days of data from the past year. Bootstrap randomly 
            picks days from these 252 days multiple times (with replacement) to create new 252-day scenarios. 
            It's like shuffling historical events into new combinations.
            """,
            "how_it_works": """
            **How does it work?**
            
            1. **Historical Returns**: Gathers actual daily returns from past year
            2. **Random Selection**: Randomly picks days from this history (can pick same day multiple times)
            3. **New Sequence**: Creates a new portfolio history by combining randomly selected days
            4. **Repeat**: Does this thousands of times to create many possible scenarios
            5. **Distribution**: Shows all possible outcomes based on real historical movements
            """,
            "why_useful": """
            **Why is this useful?**
            
            ✅ Uses **real historical data** (trustworthy)
            ✅ Creates **diverse scenarios** (shuffles historical events)
            ✅ No mathematical assumptions needed
            ✅ **Flexible** - works for any portfolio type
            ✅ Captures **real market correlations** between stocks
            """,
            "best_for": "📌 Best for: Investors who want realism + diversity without complex mathematics"
        },
        
        "Stress": {
            "title": "⚠️ Stress Test",
            "what_is_it": """
            **What is Stress Test?**
            
            A Stress Test shows what happens to your portfolio during a **market crisis** - 
            like a 10% market crash.
            
            Think of it like this: If you own a house in a flood-prone area, you want to know 
            "what damage would occur if the worst flood in 50 years happened?" 
            Stress tests do the same for your portfolio - they check vulnerability to extreme events.
            """,
            "how_it_works": """
            **How does it work?**
            
            1. **Current Portfolio**: Takes your portfolio's current value
            2. **Shock Scenario**: Applies a stress (e.g., 10% market drop) to all stocks
            3. **New Value**: Calculates new portfolio value after the shock
            4. **Loss Calculation**: Shows exactly how much you'd lose in this crisis
            5. **Simple Result**: Gives you a single worst-case scenario number
            """,
            "why_useful": """
            **Why is this useful?**
            
            ✅ Shows **worst-case scenario** (market crash impact)
            ✅ **Simple and direct** - easy to understand
            ✅ Helps identify **vulnerability** to market crashes
            ✅ **Extreme event** preparation
            ✅ Tests **portfolio resilience** during crises
            """,
            "best_for": "📌 Best for: Risk-aware investors who want to know their maximum exposure"
        }
    }
    
    return explanations


def get_personalized_var_explanation(portfolio_value, var, confidence, losses):
    """Returns personalized VaR explanation using actual simulation results"""
    
    var_percentage = (var / portfolio_value) * 100
    max_loss = losses.max()
    min_loss = losses.min()
    
    explanation = f"""
    **What is Value at Risk (VaR)? - Your Scenario**
    
    Your portfolio value: **₹{portfolio_value:,.2f}**
    
    Your VaR at {confidence}% confidence: **₹{var:,.2f}** ({var_percentage:.2f}% of portfolio)
    
    **What this means in plain English:**
    
    On a typical trading day, there's a **{confidence}% chance** that your portfolio loss will be **₹{var:,.2f} or less**.
    
    In other words:
    - ✅ Out of 100 trading days, on **{confidence} days**, you'd lose **₹{var:,.2f} or less**
    - ⚠️ Out of 100 trading days, on **{100-confidence} days**, you might lose **MORE than ₹{var:,.2f}**
    
    **Your worst possible loss in this simulation:** ₹{max_loss:,.2f}
    **Your best possible gain in this simulation:** ₹{abs(min_loss):,.2f}
    
    **Think of it like this:**
    If you had ₹100, your VaR loss of ₹{var:,.2f} means you might lose about ₹{(var/portfolio_value)*100:.2f} in a bad day.
    
    💡 **Remember:** VaR is based on past patterns. Extreme market events can occasionally exceed this amount!
    """
    
    return explanation


def get_personalized_es_explanation(portfolio_value, var, es, confidence, losses):
    """Returns personalized ES explanation using actual simulation results"""
    
    es_percentage = (es / portfolio_value) * 100
    var_percentage = (var / portfolio_value) * 100
    
    explanation = f"""
    **What is Expected Shortfall (ES)? - Your Scenario**
    
    Your portfolio value: **₹{portfolio_value:,.2f}**
    
    Your Expected Shortfall at {confidence}% confidence: **₹{es:,.2f}** ({es_percentage:.2f}% of portfolio)
    
    **What this means in plain English:**
    
    ES answers the question: **"On the REALLY BAD days, what's my average loss?"**
    
    **Comparison:**
    - VaR: ₹{var:,.2f} (the threshold - {var_percentage:.2f}% of portfolio)
    - ES: ₹{es:,.2f} (average of worst-case days - {es_percentage:.2f}% of portfolio)
    
    **What this tells you:**
    
    On the {100-confidence}% worst trading days in your simulation:
    - Your **average loss would be ₹{es:,.2f}**
    - This is **₹{es-var:,.2f} MORE than your VaR**
    
    **Think of it like this:**
    If you had 100 terrible trading days:
    - VaR shows you the "threshold" day (day 95)
    - ES shows you the AVERAGE loss of those 5 worst days combined
    
    **Why ES is more realistic:**
    
    ✅ VaR only tells you the threshold
    ✅ ES tells you what ACTUALLY happens beyond that threshold
    ✅ ES is more **honest about tail risk** (extreme losses)
    ✅ Professional investors often prefer ES for better risk management
    
    💡 **Remember:** ES is always higher than VaR because it's the average of the worst-case scenarios!
    """
    
    return explanation


def get_personalized_graph_explanation(portfolio_value, var, confidence, losses):
    """Returns personalized graph explanation using actual simulation results"""
    
    var_percentage = (var / portfolio_value) * 100
    max_loss = losses.max()
    min_loss = losses.min()
    num_within_var = (losses <= var).sum()
    num_beyond_var = (losses > var).sum()
    percentage_within_var = (num_within_var / len(losses)) * 100
    
    explanation = f"""
    **Understanding Your Loss Distribution Graph**
    
    **What your graph shows:**
    
    Your portfolio value: **₹{portfolio_value:,.2f}**
    
    📊 **Graph Details:**
    - **X-axis**: Loss amounts in rupees (from ₹{min_loss:,.0f} to ₹{max_loss:,.0f})
    - **Y-axis**: Number of scenarios with that loss amount
    - **Red dashed line**: Your VaR = **₹{var:,.2f}** ({var_percentage:.2f}% of portfolio)
    - **Bars**: Represent simulation scenarios
    
    **What the colors mean:**
    
    ✅ **Left of red line** ({percentage_within_var:.1f}% of scenarios): Your portfolio is safe
    - These are the {num_within_var:,} scenarios where losses were **≤ ₹{var:,.2f}**
    - With {confidence}% confidence, you'll be in this zone
    
    ⚠️ **Right of red line** ({100-percentage_within_var:.1f}% of scenarios): Risk zone
    - These are the {num_beyond_var:,} scenarios where losses exceeded **₹{var:,.2f}**
    - These are the "bad luck" scenarios ({100-confidence}% of the time)
    
    **How to read YOUR specific graph:**
    
    1. **Tall peak near zero**: Most outcomes cluster around small losses/gains (safer portfolio)
    2. **Long right tail**: Some scenarios show large losses (riskier portfolio)
    3. **Position of red line**: 
       - **Far left**: Your portfolio is very safe
       - **Middle**: Moderate risk
       - **Far right**: High risk
    
    **Real interpretation:**
    
    Your worst possible loss in simulation: **₹{max_loss:,.0f}** ({(max_loss/portfolio_value)*100:.2f}% of portfolio)
    Your best possible gain in simulation: **₹{abs(min_loss):,.0f}** ({(abs(min_loss)/portfolio_value)*100:.2f}% of portfolio)
    
    This range represents the full spectrum of possibilities based on historical patterns.
    """
    
    return explanation


def get_simulation_comparison():
    """Returns comparison between all simulations"""
    
    return """
    **Comparing All Simulations - Which One Should I Trust?**
    
    | Aspect | Monte Carlo | Historical | Bootstrap | Stress Test |
    |--------|------------|-----------|-----------|-------------|
    | **Based on** | Math patterns | Real events | Real + Shuffled | Hypothetical crash |
    | **Realistic** | Very | Highest | Very | Extreme scenario |
    | **Complexity** | Medium | Simple | Simple | Simplest |
    | **Best for** | Diverse portfolios | Conservative investors | Balanced approach | Worst-case prep |
    | **Assumes** | Patterns repeat | History repeats | Real events | Market crash |
    
    **My recommendation:**
    
    🎯 **Best Practice**: Run ALL simulations!
    - If all show similar results → High confidence in your risk assessment
    - If results differ → Understand why and assess your comfort level
    - Use **Historical + Bootstrap** for conservative estimate
    - Use **Monte Carlo** for comprehensive view
    - Use **Stress Test** to know your breaking point
    """