from langgraph.graph import StateGraph, END
from typing import Dict, Any

from models import ResearchState
from agents.assistant_selector import select_assistant
from agents.web_researcher import generate_search_queries, perform_web_searches, summarize_search_results, evaluate_search_relevance
from agents.report_writer import write_research_report

def create_research_graph() -> StateGraph:
    """
    Create the LangGraph research graph that coordinates the agents.
    """
    # Define the graph
    graph = StateGraph(ResearchState)
    
    # Add nodes to the graph
    graph.add_node("select_assistant", select_assistant)
    graph.add_node("generate_search_queries", generate_search_queries)
    graph.add_node("perform_web_searches", perform_web_searches)
    graph.add_node("summarize_search_results", summarize_search_results)
    graph.add_node("evaluate_search_relevance", evaluate_search_relevance)
    graph.add_node("write_research_report", write_research_report)
    
    # Define the conditional routing function for relevance evaluation
    def route_based_on_relevance(state: Dict[str, Any]) -> str:
        """
        Route to either generate new search queries or continue to report writing
        based on the relevance evaluation.
        """
        # Get the current iteration count
        iteration_count = state.get("iteration_count", 0)
        
        # Increment the iteration count
        new_iteration_count = iteration_count + 1
        
        # Update the state with the new iteration count
        state["iteration_count"] = new_iteration_count
        
        # Check if we've reached the maximum number of iterations (3)
        if new_iteration_count >= 3:
            print(f"Reached maximum iterations ({new_iteration_count}). Proceeding to write report with current results.")
            return "write_research_report"
        
        # Otherwise, check if we should regenerate queries
        if state.get("should_regenerate_queries", False):
            print(f"Iteration {new_iteration_count}: Regenerating search queries.")
            return "generate_search_queries"
        else:
            print(f"Iteration {new_iteration_count}: Search results are relevant. Proceeding to write report.")
            return "write_research_report"
    
    # Define the flow of the graph
    graph.add_edge("select_assistant", "generate_search_queries")
    graph.add_edge("generate_search_queries", "perform_web_searches")
    graph.add_edge("perform_web_searches", "summarize_search_results")
    graph.add_edge("summarize_search_results", "evaluate_search_relevance")
    
    # Add conditional routing based on relevance evaluation
    graph.add_conditional_edges(
        "evaluate_search_relevance",
        route_based_on_relevance,
        {
            "generate_search_queries": "generate_search_queries",
            "write_research_report": "write_research_report"
        }
    )
    
    graph.add_edge("write_research_report", END)
    
    # Set the entry point
    graph.set_entry_point("select_assistant")
    
    return graph

def run_research(question: str) -> str:
    """
    Run the research graph with a user question.
    
    Args:
        question: The user's research question
        
    Returns:
        The final research report
    """
    # Create the graph
    research_graph = create_research_graph()
    
    # Compile the graph
    app = research_graph.compile()
    
    # Initialize the state
    initial_state = {
        "user_question": question,
        "assistant_info": None,
        "search_queries": None,
        "search_results": None,
        "search_summaries": None,
        "research_summary": None,
        "final_report": None,
        "used_fallback_search": False,
        "relevance_evaluation": None,
        "should_regenerate_queries": None,
        "iteration_count": 0
    }
    
    # Run the graph
    result = app.invoke(initial_state)
    
    # Extract and return the final report
    return result["final_report"]

# For testing purposes
if __name__ == "__main__":
    # Example usage
    question = "What are some national dishes of Kazakhs?"
    report = run_research(question)
    print(report)


# Result:

