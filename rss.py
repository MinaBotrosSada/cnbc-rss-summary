import feedparser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from vertexai.language_models import TextGenerationModel
import vertexai


# Fetch the RSS feeds for the first X articles
def fetchRSS(URL, limit=50):
    RSS = feedparser.parse(URL)
    return RSS.entries[:limit]


# Fetch the HTML content of the article
def fetchBeautifulHTMLContent(URL):
    url = URL
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    html_text = '\n'.join(chunk for chunk in chunks if chunk)

    return html_text    


import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def few_shot_prompting(model, prompt, parameters):   
                        
    response = model.predict(
    f"""Summarize this article in 3 to 4 sentences, with new line after each sentence without bullet points

        Article:Apple shares slid less than 1% on Friday after The New York Times reported that the U.S. Department of Justice is preparing an antitrust lawsuit against the iPhone maker, which could be filed as soon as this year.

        The agency’s lawsuit could target how the Apple Watch works exclusively with the iPhone, as well as the company’s iMessage service, which is also solely available on Apple devices. It could also focus on Apple Pay, the company’s payments system, according to the report.

        The lawsuit, if it comes to pass, would be the biggest antitrust risk for Apple in years. The U.S. is Apple’s largest market, and Apple says the way in which iMessage and the Apple Watch work are essential features that distinguish iPhones from Android phones.

        The news comes as investors and analysts have started to fret about the various regulatory risks facing Apple, including new regulations in Europe over the company’s App Store’s control over iPhone software distribution, as well as a recent Justice Department trial targeting Google’s search deals, including its lucrative arrangement with Apple.

        “While Apple’s share price increased by 48% in 2023, our concerns regarding Apple’s legal risks have intensified in recent months,” CFRA analyst Nick Rodelli wrote in a note Friday.

        Apple CEO Tim Cook will meet with the European Commission’s top antitrust enforcer, Margrethe Vestager, next Thursday.

        A representative for Apple declined to comment. The Department of Justice did not immediately respond to CNBC’s requests for comment.

        Summary:The New York Times reported that the U.S. Department of Justice is preparing an antitrust lawsuit against Apple.

        The lawsuit could target the exclusivity of the Apple Watch and iMessage to Apple devices, as well as Apple Pay.

        This would be the biggest antitrust risk for Apple in years, as the U.S. is its largest market.

        Investors and analysts are concerned about the various regulatory risks facing Apple, including new regulations in Europe and a recent Justice Department trial targeting Google's search deals.

        Article: The unemployment rate for Black Americans fell significantly in December, closing out 2023 on a positive note, according to data released Friday by the Department of Labor.
        Black Americans, the group with the highest jobless percentage in the country, saw their unemployment rate dip to 5.2% last month from 5.8% in November. Still, that’s higher than the overall unemployment rate, which held at 3.7% last month, as well as the 3.5% jobless rate for white Americans.



        When accounting for gender, the unemployment rate for Black men aged 20 and older fell to 4.6%, a big decline from the 6.3% rate in November. Black women’s jobless rate remained unchanged at 4.8% in December.
        close dialog
        The top moments in business and politics - wrapped with exclusive color and context - right in your ears

        LISTEN NOW
        Experts said that while the December number is a good sign, the monthly data could be too volatile to form a trend yet.
        “We would caution against reading too much into large swings in monthly data, but in general, demographic groups, including Black Americans, that had traditionally been slower to experience the benefits of a tight labor market have realized stronger employment and wage gains in the current cycle,” Andrew Patterson, senior international economist at Vanguard, told CNBC. 
        The Current Population Survey is “very noisy,” especially when looking at smaller populations, according to Julia Pollak, ZipRecruiter’s chief economist. She noted that the unemployment rate for Black Americans in 2023 ranged between 4.7% in April and 6.0% in June. 

        Among Black workers, the labor force participation rate inched lower to 63.4% from 63.7% in the previous month.

        Black Americans were hit particularly hard by the business shutdowns in the depths of the Covid-19 pandemic, with the unemployment rate for Black workers peaking at 16.8% in 2020. The overall unemployment rate hit a high of 14.7% in April 2020.
        More progress needs to be made for Black workers as they still lag every other demographic group in the U.S.
        “The unemployment rate among Black Americans staged a significant drop in December, but remains above the lower level seen last year,” Bankrate senior economic analyst Mark Hamrick said. “Still, it remains at historically low levels and still higher than the jobless rate overall and for Whites, Asians and Hispanics.”
        For Hispanic Americans, the unemployment rate rose to 5% in December from 4.6% in November.

        Summary: The unemployment rate for Black Americans fell to 5.2% in December 2023, down from 5.8% in November.

        The decline was particularly significant for Black men aged 20 and older, whose unemployment rate dropped from 6.3% to 4.6%.

        However, the unemployment rate for Black Americans remains higher than the overall rate of 3.7% and the rate for white Americans of 3.5%.

        Despite the improvement, more progress is needed as Black workers still lag behind other demographic groups in the U.S.

        Article: Democrats and Republicans in the House of Representatives are demanding more information on Defense Secretary Lloyd Austin’s hospitalization and why it was kept under wraps for days before it was finally announced.
        The top lawmakers on the House Armed Services Committee released a statement on Sunday evening calling for "additional details" on Austin’s condition and why notification was delayed.
        "While we wish Sec. Austin a speedy recovery, we are concerned with how the disclosure of the Secretary’s condition was handled," Committee Chairman Mike Rogers, R-Ala., and ranking member Rep. Adam Smith, D-Wash., said.

        SPONSORED by IAPP - International...

        Get exclusive resources and expert analysis.


        DOD SECOND IN COMMAND TOLD OF AUSTIN'S HOSPITALIZATION 2 DAYS AFTER TAKING OVER SOME OF HIS DUTIES


        U.S. Secretary of Defense Lloyd Austin is under scrutiny for how his hospitalization has been handled ((Photo by Kevin Dietsch/Getty Images))
        "Several questions remain unanswered including what the medical procedure and resulting complications were, what the Secretary’s current health status is, how and when the delegation of the Secretary’s responsibilities were made, and the reason for the delay in notification to the President and Congress.
        "Transparency is vitally important. Sec. Austin must provide these additional details on his health and the decision-making process that occurred in the past week as soon as possible."
        DEFENSE SECRETARY AUSTIN HOSPITALIZED FOLLOWING SURGERY COMPLICATIONS

        Fox News Digital reached out to the Pentagon for a response.
        GOP Conference Chair Elise Stefanik, R-N.Y., the No. 3 House Republican, on Monday morning called for Austin’s resignation.

        House Armed Services Committee Chairman Mike Rogers, R-Ala., said he wants more information on the situation (Ting Shen/Bloomberg via Getty Images)
        "It is shocking and absolutely unacceptable that the Department of Defense waited multiple days to notify the President, the National Security Council, and the American people that Defense Secretary Austin was hospitalized and unable to perform his duties," Stefanik said. 

        "This concerning lack of transparency exemplifies a shocking lack of judgment and a significant national security threat. There must be full accountability beginning with the immediate resignation of Secretary Austin and those that lied for him and a Congressional investigation into this dangerous dereliction of duty."
        PENTAGON ANNOUNCES NEW RED SEA INTERNATIONAL MISSION TO COUNTER ESCALATING HOUTHI ATTACKS ON SHIPS

        The Pentagon publicly revealed on Friday that Austin was in the hospital due to complications from elective surgery. He had 
        been there since
        the start of the week.

        Austin was hospitalized last Monday but it was not made public knowledge until Friday (Photo by Kim Hong-Ji - Pool/Getty Images)
        CLICK HERE TO GET THE FOX NEWS APP

        But a Politico report later revealed that not only were media kept in the dark, but that the highest levels of the White House and top officials in the Pentagon itself were not aware until Thursday Austin was in the hospital.
        Democrat Rep. Chris Deluzio, D-Pa., wrote on X Sunday evening, "I serve on the House Armed Services Committee and share the concerns of Chairman Rogers and Ranking Member Smith."

        Summary:Democrats and Republicans in the House of Representatives are demanding more information on Defense Secretary Lloyd Austin's hospitalization and the delay in its announcement.

        The top lawmakers on the House Armed Services Committee, Mike Rogers and Adam Smith, have called for "additional details" on Austin's condition and the decision-making process.

        GOP Conference Chair Elise Stefanik has called for Austin's resignation, citing the lack of transparency and potential national security threat.

        Austin was hospitalized last Monday due to complications from elective surgery, but the information was not made public until Friday.

        Article: {prompt}

        Summary: 
    """,
        **parameters
    )  

    return response      