# Generating initial search queries...
# Generated 3 search queries
#   Query 1: traditional Kazakh national dishes list and descriptions
#   Query 2: Beshbarmak Kazakh dish ingredients preparation cultural significance
#   Query 3: Kazakh cuisine regional variations ceremonial foods (kazy kumis shubat)
# Performing web searches for 3 queries...
# Searching for: traditional Kazakh national dishes list and descriptions
# Fallback search was used for query: traditional Kazakh national dishes list and descriptions
# Found 3 results for query: traditional Kazakh national dishes list and descriptions
# Searching for: Beshbarmak Kazakh dish ingredients preparation cultural significance
# Found 3 results for query: Beshbarmak Kazakh dish ingredients preparation cultural significance
# Searching for: Kazakh cuisine regional variations ceremonial foods (kazy kumis shubat)
# Rate limiting: Waiting 1.43 seconds before next search request...
# Found 3 results for query: Kazakh cuisine regional variations ceremonial foods (kazy kumis shubat)
# Summarizing 9 search results...
# Scraping content from: https://en.wikipedia.org/wiki/Kazakh_cuisine
# Skipping https://en.wikipedia.org/wiki/Kazakh_cuisine due to scraping issues or insufficient content
# Scraping content from: https://www.advantour.com/kazakhstan/food.htm
# Successfully summarized content from: https://www.advantour.com/kazakhstan/food.htm
# Scraping content from: https://www.slideshare.net/slideshow/traditional-dishes-in-kazakhstan-top-stars-4-pptx/285656299
# Successfully summarized content from: https://www.slideshare.net/slideshow/traditional-dishes-in-kazakhstan-top-stars-4-pptx/285656299
# Scraping content from: https://www.instagram.com/reel/DNmKKWyNXnE/
# Successfully summarized content from: https://www.instagram.com/reel/DNmKKWyNXnE/
# Scraping content from: https://www.remitly.com/blog/en-au/food/national-dish-of-kazakhstan/
# Successfully summarized content from: https://www.remitly.com/blog/en-au/food/national-dish-of-kazakhstan/
# Scraping content from: https://vlast.kz/english/69117-the-hunt-for-beshbarmak.html
# Successfully summarized content from: https://vlast.kz/english/69117-the-hunt-for-beshbarmak.html
# Scraping content from: https://www.jarniascyril.com/expatriation/moving-to-kazakhstan-expat-complete-guide/kazakh-cuisine-guide-expats-kazakhstan/
# Successfully summarized content from: https://www.jarniascyril.com/expatriation/moving-to-kazakhstan-expat-complete-guide/kazakh-cuisine-guide-expats-kazakhstan/
# Scraping content from: https://about-kazakhstan.com/popular-food-in-kazakhstan/
# Successfully summarized content from: https://about-kazakhstan.com/popular-food-in-kazakhstan/
# Scraping content from: https://astanatimes.com/2026/03/more-than-food-how-kazakh-cuisine-tells-story-of-steppe/
# Successfully summarized content from: https://astanatimes.com/2026/03/more-than-food-how-kazakh-cuisine-tells-story-of-steppe/
# Created research summary with 8 sources
# Evaluating relevance of search summaries to the original question...
# 87.5% of search results are relevant. Proceeding to write research report...
# Iteration 1: Search results are relevant. Proceeding to write report.
# Title: National Dishes of Kazakh Cuisine: An In-Depth Exploration

# Author: AI Critical Thinker Research Assistant

# Abstract
# Kazakh cuisine is deeply anchored in nomadic history, hospitality traditions, and regional biodiversity. While Beshbarmak is widely recognized as the national dish, a broader repertoire—encompassing meat-centric dishes, noodle soups, fermented dairy products, breads, and ceremonial foods—constitutes the culinary canon associated with Kazakh national identity. This report synthesizes information from multiple sources to identify and describe key national dishes, their main ingredients, preparation methods, cultural significance, and regional variations. It also critically assesses how different sources characterize the concept of a “national dish” in Kazakhstan, including the ceremonial and social dimensions surrounding serving practices. The analysis highlights the centrality of meat (especially horse and mutton), the prominent role of dairy and fermented products, and the way hospitality and communal dining shape dish selection and presentation.

# Introduction
# The notion of a “national dish” in Kazakhstan is not confined to a single recipe but emerges from a tapestry of dishes that embody nomadic heritage, social rituals, and regional adaptability. Several dishes are repeatedly highlighted as emblematic within Kazakh culinary culture. Foremost among them is beshbarmak, a dish traditionally served on a large communal platter with meat and handmade noodles, whose very name connects to hospitality and communal eating. Beyond beshbarmak, a spectrum of dishes—ranging from kazy and shuzhyk (horsemeat sausages) to lagman, manti, and various dairy products—feed into a broader national culinary identity that emphasizes meat-centric feasts, dairy culture, and ceremonial hosting practices. The sources summarized here collectively show that Kazakh national dishes are characterized by:

# - A strong emphasis on meat, often prepared in long, slow cooking processes that render meat very tender.
# - Handcrafted noodles and broths or broths that serve as a unifying foundation across dishes.
# - A robust tradition of fermented and dairy products, reflecting nomadic dairy practices.
# - Ceremonial and communal dining practices that assign social significance to how food is served and who receives which cuts.
# - Regional variation shaped by geography, climate, and historical contact with neighboring cuisines.

# Core National Dishes and Their Profiles
# 1) Beshbarmak (besbharmak)
# - What it is: Beshbarmak is widely regarded as the national ceremonial dish of Kazakhstan. The name literally means “five fingers” in Kazakh, alluding to eating with hands as a sign of hospitality and communal sharing.
# - Main ingredients: Tender meat (traditionally horse or lamb; beef is common in some preparations), flat handmade noodles (jaima) made from flour and water (occasionally eggs), and a flavorful broth.
# - Preparation: Meat is boiled for hours until very soft. The noodles are cooked in the same broth and then served on a large platter atop the meat. The dish is accompanied by a separate bowl of sorpa (broth) or other garnishes, and the best meat pieces are given to the guest of honor or the oldest person at the table.
# - Cultural significance: Beshbarmak is a symbol of hospitality, unity, and respect and is closely tied to Kazakh nomadic heritage and dastarkhan (the tradition of hospitality and sharing around food). It is often central to ceremonial meals and communal dining, with regional serving variations such as the “sur et” version (braised beef ribs) and an “assorted” version (includes kazy and horse meat). Some sources highlight the ritual distribution of portions according to age or status, underscoring social hierarchies at the table. A modern milestone notes a Guinness World Record for the largest beshbarmak in 2015, illustrating its cultural prominence.
# - Notable variations: Regional adaptations include Almaty-style (beef and horse meat predominate) and Taraz-style (carrots, potatoes, and sur et can appear). Some locales even replace noodles with other starches, such as rice, depending on availability and tradition.
# - Source basis: This profile synthesizes descriptions from multiple sources that emphasize beshbarmak as the central national dish and root of ceremonial Kazakh dining (Remitly; Vlast.kz; Jarniascyril; Advantour excerpts; additional notes in overview sources).

# 2) Kazy and Shuzhyk (Horse Sausages)
# - What they are: Kazy is a dry-cured horse rib meat sausage; shuzhyk is a fatty horse sausage. Both are traditional ceremonial components in many Kazakh meals.
# - Cultural significance: These sausages are closely tied to hospitality rituals, festive occasions, and social storage of horse meat—a hallmark of nomadic meat culture. They are commonly present at weddings, funerals, and major holidays such as Nauryz, and are widely available in bazaars and traditional restaurants in major cities.
# - Source basis: Descriptions and cultural associations with hospitality are reported in multiple sources focusing on ceremonial foods and staples of Kazakh cuisine.

# 3) Lagman and Manti (Long Noodles and Steamed Dumplings)
# - Lagman: A long noodle dish with meat and vegetables, served in broth or with a thick vegetable gravy. Lagman has Uyghur origins but is highlighted as a notable Kazakh dish, reflecting cross-cultural influences within Central Asia.
# - Manti: Steamed dumplings filled with minced meat; served with kaymak (sour cream) or tomato sauce; sometimes filled with potato for vegetarians.
# - Significance: Both dishes illustrate the fusion of Central Asian culinary practices (Uyghur influence for lagman) and the broader Kazakh adaptation of dumplings and noodle dishes. They are frequently cited as particularly notable components of Kazakh cuisine alongside beshbarmak.
# - Source basis: Advantour’s list of traditional dishes and notes highlighting Lagman’s Uyghur roots within Kazakh cuisine, along with Manti as a staple dish.