def zero_shot_prompting(model, prompt, parameters):
                            
    response = model.predict(
    f"""Summarize this article in 3 to 4 sentences, with new line after each sentence without bullet points
        
        Article: {prompt}

        Summary: 
    """,
        **parameters
    )       

    return response   



def run():
    st.write("# Welcome to MB's Streamlit GenAI RSS Summarizer! 👋")

    title = st.text_input('RSS Feed URL', 'https://moxie.foxnews.com/google-publisher/latest.xml')
    st.write('The current RSS Feed URL is', title)
    
    if st.button('Summarize', type="primary"):        
        if title is None:
            title='https://moxie.foxnews.com/google-publisher/latest.xml'

        st.write('Summarization in progress...')

        vertexai.init(project="minab-ddf-sandbox", location="us-central1")
        parameters = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_k": 40, 
            "top_p": 0.8
        }
        model = TextGenerationModel.from_pretrained("text-bison@001")

         # Load the model            
        list_of_articles = fetchRSS(title, 10)

        # Iterate over the list of articles
        for article in list_of_articles:
            st.markdown(f"### {article.title}")
                        
            prompt = fetchBeautifulHTMLContent(article.link)
                        
            #response = zero_shot_prompting(model, prompt, parameters)

            response = few_shot_prompting(model=model, prompt=prompt, parameters=parameters)

            text = ' '.join(response.text.split()).replace('. - ', '. ')
                 
            st.markdown(f"**Summary:** {text}") 

            st.markdown(f"[Read more on this topic]({article.link})") 

if __name__ == "__main__":
    run()