# 4) Other Meat-and-Noodle Dishes (Kuyrdak; Syrne)
# - Kuyrdak: Roast meat (often served before beshbarmak), reflecting the practice of preparing a meat course prior to the main beshbarmak serving.
# - Syrne (sirne): Fried young lamb with onions and potatoes, illustrating a dish that emphasizes meat in a simpler preparation suitable for everyday meals or festive tables.
# - Source basis: The Advantour listing of meat dishes includes both kuyrydak and syrne as traditional options.

# 5) Sorpo/Shorpo/Shurpa; Kespe; Naryn (Soup and Noodle Soups)
# - Sorpo/Shorpo/Shurpa: Lamb boiled in water; broth poured into a bowl with chopped meat; commonly includes potatoes and carrots.
# - Kespe: Egg noodles with carrots and herbs added to the broth.
# - Naryn: A soup made from the meat broth of beshbarmak with very thin noodles mixed with finely chopped meat.
# - Significance: These items reflect the central place of broth-based dishes in Kazakh cuisine and their use as sustaining, communal meals that accompany meat dishes or can stand alone as hearty dishes.
# - Source basis: Advantour’s section on soups and noodle dishes.

# 6) Dairy-Focused Foods (Kurt; Irimshik; Kaymak; Katyk and Ayran)
# - Kurt: Dried balls of soured milk (2–5 cm), often eaten as a snack.
# - Irimshik: A faintly sweet hard cheese from cow or sheep milk.
# - Kaymak: Fresh cream similar to sour cream; eaten with bread or added to soups.
# - Katyk and ayran: Dairy-based drinks from cow’s milk (fermented products).
# - Significance: These items underscore the nomadic dairy tradition central to Kazakh diet, including dried dairy snacks and fermented beverages that pair with both everyday meals and ceremonial feasts.
# - Source basis: Dairy-focused foods are listed in the Advantour overview, with corroborating mentions in other sources that emphasize kumis (fermented mare’s milk) and shubat (fermented camel milk) as part of the national dairy repertoire.

# 7) Fermented and Hot Drinks (Shubat, Kumis, Shyrchay, Kefir)
# - Shubat (camel milk) and kumys/kumis (mare’s milk): Fermented milks with strong cultural associations to nomadic life and ceremonial meals.
# - Shyrchay: Black tea with milk, salt, butter, flour, and tail fat; typically served at home.
# - Kefir: Fermented milk drink.
# - Significance: Fermented dairy beverages are central to nomadic dietary patterns and are integral to hospitality customs and seasonal culinary practices.
# - Source basis: The Advantour entry and other sources highlight kumis and shubat as traditional fermented milks, with Shyrchay described as a customary tea preparation.

# 8) Bread, Pastries, and Street Foods (Baursak; Shelpeki; Tandoor Nan; Ak-nan; Samsas)
# - Baursak (baursak): Small fried yeast dough chunks; commonly served with tea, soups, and main dishes.
# - Shelpeki: Thin unleavened bread fried in oil.
# - Tandoor nan: Everyday yeast bread baked in a clay oven (tandoor).
# - Ak-nan: Flat bread with onions cooked into the dough; often served with beshbarmak.
# - Samsas: Puff pastries filled with meat, potatoes, or cheese (street food).
# - Significance: This category shows the everyday bread-and-snack culture that undergirds ceremonial foods as well as casual meals, highlighting the ubiquity of fried dough and regional bread variants.
# - Source basis: The Advantour catalog includes these items in the bread and pastries section; other sources also reflect on these baked goods as staples of Kazakh cuisine.

# 9) Sweets (Shak-shak; Balkaymak; Zhent)
# - Shak-shak (shek-shek): Fried dough pieces coated with honey; often with raisins and nuts.
# - Balkaymak: Stewed cream with flour and honey; best with hot baursak.
# - Zhent: Cottage cheese with millet, sugar, butter, and raisins; resembles halva in appearance.
# - Significance: Sweets illustrate how Kazakh cuisine balances savory meat-dominated dishes with dairy-based confections and dessert-like treats, often tied to festive occasions.
# - Source basis: The Advantour overview lists these sweets as part of the national confectionary repertoire.

# 10) Holiday and Special Dishes (Nauryz kozhe; Sumalak; Pilaf)
# - Nauryz kozhe: A festive dish with seven components (meat, water, salt, grain, butter, flour, milk); traditional variants include broth, onion, katyk, kurt, kumis, meat, kazy, barley, and millet.
# - Sumalak: Sprouted wheat cooked into a thick semisweet paste; stirred continuously for a full day.
# - Pilaf: Rice cooked with meat, onions, carrots, raisins, chickpeas, garlic, and spices; a popular dish at gatherings.
# - Significance: These dishes are emblematic of holiday feasts and community gatherings, highlighting the ritual importance of hospitality and sharing during celebrations.
# - Source basis: The Advantour listing covers these items as holiday and special dishes; Pilaf is repeatedly cited as a staple in communal gatherings across sources.

# Regional Variations and Notable Observations
# - Regional variation is a salient feature of Kazakh cuisine. North versus south contrasts, as noted in some sources, reflect differences in preferred meats (beef and horse meat more common in some northern and central regions; mutton and fattier preparations more typical in southern areas). Almaty-style preparations often emphasize beef and horse meat, while Taraz-style variations may incorporate carrots, potatoes, and sur et (rendered horse fat) in different configurations.
# - Bologna-like heterogeneity: Lagman’s Uyghur origins illustrate cross-cultural exchange within Central Asia. While lagman is highlighted among Kazakh dishes, its origin underscores the intercultural exchanges that have shaped Kazakh cuisine over centuries.
# - Rice substitution: In some regions (notably around Kyzylorda), beshbarmak noodles may be replaced with rice, indicating pragmatic adaptations to local agricultural practices and preferences.
# - Ceremonial and social dimensions: Across multiple sources, beshbarmak is presented not only as a dish but as a social ritual—an embodiment of hospitality, status-based serving norms, and communal belonging. The ritual distribution of meat pieces, the guest of honor, and the possible placement of a head of the animal as a symbolic gesture all point to a cuisine deeply interwoven with social hierarchy and ancestral custom.
# - Nomadic dairy culture: The prominence of kumis and shubat alongside dairies such as kurt and irimshik reflects the sustainable dairy practices that underpinned the nomadic economy. Fermentation and long-term preservation are recurring themes in Kazakh dairy traditions.

# Interpretive Analysis: What Counts as a “National Dish” in Kazakhstan?
# - The dominant narrative, as presented by Remitly and corroborated by other sources, centers on beshbarmak as the national ceremonial dish, serving as a culinary emblem of hospitality, unity, and social esteem.
# - However, a more expansive view of Kazakh national dishes emerges when considering:
#   - The central role of meat-centric mains (bes hbarmak, kazy, shuzhyk) and the social logic of meat distribution at festive tables.
#   - The parallel emphasis on dairy staples and fermented beverages, which reveal a broad national dairy heritage beyond meat-centric main courses.
#   - The inclusion of lagman and manti as notable dishes that show cross-cultural influence and regional adaptation—supporting the view that Kazakh national cuisine is dynamic and regionally legible.
# - Taken together, the “national dishes” of Kazakhstan are not a fixed roster but a constellation of core dishes that symbolize hospitality, communal dining, nomadic resilience, and regional diversity. Beshbarmak anchors this constellation, while accompanying meat preparations, noodles, dairy products, breads, and festive foods fill out the cultural landscape.

# Critical Reflections and Limitations
# - The sources vary in emphasis and depth. Some present beshbarmak as an indisputable national emblem, while others highlight the ceremonial and social dimensions of serving practices that frame the dish within a larger ritual culture.
# - There is an inherent reliance on secondary sources, some of which are travel or lifestyle oriented (e.g., travel guides, promotional content) rather than peer-reviewed scholarly analyses. This shapes how certain ceremonial practices and regional variations are framed.
# - The inclusion of Lagman as a Kazakh dish with Uyghur roots reflects a broader Central Asian culinary exchange rather than a purely indigenous Kazakh creation; this nuance is important for understanding national identity as fluid and historically interconnected.
# - Some lists (e.g., the slideshare and social-media snippets) are less authoritative and should be treated as supplementary rather than core to the national-dish framework.

# Key Takeaways for Understanding Kazakh National Dishes
# - Beshbarmak stands as the symbolic national dish, embodying hospitality, communal dining, and shared meat consumption on a grand scale.
# - A broad spectrum of dishes—primarily meat-based mains, noodles, and broths, complemented by dairy products and ceremonial meats like kazy and shuzhyk—constitutes the culinary core of Kazakh national identity.
# - Fermented and dairy products (kumis, shubat, kurt, ayran, katyk, kefir) play an equally essential role in daily life and festive meals, reflecting the nomadic dairy heritage.
# - Regional variations and cross-cultural influences (Lagman’s Uyghur connections, rice substitutions, and Taraz/Almaty style differences) underscore that Kazakh cuisine is not monolithic but a living tradition shaped by geography and history.
# - The social context—dastarkhan, the guest of honor, and ritual distribution of meat—gives Kazakh dishes a dimension beyond flavor and technique, infusing them with cultural meaning and hospitality ethics.

# Conclusion
# What constitutes “national dishes of Kazakhs” can be approached as both a singular emblem and a plural culinary tradition. Beshbarmak is the clearest national symbol, a dish that encapsulates hospitality, unity, and the nomadic past. Yet the broader Kazakh national palate encompasses a robust catalog of dishes that reflect meat-centric culinary practices, intricate noodle soups, diverse dairy products, ceremonial items like kazy and shuzhyk, and a wide array of breads and sweets. Regional variation and intercultural influences further enrich the canon, revealing a cuisine that is deeply rooted in history while also responsive to contemporary tastes and global connections. For policymakers, educators, and culinary historians, recognizing both the central role of beshbarmak and the diversity of supporting dishes provides a more accurate and nuanced understanding of Kazakh national cuisine as a living cultural tradition.

# References
# Advantour. (n.d.). Traditional Kazakh dishes. Retrieved from https://www.advantour.com/kazakhstan/food.htm

# Jarniascyril. (n.d.). Expat guide: Kazakh cuisine. Retrieved from https://www.jarniascyril.com/expatriation/moving-to-kazakhstan-expat-complete-guide/kazakh-cuisine-guide-expats-kazakhstan/

# Remitly. (n.d.). Beshbarmak: The national dish of Kazakhstan. Retrieved from https://www.remitly.com/blog/en-au/food/national-dish-of-kazakhstan/

# Vlast.kz. (n.d.). The hunt for beshbarmak. Retrieved from https://vlast.kz/english/69117-the-hunt-for-beshbarmak.html

# About-kazakhstan.com. (n.d.). Popular food in Kazakhstan. Retrieved from https://about-kazakhstan.com/popular-food-in-kazakhstan/

# Astana Times. (2026). More than food: How Kazakh cuisine tells story of steppe. Retrieved from https://astanatimes.com/2026/03/more-than-food-how-kazakh-cuisine-tells-story-of-steppe/

# Slideshare. (n.d.). Traditional dishes in Kazakhstan: Top stars 4 pptx. Retrieved from https://www.slideshare.net/slideshow/traditional-dishes-in-kazakhstan-top-stars-4-pptx/285656299